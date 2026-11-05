"""
legend_sec.py - SEC EDGAR Multi-Investor Quality Engine
FIN 439 - Lab 19: Legend Panel (Warren Buffett, Benjamin Graham, Michael Burry)
Student: Elliot

Python computes every financial number from SEC filings.
AI interprets those numbers using the respective legend investor's philosophy.
"""

import os
import re
import json
import gzip
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional, Set

DEFAULT_EMAIL = os.environ.get("SEC_EDGAR_EMAIL", "river313@purdue.edu")
DEFAULT_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_cache")

# XBRL Tag Candidate Hierarchy per Course Specification
METRIC_TAG_CANDIDATES = {
    "Revenue": [
        ("RevenueFromContractWithCustomerExcludingAssessedTax", True),
        ("Revenues", True),
    ],
    "NetIncome": [
        ("NetIncomeLoss", True),
    ],
    "OperatingCashFlow": [
        ("NetCashProvidedByUsedInOperatingActivities", True),
    ],
    "CapEx": [
        ("PaymentsToAcquirePropertyPlantAndEquipment", True),
        ("PaymentsToAcquireProductiveAssets", True),
    ],
    "Equity": [
        ("StockholdersEquity", False),
    ],
    "Liabilities": [
        ("Liabilities", False),
    ],
    "AssetsCurrent": [
        ("AssetsCurrent", False),
    ],
    "LiabilitiesCurrent": [
        ("LiabilitiesCurrent", False),
    ],
}


def get_sec_headers(email: Optional[str] = None) -> Dict[str, str]:
    """SEC-compliant User-Agent identifying Elliot and a valid contact email."""
    contact_email = email.strip() if email and email.strip() else DEFAULT_EMAIL
    return {
        "User-Agent": f"Elliot {contact_email}",
        "Accept-Encoding": "gzip, deflate",
    }


def lookup_cik(ticker: str, email: Optional[str] = None, cache_dir: str = DEFAULT_CACHE_DIR) -> Tuple[str, str]:
    """
    Look up 10-digit CIK and Company Title from SEC EDGAR company_tickers.json.
    Returns (cik_padded_10_digits, company_title).
    """
    os.makedirs(cache_dir, exist_ok=True)
    tickers_cache_path = os.path.join(cache_dir, "company_tickers.json")
    data = None

    if os.path.exists(tickers_cache_path):
        try:
            with open(tickers_cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = None

    if not data:
        url = "https://www.sec.gov/files/company_tickers.json"
        headers = get_sec_headers(email)
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                raw_bytes = resp.read()
                if raw_bytes.startswith(b"\x1f\x8b") or resp.headers.get("Content-Encoding") == "gzip":
                    raw_bytes = gzip.decompress(raw_bytes)
                content = raw_bytes.decode("utf-8")
                data = json.loads(content)
                with open(tickers_cache_path, "w", encoding="utf-8") as f:
                    f.write(content)
        except Exception as e:
            if not data:
                raise RuntimeError(f"Unable to retrieve SEC company_tickers.json: {e}")

    ticker_upper = ticker.strip().upper()
    for row in data.values():
        if row.get("ticker", "").upper() == ticker_upper:
            cik_int = row.get("cik_str")
            title = row.get("title", ticker_upper)
            return str(cik_int).zfill(10), title

    raise ValueError(f"Ticker '{ticker_upper}' not found in SEC EDGAR directory.")


def fetch_company_facts(cik: str, email: Optional[str] = None, cache_dir: str = DEFAULT_CACHE_DIR) -> Dict[str, Any]:
    """
    Retrieve XBRL company facts for zero-padded 10-digit CIK.
    Uses local cache if available; otherwise fetches from SEC EDGAR.
    """
    os.makedirs(cache_dir, exist_ok=True)
    cik_padded = cik.zfill(10)
    cache_path = os.path.join(cache_dir, f"CIK{cik_padded}.json")

    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_padded}.json"
    headers = get_sec_headers(email)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw_bytes = resp.read()
            if raw_bytes.startswith(b"\x1f\x8b") or resp.headers.get("Content-Encoding") == "gzip":
                raw_bytes = gzip.decompress(raw_bytes)
            content = raw_bytes.decode("utf-8")
            data = json.loads(content)
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(content)
            return data
    except urllib.error.HTTPError as e:
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        raise RuntimeError(f"SEC EDGAR returned HTTP {e.code} for CIK {cik_padded}: {e.reason}")
    except Exception as e:
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        raise RuntimeError(f"Failed to connect to SEC EDGAR API for CIK {cik_padded}: {e}")


