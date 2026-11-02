"""
app.py - Warren Buffett SEC Financial Quality Dashboard
FIN 439 - Purdue University
Student: Elliot

Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.
"""

import os
import sys
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Add Lab-18 directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import buffett_sec

# -----------------------------------------------------------------------------
# Streamlit Page Configuration & Modern Financial Research Theme
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Buffett SEC Quality Engine | FIN 439",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Dark Navy / Charcoal Institutional Design
st.markdown("""
<style>
    /* Global background and typography */
    .stApp {
        background-color: #0B0F19;
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Header typography */
    h1, h2, h3, h4 {
        color: #F8FAFC !important;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* Attribution banner */
    .attribution-banner {
        background: linear-gradient(90deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
        border-left: 3px solid #38BDF8;
        padding: 10px 16px;
        border-radius: 4px;
        font-size: 0.88rem;
        color: #94A3B8;
        margin-bottom: 24px;
    }
    
    /* Card containers */
    .metric-card {
        background: #111827;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 18px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
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
    
    /* Detector banner styles */
    .detector-clean {
        background-color: rgba(16, 185, 129, 0.1);
        border: 1px solid #10B981;
        border-radius: 6px;
        padding: 12px 16px;
        color: #A7F3D0;
        font-size: 0.9rem;
    }
    .detector-alert {
        background-color: rgba(239, 68, 68, 0.12);
        border: 1px solid #EF4444;
        border-radius: 6px;
        padding: 12px 16px;
        color: #FECACA;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Sidebar Controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Costco_Wholesale_logo.svg/320px-Costco_Wholesale_logo.svg.png" if False else "https://img.icons8.com/fluency/96/bullish.png", width=64)
    st.title("Buffett SEC Engine")
    st.caption("FIN 439 — Legend Investor as Skill")
    st.markdown("---")

    ticker_input = st.text_input("Equity Ticker", value="COST", help="Enter any publicly traded US stock symbol").strip().upper()
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        if st.button("Costco (COST)", use_container_width=True):
            ticker_input = "COST"
    with col_t2:
        if st.button("JPMorgan (JPM)", use_container_width=True):
            ticker_input = "JPM"

    st.markdown("---")
    sec_email = st.text_input(
        "SEC User-Agent Email",
        value=os.environ.get("SEC_EDGAR_EMAIL", "river313@purdue.edu"),
        help="Required by SEC fair access policy: User-Agent: Elliot <email>"
    )
    st.caption("Contact identity sent to SEC EDGAR API; not stored publicly.")
    
    cache_dir = os.path.join(current_dir, "data_cache")
    force_refresh = st.checkbox("Force SEC API Refresh", value=False, help="Bypass local cache and re-download from SEC")

# -----------------------------------------------------------------------------
# Main Header & Required Attribution
# -----------------------------------------------------------------------------
st.title(f"🏛️ Warren Buffett Quality Audit: {ticker_input}")
st.markdown("""
<div class="attribution-banner">
    <strong>Data from SEC EDGAR; built with AI help, a learning demonstration, not investment advice.</strong><br>
    <em>Python computes every financial number from SEC filings. AI interprets those numbers using Buffett's investment philosophy.</em>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Data Ingestion Engine
# -----------------------------------------------------------------------------
@st.cache_data(ttl=3600, show_spinner=False)
def load_company_data(ticker: str, email: str, refresh: bool):
    try:
        cik, company_title = buffett_sec.lookup_cik(ticker, email=email, cache_dir=cache_dir)
        facts = buffett_sec.fetch_company_facts(cik, email=email, cache_dir=cache_dir)
        tags_used, rows = buffett_sec.extract_buffett_metrics(facts)
        checks = buffett_sec.evaluate_buffett_checks(rows)
        return {
            "success": True,
            "cik": cik,
            "title": company_title,
            "tags_used": tags_used,
            "rows": rows,
            "checks": checks,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

with st.spinner(f"Retrieving and auditing 10-K filings for {ticker_input} from SEC EDGAR..."):
    comp_data = load_company_data(ticker_input, sec_email, force_refresh)

if not comp_data["success"]:
    st.error(f"❌ SEC EDGAR Retrieval Error: {comp_data['error']}")
    st.info("Check internet connectivity, verify ticker symbol, or ensure the SEC EDGAR API is responsive.")
    st.stop()

cik = comp_data["cik"]
title = comp_data["title"]
tags_used = comp_data["tags_used"]
rows = comp_data["rows"]
checks = comp_data["checks"]

# -----------------------------------------------------------------------------
# Top Row: Buffett's Three Fundamental Checks (KPIs)
# -----------------------------------------------------------------------------
st.subheader("1. Buffett's Three Fundamental Quality Checks")

col_c1, col_c2, col_c3 = st.columns(3)

def render_check_badge(status):
    if status == "PASS":
        return '<span class="badge-pass">PASS</span>'
    elif status == "FAIL":
        return '<span class="badge-fail">FAIL</span>'
    else:
        return '<span class="badge-notknown">NOT KNOWN</span>'

with col_c1:
    c1 = checks["check1"]
    st.markdown(f"""
    <div class="metric-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-size:0.82rem; text-transform:uppercase; color:#94A3B8; font-weight:600;">Check 1: ROE >= 15%</span>
            {render_check_badge(c1['status'])}
        </div>
        <div style="font-size:1.15rem; font-weight:700; color:#F8FAFC; margin-bottom:6px;">5-Year ROE Hurdle</div>
        <div style="font-size:0.84rem; color:#94A3B8; line-height:1.4;">{c1['details']}</div>
    </div>
    """, unsafe_allow_html=True)

with col_c2:
    c2 = checks["check2"]
    st.markdown(f"""
    <div class="metric-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-size:0.82rem; text-transform:uppercase; color:#94A3B8; font-weight:600;">Check 2: Owner Earnings > 0</span>
            {render_check_badge(c2['status'])}
        </div>
        <div style="font-size:1.15rem; font-weight:700; color:#F8FAFC; margin-bottom:6px;">Positive Surplus Cash</div>
        <div style="font-size:0.84rem; color:#94A3B8; line-height:1.4;">{c2['details']}</div>
    </div>
    """, unsafe_allow_html=True)

with col_c3:
    c3 = checks["check3"]
    st.markdown(f"""
    <div class="metric-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-size:0.82rem; text-transform:uppercase; color:#94A3B8; font-weight:600;">Check 3: Owner Earnings Growth</span>
            {render_check_badge(c3['status'])}
        </div>
        <div style="font-size:1.15rem; font-weight:700; color:#F8FAFC; margin-bottom:6px;">Compounding Power</div>
        <div style="font-size:0.84rem; color:#94A3B8; line-height:1.4;">{c3['details']}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Five-Year Chart: Owner Earnings vs Net Income
# -----------------------------------------------------------------------------
st.subheader("2. Five-Year Financial Chart: Owner Earnings vs. Net Income")

chart_dates = [r["fiscal_year_end"] for r in rows]
ni_chart = [(r["net_income"] / 1e6) if isinstance(r["net_income"], (int, float)) else None for r in rows]
oe_chart = [(r["owner_earnings"] / 1e6) if isinstance(r["owner_earnings"], (int, float)) else None for r in rows]

has_oe_data = any(v is not None for v in oe_chart)

fig = go.Figure()

# Net Income Bar
fig.add_trace(go.Bar(
    x=chart_dates,
    y=ni_chart,
    name="Net Income (GAAP)",
    marker_color="#3B82F6",
    opacity=0.85,
    hovertemplate="Fiscal Year End: %{x}<br>Net Income: $%{y:,.0f}M<extra></extra>"
))

# Owner Earnings Bar
if has_oe_data:
    fig.add_trace(go.Bar(
        x=chart_dates,
        y=oe_chart,
        name="Owner Earnings (OCF - CapEx)",
        marker_color="#00D2BE",
        opacity=0.95,
        hovertemplate="Fiscal Year End: %{x}<br>Owner Earnings: $%{y:,.0f}M<extra></extra>"
    ))
else:
    st.info("ℹ️ Owner Earnings cannot be charted for this institution because Capital Expenditures are not reported in standard 10-K format.")

fig.update_layout(
    template="plotly_dark",
    barmode="group",
    plot_bgcolor="#0B0F19",
    paper_bgcolor="#0B0F19",
    margin=dict(l=20, r=20, t=30, b=20),
    height=380,
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=12, color="#E2E8F0")
    ),
    xaxis=dict(
        title="Fiscal Year End Date (10-K)",
        gridcolor="#1E293B",
        tickfont=dict(color="#94A3B8", size=11)
    ),
    yaxis=dict(
        title="USD Millions ($M)",
        gridcolor="#1E293B",
        tickformat="$,.0f",
        tickfont=dict(color="#94A3B8", size=11)
    )
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------------------------
# Audited Financial Metrics Table
# -----------------------------------------------------------------------------
st.subheader("3. Audited Financial Metrics Table (SEC EDGAR 10-K)")

table_records = []
for r in rows:
    table_records.append({
        "Fiscal Year End": r["fiscal_year_end"],
        "Revenue ($M)": f"{r['revenue']/1e6:,.0f}" if isinstance(r["revenue"], (int, float)) else "not found",
        "Net Income ($M)": f"{r['net_income']/1e6:,.0f}" if isinstance(r["net_income"], (int, float)) else "not found",
        "Operating Cash Flow ($M)": f"{r['operating_cash_flow']/1e6:,.0f}" if isinstance(r["operating_cash_flow"], (int, float)) else "not found",
        "CapEx ($M)": f"{r['capex']/1e6:,.0f}" if isinstance(r["capex"], (int, float)) else "not found",
        "Equity ($M)": f"{r['equity']/1e6:,.0f}" if isinstance(r["equity"], (int, float)) else "not found",
        "ROE": f"{r['roe']*100:.1f}%" if isinstance(r["roe"], (int, float)) else str(r["roe"]),
        "Owner Earnings ($M)": f"{r['owner_earnings']/1e6:,.0f}" if isinstance(r["owner_earnings"], (int, float)) else str(r["owner_earnings"])
    })

df_metrics = pd.DataFrame(table_records)
st.dataframe(df_metrics, use_container_width=True, hide_index=True)

with st.expander("🔍 View Audited XBRL Source Tags"):
    tags_df = pd.DataFrame([
        {"Financial Metric": k, "Selected XBRL Tag": v}
        for k, v in tags_used.items()
    ])
    st.table(tags_df)

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Part 4 & 5: Investment Memo & Unsupported Number Detector
# -----------------------------------------------------------------------------
st.subheader("4. Buffett Investment Memo & Fabricated Number Detector")

# Default memo selection
default_memo_text = ""
memo_file_path = os.path.join(current_dir, "costco_buffett_memo.md")
if ticker_input == "COST" and os.path.exists(memo_file_path):
    with open(memo_file_path, "r", encoding="utf-8") as f:
        default_memo_text = f.read()
else:
    default_memo_text = buffett_sec.generate_costco_investment_memo(rows, tags_used, checks)

tab_view, tab_editor = st.tabs(["📄 Investment Memo View", "🛡️ Fabricated Number Audit & Editor"])

with tab_view:
    st.markdown(default_memo_text)

with tab_editor:
    st.caption("Edit the memo text below or use the quick buttons to test whether the application catches fabricated or hallucinated financial figures.")
    
    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("🚨 Inject Unsupported Number ('ROE was 40.0%')", use_container_width=True):
            st.session_state["memo_editor_content"] = default_memo_text + "\n\nIn addition, Costco reported ROE was 40.0% according to unverified market commentary.\n"
    with col_btn2:
        if st.button("🔄 Reset to Official Audited Memo", use_container_width=True):
            st.session_state["memo_editor_content"] = default_memo_text

    current_editor_text = st.session_state.get("memo_editor_content", default_memo_text)
    user_edited_memo = st.text_area("Investment Memo Text", value=current_editor_text, height=360)

    # Run Detector
    detected_unsupported = buffett_sec.detect_unsupported_numbers(user_edited_memo, rows)

    st.markdown("### Detector Audit Output:")
    if not detected_unsupported:
        st.markdown("""
        <div class="detector-clean">
            <strong>✅ Zero Hallucinations Detected:</strong> All financial figures, percentages, and dollar amounts in this text exactly match official SEC EDGAR 10-K calculations produced by the Python script.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="detector-alert">
            <strong>⚠️ Unsupported Financial Number Alert!</strong> The detector identified <strong>{len(detected_unsupported)}</strong> figure(s) that were NOT printed or computed by the script:
        </div>
        """, unsafe_allow_html=True)
        flag_records = []
        for flag in detected_unsupported:
            flag_records.append({
                "Line": flag["line"],
                "Unsupported Token": flag["token"],
                "Surrounding Context": flag["context"]
            })
        st.dataframe(pd.DataFrame(flag_records), use_container_width=True, hide_index=True)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(f"FIN 439 Lab 18 | Student: Elliot | CIK: {cik} ({title}) | Data Source: SEC EDGAR API")
