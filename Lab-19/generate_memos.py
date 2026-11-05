"""
generate_memos.py - Generate and save investor memos for Lab 19
FIN 439 - Purdue University
Student: Elliot

Generates Warren Buffett, Benjamin Graham, and Michael Burry memos
for any specified ticker using audited SEC EDGAR data.
"""

import os
import sys
import argparse

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import legend_sec


def generate_and_save_memos(
    ticker: str,
    graham_threshold: float = 2.0,
    cache_dir: str = None,
    email: str = None,
):
    cache_dir = cache_dir or os.path.join(current_dir, "data_cache")
    memos_dir = os.path.join(current_dir, "memos")
    os.makedirs(memos_dir, exist_ok=True)

    ticker_upper = ticker.strip().upper()
    cik, title = legend_sec.lookup_cik(ticker_upper, email=email, cache_dir=cache_dir)
    facts = legend_sec.fetch_company_facts(cik, email=email, cache_dir=cache_dir)
    tags, rows = legend_sec.extract_legend_metrics(facts)

    b_checks = legend_sec.evaluate_buffett_checks(rows)
    g_checks = legend_sec.evaluate_graham_checks(rows, current_ratio_threshold=graham_threshold)
    m_checks = legend_sec.evaluate_burry_checks(rows)

    probe_note = (
        "I kept Graham's original 2.0 threshold because lowering it to 1.0 makes Costco pass but weakens the liquidity standard, showing how a screening decision depends on the threshold chosen."
        if ticker_upper == "COST"
        else f"Screening threshold probe recorded at {graham_threshold:.1f}x."
    )

    b_memo = legend_sec.generate_buffett_memo(ticker_upper, title, rows, tags, b_checks)
    g_memo = legend_sec.generate_graham_memo(
        ticker_upper,
        title,
        rows,
        tags,
        g_checks,
        threshold_probe_note=probe_note,
    )
    m_memo = legend_sec.generate_burry_memo(ticker_upper, title, rows, tags, m_checks)

    # Standardize filename prefix (use costco_ for COST, else lowercase ticker)
    prefix = "costco" if ticker_upper == "COST" else ticker_upper.lower()
    b_path = os.path.join(memos_dir, f"{prefix}_buffett_memo.md")
    g_path = os.path.join(memos_dir, f"{prefix}_graham_memo.md")
    m_path = os.path.join(memos_dir, f"{prefix}_burry_memo.md")

    with open(b_path, "w", encoding="utf-8") as f:
        f.write(b_memo)
    with open(g_path, "w", encoding="utf-8") as f:
        f.write(g_memo)
    with open(m_path, "w", encoding="utf-8") as f:
        f.write(m_memo)

    print(f"Generated 3 investor memos for {ticker_upper} in: {memos_dir}")
    print(f"  - Buffett: {b_path}")
    print(f"  - Graham:  {g_path}")
    print(f"  - Burry:   {m_path}")
    return b_path, g_path, m_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Legend Panel Investment Memos")
    parser.add_argument("--ticker", type=str, default="COST", help="Equity stock ticker (e.g. COST, AAPL, JPM)")
    parser.add_argument("--threshold", type=float, default=2.0, help="Graham current ratio threshold (default: 2.0)")
    parser.add_argument("--email", type=str, default=None, help="Contact email for SEC EDGAR User-Agent")
    args = parser.parse_args()

    generate_and_save_memos(ticker=args.ticker, graham_threshold=args.threshold, email=args.email)