def extract_annual_metric_facts(gaap_facts: Dict[str, Any], tag_candidates: List[Tuple[str, bool]]) -> Tuple[Optional[str], Dict[str, Dict[str, Any]]]:
    """
    Extract 10-K annual observations for a metric using the tag candidate hierarchy.
    Filters:
      - form == '10-K'
      - For duration items: 350 <= (end - start).days <= 375 (one-year period)
      - When multiple filings report the same period, selects the latest filing (filed date).
    Returns (selected_tag_name, {end_date: fact_dict}).
    """
    for tag_name, is_duration in tag_candidates:
        if tag_name not in gaap_facts:
            continue
        units = gaap_facts[tag_name].get("units", {})
        unit_key = "USD" if "USD" in units else (list(units.keys())[0] if units else None)
        if not unit_key:
            continue

        raw_items = units[unit_key]
        facts_by_end: Dict[str, Dict[str, Any]] = {}

        for item in raw_items:
            if item.get("form") != "10-K":
                continue
            end = item.get("end")
            if not end:
                continue

            if is_duration:
                start = item.get("start")
                if not start:
                    continue
                try:
                    s_dt = datetime.strptime(start, "%Y-%m-%d")
                    e_dt = datetime.strptime(end, "%Y-%m-%d")
                    days = (e_dt - s_dt).days
                    if not (350 <= days <= 375):
                        continue
                except ValueError:
                    continue

            filed = item.get("filed", "")
            # Disambiguate multiple filings: select the latest filing date
            if end not in facts_by_end or filed > facts_by_end[end].get("filed", ""):
                facts_by_end[end] = item

        if facts_by_end:
            return tag_name, facts_by_end

    return None, {}


def extract_legend_metrics(facts_data: Dict[str, Any]) -> Tuple[Dict[str, str], List[Dict[str, Any]]]:
    """
    Extract the 5 fiscal years and compute all metrics for Buffett, Graham, and Burry:
      - Revenue
      - Net Income
      - Operating Cash Flow
      - CapEx
      - Stockholders' Equity
      - Liabilities
      - AssetsCurrent
      - LiabilitiesCurrent
      - Return on Equity (ROE = Net Income / Equity)
      - Owner Earnings (OCF - CapEx)
      - Current Ratio (AssetsCurrent / LiabilitiesCurrent)
      - Liabilities / Equity (Liabilities / StockholdersEquity)
    Returns (tags_used_dict, rows_list).
    """
    gaap = facts_data.get("facts", {}).get("us-gaap", {})
    extracted_tags: Dict[str, str] = {}
    metric_facts: Dict[str, Dict[str, Dict[str, Any]]] = {}

    for metric_name, candidates in METRIC_TAG_CANDIDATES.items():
        tag, facts = extract_annual_metric_facts(gaap, candidates)
        extracted_tags[metric_name] = tag if tag else "not found"
        metric_facts[metric_name] = facts

    # Determine fiscal year ends: anchor to NetIncome, Revenue, or Equity
    anchor = metric_facts.get("NetIncome") or metric_facts.get("Revenue") or metric_facts.get("Equity") or {}
    all_ends = sorted(list(anchor.keys()))
    if not all_ends:
        all_ends_set = set()
        for f_dict in metric_facts.values():
            all_ends_set.update(f_dict.keys())
        all_ends = sorted(list(all_ends_set))

    fy_ends = all_ends[-5:] if len(all_ends) >= 5 else all_ends

    rows: List[Dict[str, Any]] = []
    for end_date in fy_ends:
        rev_fact = metric_facts["Revenue"].get(end_date)
        ni_fact = metric_facts["NetIncome"].get(end_date)
        ocf_fact = metric_facts["OperatingCashFlow"].get(end_date)
        capex_fact = metric_facts["CapEx"].get(end_date)
        eq_fact = metric_facts["Equity"].get(end_date)
        liab_fact = metric_facts["Liabilities"].get(end_date)
        ca_fact = metric_facts["AssetsCurrent"].get(end_date)
        cl_fact = metric_facts["LiabilitiesCurrent"].get(end_date)

        rev_val = rev_fact.get("val") if rev_fact else None
        ni_val = ni_fact.get("val") if ni_fact else None
        ocf_val = ocf_fact.get("val") if ocf_fact else None
        capex_val = capex_fact.get("val") if capex_fact else None
        eq_val = eq_fact.get("val") if eq_fact else None
        liab_val = liab_fact.get("val") if liab_fact else None
        ca_val = ca_fact.get("val") if ca_fact else None
        cl_val = cl_fact.get("val") if cl_fact else None

        # ROE (Net Income / Year-End Equity)
        if ni_val is not None and eq_val is not None:
            if eq_val > 0:
                roe_val = ni_val / eq_val
            else:
                roe_val = "not known"
        else:
            roe_val = "not known"

        # Owner Earnings (Operating Cash Flow - CapEx)
        if ocf_val is not None and capex_val is not None:
            oe_val = ocf_val - capex_val
        else:
            oe_val = "not found"

        # Current Ratio (AssetsCurrent / LiabilitiesCurrent)
        if ca_val is not None and cl_val is not None:
            if cl_val > 0:
                cr_val = round(ca_val / cl_val, 2)
            else:
                cr_val = "not found"
        else:
            cr_val = "not found"

        # Liabilities / Equity (Liabilities / StockholdersEquity)
        if liab_val is not None and eq_val is not None:
            if eq_val > 0:
                le_val = round(liab_val / eq_val, 2)
            else:
                le_val = "not found"
        else:
            le_val = "not found"

        rows.append({
            "fiscal_year_end": end_date,
            "revenue": rev_val,
            "net_income": ni_val,
            "operating_cash_flow": ocf_val,
            "capex": capex_val,
            "equity": eq_val,
            "liabilities": liab_val,
            "assets_current": ca_val,
            "liabilities_current": cl_val,
            "roe": roe_val,
            "owner_earnings": oe_val,
            "current_ratio": cr_val,
            "liabilities_equity": le_val,
            "source_tags": {
                "revenue": extracted_tags["Revenue"],
                "net_income": extracted_tags["NetIncome"],
                "operating_cash_flow": extracted_tags["OperatingCashFlow"],
                "capex": extracted_tags["CapEx"],
                "equity": extracted_tags["Equity"],
                "liabilities": extracted_tags["Liabilities"],
                "assets_current": extracted_tags["AssetsCurrent"],
                "liabilities_current": extracted_tags["LiabilitiesCurrent"],
            }
        })

    return extracted_tags, rows


