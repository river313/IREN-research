"""
FIN 43900 — Lab 16: Provenance Gate (Point-in-Time Data Filter)
Student: Elliot
Course: FIN 43900 (Applied Financial Modeling & Corporate Valuation, Purdue University)

Description:
Point-in-time provenance filter enforcing strict temporal availability constraints
to prevent look-ahead bias in macroeconomic and retail card-spend signals.

Standard Library Only.
"""

import sys
from datetime import datetime

# ============================================================================
# EDITABLE INPUTS (Top of File)
# ============================================================================

# Default decision date: A row is knowable only if published on or before this date.
DECISION_DATE = "2026-03-31"

# Fictional card-spend index table (12 rows, 3 retailers: AAA, BBB, CCC)
RAW_DATA = [
    {"row": 1,  "ticker": "AAA", "month_measured": "2026-01", "published_on": "2026-02-10", "index": 101.0},
    {"row": 2,  "ticker": "AAA", "month_measured": "2026-02", "published_on": "2026-03-10", "index": 104.0},
    {"row": 3,  "ticker": "AAA", "month_measured": "2026-03", "published_on": "2026-04-10", "index": 109.0},
    {"row": 4,  "ticker": "AAA", "month_measured": "2026-02", "published_on": "2026-03-25", "index": 103.0},
    {"row": 5,  "ticker": "BBB", "month_measured": "2026-01", "published_on": "2026-02-10", "index": 98.0},
    {"row": 6,  "ticker": "BBB", "month_measured": "2026-02", "published_on": "2026-03-10", "index": 97.0},
    {"row": 7,  "ticker": "BBB", "month_measured": "2026-02", "published_on": "2026-03-10", "index": 97.0},
    {"row": 8,  "ticker": "BBB", "month_measured": "2026-03", "published_on": "2026-04-10", "index": 92.0},
    {"row": 9,  "ticker": "CCC", "month_measured": "2026-01", "published_on": "2026-02-10", "index": 110.0},
    {"row": 10, "ticker": "CCC", "month_measured": "2026-02", "published_on": "2026-04-05", "index": 112.0},
    {"row": 11, "ticker": "",    "month_measured": "2026-02", "published_on": "2026-03-10", "index": 99.0},
    {"row": 12, "ticker": "CCC", "month_measured": "2026-02", "published_on": "2026-03-10", "index": 111.0},
]


# ============================================================================
# FILTER IMPLEMENTATION
# ============================================================================

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def format_month_name(month_str):
    """Convert 'YYYY-MM' to full month name (e.g., '2026-02' -> 'February')."""
    return datetime.strptime(month_str, "%Y-%m").strftime("%B")


