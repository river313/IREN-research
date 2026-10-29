"""
FIN 43900 — Lab 17: Point-in-Time Audit Streamlit Application
Student: Elliot (ONE T)
Institution: Purdue University

Description:
A Streamlit web application providing point-in-time data provenance audits for
macroeconomic and interest rate time series using live public FRED and ALFRED
downloads from the Federal Reserve Bank of St. Louis.
"""

import io
import sys
from datetime import date, datetime
from typing import Optional, Tuple
import pandas as pd
import streamlit as st

# Attempt to import curl_cffi for robust TLS impersonation; fall back to requests
try:
    from curl_cffi import requests as cffi_requests
    HAS_CURL_CFFI = True
except ImportError:
    import requests as std_requests
    HAS_CURL_CFFI = False


# ============================================================================
# DATA DOWNLOAD & CACHING FUNCTIONS
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
# STREAMLIT UI SETUP
# ============================================================================

st.set_page_config(
    page_title="Point-in-Time Audit | FIN 439 Lab 17",
    page_icon="📈",
    layout="wide",
)

# Page Title & Attribution
st.title("Point-in-Time Interest Rate Audit")
st.markdown(
    "Data from FRED and ALFRED, Federal Reserve Bank of St. Louis, downloaded today; "
    "built with AI help, a learning demonstration, not investment advice."
)
st.write("---")

# ============================================================================
# SIDEBAR CONFIGURATION
# ============================================================================

DEFAULT_SERIES = {
    "BAA": "Moody's Baa corporate bond yield",
    "FEDFUNDS": "Effective federal funds rate",
    "DGS10": "10-year Treasury yield",
    "MORTGAGE30US": "30-year fixed mortgage rate",
}

st.sidebar.header("Data & Vintage Controls")

selected_default_keys = st.sidebar.multiselect(
    "Select Series",
    options=list(DEFAULT_SERIES.keys()),
    default=list(DEFAULT_SERIES.keys()),
    format_func=lambda s: f"{s} ({DEFAULT_SERIES.get(s, '')})",
)

additional_series_input = st.sidebar.text_input(
    "Additional FRED Series ID",
    value="",
    placeholder="e.g. PAYEMS",
    help="Enter any valid FRED series ID to include in the audit.",
).strip()

start_date_input = st.sidebar.date_input(
    "Start Date",
    value=date(2020, 1, 1),
    help="Start date for current time series charts.",
)

as_of_date_input = st.sidebar.date_input(
    "As known on",
    value=date.today(),
    help="Historical date cutoff: shows values as knowable on this vintage date.",
)

vintage_date_str = as_of_date_input.strftime("%Y-%m-%d")
start_datetime = pd.to_datetime(start_date_input)

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
        })
        
    except Exception as exc:
        st.error(f"Error loading series **{series_id}**: {exc}")


# ============================================================================
# LINE CHARTS SECTION
# ============================================================================

st.subheader("Historical & Current Time Series")

if valid_series_data:
    for series_id, sdata in valid_series_data.items():
        desc = DEFAULT_SERIES.get(series_id, "Custom Series")
        st.markdown(f"#### **{series_id}** — {desc}")
        
        df_curr = sdata["current"]
        df_hist = sdata["vintage"]
        is_monthly = is_monthly_series(df_curr, series_id)
        
        # Filter chart from selected start date
        chart_df = df_curr[df_curr["observation_date"] >= start_datetime].copy()
        if not chart_df.empty:
            chart_data = chart_df.set_index("observation_date")["value"]
            st.line_chart(chart_data)
        else:
            st.info(f"No current observations available after start date {start_date_input}.")
            
        last_hist_row = df_hist.iloc[-1]
        last_hist_date_str = format_observation_date(last_hist_row["observation_date"], is_monthly)
        last_hist_val_str = format_numeric_value(last_hist_row["value"])
        
        st.caption(
            f"**Last date in the data known on {as_of_date_input.strftime('%B %d, %Y')}:** "
            f"**{last_hist_date_str}** (Value: **{last_hist_val_str}**)"
        )
        st.write("")


# ============================================================================
# COMPARISON TABLE SECTION
# ============================================================================

st.subheader("Point-in-Time Audit & Revision Summary")

if audit_results:
    table_df = pd.DataFrame(audit_results)
    
    # Display clean GitHub-style markdown table with clickable FRED links
    md_lines = [
        "| Series | Last date known | Value known | Latest date today | Latest value today | Observations added after cutoff | Observations revised since |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in audit_results:
        md_lines.append(
            f"| {row['Series_Link']} | {row['Last Date Known (As Of)']} | {row['Value Known (As Of)']} | "
            f"{row['Latest Date (Today)']} | {row['Latest Value (Today)']} | "
            f"{row['Observations Added After']} | {row['Observations Revised Since']} |"
        )
    st.markdown("\n".join(md_lines), unsafe_allow_html=True)
else:
    st.warning("No audit records available to display.")

# Footer note with execution command
st.write("---")
st.markdown(
    "**Run this application locally:**  \n"
    "`streamlit run asof_app.py`"
)
