"""
generate_memos.py - Generate and save investor memos for Lab 19
"""
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import legend_sec


def generate_and_save_memos(ticker: str, cache_dir: str = None, email: str = None):
    cache_dir = cache_dir or os.path.join(current_dir, "data_cache")
    memos_dir = os.path.join(current_dir, "memos")
    os.makedirs(memos_dir, exist_ok=True)

    cik, title = legend_sec.lookup_cik(ticker, email=email, cache_dir=cache_dir)
    facts = legend_sec.fetch_company_facts(cik, email=email, cache_dir=cache_dir)
    tags, rows = legend_sec.extract_legend_metrics(facts)

    b_checks = legend_sec.evaluate_buffett_checks(rows)
    g_checks = legend_sec.evaluate_graham_checks(rows, current_ratio_threshold=2.0)
    m_checks = legend_sec.evaluate_burry_checks(rows)

    b_memo = legend_sec.generate_buffett_memo(ticker, title, rows, tags, b_checks)
    g_memo = legend_sec.generate_graham_memo(
        ticker,
        title,
        rows,
        tags,
        g_checks,
        threshold_probe_note=(
            "I kept Graham's original 2.0 threshold because lowering it to 1.0 makes Costco pass but weakens the liquidity standard, showing how a screening decision depends on the threshold chosen."
            if ticker.upper() == "COST"
            else None
        ),
    )
    m_memo = legend_sec.generate_burry_memo(ticker, title, rows, tags, m_checks)

    prefix = ticker.lower()
    b_path = os.path.join(memos_dir, f"{prefix}_buffett_memo.md")
    g_path = os.path.join(memos_dir, f"{prefix}_graham_memo.md")
    m_path = os.path.join(memos_dir, f"{prefix}_burry_memo.md")

    with open(b_path, "w", encoding="utf-8") as f:
        f.write(b_memo)
    with open(g_path, "w", encoding="utf-8") as f:
        f.write(g_memo)
    with open(m_path, "w", encoding="utf-8") as f:
        f.write(m_memo)

    if ticker.upper() == "COST":
        with open(os.path.join(memos_dir, "costco_buffett_memo.md"), "w", encoding="utf-8") as f:
            f.write(b_memo)
        with open(os.path.join(memos_dir, "costco_graham_memo.md"), "w", encoding="utf-8") as f:
            f.write(g_memo)
        with open(os.path.join(memos_dir, "costco_burry_memo.md"), "w", encoding="utf-8") as f:
            f.write(m_memo)

    print(f"Generated memos for {ticker.upper()} in {memos_dir}")
    return b_path, g_path, m_path


if __name__ == "__main__":
    generate_and_save_memos("COST")