# ============================================================================
# Investor Check Evaluation Engines
# ============================================================================

def evaluate_buffett_checks(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Warren Buffett's Three Checks:
      1. ROE >= 15% every year
      2. Owner earnings positive every year
      3. Owner earnings grew from first to last year
    """
    if not rows:
        return {
            "check1": {"name": "ROE >= 15% every year", "status": "NOT KNOWN", "details": "No fiscal years retrieved."},
            "check2": {"name": "Owner earnings positive every year", "status": "NOT KNOWN", "details": "No fiscal years retrieved."},
            "check3": {"name": "Owner earnings growth (FY5 > FY1)", "status": "NOT KNOWN", "details": "No fiscal years retrieved."},
        }

    # Check 1: ROE >= 15%
    roe_vals = [r["roe"] for r in rows]
    if len(rows) < 5:
        c1_status = "NOT KNOWN"
        c1_details = f"Fewer than 5 fiscal years available ({len(rows)} found)."
    elif any(r == "not known" or r is None for r in roe_vals):
        c1_status = "NOT KNOWN"
        c1_details = "One or more fiscal years have unknown ROE (missing net income or negative/zero equity)."
    elif all(isinstance(r, (int, float)) and r >= 0.15 for r in roe_vals):
        c1_status = "PASS"
        pct_list = [f"{r*100:.1f}%" for r in roe_vals]
        c1_details = f"ROE exceeded 15.0% in all 5 fiscal years: {', '.join(pct_list)}."
    else:
        c1_status = "FAIL"
        failed_years = [f"{rows[i]['fiscal_year_end']} ({roe_vals[i]*100:.1f}%)" for i, r in enumerate(roe_vals) if r < 0.15]
        c1_details = f"ROE failed 15% threshold in: {', '.join(failed_years)}."

    # Check 2: Owner Earnings > 0
    oe_vals = [r["owner_earnings"] for r in rows]
    if len(rows) < 5:
        c2_status = "NOT KNOWN"
        c2_details = f"Fewer than 5 fiscal years available ({len(rows)} found)."
    elif any(oe == "not found" or oe is None for oe in oe_vals):
        c2_status = "NOT KNOWN"
        c2_details = "Owner earnings cannot be computed because CapEx or Operating Cash Flow is not found."
    elif all(isinstance(oe, (int, float)) and oe > 0 for oe in oe_vals):
        c2_status = "PASS"
        oe_millions = [f"${oe/1e6:,.0f}M" for oe in oe_vals]
        c2_details = f"Owner earnings were positive in all 5 fiscal years: {', '.join(oe_millions)}."
    else:
        c2_status = "FAIL"
        failed_oe = [f"{rows[i]['fiscal_year_end']} (${oe_vals[i]/1e6:,.0f}M)" for i, oe in enumerate(oe_vals) if oe <= 0]
        c2_details = f"Owner earnings non-positive in: {', '.join(failed_oe)}."

    # Check 3: Owner Earnings Growth (final year > first year)
    if len(rows) < 5 or oe_vals[0] == "not found" or oe_vals[-1] == "not found" or oe_vals[0] is None or oe_vals[-1] is None:
        c3_status = "NOT KNOWN"
        c3_details = "Owner earnings growth cannot be determined due to missing data or incomplete 5-year history."
    elif isinstance(oe_vals[0], (int, float)) and isinstance(oe_vals[-1], (int, float)):
        oe_initial = oe_vals[0]
        oe_final = oe_vals[-1]
        diff = oe_final - oe_initial
        growth_pct = (diff / abs(oe_initial)) * 100 if oe_initial != 0 else 0
        if oe_final > oe_initial:
            c3_status = "PASS"
            c3_details = f"Owner earnings grew from ${oe_initial/1e6:,.0f}M in {rows[0]['fiscal_year_end']} to ${oe_final/1e6:,.0f}M in {rows[-1]['fiscal_year_end']} (+${diff/1e6:,.0f}M, +{growth_pct:.1f}%)."
        else:
            c3_status = "FAIL"
            c3_details = f"Owner earnings declined from ${oe_initial/1e6:,.0f}M to ${oe_final/1e6:,.0f}M ({diff/1e6:,.0f}M)."
    else:
        c3_status = "NOT KNOWN"
        c3_details = "Owner earnings data incomplete."

    passed_count = sum(1 for c in [c1_status, c2_status, c3_status] if c == "PASS")
    if passed_count == 3:
        verdict = "OWN THE BUSINESS"
    elif any(c == "FAIL" for c in [c1_status, c2_status, c3_status]):
        verdict = "REJECT / DEFICIENT"
    else:
        verdict = "WATCHLIST"

    return {
        "check1": {"name": "ROE >= 15% every year", "status": c1_status, "details": c1_details},
        "check2": {"name": "Owner earnings positive every year", "status": c2_status, "details": c2_details},
        "check3": {"name": "Owner earnings growth (FY5 > FY1)", "status": c3_status, "details": c3_details},
        "passed_count": passed_count,
        "total_checks": 3,
        "verdict": verdict,
    }


def evaluate_graham_checks(rows: List[Dict[str, Any]], current_ratio_threshold: float = 2.0) -> Dict[str, Dict[str, Any]]:
    """
    Benjamin Graham's Three Checks:
      1. Latest-year current ratio >= threshold (default 2.0, probe 1.0)
      2. Net income positive in every one of the five years
      3. Net income in the last year greater than the first year
    """
    if not rows:
        return {
            "check1": {"name": f"Current ratio >= {current_ratio_threshold:.1f} (latest year)", "status": "NOT KNOWN", "details": "No fiscal years retrieved."},
            "check2": {"name": "Net income positive every year", "status": "NOT KNOWN", "details": "No fiscal years retrieved."},
            "check3": {"name": "Net income growth (FY5 > FY1)", "status": "NOT KNOWN", "details": "No fiscal years retrieved."},
        }

    # Check 1: Current Ratio >= threshold (latest year)
    latest_row = rows[-1]
    latest_cr = latest_row["current_ratio"]
    if latest_cr == "not found" or latest_cr is None:
        c1_status = "NOT KNOWN"
        c1_details = "Current assets or current liabilities not found for latest fiscal year."
    elif isinstance(latest_cr, (int, float)):
        if latest_cr >= current_ratio_threshold:
            c1_status = "PASS"
            c1_details = f"Latest-year current ratio of {latest_cr:.2f} met or exceeded the {current_ratio_threshold:.1f} threshold."
        else:
            c1_status = "FAIL"
            c1_details = f"Latest-year current ratio of {latest_cr:.2f} fell below the {current_ratio_threshold:.1f} threshold."
    else:
        c1_status = "NOT KNOWN"
        c1_details = "Invalid current ratio data."

    # Check 2: Net Income Positive Every Year
    ni_vals = [r["net_income"] for r in rows]
    if len(rows) < 5:
        c2_status = "NOT KNOWN"
        c2_details = f"Fewer than 5 fiscal years available ({len(rows)} found)."
    elif any(ni is None or ni == "not found" for ni in ni_vals):
        c2_status = "NOT KNOWN"
        c2_details = "Net income missing for one or more fiscal years."
    elif all(isinstance(ni, (int, float)) and ni > 0 for ni in ni_vals):
        c2_status = "PASS"
        ni_millions = [f"${ni/1e6:,.0f}M" for ni in ni_vals]
        c2_details = f"Net income was positive in all 5 fiscal years: {', '.join(ni_millions)}."
    else:
        c2_status = "FAIL"
        failed_ni = [f"{rows[i]['fiscal_year_end']} (${ni_vals[i]/1e6:,.0f}M)" for i, ni in enumerate(ni_vals) if ni <= 0]
        c2_details = f"Net income non-positive in: {', '.join(failed_ni)}."

    # Check 3: Net Income Growth (final year > first year)
    if len(rows) < 5 or ni_vals[0] is None or ni_vals[-1] is None or ni_vals[0] == "not found" or ni_vals[-1] == "not found":
        c3_status = "NOT KNOWN"
        c3_details = "Net income growth cannot be determined due to missing data or incomplete 5-year history."
    elif isinstance(ni_vals[0], (int, float)) and isinstance(ni_vals[-1], (int, float)):
        ni_initial = ni_vals[0]
        ni_final = ni_vals[-1]
        diff = ni_final - ni_initial
        growth_pct = (diff / abs(ni_initial)) * 100 if ni_initial != 0 else 0
        if ni_final > ni_initial:
            c3_status = "PASS"
            c3_details = f"Net income grew from ${ni_initial/1e6:,.0f}M in {rows[0]['fiscal_year_end']} to ${ni_final/1e6:,.0f}M in {rows[-1]['fiscal_year_end']} (+${diff/1e6:,.0f}M, +{growth_pct:.1f}%)."
        else:
            c3_status = "FAIL"
            c3_details = f"Net income declined from ${ni_initial/1e6:,.0f}M to ${ni_final/1e6:,.0f}M ({diff/1e6:,.0f}M)."
    else:
        c3_status = "NOT KNOWN"
        c3_details = "Net income data incomplete."

    passed_count = sum(1 for c in [c1_status, c2_status, c3_status] if c == "PASS")
    if passed_count == 3:
        verdict = "DEFENSIVE BUY"
    elif passed_count == 2:
        verdict = "ENTERPRISING / WATCH"
    else:
        verdict = "REJECT / DEFICIENT"

    return {
        "check1": {"name": f"Current ratio >= {current_ratio_threshold:.1f} (latest year)", "status": c1_status, "details": c1_details, "value": latest_cr},
        "check2": {"name": "Net income positive every year", "status": c2_status, "details": c2_details},
        "check3": {"name": "Net income growth (FY5 > FY1)", "status": c3_status, "details": c3_details},
        "passed_count": passed_count,
        "total_checks": 3,
        "verdict": verdict,
        "threshold_used": current_ratio_threshold,
    }


def evaluate_burry_checks(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Michael Burry's Two Checks:
      1. Operating cash flow >= Net income in every one of the five years (Accounting/Earnings Quality)
      2. Latest-year total liabilities <= 2 × stockholders' equity (Liabilities / Equity <= 2.0)
    """
    if not rows:
        return {
            "check1": {"name": "Operating cash flow >= net income every year", "status": "NOT KNOWN", "details": "No fiscal years retrieved."},
            "check2": {"name": "Liabilities <= 2 × equity (latest year)", "status": "NOT KNOWN", "details": "No fiscal years retrieved."},
        }

    # Check 1: OCF >= Net Income every year
    ocf_vals = [r["operating_cash_flow"] for r in rows]
    ni_vals = [r["net_income"] for r in rows]

    if len(rows) < 5:
        c1_status = "NOT KNOWN"
        c1_details = f"Fewer than 5 fiscal years available ({len(rows)} found)."
    elif any(ocf is None or ni is None or ocf == "not found" or ni == "not found" for ocf, ni in zip(ocf_vals, ni_vals)):
        c1_status = "NOT KNOWN"
        c1_details = "Operating cash flow or net income missing for one or more fiscal years."
    elif all(isinstance(ocf, (int, float)) and isinstance(ni, (int, float)) and ocf >= ni for ocf, ni in zip(ocf_vals, ni_vals)):
        c1_status = "PASS"
        c1_details = f"Operating cash flow exceeded net income in all 5 fiscal years, confirming high earnings quality and cash backing."
    else:
        c1_status = "FAIL"
        failed_years = []
        for i in range(len(rows)):
            if ocf_vals[i] < ni_vals[i]:
                failed_years.append(f"{rows[i]['fiscal_year_end']} (OCF ${ocf_vals[i]/1e6:,.0f}M < NI ${ni_vals[i]/1e6:,.0f}M)")
        c1_details = f"Operating cash flow trailed net income in: {', '.join(failed_years)}."

    # Check 2: Liabilities <= 2 × Equity (latest year)
    latest_row = rows[-1]
    latest_le = latest_row["liabilities_equity"]
    latest_liab = latest_row["liabilities"]
    latest_eq = latest_row["equity"]

    if latest_le == "not found" or latest_le is None:
        c2_status = "NOT KNOWN"
        c2_details = "Total liabilities or equity not found for latest fiscal year."
    elif isinstance(latest_le, (int, float)):
        if latest_le <= 2.0:
            c2_status = "PASS"
            c2_details = f"Latest-year liabilities/equity ratio of {latest_le:.2f} satisfies the conservative solvency limit (<= 2.0)."
        else:
            c2_status = "FAIL"
            c2_details = f"Latest-year liabilities/equity ratio of {latest_le:.2f} exceeds conservative leverage limit (<= 2.0)."
    else:
        c2_status = "NOT KNOWN"
        c2_details = "Invalid liabilities or equity data."

    passed_count = sum(1 for c in [c1_status, c2_status] if c == "PASS")
    if passed_count == 2:
        verdict = "VALUE LONG"
    elif passed_count == 1:
        verdict = "NEUTRAL / CAUTION"
    else:
        verdict = "SHORT CANDIDATE / AVOID"

    return {
        "check1": {"name": "Operating cash flow >= net income every year", "status": c1_status, "details": c1_details},
        "check2": {"name": "Liabilities <= 2 × equity (latest year)", "status": c2_status, "details": c2_details, "value": latest_le},
        "passed_count": passed_count,
        "total_checks": 2,
        "verdict": verdict,
    }


# ============================================================================
# Canonical Number Extraction & Fabrication Detector
# ============================================================================

def get_canonical_numbers(rows: List[Dict[str, Any]]) -> Set[str]:
    """
    Produce the canonical set of valid string representations of all financial numbers
    calculated and printed by the script. Used to detect fabricated numbers in investment memos.
    """
    valid_numbers: Set[str] = set()

    # Allowed threshold constants across Buffett, Graham, and Burry
    valid_numbers.update([
        "15", "15.0", "15%", "15.0%", "0", "0.0", "5", "3", "1", "2",
        "2.0", "1.0", "2x", "2X", "2.0x", "1.0x"
    ])

    for r in rows:
        end_date = r["fiscal_year_end"]
        valid_numbers.add(end_date)
        year_str = end_date.split("-")[0]
        valid_numbers.add(year_str)

        # Dollar items
        for key in ["revenue", "net_income", "operating_cash_flow", "capex", "equity", "liabilities", "assets_current", "liabilities_current", "owner_earnings"]:
            val = r.get(key)
            if isinstance(val, (int, float)):
                valid_numbers.add(str(int(val)))
                valid_numbers.add(f"{val:,}")
                m_val = round(val / 1e6)
                valid_numbers.add(str(m_val))
                valid_numbers.add(f"{m_val:,}")
                valid_numbers.add(f"${m_val:,}")
                valid_numbers.add(f"${m_val:,}M")
                valid_numbers.add(f"${m_val}M")
                m_val_1 = f"{val/1e6:.1f}"
                valid_numbers.add(m_val_1)
                b_val_1 = f"{val/1e9:.1f}"
                b_val_2 = f"{val/1e9:.2f}"
                valid_numbers.add(b_val_1)
                valid_numbers.add(b_val_2)
                valid_numbers.add(f"${b_val_1}B")
                valid_numbers.add(f"${b_val_2}B")

        # Ratios & Percentages
        roe = r.get("roe")
        if isinstance(roe, (int, float)):
            pct_1 = f"{roe*100:.1f}"
            pct_2 = f"{roe*100:.2f}"
            valid_numbers.add(pct_1)
            valid_numbers.add(pct_2)
            valid_numbers.add(f"{pct_1}%")
            valid_numbers.add(f"{pct_2}%")

        cr = r.get("current_ratio")
        if isinstance(cr, (int, float)):
            valid_numbers.add(f"{cr:.2f}")
            valid_numbers.add(f"{cr:.1f}")

        le = r.get("liabilities_equity")
        if isinstance(le, (int, float)):
            valid_numbers.add(f"{le:.2f}")
            valid_numbers.add(f"{le:.1f}")

    # Growth differences and percentages
    if len(rows) >= 2:
        for k in ["owner_earnings", "net_income"]:
            v0 = rows[0].get(k)
            vn = rows[-1].get(k)
            if isinstance(v0, (int, float)) and isinstance(vn, (int, float)):
                diff = vn - v0
                diff_m = round(diff / 1e6)
                valid_numbers.add(str(diff_m))
                valid_numbers.add(f"{diff_m:,}")
                valid_numbers.add(f"${diff_m:,}")
                valid_numbers.add(f"${diff_m:,}M")
                if v0 != 0:
                    pct = (diff / abs(v0)) * 100
                    valid_numbers.add(f"{pct:.1f}")
                    valid_numbers.add(f"{pct:.1f}%")
                    valid_numbers.add(f"{round(pct)}")
                    valid_numbers.add(f"{round(pct)}%")

    return valid_numbers


def detect_unsupported_numbers(memo_text: str, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detector that flags any financial number, ratio, or percentage in the memo that was NOT printed by the script.
    Applies across all three investor memos (Buffett, Graham, Burry).
    """
    canonical_set = get_canonical_numbers(rows)
    unsupported = []

    pct_pattern = re.compile(r"\b\d+(?:\.\d+)?%")
    curr_pattern = re.compile(r"\$[\d,]+(?:\.\d+)?(?:[MBmb])?")
    num_pattern = re.compile(r"(?<![A-Za-z0-9_#\-\/])(?:\b\d{1,3}(?:,\d{3})+(?:\.\d+)?|\b\d+\.\d+)(?![A-Za-z0-9_%])")

    lines = memo_text.splitlines()
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith(("```", "http://", "https://", "<!--")):
            continue

        # Strip markdown heading characters so headings are actively audited
        scanned_line = stripped.lstrip("#").strip()

        tokens = []
        matched_spans = []

        for m in pct_pattern.finditer(scanned_line):
            tokens.append(m.group(0))
            matched_spans.append((m.start(), m.end()))

        for m in curr_pattern.finditer(scanned_line):
            tokens.append(m.group(0))
            matched_spans.append((m.start(), m.end()))

        for m in num_pattern.finditer(scanned_line):
            span = (m.start(), m.end())
            if not any(s <= span[0] and span[1] <= e for s, e in matched_spans):
                tokens.append(m.group(0))

        for tok in tokens:
            cleaned = tok.strip()
            base_cleaned = cleaned.replace("$", "").replace("%", "").replace("M", "").replace("B", "").replace(",", "")

            is_valid = (
                cleaned in canonical_set
                or base_cleaned in canonical_set
                or tok in canonical_set
            )

            # Ignore common structural numbers (e.g. 10-K, years 2020-2026, check numbers 1, 2, 3, 4, 5, 0)
            if base_cleaned in {"10", "1", "2", "3", "4", "5", "0"}:
                is_valid = True

            if not is_valid:
                unsupported.append({
                    "line": line_num,
                    "token": tok,
                    "context": line.strip()
                })

    return unsupported


# ============================================================================
# Multi-Investor Memo Generators
# ============================================================================

def build_financial_table_markdown(rows: List[Dict[str, Any]]) -> str:
    """Build standardized Markdown financial table showing all metrics."""
    table_lines = [
        "| Fiscal Year End | Revenue | Net Income | Operating Cash Flow | CapEx | Equity | Current Ratio | Liab / Eq | ROE | Owner Earnings |",
        "| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"
    ]
    for r in rows:
        rev_s = f"{r['revenue']/1e6:,.0f}" if isinstance(r['revenue'], (int, float)) else "not found"
        ni_s = f"{r['net_income']/1e6:,.0f}" if isinstance(r['net_income'], (int, float)) else "not found"
        ocf_s = f"{r['operating_cash_flow']/1e6:,.0f}" if isinstance(r['operating_cash_flow'], (int, float)) else "not found"
        capex_s = f"{r['capex']/1e6:,.0f}" if isinstance(r['capex'], (int, float)) else "not found"
        eq_s = f"{r['equity']/1e6:,.0f}" if isinstance(r['equity'], (int, float)) else "not found"
        cr_s = f"{r['current_ratio']:.2f}" if isinstance(r['current_ratio'], (int, float)) else str(r['current_ratio'])
        le_s = f"{r['liabilities_equity']:.2f}" if isinstance(r['liabilities_equity'], (int, float)) else str(r['liabilities_equity'])
        roe_s = f"{r['roe']*100:.1f}%" if isinstance(r['roe'], (int, float)) else str(r['roe'])
        oe_s = f"{r['owner_earnings']/1e6:,.0f}" if isinstance(r['owner_earnings'], (int, float)) else str(r['owner_earnings'])
        table_lines.append(f"| {r['fiscal_year_end']} | {rev_s} | {ni_s} | {ocf_s} | {capex_s} | {eq_s} | {cr_s} | {le_s} | {roe_s} | {oe_s} |")
    return "\n".join(table_lines)


def generate_buffett_memo(
    ticker: str,
    company_title: str,
    rows: List[Dict[str, Any]],
    tags_used: Dict[str, str],
    checks: Dict[str, Dict[str, Any]],
    personal_verdict: Optional[str] = None
) -> str:
    """Generate Warren Buffett investment memo evaluating franchise quality and owner earnings."""
    ticker_clean = ticker.strip().upper()
    c1 = checks["check1"]["status"]
    c2 = checks["check2"]["status"]
    c3 = checks["check3"]["status"]
    verdict = checks["verdict"]

    table_md = build_financial_table_markdown(rows)

    student_verdict = personal_verdict or (
        '"I agree that Costco has strong financial performance, but I would still want to know whether its stock price is reasonable before investing."'
        if ticker_clean == "COST" else
        f'"I would use the three-investor panel as an initial screening tool for {ticker_clean}, but I would verify the financial data and consider valuation before making an investment decision."'
    )

    missing_notice = ""
    if c2 == "NOT KNOWN":
        missing_notice = f"\n> **Missing Data Note:** Owner earnings cannot be evaluated with the available inputs because capital expenditures (CapEx) are not found in official SEC 10-K filings for {ticker_clean}.\n"

    memo = f"""# Warren Buffett Investment Memo: {company_title} ({ticker_clean})

**Analyst:** Elliot | **Framework:** Franchise Quality & Owner Cash Flow | **Data:** SEC EDGAR 10-K

---

### Executive Summary & Verdict
**Conclusion:** **{verdict}** ({checks['passed_count']}/{checks['total_checks']} Checks Passed)

Warren Buffett evaluates companies as an owner buying the entire operating business, seeking high return on equity, compounding owner earnings, and a wide economic moat.
{missing_notice}
* **Check 1 (ROE >= 15.0% every year):** **{c1}** — {checks['check1']['details']}
* **Check 2 (Owner Earnings > 0 every year):** **{c2}** — {checks['check2']['details']}
* **Check 3 (Owner Earnings Growth):** **{c3}** — {checks['check3']['details']}

---

### Audited SEC Financial Foundation (USD Millions, except ROE & Ratios)
{table_md}

---

### Business Quality & Operational Synthesis
* **Franchise Castle & Moat:** Buffett prioritizes durable economic castles protected by unassailable moats (low-cost shared scale, customer switching friction, or strong brand intangibles).
* **Capital Reinvestment:** Businesses must generate surplus cash beyond maintenance capital requirements to satisfy Buffett's ownership test.

---

### Elliot's Personal Verdict
> {student_verdict}
"""
    return memo


def generate_graham_memo(
    ticker: str,
    company_title: str,
    rows: List[Dict[str, Any]],
    tags_used: Dict[str, str],
    checks: Dict[str, Dict[str, Any]],
    threshold_probe_note: Optional[str] = None
) -> str:
    """Generate Benjamin Graham investment memo evaluating balance sheet conservatism and earnings stability."""
    ticker_clean = ticker.strip().upper()
    c1 = checks["check1"]["status"]
    c2 = checks["check2"]["status"]
    c3 = checks["check3"]["status"]
    verdict = checks["verdict"]
    thresh = checks.get("threshold_used", 2.0)

    table_md = build_financial_table_markdown(rows)

    probe_explanation = threshold_probe_note or (
        "I kept Graham's original 2.0 threshold because lowering it to 1.0 makes Costco pass but weakens the liquidity standard, showing how a screening decision depends on the threshold chosen."
        if ticker_clean == "COST" else
        f"Graham's working capital threshold of {thresh:.1f} tests whether current assets provide a substantial cushion over short-term obligations."
    )

    memo = f"""# Benjamin Graham Investment Memo: {company_title} ({ticker_clean})

**Analyst:** Elliot | **Framework:** Balance Sheet Margin of Safety | **Data:** SEC EDGAR 10-K

---

### Executive Summary & Verdict
**Conclusion:** **{verdict}** ({checks['passed_count']}/{checks['total_checks']} Checks Passed)

Benjamin Graham, the father of value investing, insists on rigorous balance-sheet conservatism, working capital adequacy, and multi-year positive earnings stability.

* **Check 1 (Current Ratio >= {thresh:.1f}, latest year):** **{c1}** — {checks['check1']['details']}
* **Check 2 (Net Income positive every year):** **{c2}** — {checks['check2']['details']}
* **Check 3 (Net Income Growth FY5 > FY1):** **{c3}** — {checks['check3']['details']}

---

### Audited SEC Financial Foundation (USD Millions, except ROE & Ratios)
{table_md}

---

### Balance Sheet & Liquidity Appraisal
* **Working Capital Cushion:** Graham's defensive criteria mandate a current ratio of at least 2.0 to ensure short-term operational obligations are covered twice over by liquid assets.
* **Earnings Stability:** Five consecutive years of positive GAAP net income with multi-year expansion demonstrate defensive solvency.

---

### Graham Threshold Probe & Design Choice
> **Threshold Recorded:** {thresh:.1f}  
> **Rationale:** {probe_explanation}
"""
    return memo


def generate_burry_memo(
    ticker: str,
    company_title: str,
    rows: List[Dict[str, Any]],
    tags_used: Dict[str, str],
    checks: Dict[str, Dict[str, Any]]
) -> str:
    """Generate Michael Burry investment memo evaluating cash flow accounting quality and debt leverage."""
    ticker_clean = ticker.strip().upper()
    c1 = checks["check1"]["status"]
    c2 = checks["check2"]["status"]
    verdict = checks["verdict"]

    table_md = build_financial_table_markdown(rows)

    memo = f"""# Michael Burry Investment Memo: {company_title} ({ticker_clean})

**Analyst:** Elliot | **Framework:** Forensic Cash Flow Quality & Solvency | **Data:** SEC EDGAR 10-K

---

### Executive Summary & Verdict
**Conclusion:** **{verdict}** ({checks['passed_count']}/{checks['total_checks']} Checks Passed)

Dr. Michael Burry focuses on deep-value fundamentals, forensic cash flow conversion (rejecting paper earnings not backed by real cash), and balance sheet leverage constraints.

* **Check 1 (Operating Cash Flow >= Net Income every year):** **{c1}** — {checks['check1']['details']}
* **Check 2 (Liabilities <= 2 × Equity, latest year):** **{c2}** — {checks['check2']['details']}

---

### Audited SEC Financial Foundation (USD Millions, except ROE & Ratios)
{table_md}

---

### Forensic Accounting & Leverage Synthesis
* **Earnings Quality (OCF / NI Conversion):** When Operating Cash Flow consistently exceeds GAAP Net Income across all evaluated fiscal years, reported profits reflect real incoming cash receipts rather than accrual adjustments or aggressive revenue recognition.
* **Capital Structure Risk:** Total liabilities must not exceed twice stockholders' equity to prevent insolvency distress during credit contractions.
"""
    return memo


def format_panel_table(buffett_c: Dict[str, Any], graham_c: Dict[str, Any], burry_c: Dict[str, Any], ticker: str) -> str:
    """Format console output comparing all three investors across all 8 checks."""
    out = []
    out.append("=" * 80)
    out.append(f"FIN 439 - Lab 19: Legend Investor Panel ({ticker})")
    out.append("=" * 80)
    out.append(f"{'Investor':<10} | {'Check Description':<50} | {'Result':<10}")
    out.append("-" * 80)

    # Buffett
    out.append(f"{'Buffett':<10} | {buffett_c['check1']['name']:<50} | {buffett_c['check1']['status']}")
    out.append(f"{'Buffett':<10} | {buffett_c['check2']['name']:<50} | {buffett_c['check2']['status']}")
    out.append(f"{'Buffett':<10} | {buffett_c['check3']['name']:<50} | {buffett_c['check3']['status']}")

    # Graham
    out.append(f"{'Graham':<10} | {graham_c['check1']['name']:<50} | {graham_c['check1']['status']}")
    out.append(f"{'Graham':<10} | {graham_c['check2']['name']:<50} | {graham_c['check2']['status']}")
    out.append(f"{'Graham':<10} | {graham_c['check3']['name']:<50} | {graham_c['check3']['status']}")

    # Burry
    out.append(f"{'Burry':<10} | {burry_c['check1']['name']:<50} | {burry_c['check1']['status']}")
    out.append(f"{'Burry':<10} | {burry_c['check2']['name']:<50} | {burry_c['check2']['status']}")

    out.append("-" * 80)
    out.append(f"Verdicts: Buffett: {buffett_c['verdict']} ({buffett_c['passed_count']}/3) | Graham: {graham_c['verdict']} ({graham_c['passed_count']}/3) | Burry: {burry_c['verdict']} ({burry_c['passed_count']}/2)")
    out.append("=" * 80)
    return "\n".join(out)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Legend Panel: Warren Buffett, Benjamin Graham, Michael Burry")
    parser.add_argument("--ticker", type=str, default="COST", help="Equity stock ticker (e.g. COST, JPM)")
    parser.add_argument("--email", type=str, default=DEFAULT_EMAIL, help="User contact email for SEC User-Agent")
    parser.add_argument("--graham-threshold", type=float, default=2.0, help="Graham current ratio threshold (default 2.0, probe 1.0)")
    parser.add_argument("--memos", action="store_true", help="Print all three investor memos")
    args = parser.parse_args()

    cik, title = lookup_cik(args.ticker, email=args.email)
    facts = fetch_company_facts(cik, email=args.email)
    tags, rows = extract_legend_metrics(facts)

    b_checks = evaluate_buffett_checks(rows)
    g_checks = evaluate_graham_checks(rows, current_ratio_threshold=args.graham_threshold)
    m_checks = evaluate_burry_checks(rows)

    print(format_panel_table(b_checks, g_checks, m_checks, args.ticker.upper()))