def filter_point_in_time(raw_data, decision_date):
    """
    Applies the four provenance rules in exact sequence:
      Rule 1: Quarantine rows with missing tickers.
      Rule 2: Remove exact duplicate observations.
      Rule 3: Remove observations published after the decision date.
      Rule 4: For each ticker and measured month, retain the latest publication
              available as of the decision date (superseding older revisions).
    """
    funnel = {}
    
    # ------------------------------------------------------------------------
    # Rule 1: Quarantine rows with missing tickers
    # ------------------------------------------------------------------------
    surviving_r1 = []
    removed_r1 = []
    for item in raw_data:
        ticker = item.get("ticker", "")
        if ticker is None or ticker.strip() == "":
            removed_r1.append(item["row"])
        else:
            surviving_r1.append(item)
    funnel["Rule 1: Quarantined: no ticker"] = removed_r1

    # ------------------------------------------------------------------------
    # Rule 2: Remove exact duplicate observations
    # ------------------------------------------------------------------------
    surviving_r2 = []
    removed_r2 = []
    seen_exact = set()
    for item in surviving_r1:
        key = (item["ticker"].strip(), item["month_measured"], item["published_on"], item["index"])
        if key in seen_exact:
            removed_r2.append(item["row"])
        else:
            seen_exact.add(key)
            surviving_r2.append(item)
    funnel["Rule 2: Exact duplicate"] = removed_r2

    # ------------------------------------------------------------------------
    # Rule 3: Remove observations published after the decision date
    # ------------------------------------------------------------------------
    surviving_r3 = []
    removed_r3 = []
    for item in surviving_r2:
        if item["published_on"] > decision_date:
            removed_r3.append(item["row"])
        else:
            surviving_r3.append(item)
    funnel[f"Rule 3: Published after {decision_date}"] = removed_r3

    # ------------------------------------------------------------------------
    # Rule 4: Retain the latest publication available as of the decision date
    # ------------------------------------------------------------------------
    # Group remaining observations by (ticker, month_measured)
    groups = {}
    for item in surviving_r3:
        group_key = (item["ticker"], item["month_measured"])
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(item)

    surviving_r4 = []
    removed_r4 = []
    for group_key, items in groups.items():
        if len(items) == 1:
            surviving_r4.append(items[0])
        else:
            # Sort by published_on descending, then row id descending if tied
            sorted_items = sorted(items, key=lambda x: (x["published_on"], x["row"]), reverse=True)
            winner = sorted_items[0]
            surviving_r4.append(winner)
            for loser in sorted_items[1:]:
                removed_r4.append(loser["row"])
                
    # Sort removed_r4 to report clean row numbers
    removed_r4.sort()
    funnel["Rule 4: Older vintage replaced by a revision"] = removed_r4

    # Sort final surviving panel by row id
    surviving_r4.sort(key=lambda x: x["row"])
    funnel["As-of panel"] = [x["row"] for x in surviving_r4]

    return funnel, surviving_r4


def build_naive_panel(raw_data):
    """
    Builds the naive panel using data hygiene (Rules 1 & 2), but ignoring the
    decision date cutoff (Rule 3) and selecting the latest publication across all time (Rule 4).
    """
    # Rule 1
    surviving_r1 = [item for item in raw_data if item.get("ticker", "").strip() != ""]
    # Rule 2
    surviving_r2 = []
    seen_exact = set()
    for item in surviving_r1:
        key = (item["ticker"].strip(), item["month_measured"], item["published_on"], item["index"])
        if key not in seen_exact:
            seen_exact.add(key)
            surviving_r2.append(item)
            
    # Group by (ticker, month_measured) and take latest published_on across all dates
    groups = {}
    for item in surviving_r2:
        group_key = (item["ticker"], item["month_measured"])
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(item)

    naive_panel = []
    for group_key, items in groups.items():
        sorted_items = sorted(items, key=lambda x: (x["published_on"], x["row"]), reverse=True)
        winner = sorted_items[0]
        # Track whether this was a revised vintage (multiple publications exist for this month)
        winner_copy = dict(winner)
        winner_copy["is_revised"] = len(items) > 1
        naive_panel.append(winner_copy)

    naive_panel.sort(key=lambda x: x["row"])
    return naive_panel


def compute_ticker_signals(panel, label=""):
    """
    Computes signals for each ticker in the panel:
    Percent change from previous month to latest month:
      Percentage change = (Latest index / Previous month's index - 1) * 100
    """
    # Group by ticker
    by_ticker = {}
    for item in panel:
        t = item["ticker"]
        if t not in by_ticker:
            by_ticker[t] = []
        by_ticker[t].append(item)

    signals = {}
    for ticker, items in sorted(by_ticker.items()):
        # Sort items chronologically by month_measured
        sorted_months = sorted(items, key=lambda x: x["month_measured"])
        if len(sorted_months) < 2:
            signals[ticker] = {
                "pct_change": None,
                "latest_month": sorted_months[-1]["month_measured"] if sorted_months else None,
                "formatted": "N/A (insufficient history)",
                "details": None
            }
            continue

        prev_item = sorted_months[-2]
        latest_item = sorted_months[-1]
        
        pct_change = ((latest_item["index"] / prev_item["index"]) - 1.0) * 100.0
        month_name = format_month_name(latest_item["month_measured"])
        
        sign = "+" if pct_change > 0 else ("-" if pct_change < 0 else "")
        # Format string
        val_str = f"{sign}{abs(pct_change):.2f}%"
        
        revised_note = ""
        if latest_item.get("is_revised", False):
            revised_note = ", revised"

        display_str = f"{val_str} ({month_name}{revised_note})"
        
        signals[ticker] = {
            "pct_change": pct_change,
            "latest_month": latest_item["month_measured"],
            "month_name": month_name,
            "prev_index": prev_item["index"],
            "latest_index": latest_item["index"],
            "prev_row": prev_item["row"],
            "latest_row": latest_item["row"],
            "formatted": display_str
        }

    return signals


