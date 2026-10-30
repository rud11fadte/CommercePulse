"""CommercePulse — ecommerce analytics dashboard."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_DIR = Path(__file__).parent / "data"

st.set_page_config(
    page_title="CommercePulse",
    page_icon="📊",
    layout="wide",
)

st.title("📊 CommercePulse")
st.caption("E-commerce data engineering and analytics platform")


@st.cache_data
def fetch_monthly_analytics():
    file_path = DATA_DIR / "monthly_order_analytics.parquet"
    return pd.read_parquet(file_path)


@st.cache_data
def fetch_quality_report():
    file_path = DATA_DIR / "data_quality_report.csv"
    report_df = pd.read_csv(file_path)
    return dict(zip(report_df["metric"], report_df["value"].astype(str)))


try:
    df = fetch_monthly_analytics()
    quality = fetch_quality_report()
except Exception as exc:
    st.error(f"Could not load CommercePulse data: {exc}")
    st.info("Make sure the analytics and quality report files exist in app/data/.")
    st.stop()

if df.empty:
    st.warning("No analytics data is available. Run the data pipeline first.")
    st.stop()

df["order_count"] = pd.to_numeric(
    df["order_count"], errors="coerce"
).fillna(0)

df["purchase_month"] = pd.to_datetime(
    df["purchase_month"], format="%Y-%m"
)

# Sidebar filters
st.sidebar.header("Dashboard filters")

months = sorted(df["purchase_month"].dt.strftime("%Y-%m").unique())
selected_months = st.sidebar.multiselect(
    "Purchase month",
    options=months,
    default=months,
)

statuses = sorted(df["order_status"].dropna().unique())
selected_statuses = st.sidebar.multiselect(
    "Order status",
    options=statuses,
    default=statuses,
)

filtered = df[
    df["purchase_month"].dt.strftime("%Y-%m").isin(selected_months)
    & df["order_status"].isin(selected_statuses)
].copy()

total_orders = int(filtered["order_count"].sum())
month_count = filtered["purchase_month"].nunique()
status_count = filtered["order_status"].nunique()

# KPI cards
st.subheader("Business overview")

col1, col2, col3 = st.columns(3)
col1.metric("Orders in selection", f"{total_orders:,}")
col2.metric("Months in selection", month_count)
col3.metric("Order statuses", status_count)

st.caption(
    "Order totals reflect the selected statuses and months. "
    "They represent order counts, not revenue."
)

# Charts
left, right = st.columns(2)

with left:
    st.subheader("Monthly order trends")

    if filtered.empty:
        st.info("No records match the selected filters.")
    else:
        monthly = (
            filtered.groupby("purchase_month", as_index=False)["order_count"]
            .sum()
            .sort_values("purchase_month")
        )

        fig = px.line(
            monthly,
            x="purchase_month",
            y="order_count",
            markers=True,
            title="Orders by purchase month",
            labels={
                "purchase_month": "Month",
                "order_count": "Number of orders",
            },
        )
        fig.update_layout(hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Order status distribution")

    if filtered.empty:
        st.info("No records match the selected filters.")
    else:
        status_summary = (
            filtered.groupby("order_status", as_index=False)["order_count"]
            .sum()
            .sort_values("order_count", ascending=False)
        )

        fig = px.bar(
            status_summary,
            x="order_status",
            y="order_count",
            title="Orders by status",
            labels={
                "order_status": "Order status",
                "order_count": "Number of orders",
            },
        )
        st.plotly_chart(fig, use_container_width=True)

# Data quality
st.divider()
st.subheader("Data quality monitoring")

validation_passed = quality.get("validation_passed", "").lower() == "true"

if validation_passed:
    st.success("Data validation passed")
else:
    st.warning("Data validation has not passed")

metric_cols = st.columns(4)

quality_metrics = [
    ("Total source rows", "total_rows"),
    ("Unique order IDs", "unique_order_ids"),
    ("Duplicate order IDs", "duplicate_order_ids"),
    ("Validation errors", "validation_error_count"),
]

for col, (label, key) in zip(metric_cols, quality_metrics):
    raw_value = quality.get(key, "N/A")
    try:
        value = f"{int(float(raw_value)):,}"
    except (ValueError, TypeError):
        value = str(raw_value)
    col.metric(label, value)

with st.expander("View complete data quality report"):
    st.json(quality)

with st.expander("View monthly analytics data"):
    display_df = filtered.copy()
    display_df["purchase_month"] = (
        display_df["purchase_month"].dt.strftime("%Y-%m")
    )
    st.dataframe(display_df, use_container_width=True)

st.caption("CommercePulse | Built with Streamlit, FastAPI and PostgreSQL")
