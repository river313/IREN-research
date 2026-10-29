"""
FIN 43900 — Lab 17: Point-in-Time Audit Streamlit Application
Student: Elliot
Institution: Purdue University

Brand: VINTAGE — Point-in-Time Intelligence
Description:
A modern investment research dashboard providing point-in-time data provenance
audits for macroeconomic and interest rate time series using live public FRED and
ALFRED downloads from the Federal Reserve Bank of St. Louis.
"""

import io
import sys
from datetime import date, datetime
from typing import Optional, Tuple
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Attempt to import curl_cffi for robust TLS impersonation; fall back to requests
try:
    from curl_cffi import requests as cffi_requests
    HAS_CURL_CFFI = True
except ImportError:
    import requests as std_requests
    HAS_CURL_CFFI = False


# ============================================================================
# DATA DOWNLOAD & CACHING FUNCTIONS (PRESERVED UNCHANGED)
# ============================================================================

def _fetch_url_text(url: str, timeout: int = 30) -> str:
    """Fetch text content from a URL using curl_cffi (Chrome impersonation) or requests."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }
    if HAS_CURL_CFFI:
        resp = cffi_requests.get(url, impersonate="chrome", timeout=timeout)
    else:
        resp = std_requests.get(url, headers=headers, timeout=timeout)

    if resp.status_code != 200:
        raise ValueError(f"HTTP {resp.status_code}: Failed to download from {url}")

    text = resp.text
    if text.strip().startswith("<!DOCTYPE") or text.strip().startswith("<html"):
        raise ValueError(f"Invalid series or error page returned from {url}")

    return text


def _parse_fred_csv(csv_text: str, series_id: str) -> pd.DataFrame:
    """Parse raw FRED/ALFRED CSV text, handling '.' missing values and dates."""
    df = pd.read_csv(io.StringIO(csv_text))
    if df.empty or len(df.columns) < 2:
        raise ValueError(f"Malformed or empty dataset returned for series '{series_id}'")

    date_col = df.columns[0]
    val_col = df.columns[1]

    # Treat '.' as missing data per specifications
    df = df[df[val_col] != "."].copy()
    if df.empty:
        raise ValueError(f"No valid non-missing observations found for series '{series_id}'")

    df["observation_date"] = pd.to_datetime(df[date_col])
    df["value"] = pd.to_numeric(df[val_col])
    df = df.sort_values(by="observation_date").reset_index(drop=True)
    return df[["observation_date", "value"]]


@st.cache_data(ttl=3600, show_spinner=False)
def download_fred_current(series_id: str) -> pd.DataFrame:
    """Download current time series data from FRED."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    csv_text = _fetch_url_text(url)
    return _parse_fred_csv(csv_text, series_id)


@st.cache_data(ttl=3600, show_spinner=False)
def download_alfred_vintage(series_id: str, vintage_date: str) -> pd.DataFrame:
    """Download historical vintage data from ALFRED as known on vintage_date."""
    url = f"https://alfred.stlouisfed.org/graph/alfredgraph.csv?id={series_id}&vintage_date={vintage_date}"
    csv_text = _fetch_url_text(url)
    return _parse_fred_csv(csv_text, series_id)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def is_monthly_series(df: pd.DataFrame, series_id: str) -> bool:
    """Detect whether a series is published at monthly frequency."""
    monthly_known = {"BAA", "FEDFUNDS", "PAYEMS", "CPIAUCSL", "UNRATE", "INDPRO"}
    if series_id.upper() in monthly_known:
        return True
    if len(df) > 1:
        day_is_first = (df["observation_date"].dt.day == 1).all()
        median_gap = df["observation_date"].diff().dt.days.median()
        if day_is_first and median_gap >= 25:
            return True
    return False


def format_observation_date(dt: pd.Timestamp, is_monthly: bool) -> str:
    """Format observation date according to frequency conventions."""
    if is_monthly:
        return dt.strftime("%B %Y")
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"