# ============================================================================
# MAIN EXECUTION AND REPORTING
# ============================================================================

def run_pipeline(decision_date=DECISION_DATE, verbose=True):
    """Executes the full pipeline for a given decision date."""
    funnel, asof_panel = filter_point_in_time(RAW_DATA, decision_date)
    naive_panel = build_naive_panel(RAW_DATA)
    
    asof_signals = compute_ticker_signals(asof_panel, label="As-Of")
    naive_signals = compute_ticker_signals(naive_panel, label="Naive")
    
    if verbose:
        print("=" * 80)
        print(f"FIN 439 LAB 16: PROVENANCE GATE -- POINT-IN-TIME FILTER")
        print(f"DECISION DATE: {decision_date}")
        print("=" * 80)
        
        print("\n--- 1. ROW FUNNEL ---")
        print(f"{'Funnel Step':<42} | {'Count':<5} | {'Row Numbers':<20}")
        print("-" * 75)
        for step, rows in funnel.items():
            row_str = ", ".join(map(str, rows)) if rows else "(none)"
            print(f"{step:<42} | {len(rows):<5} | {row_str:<20}")
            
        print("\n--- 2. FINAL AS-OF PANEL ---")
        print(f"{'Row':<4} | {'Ticker':<6} | {'Month Measured':<14} | {'Published On':<12} | {'Index Value':<10}")
        print("-" * 55)
        for r in asof_panel:
            print(f"{r['row']:<4} | {r['ticker']:<6} | {r['month_measured']:<14} | {r['published_on']:<12} | {r['index']:<10.1f}")
            
        print("\n--- 3. SIGNAL COMPARISON (AS-OF VS NAIVE) ---")
        print(f"{'Ticker':<8} | {'As-Of Signal':<25} | {'Naive Signal':<28}")
        print("-" * 65)
        for ticker in sorted(asof_signals.keys()):
            asof_str = asof_signals[ticker]["formatted"]
            naive_str = naive_signals[ticker]["formatted"]
            print(f"{ticker:<8} | {asof_str:<25} | {naive_str:<28}")

        print("\n--- 4. NUMERICAL VERIFICATION AUDIT ---")
        for ticker in sorted(asof_signals.keys()):
            s = asof_signals[ticker]
            print(f"[{ticker} As-Of] Month: {s['month_name']} | "
                  f"Formula: ({s['latest_index']} / {s['prev_index']} - 1) * 100 = {s['pct_change']:+.4f}% -> {s['formatted']}")
            ns = naive_signals[ticker]
            print(f"[{ticker} Naive] Month: {ns['month_name']} | "
                  f"Formula: ({ns['latest_index']} / {ns['prev_index']} - 1) * 100 = {ns['pct_change']:+.4f}% -> {ns['formatted']}")
        print("=" * 80)

    return {
        "funnel": funnel,
        "asof_panel": asof_panel,
        "naive_panel": naive_panel,
        "asof_signals": asof_signals,
        "naive_signals": naive_signals,
    }


if __name__ == "__main__":
    # Allow overriding decision date via CLI argument if passed, else use DECISION_DATE
    active_date = sys.argv[1] if len(sys.argv) > 1 else DECISION_DATE
    run_pipeline(active_date)
