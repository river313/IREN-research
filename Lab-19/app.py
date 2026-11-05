"""
app.py - Multi-Investor Legend Panel (Warren Buffett, Benjamin Graham, Michael Burry)
FIN 439 - Purdue University
Student: Elliot

Python computes every financial number from SEC EDGAR filings.
AI interprets those figures using each legend investor's philosophy.
Educational demonstration, not investment advice.
"""

import os
import sys
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Ensure Lab-19 directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import legend_sec

# -----------------------------------------------------------------------------
# Streamlit Page Configuration & Modern Financial Theme
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Legend Investor Panel | FIN 439",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Dark Navy Institutional Financial Dashboard
st.markdown("""
<style>
    /* Global background and base typography */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Headers */
    h1, h2, h3, h4 {
        color: #F8FAFC !important;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* Institutional disclaimer banner */
    .attribution-banner {
        background: linear-gradient(90deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-left: 3px solid #38BDF8;
        padding: 12px 18px;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #94A3B8;
        margin-bottom: 24px;
    }
    
    /* Metric & verdict cards */
    .metric-card {
        background: #111827;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.25);
    }
    
    /* Status Badges */
    .badge-pass {
        background-color: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid #059669;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-fail {
        background-color: rgba(239, 68, 68, 0.15);
        color: #F87171;
        border: 1px solid #DC2626;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-block;
    }
    .badge-notknown {
        background-color: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid #D97706;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 700;
        display: inline-block;
    }

    /* Memo scroll containers */
    .memo-container {
        background: #111827;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 18px;
        height: 640px;
        overflow-y: auto;
        font-size: 0.9rem;
        line-height: 1.55;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Sidebar Configuration & Controls
# -----------------------------------------------------------------------------
st.sidebar.markdown("## 🏛️ Legend Panel Controls")
st.sidebar.markdown("**Student:** Elliot  \n**Course:** FIN 43900 | Purdue University")

st.sidebar.markdown("---")
email_input = st.sidebar.text_input(
    "SEC User-Agent Contact Email",
    value=os.environ.get("SEC_EDGAR_EMAIL", "river313@purdue.edu"),
    help="Identifies Elliot in accordance with SEC fair-access policy.",
)

st.sidebar.markdown("### Target Company")
prefill_ticker = st.sidebar.selectbox(
    "Quick Select Benchmark / Test:",
    ["COST (Costco)", "AAPL (Apple - Project 2 Holding)", "JPM (JPMorgan - Missing CapEx Test)", "Custom Ticker"],
    index=0,
)

if prefill_ticker.startswith("COST"):
    default_t = "COST"
elif prefill_ticker.startswith("AAPL"):
    default_t = "AAPL"
elif prefill_ticker.startswith("JPM"):
    default_t = "JPM"
else:
    default_t = "MSFT"

ticker_input = st.sidebar.text_input("Equity Stock Ticker", value=default_t).strip().upper()

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Graham Threshold Probe")
graham_thresh = st.sidebar.slider(
    "Graham Current Ratio Threshold",
    min_value=0.5,
    max_value=3.0,
    value=2.0,
    step=0.1,
    help="Default is 2.0 (Graham's classical defensive standard). Probe at 1.0 to evaluate retail working capital sensitivity."
)

if graham_thresh == 2.0:
    st.sidebar.info("📐 **Standard Benchmark:** 2.0 (Graham's classical defensive standard)")
elif graham_thresh == 1.0:
    st.sidebar.success("🔬 **Probe Active:** 1.0 (Testing retail operating cash conversion)")
else:
    st.sidebar.warning(f"⚡ Custom Threshold: {graham_thresh:.1f}")

cache_dir = os.path.join(current_dir, "data_cache")
os.makedirs(cache_dir, exist_ok=True)


# -----------------------------------------------------------------------------
# Main Dashboard Header
# -----------------------------------------------------------------------------
st.title("🏛️ Multi-Investor Legend Panel")
st.markdown(f"**Comparative Security Analysis: Warren Buffett · Benjamin Graham · Michael Burry**")

st.markdown(
    """
    <div class="attribution-banner">
        <strong>FIN 439 Academic Notice:</strong> Educational analysis prepared by Elliot for FIN 439 at Purdue University. 
        <strong>Python calculates every financial metric and ratio directly from official SEC EDGAR 10-K filings.</strong> 
        AI agents interpret those audited figures through the respective investment philosophies. This application is an academic demonstration and does not constitute investment advice.
    </div>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# SEC EDGAR Data Ingestion & Engine Processing
# -----------------------------------------------------------------------------
with st.spinner(f"Retrieving and processing SEC EDGAR 10-K facts for {ticker_input}..."):
    try:
        cik, company_title = legend_sec.lookup_cik(ticker_input, email=email_input, cache_dir=cache_dir)
        facts = legend_sec.fetch_company_facts(cik, email=email_input, cache_dir=cache_dir)
        tags_used, rows = legend_sec.extract_legend_metrics(facts)
        
        # Evaluate checks
        buffett_checks = legend_sec.evaluate_buffett_checks(rows)
        graham_checks = legend_sec.evaluate_graham_checks(rows, current_ratio_threshold=graham_thresh)
        burry_checks = legend_sec.evaluate_burry_checks(rows)
        
        # Generate memos
        buffett_memo = legend_sec.generate_buffett_memo(ticker_input, company_title, rows, tags_used, buffett_checks)
        graham_memo = legend_sec.generate_graham_memo(
            ticker_input,
            company_title,
            rows,
            tags_used,
            graham_checks,
            threshold_probe_note=(
                "I kept Graham's original 2.0 threshold because lowering it to 1.0 makes Costco pass but weakens the liquidity standard, showing how a screening decision depends on the threshold chosen."
                if ticker_input == "COST" and graham_thresh == 2.0 else None
            )
        )
        burry_memo = legend_sec.generate_burry_memo(ticker_input, company_title, rows, tags_used, burry_checks)
        
    except Exception as e:
        st.error(f"Error processing SEC EDGAR data for '{ticker_input}': {e}")
        st.stop()


# -----------------------------------------------------------------------------
# Section 1: Executive Verdict Badges
# -----------------------------------------------------------------------------
v1, v2, v3 = st.columns(3)

def render_verdict_card(col, investor_name, verdict, passed, total, philosophy):
    color_map = {
        "OWN THE BUSINESS": ("#34D399", "rgba(16, 185, 129, 0.15)", "#059669"),
        "DEFENSIVE BUY": ("#34D399", "rgba(16, 185, 129, 0.15)", "#059669"),
        "VALUE LONG": ("#34D399", "rgba(16, 185, 129, 0.15)", "#059669"),
        "ENTERPRISING / WATCH": ("#FBBF24", "rgba(245, 158, 11, 0.15)", "#D97706"),
        "HIGH RISK / SKEPTICAL": ("#FBBF24", "rgba(245, 158, 11, 0.15)", "#D97706"),
        "REJECT / DEFICIENT": ("#F87171", "rgba(239, 68, 68, 0.15)", "#DC2626"),
        "SHORT CANDIDATE / AVOID": ("#F87171", "rgba(239, 68, 68, 0.15)", "#DC2626"),
    }
    text_color, bg_color, border_color = color_map.get(verdict, ("#94A3B8", "rgba(148, 163, 184, 0.15)", "#475569"))
    
    with col:
        st.markdown(f"""
        <div class="metric-card" style="border-top: 3px solid {text_color};">
            <div style="font-size: 0.85rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">{investor_name}</div>
            <div style="font-size: 1.35rem; font-weight: 700; color: #F8FAFC; margin: 4px 0;">{verdict}</div>
            <div style="margin-top: 6px;">
                <span style="background-color: {bg_color}; color: {text_color}; border: 1px solid {border_color}; padding: 2px 8px; border-radius: 9999px; font-size: 0.75rem; font-weight: 700;">
                    {passed}/{total} Checks Passed
                </span>
            </div>
            <div style="font-size: 0.8rem; color: #64748B; margin-top: 10px;">{philosophy}</div>
        </div>
        """, unsafe_allow_html=True)

render_verdict_card(v1, "Warren Buffett", buffett_checks["verdict"], buffett_checks["passed_count"], 3, "Franchise moat, high ROE, positive & growing owner cash flow.")
render_verdict_card(v2, "Benjamin Graham", graham_checks["verdict"], graham_checks["passed_count"], 3, f"Defensive margin of safety: Current Ratio >= {graham_thresh:.1f}, multi-year positive earnings.")
render_verdict_card(v3, "Michael Burry", burry_checks["verdict"], burry_checks["passed_count"], 2, "Forensic cash quality (OCF >= Net Income), debt leverage limit (Liab <= 2x Eq).")

st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Section 2: Panel Comparison Table (Investor x Check)
# -----------------------------------------------------------------------------
st.markdown("### 📋 Multi-Investor 8-Check Comparison Panel")

panel_data = [
    {
        "Investor": "Warren Buffett",
        "Check": "1. ROE >= 15% every year",
        "Criterion": "ROE >= 15.0% in all 5 years",
        "Details": buffett_checks["check1"]["details"],
        "Status": buffett_checks["check1"]["status"],
    },
    {
        "Investor": "Warren Buffett",
        "Check": "2. Owner earnings positive every year",
        "Criterion": "OCF - CapEx > 0 in all 5 years",
        "Details": buffett_checks["check2"]["details"],
        "Status": buffett_checks["check2"]["status"],
    },
    {
        "Investor": "Warren Buffett",
        "Check": "3. Owner earnings grew (FY5 > FY1)",
        "Criterion": "Owner Earnings FY5 > FY1",
        "Details": buffett_checks["check3"]["details"],
        "Status": buffett_checks["check3"]["status"],
    },
    {
        "Investor": "Benjamin Graham",
        "Check": f"1. Current ratio >= {graham_thresh:.1f} (latest year)",
        "Criterion": f"Current Assets / Current Liab >= {graham_thresh:.1f}",
        "Details": graham_checks["check1"]["details"],
        "Status": graham_checks["check1"]["status"],
    },
    {
        "Investor": "Benjamin Graham",
        "Check": "2. Net income positive every year",
        "Criterion": "GAAP Net Income > 0 in all 5 years",
        "Details": graham_checks["check2"]["details"],
        "Status": graham_checks["check2"]["status"],
    },
    {
        "Investor": "Benjamin Graham",
        "Check": "3. Net income grew (FY5 > FY1)",
        "Criterion": "Net Income FY5 > FY1",
        "Details": graham_checks["check3"]["details"],
        "Status": graham_checks["check3"]["status"],
    },
    {
        "Investor": "Michael Burry",
        "Check": "1. Operating cash flow >= Net income every year",
        "Criterion": "OCF >= Net Income in all 5 years",
        "Details": burry_checks["check1"]["details"],
        "Status": burry_checks["check1"]["status"],
    },
    {
        "Investor": "Michael Burry",
        "Check": "2. Liabilities <= 2 × Equity (latest year)",
        "Criterion": "Total Liabilities / Equity <= 2.0",
        "Details": burry_checks["check2"]["details"],
        "Status": burry_checks["check2"]["status"],
    },
]

# Render interactive HTML table with badges
table_html = """
<table style="width:100%; border-collapse: collapse; background: #111827; border-radius: 8px; overflow: hidden; border: 1px solid #1E293B; font-size: 0.9rem;">
    <thead>
        <tr style="background: #1E293B; text-align: left; color: #94A3B8; font-size: 0.82rem; text-transform: uppercase;">
            <th style="padding: 12px 16px;">Investor</th>
            <th style="padding: 12px 16px;">Check</th>
            <th style="padding: 12px 16px;">Mandate Requirement</th>
            <th style="padding: 12px 16px;">Audited Filing Evidence</th>
            <th style="padding: 12px 16px; text-align: center;">Result</th>
        </tr>
    </thead>
    <tbody>
"""

for row in panel_data:
    st_class = "badge-pass" if row["Status"] == "PASS" else ("badge-fail" if row["Status"] == "FAIL" else "badge-notknown")
    table_html += f"""
        <tr style="border-bottom: 1px solid #1E293B;">
            <td style="padding: 12px 16px; font-weight: 600; color: #F8FAFC;">{row["Investor"]}</td>
            <td style="padding: 12px 16px; color: #CBD5E1;">{row["Check"]}</td>
            <td style="padding: 12px 16px; color: #94A3B8;">{row["Criterion"]}</td>
            <td style="padding: 12px 16px; color: #E2E8F0; font-size: 0.85rem;">{row["Details"]}</td>
            <td style="padding: 12px 16px; text-align: center;"><span class="{st_class}">{row["Status"]}</span></td>
        </tr>
    """

table_html += "</tbody></table>"
st.markdown(table_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Section 3: Visual Analytics (3 Plots)
# -----------------------------------------------------------------------------
st.markdown("### 📊 Interactive Visual Analytics")

dates = [r["fiscal_year_end"] for r in rows]

c1, c2, c3 = st.columns(3)

# Chart 1: Owner Earnings vs Net Income vs Operating Cash Flow
with c1:
    fig1 = go.Figure()
    
    ni_vals = [r["net_income"] / 1e6 if isinstance(r.get("net_income"), (int, float)) else None for r in rows]
    ocf_vals = [r["operating_cash_flow"] / 1e6 if isinstance(r.get("operating_cash_flow"), (int, float)) else None for r in rows]
    oe_vals = [r["owner_earnings"] / 1e6 if isinstance(r.get("owner_earnings"), (int, float)) else None for r in rows]
    
    fig1.add_trace(go.Bar(name="Net Income", x=dates, y=ni_vals, marker_color="#38BDF8"))
    fig1.add_trace(go.Bar(name="Operating CF", x=dates, y=ocf_vals, marker_color="#10B981"))
    fig1.add_trace(go.Bar(name="Owner Earnings", x=dates, y=oe_vals, marker_color="#A855F7"))
    
    fig1.update_layout(
        title="Buffett/Burry: Earnings & Cash Flow ($M)",
        barmode="group",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#94A3B8"),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=320,
    )
    fig1.update_yaxes(gridcolor="#1E293B")
    fig1.update_xaxes(gridcolor="#1E293B")
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Current Ratio over time with Graham Threshold
with c2:
    fig2 = go.Figure()
    cr_vals = [r.get("current_ratio") if isinstance(r.get("current_ratio"), (int, float)) else None for r in rows]
    
    fig2.add_trace(go.Scatter(
        x=dates, y=cr_vals,
        mode="lines+markers",
        name="Current Ratio",
        line=dict(color="#38BDF8", width=3),
        marker=dict(size=8, color="#38BDF8"),
    ))
    
    # Threshold line
    fig2.add_hline(
        y=graham_thresh,
        line_dash="dash",
        line_color="#F59E0B",
        annotation_text=f"Graham Hurdle ({graham_thresh:.1f}x)",
        annotation_position="bottom right",
    )
    
    fig2.update_layout(
        title="Graham: Current Ratio vs Threshold",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#94A3B8"),
        margin=dict(l=20, r=20, t=40, b=20),
        height=320,
    )
    fig2.update_yaxes(gridcolor="#1E293B", rangemode="tozero")
    fig2.update_xaxes(gridcolor="#1E293B")
    st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Liabilities / Equity over time with Burry 2.0 Hurdle
with c3:
    fig3 = go.Figure()
    le_vals = [r.get("liabilities_equity") if isinstance(r.get("liabilities_equity"), (int, float)) else None for r in rows]
    
    fig3.add_trace(go.Scatter(
        x=dates, y=le_vals,
        mode="lines+markers",
        name="Liabilities / Equity",
        line=dict(color="#F87171", width=3),
        marker=dict(size=8, color="#F87171"),
    ))
    
    # Burry 2.0 ceiling
    fig3.add_hline(
        y=2.0,
        line_dash="dash",
        line_color="#EF4444",
        annotation_text="Burry Ceiling (2.0x)",
        annotation_position="top right",
    )
    
    fig3.update_layout(
        title="Burry: Total Liabilities / Equity vs Ceiling",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#94A3B8"),
        margin=dict(l=20, r=20, t=40, b=20),
        height=320,
    )
    fig3.update_yaxes(gridcolor="#1E293B", rangemode="tozero")
    fig3.update_xaxes(gridcolor="#1E293B")
    st.plotly_chart(fig3, use_container_width=True)


# -----------------------------------------------------------------------------
# Section 4: Audited 10-K Historical Financial Foundation Table
# -----------------------------------------------------------------------------
st.markdown("### 📊 Audited SEC EDGAR 10-K Financial Foundation (USD Millions)")

display_df_data = []
for r in rows:
    display_df_data.append({
        "Fiscal Year End": r["fiscal_year_end"],
        "Revenue ($M)": f"{round(r['revenue']/1e6):,}" if isinstance(r.get("revenue"), (int, float)) else "not found",
        "Net Income ($M)": f"{round(r['net_income']/1e6):,}" if isinstance(r.get("net_income"), (int, float)) else "not found",
        "Operating CF ($M)": f"{round(r['operating_cash_flow']/1e6):,}" if isinstance(r.get("operating_cash_flow"), (int, float)) else "not found",
        "CapEx ($M)": f"{round(r['capex']/1e6):,}" if isinstance(r.get("capex"), (int, float)) else "not found",
        "Equity ($M)": f"{round(r['equity']/1e6):,}" if isinstance(r.get("equity"), (int, float)) else "not found",
        "Current Ratio": f"{r['current_ratio']:.2f}" if isinstance(r.get("current_ratio"), (int, float)) else "not found",
        "Liabilities / Equity": f"{r['liabilities_equity']:.2f}" if isinstance(r.get("liabilities_equity"), (int, float)) else "not found",
        "ROE (%)": f"{r['roe']*100:.1f}%" if isinstance(r.get("roe"), (int, float)) else "not known",
        "Owner Earnings ($M)": f"{round(r['owner_earnings']/1e6):,}" if isinstance(r.get("owner_earnings"), (int, float)) else "not found",
    })

df_display = pd.DataFrame(display_df_data)
st.dataframe(df_display, use_container_width=True, hide_index=True)

with st.expander("🔍 Inspect Audited XBRL Tags Used from SEC EDGAR Taxonomy"):
    st.json(tags_used)


# -----------------------------------------------------------------------------
# Section 5: Side-by-Side Legend Investor Memos
# -----------------------------------------------------------------------------
st.markdown("### 📝 Side-by-Side Investment Memos")
st.markdown("Three distinct investment frameworks evaluated on the identical audited SEC EDGAR financial disclosures.")

col_b, col_g, col_m = st.columns(3)

with col_b:
    st.markdown("#### 🎯 Warren Buffett Memo")
    with st.container(height=650):
        st.markdown(buffett_memo)

with col_g:
    st.markdown("#### 🛡️ Benjamin Graham Memo")
    with st.container(height=650):
        st.markdown(graham_memo)

with col_m:
    st.markdown("#### 🔍 Michael Burry Memo")
    with st.container(height=650):
        st.markdown(burry_memo)


# -----------------------------------------------------------------------------
# Section 6: Active Fabricated-Number Audit across All Three Memos
# -----------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🛡️ Real-Time Unsupported-Number Audit across All Memos")

b_unsupported = legend_sec.detect_unsupported_numbers(buffett_memo, rows)
g_unsupported = legend_sec.detect_unsupported_numbers(graham_memo, rows)
m_unsupported = legend_sec.detect_unsupported_numbers(burry_memo, rows)
total_unsupported = b_unsupported + g_unsupported + m_unsupported

if len(total_unsupported) == 0:
    st.success("✅ **Zero Unsupported Numbers Detected across all 3 Investor Memos.** Every single financial metric, ratio, dollar amount, and percentage in all three memos originates strictly from audited numbers computed by Python from SEC EDGAR 10-K filings.")
else:
    st.error(f"⚠️ **FLAGGED:** {len(total_unsupported)} unsupported or hallucinated number(s) detected across memo drafts:")
    for item in total_unsupported:
        st.markdown(f"- **Line {item['line']}:** `{item['token']}` in context: *\"{item['context']}\"*")


# -----------------------------------------------------------------------------
# Section 7: Graham Threshold Probe Summary
# -----------------------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🔬 Graham Threshold Probe & Design Choice Synthesis")

# Dynamically calculate outcomes at 2.0 and 1.0 for the currently loaded company
g_standard = legend_sec.evaluate_graham_checks(rows, current_ratio_threshold=2.0)
g_probed = legend_sec.evaluate_graham_checks(rows, current_ratio_threshold=1.0)

latest_cr = rows[-1].get("current_ratio")
latest_cr_str = f"{latest_cr:.2f}" if isinstance(latest_cr, (int, float)) else str(latest_cr)

probe_note_display = (
    '"I kept Graham\'s original 2.0 threshold because lowering it to 1.0 makes Costco pass but weakens the liquidity standard, showing how a screening decision depends on the threshold chosen."'
    if ticker_input == "COST"
    else f"Screening threshold probe for {ticker_input}: At 2.0x, Check 1 is {g_standard['check1']['status']}; at 1.0x, Check 1 is {g_probed['check1']['status']}. Active slider threshold: {graham_thresh:.1f}x (Check 1: {graham_checks['check1']['status']})."
)

st.markdown(
    f"""
    <div class="metric-card">
        <h4 style="color: #F8FAFC; margin-bottom: 8px;">Thresholds as Analytical Design Choices: {company_title} ({ticker_input})</h4>
        <p style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.6;">
            In quantitative security screening, financial thresholds represent deliberate design choices rather than immutable laws. 
            Benjamin Graham formulated his 2.0 current ratio rule in 1934 for asset-heavy industrial, rail, and manufacturing firms requiring substantial inventory and trade receivable cushions.
        </p>
        <p style="color: #CBD5E1; font-size: 0.9rem; line-height: 1.6;">
            <strong>Empirical Threshold Comparison for {ticker_input}:</strong><br>
            • <strong>Standard 2.0 Threshold:</strong> Latest current ratio of <strong>{latest_cr_str}</strong> &rarr; <strong>{g_standard['check1']['status']}</strong> (Overall: {g_standard['passed_count']}/3 passed, Verdict: <em>{g_standard['verdict']}</em>).<br>
            • <strong>Probed 1.0 Threshold:</strong> Latest current ratio of <strong>{latest_cr_str}</strong> &rarr; <strong>{g_probed['check1']['status']}</strong> (Overall: {g_probed['passed_count']}/3 passed, Verdict: <em>{g_probed['verdict']}</em>).<br>
            • <strong>Active Slider Setting ({graham_thresh:.1f}x):</strong> Check 1 is <strong>{graham_checks['check1']['status']}</strong> (Overall: {graham_checks['passed_count']}/3 passed, Verdict: <em>{graham_checks['verdict']}</em>).
        </p>
        <p style="color: #38BDF8; font-size: 0.9rem; font-weight: 600; margin-top: 12px;">
            Recorded Design Choice: {probe_note_display}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