def format_numeric_value(val: float) -> str:
    """Format numeric values cleanly (comma-separated integers or 2 decimal places)."""
    if pd.isna(val):
        return "N/A"
    if abs(val) >= 1000:
        return f"{val:,.0f}" if float(val).is_integer() else f"{val:,.2f}"
    return f"{val:.2f}"


# ============================================================================
# BRAND PALETTE & SERIES COLOR SYSTEM
# ============================================================================

# User specifications:
# Background: #0B1220, Sidebar: #111827, Cards: #1E293B, Borders: #334155
# BAA: Cyan (#38BDF8), FEDFUNDS: Indigo (#818CF8), DGS10: Emerald (#34D399), MORTGAGE30US: Amber (#FBBF24)
SERIES_PALETTE = {
    "BAA": {"color": "#38BDF8", "name": "Moody's Baa Corporate Bond Yield", "freq": "Monthly"},
    "FEDFUNDS": {"color": "#818CF8", "name": "Effective Federal Funds Rate", "freq": "Monthly"},
    "DGS10": {"color": "#34D399", "name": "10-Year Treasury Constant Maturity", "freq": "Daily"},
    "MORTGAGE30US": {"color": "#FBBF24", "name": "30-Year Fixed Mortgage Rate", "freq": "Weekly"},
    "PAYEMS": {"color": "#FB7185", "name": "All Employees: Total Nonfarm Payrolls", "freq": "Monthly"},
}

DEFAULT_COLOR = "#38BDF8"


# ============================================================================
# STREAMLIT UI SETUP & STYLESHEET
# ============================================================================

