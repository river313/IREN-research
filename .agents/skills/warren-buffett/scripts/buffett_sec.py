"""
buffett_sec.py - SEC EDGAR Retrieval & Warren Buffett Investment Quality Engine
FIN 439 - Purdue University
Student: Elliot

Python computes every financial number from SEC filings.
AI interprets those numbers using Buffett's investment philosophy.
"""

import os
import re
import json
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional, Set

DEFAULT_EMAIL = os.environ.get("SEC_EDGAR_EMAIL", "river313@purdue.edu")
DEFAULT_CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_cache")

# XBRL Tag Definitions per Lab 18 Specification
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
}


def get_sec_headers(email: Optional[str] = None) -> Dict[str, str]:
    """SEC-compliant User-Agent identifying Elliot and a valid contact email."""
    contact_email = email.strip() if email and email.strip() else DEFAULT_EMAIL
    return {
        "User-Agent": f"Elliot {contact_email}",
        "Accept-Encoding": "gzip, deflate",
        "Host": "data.sec.gov" if False else None  # Header host managed by urllib
    }


def lookup_cik(ticker: str, email: Optional[str] = None, cache_dir: str = DEFAULT_CACHE_DIR) -> Tuple[str, str]:
    """
    Look up 10-digit CIK and Company Title from SEC EDGAR company_tickers.json.
    Returns (cik_padded_10_digits, company_title).
    """
    os.makedirs(cache_dir, exist_ok=True)
    tickers_cache_path = os.path.join(cache_dir, "company_tickers.json")
    data = None

    # Try local cache first
    if os.path.exists(tickers_cache_path):
        try:
            with open(tickers_cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = None

    # Fetch from SEC if not in cache
    if not data:
        url = "https://www.sec.gov/files/company_tickers.json"
        headers = {"User-Agent": f"Elliot {email or DEFAULT_EMAIL}"}
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read().decode("utf-8")
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

    # Try reading from cache
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # Fetch live from SEC
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_padded}.json"
    headers = {"User-Agent": f"Elliot {email or DEFAULT_EMAIL}"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read().decode("utf-8")
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


def extract_buffett_metrics(facts_data: Dict[str, Any]) -> Tuple[Dict[str, str], List[Dict[str, Any]]]:
    """
    Extract the 5 fiscal years and calculate:
      - Revenue
      - Net Income
      - Operating Cash Flow
      - CapEx
      - Equity
      - ROE (Net Income / Equity)
      - Owner Earnings (Operating Cash Flow - CapEx)
    Returns (tags_used_dict, rows_list).
    """
    gaap = facts_data.get("facts", {}).get("us-gaap", {})
    extracted_tags: Dict[str, str] = {}
    metric_facts: Dict[str, Dict[str, Dict[str, Any]]] = {}

    for metric_name, candidates in METRIC_TAG_CANDIDATES.items():
        tag, facts = extract_annual_metric_facts(gaap, candidates)
        extracted_tags[metric_name] = tag if tag else "not found"
        metric_facts[metric_name] = facts

    # Determine fiscal year ends: anchor to NetIncome, or Revenue, or common ends
    anchor = metric_facts.get("NetIncome") or metric_facts.get("Revenue") or {}
    all_ends = sorted(list(anchor.keys()))
    if not all_ends:
        # Fallback to union of all available ends
        all_ends_set = set()
        for f_dict in metric_facts.values():
            all_ends_set.update(f_dict.keys())
        all_ends = sorted(list(all_ends_set))

    # Take the last 5 fiscal years
    fy_ends = all_ends[-5:] if len(all_ends) >= 5 else all_ends

    rows: List[Dict[str, Any]] = []
    for end_date in fy_ends:
        rev_fact = metric_facts["Revenue"].get(end_date)
        ni_fact = metric_facts["NetIncome"].get(end_date)
        ocf_fact = metric_facts["OperatingCashFlow"].get(end_date)
        capex_fact = metric_facts["CapEx"].get(end_date)
        eq_fact = metric_facts["Equity"].get(end_date)

        rev_val = rev_fact.get("val") if rev_fact else None
        ni_val = ni_fact.get("val") if ni_fact else None
        ocf_val = ocf_fact.get("val") if ocf_fact else None
        capex_val = capex_fact.get("val") if capex_fact else None
        eq_val = eq_fact.get("val") if eq_fact else None

        # ROE Calculation
        # Rule: If equity is zero or negative, ROE must be "not known"
        if ni_val is not None and eq_val is not None:
            if eq_val > 0:
                roe_val = ni_val / eq_val
            else:
                roe_val = "not known"
        else:
            roe_val = "not known"

        # Owner Earnings Calculation: Operating Cash Flow - CapEx
        # Rule: If CapEx or OCF missing, Owner Earnings must be "not found"
        if ocf_val is not None and capex_val is not None:
            oe_val = ocf_val - capex_val
        else:
            oe_val = "not found"

        rows.append({
            "fiscal_year_end": end_date,
            "revenue": rev_val,
            "net_income": ni_val,
            "operating_cash_flow": ocf_val,
            "capex": capex_val,
            "equity": eq_val,
            "roe": roe_val,
            "owner_earnings": oe_val,
            "source_tags": {
                "revenue": extracted_tags["Revenue"],
                "net_income": extracted_tags["NetIncome"],
                "operating_cash_flow": extracted_tags["OperatingCashFlow"],
                "capex": extracted_tags["CapEx"],
                "equity": extracted_tags["Equity"],
            }
        })

    return extracted_tags, rows


def evaluate_buffett_checks(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Implement Buffett's Three Checks:
      Check 1: ROE >= 15% in EACH of the 5 fiscal years
      Check 2: Owner earnings > 0 in EACH of the 5 fiscal years
      Check 3: Owner earnings in final year > owner earnings in first year
    Each check produces PASS, FAIL, or NOT KNOWN.
    """
    if not rows:
        return {
            "check1": {"name": "ROE >= 15% every year", "status": "NOT KNOWN", "details": "No fiscal years retrieved."},
            "check2": {"name": "Owner earnings positive every year", "status": "NOT KNOWN", "details": "No fiscal years retrieved."},
            "check3": {"name": "Owner earnings growth (FY5 > FY1)", "status": "NOT KNOWN", "details": "No fiscal years retrieved."},
        }

    # Check 1: ROE >= 15%
    roe_vals = [r["roe"] for r in rows]
    if any(r == "not known" or r is None for r in roe_vals):
        c1_status = "NOT KNOWN"
        c1_details = "One or more fiscal years have unknown ROE (missing net income or negative/zero equity)."
    elif all(isinstance(r, (int, float)) and r >= 0.15 for r in roe_vals):
        c1_status = "PASS"
        pct_list = [f"{r*100:.1f}%" for r in roe_vals]
        c1_details = f"ROE exceeded 15.0% in all {len(rows)} fiscal years: {', '.join(pct_list)}."
    else:
        c1_status = "FAIL"
        failed_years = [f"{rows[i]['fiscal_year_end']} ({roe_vals[i]*100:.1f}%)" for i, r in enumerate(roe_vals) if r < 0.15]
        c1_details = f"ROE failed 15% threshold in: {', '.join(failed_years)}."

    # Check 2: Owner Earnings > 0
    oe_vals = [r["owner_earnings"] for r in rows]
    if any(oe == "not found" or oe is None for oe in oe_vals):
        c2_status = "NOT KNOWN"
        c2_details = "Owner earnings cannot be computed because CapEx or Operating Cash Flow is not found."
    elif all(isinstance(oe, (int, float)) and oe > 0 for oe in oe_vals):
        c2_status = "PASS"
        oe_millions = [f"${oe/1e6:,.0f}M" for oe in oe_vals]
        c2_details = f"Owner earnings were positive in all {len(rows)} fiscal years: {', '.join(oe_millions)}."
    else:
        c2_status = "FAIL"
        failed_oe = [f"{rows[i]['fiscal_year_end']} (${oe_vals[i]/1e6:,.0f}M)" for i, oe in enumerate(oe_vals) if oe <= 0]
        c2_details = f"Owner earnings non-positive in: {', '.join(failed_oe)}."

    # Check 3: Owner Earnings Growth (final year > first year)
    if len(rows) < 2 or oe_vals[0] == "not found" or oe_vals[-1] == "not found":
        c3_status = "NOT KNOWN"
        c3_details = "Owner earnings growth cannot be determined because initial or final owner earnings is not found."
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

    return {
        "check1": {"name": "ROE >= 15% every year", "status": c1_status, "details": c1_details},
        "check2": {"name": "Owner earnings positive every year", "status": c2_status, "details": c2_details},
        "check3": {"name": "Owner earnings growth (FY5 > FY1)", "status": c3_status, "details": c3_details},
    }


def get_canonical_numbers(rows: List[Dict[str, Any]]) -> Set[str]:
    """
    Produce the canonical set of valid string representations of all financial numbers
    calculated and printed by the script. Used to detect fabricated numbers in investment memos.
    """
    valid_numbers: Set[str] = set()

    # Allowed threshold constants in Buffett methodology
    valid_numbers.update(["15", "15.0", "15%", "15.0%", "0", "0.0", "5", "3", "1", "2"])

    for r in rows:
        # Years / Dates
        end_date = r["fiscal_year_end"]
        valid_numbers.add(end_date)
        year_str = end_date.split("-")[0]
        valid_numbers.add(year_str)

        for key in ["revenue", "net_income", "operating_cash_flow", "capex", "equity", "owner_earnings"]:
            val = r.get(key)
            if isinstance(val, (int, float)):
                # Exact dollar value
                valid_numbers.add(str(int(val)))
                valid_numbers.add(f"{val:,}")
                # Value in millions rounded to integer
                m_val = round(val / 1e6)
                valid_numbers.add(str(m_val))
                valid_numbers.add(f"{m_val:,}")
                # With dollar sign and suffixes
                valid_numbers.add(f"${m_val:,}")
                valid_numbers.add(f"${m_val:,}M")
                valid_numbers.add(f"${m_val}M")
                # Value in millions with 1 decimal
                m_val_1 = f"{val/1e6:.1f}"
                valid_numbers.add(m_val_1)
                # Value in billions
                b_val_1 = f"{val/1e9:.1f}"
                b_val_2 = f"{val/1e9:.2f}"
                valid_numbers.add(b_val_1)
                valid_numbers.add(b_val_2)
                valid_numbers.add(f"${b_val_1}B")
                valid_numbers.add(f"${b_val_2}B")

        # ROE representations
        roe = r.get("roe")
        if isinstance(roe, (int, float)):
            pct_1 = f"{roe*100:.1f}"
            pct_2 = f"{roe*100:.2f}"
            valid_numbers.add(pct_1)
            valid_numbers.add(pct_2)
            valid_numbers.add(f"{pct_1}%")
            valid_numbers.add(f"{pct_2}%")

    # If rows exist, also include growth numbers
    if len(rows) >= 2:
        oe_0 = rows[0].get("owner_earnings")
        oe_n = rows[-1].get("owner_earnings")
        if isinstance(oe_0, (int, float)) and isinstance(oe_n, (int, float)):
            diff = oe_n - oe_0
            diff_m = round(diff / 1e6)
            valid_numbers.add(str(diff_m))
            valid_numbers.add(f"{diff_m:,}")
            valid_numbers.add(f"${diff_m:,}")
            valid_numbers.add(f"${diff_m:,}M")
            if oe_0 != 0:
                pct = (diff / abs(oe_0)) * 100
                valid_numbers.add(f"{pct:.1f}")
                valid_numbers.add(f"{pct:.1f}%")
                valid_numbers.add(f"{round(pct)}")
                valid_numbers.add(f"{round(pct)}%")

    return valid_numbers


def detect_unsupported_numbers(memo_text: str, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detector that flags any financial number or percentage in the memo that was NOT printed by the script.
    Extracts percentages (e.g. 40.0%), currency amounts (e.g. $4,000M), and standalone numeric tokens.
    Excludes markdown headers, citations, and structural numbering.
    """
    canonical_set = get_canonical_numbers(rows)
    unsupported = []

    # Regex patterns for financial figures
    # 1. Percentages: e.g. 40.0%, 28.3%, 15%
    pct_pattern = re.compile(r"\b\d+(?:\.\d+)?%")
    # 2. Currency: e.g. $226,954, $5,844M, $227B, $40.0
    curr_pattern = re.compile(r"\$[\d,]+(?:\.\d+)?(?:[MBmb])?")
    # 3. Standalone numbers with commas or decimals: e.g. 226,954, 40.0
    num_pattern = re.compile(r"(?<![A-Za-z0-9_#\-\/])(?:\b\d{1,3}(?:,\d{3})+(?:\.\d+)?|\b\d+\.\d+)(?![A-Za-z0-9_%])")

    lines = memo_text.splitlines()
    for line_num, line in enumerate(lines, 1):
        # Ignore markdown headers, URLs, code blocks, or markdown comments
        stripped = line.strip()
        if stripped.startswith(("#", "```", "http://", "https://", "<!--", "* [Elliot")):
            continue

        # Extract tokens, preferring longer specific matches (percentages and currencies first)
        tokens = []
        # Find spans of percentages and currencies so we don't double count their substrings
        matched_spans = []

        for m in pct_pattern.finditer(line):
            tokens.append(m.group(0))
            matched_spans.append((m.start(), m.end()))

        for m in curr_pattern.finditer(line):
            tokens.append(m.group(0))
            matched_spans.append((m.start(), m.end()))

        for m in num_pattern.finditer(line):
            # Check if this span overlaps with an already matched pct or currency
            span = (m.start(), m.end())
            if not any(s <= span[0] and span[1] <= e for s, e in matched_spans):
                tokens.append(m.group(0))

        for tok in tokens:
            cleaned = tok.strip()
            base_cleaned = cleaned.replace("$", "").replace("%", "").replace("M", "").replace("B", "").replace(",", "")

            # Check if token itself or base is in canonical set
            is_valid = (
                cleaned in canonical_set
                or base_cleaned in canonical_set
                or tok in canonical_set
            )

            # Common narrative non-financial numbers to ignore (e.g. 10-K, year 2022-2026, 1, 2, 3)
            if base_cleaned in {"10", "1", "2", "3", "4", "5", "0"}:
                is_valid = True

            if not is_valid:
                unsupported.append({
                    "line": line_num,
                    "token": tok,
                    "context": line.strip()
                })

    return unsupported


def generate_investment_memo(
    ticker: str,
    company_title: str,
    rows: List[Dict[str, Any]],
    tags_used: Dict[str, str],
    checks: Dict[str, Dict[str, Any]]
) -> str:
    """
    Generate Buffett Investment Memo dynamically for any company ticker:
      - Strictly references only financial numbers actually printed/computed by the script
      - Dynamically builds the financial table from retrieved SEC 10-K rows
      - Explains Buffett's three fundamental checks with exact status and empirical values
      - Acknowledges missing data (e.g. CapEx and Owner Earnings for commercial banks like JPM)
      - Chooses conclusion: OWN THE BUSINESS, WATCH, or PASS
      - Evaluates business quality, not valuation or stock price
      - Leaves clearly marked placeholder for Elliot's personal decision
    """
    ticker_clean = ticker.strip().upper()
    c1 = checks["check1"]["status"]
    c2 = checks["check2"]["status"]
    c3 = checks["check3"]["status"]

    # Format dynamic markdown table
    table_lines = [
        "| Fiscal Year End | Revenue | Net Income | Operating Cash Flow | CapEx | Equity | ROE | Owner Earnings |",
        "| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"
    ]
    for r in rows:
        rev_s = f"{r['revenue']/1e6:,.0f}" if isinstance(r['revenue'], (int, float)) else "not found"
        ni_s = f"{r['net_income']/1e6:,.0f}" if isinstance(r['net_income'], (int, float)) else "not found"
        ocf_s = f"{r['operating_cash_flow']/1e6:,.0f}" if isinstance(r['operating_cash_flow'], (int, float)) else "not found"
        capex_s = f"{r['capex']/1e6:,.0f}" if isinstance(r['capex'], (int, float)) else "not found"
        eq_s = f"{r['equity']/1e6:,.0f}" if isinstance(r['equity'], (int, float)) else "not found"
        roe_s = f"{r['roe']*100:.1f}%" if isinstance(r['roe'], (int, float)) else str(r['roe'])
        oe_s = f"{r['owner_earnings']/1e6:,.0f}" if isinstance(r['owner_earnings'], (int, float)) else str(r['owner_earnings'])
        table_lines.append(f"| {r['fiscal_year_end']} | {rev_s} | {ni_s} | {ocf_s} | {capex_s} | {eq_s} | {roe_s} | {oe_s} |")
    table_md = "\n".join(table_lines)

    # Determine Verdict based on checks
    if c1 == "PASS" and c2 == "PASS" and c3 == "PASS":
        verdict = "OWN THE BUSINESS"
        verdict_summary = f"{company_title} ({ticker_clean}) satisfies all three of Warren Buffett's operational quality checks, demonstrating an expanding economic moat and compounding owner cash flows."
    elif c2 == "NOT KNOWN" or c3 == "NOT KNOWN":
        verdict = "WATCH"
        verdict_summary = f"For {company_title} ({ticker_clean}), owner earnings cannot be evaluated with the available inputs because capital spending (CapEx) is not found in official SEC 10-K filings. The business requires contextual monitoring outside standard industrial owner earnings models."
    else:
        verdict = "PASS"
        verdict_summary = f"{company_title} ({ticker_clean}) fails one or more of Buffett's fundamental hurdles, indicating cyclicality, margin pressure, or inadequate return on shareholder equity."

    # Company specific moat & limitation sections
    if ticker_clean == "COST":
        moat_content = """1. **Unassailable Low-Cost Scale (The Shared-Economy Moat):**  
   Costco operates on a strict gross margin ceiling across branded merchandise. Instead of pocketing supplier discounts, management passes wholesale volume savings directly to members. This creates an impenetrable barrier to entry: competitors cannot underprice Costco without sustaining catastrophic operating losses.
2. **Membership Fee Cash Flow Engine:**  
   Membership fees provide pure, upfront, recurring cash flow with renewal rates remaining near-total across North America. This subscription layer de-risks cash flow volatility.
3. **Working Capital Efficiency:**  
   Because of rapid inventory turns, Costco routinely sells goods and collects cash from customers before it has to pay suppliers, allowing the business to finance its operations on negative working capital.
4. **Kirkland Signature Brand Power:**  
   Costco's proprietary private-label brand generates billions in high-loyalty sales, giving Costco immense leverage against national consumer packaged goods manufacturers."""
        risk_content = """1. **Brick-and-Mortar Capital Intensity:**  
   CapEx rose across recent fiscal years as warehouse construction, depot automation, and land acquisition costs increased. Continued physical warehouse expansion requires sustained capital allocation.
2. **Ultra-Thin Operating Margin Cushion:**  
   Because Costco passes savings to consumers, its operating margin remains intentionally narrow. Any unexpected surge in freight, labor, or supply chain bottlenecks must be offset by volume or membership fee adjustments.
3. **Geographic Saturation in Core Markets:**  
   Future multi-decade compounding increasingly relies on international warehouse penetration, which carries regulatory, currency, and local supply chain complexities."""
    elif ticker_clean == "JPM":
        moat_content = """1. **Fortress Balance Sheet & Systemic Scale:**  
   JPMorgan Chase operates the largest deposit and commercial banking franchise in the United States, providing an unmatched funding base and lower relative cost of funds.
2. **Diversified Non-Interest Fee Engines:**  
   Substantial fee streams across asset management, payment processing, and corporate advisory mitigate net interest income cyclicality.
3. **Technological Reinvestment Scale:**  
   Management reinvests billions annually in financial cybersecurity, payment infrastructure, and digital banking platforms, widening its moat over smaller regional institutions."""
        risk_content = """1. **Unavailability of Standard Owner Earnings:**  
   Commercial banks do not report conventional capital expenditures (`PaymentsToAcquirePropertyPlantAndEquipment` or `PaymentsToAcquireProductiveAssets`). As a result, Buffett's industrial Owner Earnings metric cannot be computed from standard 10-K filings.
2. **Cyclical Credit & Interest Rate Exposure:**  
   Net income and return on equity are inherently sensitive to Federal Reserve benchmark rate cycles, loan loss provisions, and macroeconomic credit deterioration.
3. **Regulatory Capital Constraints:**  
   Stringent Basel III / Federal Reserve capital adequacy rules constrain capital return and limit equity compounding compared to unencumbered industrial franchises."""
    else:
        moat_content = f"""1. **Franchise Durability:**  
   Evaluating whether {company_title} possesses sustainable structural cost advantages, customer switching costs, or network effects.
2. **Capital Efficiency:**  
   Assessing whether high returns on capital can be sustained without reliance on destructive financial leverage."""
        risk_content = f"""1. **Reinvestment Burden:**  
   Capital required to maintain competitive standing and volume.
2. **Industry Headwinds:**  
   Technological obsolescence, supplier concentration, or pricing pressure."""

    memo = f"""# Warren Buffett Investment Memo: {company_title} ({ticker_clean})

**Prepared for:** FIN 439 — Applied Financial Modeling & Corporate Valuation  
**Analyst:** Elliot  
**Data Source:** Official SEC EDGAR 10-K Filings  
**Mandate:** Quality Business Appraisal (Valuation & Market Price Intentionally Excluded)  

---

## 1. Executive Summary & Quality Verdict

**Conclusion:** **{verdict}**

{verdict_summary}

### Buffett Quality Audit Overview:
* **Check 1 (Return on Equity >= 15.0%):** **{c1}**
* **Check 2 (Owner Earnings Positive Every Year):** **{c2}**
* **Check 3 (Owner Earnings Growth):** **{c3}**

This appraisal evaluates {company_title} strictly on the durability of its economic castle and competitive barriers. In accordance with FIN 439 Lab 18 requirements, no stock price, valuation multiple, or market-timing data is permitted.

---

## 2. Audited SEC Financial Foundation

All figures below were retrieved dynamically from official 10-K filings via the SEC EDGAR API and computed in Python. Figures are presented in USD millions, except Return on Equity.

{table_md}

### Source XBRL Taxonomy Tags
* **Revenue:** `{tags_used.get('Revenue', 'not found')}`
* **Net Income:** `{tags_used.get('NetIncome', 'not found')}`
* **Operating Cash Flow:** `{tags_used.get('OperatingCashFlow', 'not found')}`
* **Capital Spending (CapEx):** `{tags_used.get('CapEx', 'not found')}`
* **Stockholders' Equity:** `{tags_used.get('Equity', 'not found')}`

---

## 3. Buffett's Three Fundamental Checks

### Check 1: Return on Equity (ROE >= 15.0% in All Five Years)
* **Result:** **{c1}**
* **Buffett Philosophy:** Return on equity demonstrates how productively management deploys shareholder capital without relying on excessive financial leverage. Buffett looks for businesses that can sustain an ROE of at least 15.0% year in and year out.
* **Empirical Evidence:** {checks['check1']['details']}

### Check 2: Owner Earnings Positive in All Five Years
* **Result:** **{c2}**
* **Buffett Philosophy:** In his 1986 Berkshire Hathaway shareholder letter, Buffett defined **Owner Earnings** as Operating Cash Flow minus Capital Expenditures (the capital necessary to fully maintain long-term competitive position and unit volume). A true franchise generates surplus cash beyond maintenance reinvestment.
* **Empirical Evidence:** {checks['check2']['details']}

### Check 3: Owner Earnings Growth (Final Year > First Year)
* **Result:** **{c3}**
* **Buffett Philosophy:** A business possessing an expanding moat must see its cash-generating power compound over time. An inflationary environment exposes weak businesses whose capital requirements outpace earnings.
* **Empirical Evidence:** {checks['check3']['details']}

---

## 4. Economic Moat & Business Strengths

{moat_content}

---

## 5. Business Limitations & Operational Risks

{risk_content}

---

## 6. Synthesis & Final Verdict

Warren Buffett prioritizes business quality above all else: *"It's far better to buy a wonderful company at a fair price than a fair company at a wonderful price."*

**Quality Verdict:** **{verdict}**

---

## 7. Student Reflection & Personal Verdict

<!-- STUDENT DECISION PLACEHOLDER: DO NOT FABRICATE -->
### Elliot's Personal Decision:
> **Do I personally trust Buffett's verdict on {ticker_clean}?**  
> *[Elliot's one-sentence decision to be entered here before submission]*
"""
    return memo


def generate_costco_investment_memo(rows: List[Dict[str, Any]], tags_used: Dict[str, str], checks: Dict[str, Dict[str, Any]]) -> str:
    """Generate Costco investment memo using the general memo generator."""
    return generate_investment_memo("COST", "Costco Wholesale Corporation", rows, tags_used, checks)



def format_table_output(tags_used: Dict[str, str], rows: List[Dict[str, Any]], checks: Dict[str, Dict[str, Any]]) -> str:
    """Format console output as a clean table matching Lab 18 requirements."""
    out = []
    out.append("=" * 80)
    out.append("FIN 439 - Lab 18: Warren Buffett SEC Financial Analysis")
    out.append("Data Source: SEC EDGAR API (10-K Filings Only)")
    out.append("=" * 80)
    out.append("\nSource XBRL Tags Used:")
    for metric, tag in tags_used.items():
        out.append(f"  * {metric:<20}: {tag}")

    out.append("\nAudited Financial Metrics Table (USD Millions, except ROE):")
    header = f"{'Fiscal Year End':<16} | {'Revenue':>10} | {'Net Income':>10} | {'OCF':>10} | {'CapEx':>10} | {'Equity':>10} | {'ROE':>8} | {'Owner Earn':>10}"
    out.append("-" * len(header))
    out.append(header)
    out.append("-" * len(header))

    for r in rows:
        rev_s = f"{r['revenue']/1e6:,.0f}" if isinstance(r['revenue'], (int, float)) else "not found"
        ni_s = f"{r['net_income']/1e6:,.0f}" if isinstance(r['net_income'], (int, float)) else "not found"
        ocf_s = f"{r['operating_cash_flow']/1e6:,.0f}" if isinstance(r['operating_cash_flow'], (int, float)) else "not found"
        capex_s = f"{r['capex']/1e6:,.0f}" if isinstance(r['capex'], (int, float)) else "not found"
        eq_s = f"{r['equity']/1e6:,.0f}" if isinstance(r['equity'], (int, float)) else "not found"
        roe_s = f"{r['roe']*100:.1f}%" if isinstance(r['roe'], (int, float)) else str(r['roe'])
        oe_s = f"{r['owner_earnings']/1e6:,.0f}" if isinstance(r['owner_earnings'], (int, float)) else str(r['owner_earnings'])

        out.append(f"{r['fiscal_year_end']:<16} | {rev_s:>10} | {ni_s:>10} | {ocf_s:>10} | {capex_s:>10} | {eq_s:>10} | {roe_s:>8} | {oe_s:>10}")
    out.append("-" * len(header))

    out.append("\nBuffett's Three Fundamental Checks:")
    for key in ["check1", "check2", "check3"]:
        c = checks[key]
        out.append(f"  [{c['status']}] {c['name']}")
        out.append(f"         {c['details']}")

    out.append("=" * 80)
    return "\n".join(out)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Warren Buffett SEC Financial Retrieval & Analysis")
    parser.add_argument("--ticker", type=str, default="COST", help="Company stock ticker (e.g. COST, JPM)")
    parser.add_argument("--email", type=str, default=DEFAULT_EMAIL, help="User contact email for SEC User-Agent")
    parser.add_argument("--cache-dir", type=str, default=DEFAULT_CACHE_DIR, help="Directory for caching SEC responses")
    parser.add_argument("--memo", action="store_true", help="Generate Buffett investment memo")
    args = parser.parse_args()

    cik, title = lookup_cik(args.ticker, email=args.email, cache_dir=args.cache_dir)
    facts = fetch_company_facts(cik, email=args.email, cache_dir=args.cache_dir)
    tags, rows = extract_buffett_metrics(facts)
    checks = evaluate_buffett_checks(rows)

    print(format_table_output(tags, rows, checks))

    if args.memo:
        memo = generate_investment_memo(args.ticker, title, rows, tags, checks)
        print("\n" + "=" * 80)
        print(f"INVESTMENT MEMO PREVIEW: {title} ({args.ticker.upper()})")
        print("=" * 80)
        print(memo[:1500] + "\n... [truncated] ...")