st.set_page_config(
    page_title="VINTAGE — Point-in-Time Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Institutional CSS
st.markdown(
    """
    <style>
    /* Global Canvas */
    .stApp {
        background-color: #0B1220;
        color: #F8FAFC;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1E293B !important;
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #CBD5E1 !important;
        font-size: 0.88rem !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #F8FAFC !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }

    /* Custom Dividers */
    hr {
        border: none !important;
        height: 1px !important;
        background-color: #1E293B !important;
        margin: 22px 0 !important;
    }

    /* Top KPI Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin: 16px 0 24px 0;
    }

    .kpi-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 14px 16px;
        position: relative;
        overflow: hidden;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }

    .kpi-card:hover {
        border-color: #475569;
        transform: translateY(-1px);
    }

    .kpi-stripe {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
    }

    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }

    .kpi-symbol {
        font-size: 0.82rem;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: 0.04em;
    }

    .kpi-badge {
        font-size: 0.68rem;
        font-weight: 600;
        padding: 2px 6px;
        border-radius: 4px;
        background-color: rgba(51, 65, 85, 0.4);
        color: #94A3B8;
        text-transform: uppercase;
    }

    .kpi-value {
        font-size: 1.55rem;
        font-weight: 700;
        color: #F8FAFC;
        line-height: 1.2;
        margin-bottom: 4px;
    }

    .kpi-name {
        font-size: 0.72rem;
        color: #94A3B8;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 6px;
    }

    .kpi-asof {
        font-size: 0.70rem;
        color: #64748B;
        border-top: 1px solid rgba(51, 65, 85, 0.5);
        padding-top: 6px;
        margin-top: 4px;
    }

    /* Comparison Table Styling */
    .vintage-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        background-color: #0F172A;
        border: 1px solid #334155;
        border-radius: 8px;
        overflow: hidden;
        margin: 14px 0 24px 0;
    }

    .vintage-table th {
        background-color: #1E293B;
        color: #38BDF8;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 12px 14px;
        border-bottom: 1px solid #334155;
        text-align: left;
    }

    .vintage-table td {
        padding: 11px 14px;
        color: #CBD5E1;
        font-size: 0.84rem;
        border-bottom: 1px solid #1E293B;
    }

    .vintage-table tr:hover td {
        background-color: #1E293B;
    }

    .vintage-table tr:last-child td {
        border-bottom: none;
    }

    .vintage-link {
        color: #38BDF8 !important;
        font-weight: 600;
        text-decoration: none;
    }

    .vintage-link:hover {
        text-decoration: underline;
    }

    .pill-added {
        background-color: rgba(56, 189, 248, 0.12);
        color: #38BDF8;
        font-weight: 600;
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 12px;
        border: 1px solid rgba(56, 189, 248, 0.25);
    }

    .pill-clean {
        background-color: rgba(52, 211, 153, 0.12);
        color: #34D399;
        font-weight: 600;
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 12px;
        border: 1px solid rgba(52, 211, 153, 0.25);
    }

    .pill-revised {
        background-color: rgba(251, 113, 133, 0.12);
        color: #FB7185;
        font-weight: 600;
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 12px;
        border: 1px solid rgba(251, 113, 133, 0.25);
    }

    /* Chart Section Card */
    .chart-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 18px 20px 14px 20px;
        margin-bottom: 22px;
    }

    .chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }

    .chart-title-left {
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .chart-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
    }

    .chart-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #F8FAFC;
    }

    .chart-subtitle {
        font-size: 0.80rem;
        color: #94A3B8;
        margin-left: 6px;
    }

    .chart-meta {
        font-size: 0.75rem;
        font-weight: 600;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================================
# HEADER WITH BRANDING & REQUIRED ATTRIBUTION
# ============================================================================

st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: space-between; padding-bottom: 8px; border-bottom: 1px solid #1E293B; margin-bottom: 10px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <span style="background: linear-gradient(135deg, #38BDF8, #818CF8); color: #0B1220; font-weight: 800; font-size: 0.85rem; padding: 4px 10px; border-radius: 6px; letter-spacing: 0.08em;">
                VINTAGE
            </span>
            <div>
                <h1 style="margin: 0; font-size: 1.75rem; font-weight: 700; color: #F8FAFC; letter-spacing: -0.03em;">
                    Point-in-Time Intelligence
                </h1>
            </div>
        </div>
        <div style="text-align: right;">
            <span style="background-color: #1E293B; border: 1px solid #334155; color: #38BDF8; font-size: 0.75rem; font-weight: 600; padding: 5px 12px; border-radius: 20px;">
                FIN 439 • LIVE FED DATA
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Mandatory Professor Attribution (Directly Under Title)
st.markdown(
    "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today; "
    "built with AI help, a learning demonstration, not investment advice."
)
st.caption(f"Audit execution timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (actual download time, distinct from latest observation dates).")
st.write("---")


# ============================================================================
# SIDEBAR CONFIGURATION (PRESERVED EXACT STRUCTURE)
# ============================================================================

DEFAULT_SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Effective federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year fixed mortgage rate",
}

st.sidebar.markdown(
    """
    <div style="margin-bottom: 16px;">
        <span style="color: #38BDF8; font-weight: 700; font-size: 0.82rem; letter-spacing: 0.08em; text-transform: uppercase;">
            Audit Configuration
        </span>
        <p style="color: #64748B; font-size: 0.75rem; margin: 2px 0 0 0;">Point-in-Time Temporal Gate</p>
    </div>
    """,
    unsafe_allow_html=True,
)

selected_default_keys = st.sidebar.multiselect(
    "Select Series",
    options=list(DEFAULT_SERIES.keys()),
    default=list(DEFAULT_SERIES.keys()),
    format_func=lambda s: f"{s} — {DEFAULT_SERIES.get(s, '')}",
)

additional_series_input = st.sidebar.text_input(
    "Additional FRED Series ID",
    value="",
    placeholder="e.g. PAYEMS, UNRATE",
    help="Enter any valid FRED series ID to include in the audit.",
).strip()

start_date_input = st.sidebar.date_input(
    "Start Date",
    value=date(2020, 1, 1),
    help="Filter start date for current time series charts.",
)

as_of_date_input = st.sidebar.date_input(
    "As known on",
    value=date.today(),
    help="Historical date cutoff: shows values as knowable on this vintage date.",
)

vintage_date_str = as_of_date_input.strftime("%Y-%m-%d")
start_datetime = pd.to_datetime(start_date_input)
as_of_datetime = pd.to_datetime(as_of_date_input)

# Combine active series list preserving order
active_series = list(selected_default_keys)
if additional_series_input:
    for extra in [s.strip().upper() for s in additional_series_input.replace(",", " ").split()]:
        if extra and extra not in active_series:
            active_series.append(extra)

if not active_series:
    st.warning("Please select or enter at least one FRED series ID from the sidebar.")
    st.stop()


# ============================================================================
# DATA RETRIEVAL & AUDIT PROCESSING
# ============================================================================

audit_results = []
valid_series_data = {}

for series_id in active_series:
    try:
        df_curr = download_fred_current(series_id)
        df_hist = download_alfred_vintage(series_id, vintage_date_str)
        
        valid_series_data[series_id] = {
            "current": df_curr,
            "vintage": df_hist,
        }
        
        is_monthly = is_monthly_series(df_curr, series_id)
        
        # Latest observation in historical vintage
        last_hist_row = df_hist.iloc[-1]
        last_hist_date = last_hist_row["observation_date"]
        last_hist_val = last_hist_row["value"]
        
        # Latest observation in current data
        last_curr_row = df_curr.iloc[-1]
        last_curr_date = last_curr_row["observation_date"]
        last_curr_val = last_curr_row["value"]
        
        # Matching dates revision analysis
        merged = pd.merge(
            df_hist,
            df_curr,
            on="observation_date",
            suffixes=("_hist", "_curr"),
        )
        revised_mask = (merged["value_hist"] - merged["value_curr"]).abs() > 1e-4
        revised_count = int(revised_mask.sum())
        
        # Observations added after historical cutoff
        added_after_count = int((df_curr["observation_date"] > last_hist_date).sum())
        
        audit_results.append({
            "Series_ID": series_id,
            "Series_Link": f"[{series_id}](https://fred.stlouisfed.org/series/{series_id})",
            "Last Date Known (As Of)": format_observation_date(last_hist_date, is_monthly),
            "Value Known (As Of)": format_numeric_value(last_hist_val),
            "Latest Date (Today)": format_observation_date(last_curr_date, is_monthly),
            "Latest Value (Today)": format_numeric_value(last_curr_val),
            "Observations Added After": added_after_count,
            "Observations Revised Since": revised_count,
            "_raw_hist_val": last_hist_val,
            "_raw_curr_val": last_curr_val,
            "_is_monthly": is_monthly,
            "_hist_date": last_hist_date,
            "_curr_date": last_curr_date,
        })
        
    except Exception as exc:
        st.error(f"Error loading series **{series_id}**: {exc}")


# ============================================================================
# TOP KPI CARDS (LATEST RETRIEVED VALUES OF 4 DEFAULT SERIES)
# ============================================================================

# Pre-fetch default series for top cards if available
kpi_items = ["BAA", "FEDFUNDS", "DGS10", "MORTGAGE30US"]
kpi_data = {}

for k_id in kpi_items:
    # Check if already downloaded
    if k_id in valid_series_data:
        rec = next((r for r in audit_results if r["Series_ID"] == k_id), None)
        if rec:
            kpi_data[k_id] = rec
    else:
        # Fetch current and historical for card display
        try:
            k_curr = download_fred_current(k_id)
            k_hist = download_alfred_vintage(k_id, vintage_date_str)
            k_is_m = is_monthly_series(k_curr, k_id)
            kpi_data[k_id] = {
                "Series_ID": k_id,
                "Last Date Known (As Of)": format_observation_date(k_hist.iloc[-1]["observation_date"], k_is_m),
                "Value Known (As Of)": format_numeric_value(k_hist.iloc[-1]["value"]),
                "Latest Date (Today)": format_observation_date(k_curr.iloc[-1]["observation_date"], k_is_m),
                "Latest Value (Today)": format_numeric_value(k_curr.iloc[-1]["value"]),
            }
        except Exception:
            pass

if kpi_data:
    st.markdown('<div class="kpi-container">', unsafe_allow_html=True)
    cards_html = []
    for k_id in kpi_items:
        if k_id in kpi_data:
            c_info = SERIES_PALETTE.get(k_id, {})
            c_color = c_info.get("color", DEFAULT_COLOR)
            c_name = c_info.get("name", k_id)
            c_freq = c_info.get("freq", "")
            rec = kpi_data[k_id]
            curr_val = rec["Latest Value (Today)"]
            curr_date = rec["Latest Date (Today)"]
            hist_val = rec["Value Known (As Of)"]
            hist_date = rec["Last Date Known (As Of)"]
            
            card_html = f"""
            <div class="kpi-card">
                <div class="kpi-stripe" style="background-color: {c_color};"></div>
                <div class="kpi-header">
                    <span class="kpi-symbol" style="color: {c_color};">{k_id}</span>
                    <span class="kpi-badge">{c_freq}</span>
                </div>
                <div class="kpi-value">{curr_val}%</div>
                <div class="kpi-name" title="{c_name}">{c_name}</div>
                <div class="kpi-asof">
                    As-Of {as_of_date_input.strftime('%b %d, %Y')}: <strong style="color: #E2E8F0;">{hist_val}%</strong> ({hist_date})
                </div>
            </div>
            """
            cards_html.append(card_html)
            
    st.markdown('<div class="kpi-container">' + "".join(cards_html) + '</div>', unsafe_allow_html=True)


# ============================================================================
# COMPARISON TABLE SECTION (ONE CLEAN TABLE WITH REQUIRED COLUMNS)
# ============================================================================

st.markdown("### **Point-in-Time Audit & Revision Summary**")

if audit_results:
    # Custom HTML table matching Bloomberg institutional styling
    table_rows_html = []
    for row in audit_results:
        s_id = row["Series_ID"]
        s_color = SERIES_PALETTE.get(s_id, {}).get("color", DEFAULT_COLOR)
        added_cnt = row["Observations Added After"]
        rev_cnt = row["Observations Revised Since"]
        
        added_badge = f'<span class="pill-added">+{added_cnt}</span>' if added_cnt > 0 else '<span style="color: #64748B;">0</span>'
        rev_badge = f'<span class="pill-revised">{rev_cnt}</span>' if rev_cnt > 0 else '<span class="pill-clean">0 (Clean)</span>'
        
        table_rows_html.append(f"""
        <tr>
            <td>
                <span style="color: {s_color}; font-size: 1.1rem; vertical-align: middle; margin-right: 6px;">●</span>
                <a class="vintage-link" href="https://fred.stlouisfed.org/series/{s_id}" target="_blank">{s_id}</a>
            </td>
            <td><strong style="color: #F8FAFC;">{row['Last Date Known (As Of)']}</strong></td>
            <td style="color: #F8FAFC; font-weight: 600;">{row['Value Known (As Of)']}</td>
            <td>{row['Latest Date (Today)']}</td>
            <td style="color: #F8FAFC; font-weight: 600;">{row['Latest Value (Today)']}</td>
            <td>{added_badge}</td>
            <td>{rev_badge}</td>
        </tr>
        """)
        
    full_table_html = f"""
    <table class="vintage-table">
        <thead>
            <tr>
                <th>Series ID</th>
                <th>Last Date Known</th>
                <th>Value Known</th>
                <th>Latest Date Today</th>
                <th>Latest Value Today</th>
                <th>Observations Added After Cutoff</th>
                <th>Observations Revised Since</th>
            </tr>
        </thead>
        <tbody>
            {"".join(table_rows_html)}
        </tbody>
    </table>
    """
    st.markdown(full_table_html, unsafe_allow_html=True)
else:
    st.warning("No audit records available to display.")

st.write("---")


# ============================================================================
# LINE CHARTS SECTION (ONE INTERACTIVE PLOTLY CHART PER SELECTED SERIES)
# ============================================================================

st.markdown("### **Historical & Current Time Series Analysis**")

if valid_series_data:
    for series_id, sdata in valid_series_data.items():
        s_palette = SERIES_PALETTE.get(series_id, {})
        color = s_palette.get("color", DEFAULT_COLOR)
        desc = DEFAULT_SERIES.get(series_id, s_palette.get("name", "Custom Series"))
        
        df_curr = sdata["current"]
        df_hist = sdata["vintage"]
        is_monthly = is_monthly_series(df_curr, series_id)
        
        last_hist_row = df_hist.iloc[-1]
        last_hist_date_str = format_observation_date(last_hist_row["observation_date"], is_monthly)
        last_hist_val_str = format_numeric_value(last_hist_row["value"])
        
        # Filter chart from selected start date
        chart_df = df_curr[df_curr["observation_date"] >= start_datetime].copy()
        
        # Card container
        st.markdown(
            f"""
            <div class="chart-card">
                <div class="chart-header">
                    <div class="chart-title-left">
                        <span class="chart-dot" style="background-color: {color};"></span>
                        <span class="chart-title">{series_id}</span>
                        <span class="chart-subtitle">— {desc}</span>
                    </div>
                    <span class="chart-meta">FRED • CURRENT VINTAGE</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        if not chart_df.empty:
            # Build interactive Plotly chart with institutional dark styling
            fig = go.Figure()
            
            # Value formatting for tooltip
            y_hover_fmt = ",.0f" if (chart_df["value"].abs().max() > 1000) else ".2f"
            
            fig.add_trace(
                go.Scatter(
                    x=chart_df["observation_date"],
                    y=chart_df["value"],
                    mode="lines",
                    name=series_id,
                    line=dict(color=color, width=2.5),
                    hovertemplate=f"<b>%{{x|%b %d, %Y}}</b><br>Value: <b>%{{y:{y_hover_fmt}}}</b><extra></extra>",
                )
            )
            
            # Visual Historical Cutoff Marker (Vertical Dashed Line)
            if chart_df["observation_date"].min() <= as_of_datetime <= chart_df["observation_date"].max():
                fig.add_vline(
                    x=as_of_datetime,
                    line_width=1.5,
                    line_dash="dash",
                    line_color="#94A3B8",
                    annotation_text=f"As-Of ({as_of_date_input.strftime('%b %d, %Y')})",
                    annotation_position="top left",
                    annotation_font=dict(size=10, color="#CBD5E1"),
                )
            
            fig.update_layout(
                paper_bgcolor="#1E293B",
                plot_bgcolor="#1E293B",
                margin=dict(l=35, r=25, t=15, b=35),
                height=320,
                xaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(51, 65, 85, 0.4)",
                    color="#94A3B8",
                    tickfont=dict(size=10, color="#94A3B8"),
                    zeroline=False,
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(51, 65, 85, 0.4)",
                    color="#94A3B8",
                    tickfont=dict(size=10, color="#94A3B8"),
                    zeroline=False,
                ),
                hoverlabel=dict(
                    bgcolor="#0F172A",
                    font_size=12,
                    font_family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto",
                    bordercolor="#334155",
                ),
                showlegend=False,
            )
            
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info(f"No current observations available after start date {start_date_input}.")
            
        # Required Under-Chart Caption (Preserved Word-for-Word)
        st.caption(
            f"**Last date in the data known on {as_of_date_input.strftime('%B %d, %Y')}:** "
            f"**{last_hist_date_str}** (Value: **{last_hist_val_str}**)"
        )
        st.write("")


# ============================================================================
# FOOTER
# ============================================================================

st.write("---")
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center; color: #64748B; font-size: 0.78rem;">
        <div>
            VINTAGE Analytics • FIN 439 Applied Financial Modeling
        </div>
        <div>
            Launch locally: <code>py -m streamlit run .\\IREN-research\\Lab-17\\asof_app.py</code>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
