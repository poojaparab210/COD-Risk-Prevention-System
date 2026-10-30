import streamlit as st
import pandas as pd
import altair as alt
import html as html_lib
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# 1. PROJECT CONFIGURATION & CONSTANTS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DECISION_FILE = BASE_DIR / "reports" / "final_decision_log.csv"
WHATSAPP_FILE = BASE_DIR / "reports" / "whatsapp_simulation.csv"
ORDERS_FILE = BASE_DIR / "data" / "cleaned_orders.csv"

# Financial parameters from the business assignment
RTO_FORWARD = 65.00
RTO_REVERSE = 65.00
RTO_PACKAGING = 25.00
DAMAGE_RATE = 0.08
DAMAGE_PRODUCT_COST = 180.00
# Total per-RTO loss: 65 + 65 + 25 + (0.08 * 180) = ₹169.40
RTO_COST = RTO_FORWARD + RTO_REVERSE + RTO_PACKAGING + (DAMAGE_RATE * DAMAGE_PRODUCT_COST)

CAC_COST = 300.00          # Meta Ad CAC spend per acquired customer
GROSS_MARGIN_RATE = 0.62   # 62% gross margin on delivered orders
PREPAID_RTO_RATE = 0.04    # 4% baseline RTO on prepaid orders


st.set_page_config(
    page_title="Founder COD Risk Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    decisions = pd.read_csv(DECISION_FILE)
    whatsapp = pd.read_csv(WHATSAPP_FILE)
    orders = pd.read_csv(ORDERS_FILE)

    orders["order_datetime"] = pd.to_datetime(
        orders["order_datetime"],
        errors="coerce"
    )

    whatsapp["discount"] = pd.to_numeric(
        whatsapp["discount"],
        errors="coerce"
    ).fillna(0)

    return decisions, whatsapp, orders


try:
    decisions, whatsapp, orders = load_data()
except FileNotFoundError as error:
    st.error(f"Required file not found: {error}")
    st.stop()


# ============================================================
# 3. SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown("## 📦 COD Intelligence")
    st.caption("AI-powered RTO prevention system")

    st.divider()

    st.markdown("### Appearance")
    dark_mode = st.toggle("🌙 Dark Mode", value=True)

    st.divider()

    st.markdown("### Dashboard Navigation")
    page = st.radio(
        "Navigate",
        [
            "Founder Morning View",
            "Overview",
            "Decision Analysis",
            "WhatsApp Analysis",
            "Financial Impact",
            "Order Logs"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### Model & System Specs")
    st.write("**ML Model:** Logistic Regression")
    st.write("**Address AI:** Llama 3.2 (Local 3B)")
    st.write("**Messaging:** Mock WhatsApp (Dual-lang)")
    st.write("**RTO Cost / Order:** ₹169.40")
    st.write("**Marketing CAC:** ₹300.00")

    st.divider()
    st.caption("Associate Software Engineer Take-Home | COD Engine")


# ============================================================
# 4. THEME COLORS & STYLING
# ============================================================

if dark_mode:
    theme = {
        "background": "#0B1120",
        "sidebar": "#111827",
        "card": "#172033",
        "border": "#334155",
        "text": "#F8FAFC",
        "muted": "#A8B8CC",
        "track": "#334155",
        "accent": "#38BDF8"
    }
else:
    theme = {
        "background": "#F4F7FC",
        "sidebar": "#EAF1FB",
        "card": "#FFFFFF",
        "border": "#D5E1F0",
        "text": "#172554",
        "muted": "#526581",
        "track": "#E4EBF5",
        "accent": "#2563EB"
    }

st.markdown(
    f"""
    <style>
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
        background-color: {theme["background"]} !important;
        color: {theme["text"]} !important;
    }}
    [data-testid="stHeader"] {{
        background-color: {theme["background"]} !important;
    }}
    [data-testid="stSidebar"] {{
        background-color: {theme["sidebar"]} !important;
        border-right: 1px solid {theme["border"]};
    }}
    [data-testid="stSidebar"] * {{
        color: {theme["text"]} !important;
    }}
    .block-container {{
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}
    h1, h2, h3, h4, h5 {{
        color: {theme["text"]} !important;
        font-weight: 750 !important;
    }}
    p, label, [data-testid="stCaptionContainer"] {{
        color: {theme["muted"]} !important;
    }}
    [data-testid="stMetric"] {{
        background-color: {theme["card"]} !important;
        border: 1px solid {theme["border"]} !important;
        border-radius: 13px;
        padding: 16px;
    }}
    [data-testid="stMetricLabel"] {{
        color: {theme["muted"]} !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {theme["text"]} !important;
        font-weight: 750 !important;
    }}
    hr {{
        border-color: {theme["border"]} !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 5. HELPER FUNCTIONS
# ============================================================

def show_kpi(label, value, color, note=""):
    card_html = f"""
    <div style="
        background-color: {theme['card']};
        border: 1px solid {theme['border']};
        border-left: 5px solid {color};
        border-radius: 13px;
        padding: 17px;
        min-height: 112px;
        margin-bottom: 12px;
        box-sizing: border-box;
    ">
        <div style="color: {theme['muted']}; font-size: 13px; font-weight: 600;">
            {label}
        </div>
        <div style="color: {color}; font-size: 27px; font-weight: 800; margin-top: 8px;">
            {value}
        </div>
        <div style="color: {theme['muted']}; font-size: 11px; margin-top: 4px;">
            {note}
        </div>
    </div>
    """
    st.html(card_html)


DECISION_PALETTE = ["#10B981", "#8B5CF6", "#F59E0B", "#EF4444", "#38BDF8", "#EC4899"]


def themed_bar_chart(data, height=320):
    if isinstance(data, pd.Series):
        df = data.rename("count").rename_axis("category").reset_index()
        chart = alt.Chart(df).mark_bar(
            color=theme["accent"],
            cornerRadiusTopLeft=4,
            cornerRadiusTopRight=4
        ).encode(
            x=alt.X("category:N", sort=None, title=None, axis=alt.Axis(labelAngle=-25)),
            y=alt.Y("count:Q", title=None),
            tooltip=["category", "count"]
        )
    else:
        index_name = data.index.name or "index"
        series_name = data.columns.name or "series"
        long_df = data.reset_index().melt(
            id_vars=index_name,
            var_name=series_name,
            value_name="count"
        )
        chart = alt.Chart(long_df).mark_bar(
            cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3
        ).encode(
            x=alt.X(f"{index_name}:N", title=None, axis=alt.Axis(labelAngle=-25)),
            y=alt.Y("count:Q", title=None),
            color=alt.Color(
                f"{series_name}:N",
                scale=alt.Scale(domain=list(data.columns), range=DECISION_PALETTE[:len(data.columns)])
            ),
            tooltip=[index_name, series_name, "count"]
        )

    chart = (
        chart.properties(height=height)
        .configure(background=theme["card"])
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelColor=theme["muted"],
            titleColor=theme["muted"],
            gridColor=theme["border"],
            domainColor=theme["border"],
            tickColor=theme["border"]
        )
        .configure_legend(labelColor=theme["text"], titleColor=theme["text"])
    )
    st.altair_chart(chart, use_container_width=True, theme=None)


def show_table(df, height=460):
    header_cells = "".join(
        f"""<th style="
            position:sticky;
            top:0;
            z-index:1;
            background:{theme['sidebar']};
            color:{theme['text']};
            text-align:left;
            padding:10px 12px;
            font-size:12px;
            font-weight:700;
            white-space:nowrap;
            border-bottom:1px solid {theme['border']};
        ">{html_lib.escape(str(col))}</th>"""
        for col in df.columns
    )

    body_rows = []
    for row_number, row in enumerate(df.itertuples(index=False)):
        row_background = theme["card"] if row_number % 2 == 0 else theme["background"]
        cells = []
        for value in row:
            if pd.isna(value):
                text = ""
            elif isinstance(value, float):
                text = f"{value:,.2f}"
            else:
                text = str(value)

            wrap = "white-space:normal;min-width:260px;" if len(text) > 40 else "white-space:nowrap;"
            cells.append(
                f"""<td style="
                    color:{theme['text']};
                    padding:8px 12px;
                    font-size:12px;
                    border-bottom:1px solid {theme['border']};
                    vertical-align:top;
                    {wrap}
                ">{html_lib.escape(text)}</td>"""
            )
        body_rows.append(f'<tr style="background:{row_background};">' + "".join(cells) + "</tr>")

    table_html = f"""
    <div style="
        max-height:{height}px;
        overflow:auto;
        background:{theme['card']};
        border:1px solid {theme['border']};
        border-radius:12px;
        margin-bottom:12px;
    ">
        <table style="width:100%; border-collapse:collapse; font-family:inherit;">
            <thead><tr>{header_cells}</tr></thead>
            <tbody>{"".join(body_rows)}</tbody>
        </table>
    </div>
    """
    st.html(table_html)


# ============================================================
# 6. DATA PREPARATION & MERGING
# ============================================================

dashboard_data = decisions.merge(
    orders[["order_id", "order_datetime", "city"]],
    on="order_id",
    how="left"
)

dashboard_data["risk_probability"] = (
    pd.to_numeric(dashboard_data["rto_risk_percent"], errors="coerce") / 100
)

whatsapp_data = whatsapp.merge(
    decisions[["order_id", "order_value", "rto_risk_percent"]],
    on="order_id",
    how="left"
)

whatsapp_data["risk_probability"] = (
    pd.to_numeric(whatsapp_data["rto_risk_percent"], errors="coerce") / 100
)

total_orders = len(dashboard_data)
decision_counts = dashboard_data["decision"].value_counts()

ship_count = int(decision_counts.get("Ship as-is", 0))
confirmation_count = int(decision_counts.get("Ship after WhatsApp confirmation", 0))
prepaid_count = int(decision_counts.get("Nudge to prepaid", 0))
hold_count = int(
    dashboard_data["decision"]
    .astype(str)
    .str.contains("Hold|cancel", case=False, na=False)
    .sum()
)

address_checked = int(
    dashboard_data["address_status"].fillna("Not checked").ne("Not checked").sum()
)

address_review_count = int(
    dashboard_data["manual_review"]
    .fillna(False)
    .astype(str)
    .str.lower()
    .isin(["true", "1", "yes"])
    .sum()
)


# ============================================================
# PAGE 1: FOUNDER MORNING VIEW (ASSIGNMENT PART 3)
# ============================================================

if page == "Founder Morning View":

    st.header("🌅 Founder Morning Overview")
    st.caption("Daily high-level decision summary and financial reconciliation.")

    # 1. Financial Computations
    # Avoided RTOs from successful prepaid nudges
    prepaid_accepted = whatsapp_data[
        whatsapp_data["simulated_outcome"] == "Prepaid Accepted - Ship"
    ].copy()
    prepaid_accepted["rto_reduction"] = (
        prepaid_accepted["risk_probability"] - PREPAID_RTO_RATE
    ).clip(lower=0)
    avoided_rtos_prepaid = prepaid_accepted["rto_reduction"].sum()
    discounts_paid = prepaid_accepted["discount"].sum()

    # Avoided RTOs from explicit buyer cancellations (avoiding shipping money waste)
    cancelled_rto_avoided = whatsapp_data[
        whatsapp_data["simulated_outcome"] == "Customer Cancelled"
    ]["risk_probability"].sum()

    # Total avoided RTO units and money saved
    total_avoided_rtos = avoided_rtos_prepaid + cancelled_rto_avoided
    saved_from_rtos = total_avoided_rtos * RTO_COST

    # Estimated lost from genuine orders cancelled/held (Marketing CAC ₹300 + Gross Margin 62%)
    cancelled_genuine = whatsapp_data[
        whatsapp_data["simulated_outcome"] == "Customer Cancelled"
    ].copy()
    cancelled_genuine["lost_value"] = (1 - cancelled_genuine["risk_probability"]) * (
        (cancelled_genuine["order_value"] * GROSS_MARGIN_RATE) + CAC_COST
    )
    lost_from_cancellations = cancelled_genuine["lost_value"].sum()

    # Net Impact: Saved RTO logistics costs - Lost margin/CAC - Discounts paid
    net_founder_impact = saved_from_rtos - lost_from_cancellations - discounts_paid

    # 2. Top-level 4 Metric Cards Required by Part 3
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_kpi(
            "1. Orders in 4 Buckets",
            f"{total_orders:,}",
            "#3B82F6",
            f"{ship_count} Ship | {confirmation_count} Confirm | {prepaid_count} Nudge | {hold_count} Hold"
        )

    with col2:
        show_kpi(
            "2. Saved from Avoided RTOs",
            f"₹{saved_from_rtos:,.0f}",
            "#10B981",
            f"~{total_avoided_rtos:.1f} RTOs avoided (@ ₹169.40)"
        )

    with col3:
        show_kpi(
            "3. Lost from False Cancels",
            f"-₹{lost_from_cancellations:,.0f}",
            "#EF4444",
            "Sunk CAC (₹300) + 62% Margin"
        )

    with col4:
        delta_sign = "+" if net_founder_impact >= 0 else ""
        net_color = "#10B981" if net_founder_impact >= 0 else "#EF4444"
        show_kpi(
            "4. Net Financial Impact",
            f"{delta_sign}₹{net_founder_impact:,.0f}",
            net_color,
            f"After ₹{discounts_paid:,.0f} prepaid incentives"
        )

    st.divider()

    # 3. Founder Summary Cards
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.subheader("Daily Order Ingestion by Action Tier")
        bucket_df = pd.Series({
            "1. Ship As-Is": ship_count,
            "2. WhatsApp Confirm": confirmation_count,
            "3. Nudge to Prepaid": prepaid_count,
            "4. Hold / Review": hold_count
        })
        themed_bar_chart(bucket_df, height=280)

    with col_right:
        st.subheader("Unit Economics Reconciliation")
        reconciliation_df = pd.DataFrame({
            "Metric": [
                "Avoided RTO Shipping & Damage Savings",
                "Prepaid Conversion Discounts Paid",
                "Estimated Margin & CAC Foregone (False Cancels)",
                "Net Realized Daily Impact"
            ],
            "Amount": [
                f"+₹{saved_from_rtos:,.2f}",
                f"-₹{discounts_paid:,.2f}",
                f"-₹{lost_from_cancellations:,.2f}",
                f"₹{net_founder_impact:,.2f}"
            ]
        })
        show_table(reconciliation_df, height=280)


# ============================================================
# PAGE 2: OVERVIEW
# ============================================================

elif page == "Overview":

    st.header("Business Overview")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        show_kpi("Total Orders", f"{total_orders:,}", "#3B82F6", "Orders analysed")
    with col2:
        show_kpi("Ship As-Is", f"{ship_count:,}", "#10B981", "Low-risk orders")
    with col3:
        show_kpi("WhatsApp Confirmation", f"{confirmation_count:,}", "#8B5CF6", "Confirmation required")
    with col4:
        show_kpi("Prepaid Nudge", f"{prepaid_count:,}", "#F59E0B", "Prepaid offer required")

    col1, col2, col3 = st.columns(3)
    with col1:
        show_kpi("Hold / Manual Review", f"{hold_count:,}", "#EF4444", "Review before dispatch")
    with col2:
        show_kpi("WhatsApp Messages", f"{len(whatsapp_data):,}", "#06B6D4", "Simulated messages")
    with col3:
        show_kpi("Address Checks", f"{address_checked:,}", "#A78BFA", "LLM sample checks")

    st.divider()
    st.subheader("Order Decision Distribution")

    decision_details = [
        ("Ship As-Is", ship_count, "#10B981"),
        ("WhatsApp Confirmation", confirmation_count, "#8B5CF6"),
        ("Prepaid Nudge", prepaid_count, "#F59E0B"),
        ("Hold / Review", hold_count, "#EF4444")
    ]
    max_count = max([item[1] for item in decision_details] + [1])

    left_column, right_column = st.columns([1.25, 1])

    with left_column:
        chart_rows = ""
        for label, count, color in decision_details:
            percentage = (count / total_orders * 100 if total_orders else 0)
            bar_width = count / max_count * 100
            chart_rows += f"""
            <div style="margin-bottom:25px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:9px; gap:10px;">
                    <span style="color:{theme['text']}; font-size:14px; font-weight:600;">{label}</span>
                    <span style="color:{theme['muted']}; font-size:13px; font-weight:700;">{count:,} ({percentage:.1f}%)</span>
                </div>
                <div style="width:100%; height:15px; background:{theme['track']}; border-radius:20px; overflow:hidden;">
                    <div style="width:{bar_width:.2f}%; height:15px; background:{color}; border-radius:20px;"></div>
                </div>
            </div>
            """

        chart_html = f"""
        <div style="background:{theme['card']}; border:1px solid {theme['border']}; border-radius:15px; padding:24px; min-height:310px; box-sizing:border-box;">
            <div style="color:{theme['text']}; font-size:17px; font-weight:750; margin-bottom:25px;">Order Distribution</div>
            {chart_rows}
            <div style="color:{theme['muted']}; font-size:11px; margin-top:15px;">Total orders: {total_orders:,}</div>
        </div>
        """
        st.html(chart_html)

    with right_column:
        st.markdown("#### Decision Breakdown")
        for label, count, color in decision_details:
            percentage = (count / total_orders * 100 if total_orders else 0)
            summary_html = f"""
            <div style="background:{theme['card']}; border:1px solid {theme['border']}; border-left:4px solid {color}; border-radius:12px; padding:15px; margin-bottom:13px; box-sizing:border-box;">
                <div style="display:flex; justify-content:space-between; align-items:center; gap:8px;">
                    <span style="color:{theme['text']}; font-size:13px; font-weight:650;">{label}</span>
                    <span style="color:{color}; font-size:19px; font-weight:800;">{count:,}</span>
                </div>
                <div style="color:{theme['muted']}; font-size:11px; margin-top:8px;">{percentage:.1f}% of total orders</div>
            </div>
            """
            st.html(summary_html)

    st.divider()
    st.subheader("Address Validation Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Address Checks Completed", address_checked)
    col2.metric("Not Checked", total_orders - address_checked)
    col3.metric("Flagged for Review", address_review_count)

    st.warning("The local LLM validator has checked 10 orders as a prototype. Remaining orders use heuristic fallbacks.")


# ============================================================
# PAGE 3: DECISION ANALYSIS
# ============================================================

elif page == "Decision Analysis":

    st.header("Decision Analysis")
    st.caption("Explore how the system distributes orders across four actions.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Ship As-Is", ship_count)
    col2.metric("WhatsApp Confirmation", confirmation_count)
    col3.metric("Prepaid Nudge", prepaid_count)
    col4.metric("Hold / Review", hold_count)

    st.divider()
    st.subheader("Decisions by City")

    city_data = dashboard_data.dropna(subset=["city"])
    if not city_data.empty:
        city_decisions = pd.crosstab(city_data["city"], city_data["decision"])
        themed_bar_chart(city_decisions)

    st.divider()
    st.subheader("Filter Order Decisions")

    available_decisions = dashboard_data["decision"].dropna().unique().tolist()
    selected_decisions = st.multiselect(
        "Select decision categories",
        options=available_decisions,
        default=available_decisions
    )

    filtered_decisions = dashboard_data[dashboard_data["decision"].isin(selected_decisions)]

    decision_columns = [
        "order_id",
        "order_value",
        "rto_risk_percent",
        "decision",
        "prepaid_discount",
        "address_status",
        "explanation"
    ]
    show_table(filtered_decisions[decision_columns])


# ============================================================
# PAGE 4: WHATSAPP ANALYSIS
# ============================================================

elif page == "WhatsApp Analysis":

    st.header("WhatsApp Simulation Analysis")
    st.caption("Explore simulated English and Hinglish messages and customer responses.")

    outcome_counts = whatsapp_data["simulated_outcome"].value_counts()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Messages", len(whatsapp_data))
    col2.metric("COD Confirmed", int(outcome_counts.get("COD Confirmed - Ship", 0)))
    col3.metric("Prepaid Accepted", int(outcome_counts.get("Prepaid Accepted - Ship", 0)))

    col1, col2, col3 = st.columns(3)
    col1.metric("Customer Cancelled", int(outcome_counts.get("Customer Cancelled", 0)))
    col2.metric("No Reply", int(outcome_counts.get("No Reply - Hold for Review", 0)))
    col3.metric("Manual Follow-up", int(outcome_counts.get("Manual Follow-up Required", 0)))

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Customer Reply Distribution")
        themed_bar_chart(whatsapp_data["reply"].value_counts())

    with col2:
        st.subheader("WhatsApp Outcomes")
        themed_bar_chart(outcome_counts)

    st.divider()
    st.subheader("Language Distribution")
    themed_bar_chart(whatsapp_data["language"].value_counts())

    st.divider()
    st.subheader("WhatsApp Message History")
    show_table(whatsapp_data[["order_id", "decision", "language", "message", "reply", "simulated_outcome", "discount"]])


# ============================================================
# PAGE 5: FINANCIAL IMPACT
# ============================================================

elif page == "Financial Impact":

    st.header("Estimated Financial Impact & Unit Economics")
    st.caption("Reconciles avoided RTO losses against customer acquisition costs (CAC) and margin foregone.")

    # Avoided RTO calculation
    prepaid_accepted = whatsapp_data[
        whatsapp_data["simulated_outcome"] == "Prepaid Accepted - Ship"
    ].copy()
    prepaid_accepted["expected_rto_reduction"] = (
        prepaid_accepted["risk_probability"] - PREPAID_RTO_RATE
    ).clip(lower=0)
    expected_avoided_rtos = prepaid_accepted["expected_rto_reduction"].sum()
    estimated_rto_savings = expected_avoided_rtos * RTO_COST

    total_discounts = prepaid_accepted["discount"].sum()
    estimated_prepaid_benefit = estimated_rto_savings - total_discounts

    # Margin and CAC foregone calculation
    cancelled_orders = whatsapp_data[
        whatsapp_data["simulated_outcome"] == "Customer Cancelled"
    ].copy()
    cancelled_orders["estimated_loss"] = (
        (1 - cancelled_orders["risk_probability"])
        * ((cancelled_orders["order_value"] * GROSS_MARGIN_RATE) + CAC_COST)
    )
    estimated_margin_and_cac_foregone = cancelled_orders["estimated_loss"].sum()

    estimated_net_impact = estimated_prepaid_benefit - estimated_margin_and_cac_foregone

    col1, col2 = st.columns(2)
    col1.metric("Avoided RTO Shipping Savings", f"₹{estimated_rto_savings:,.2f}")
    col2.metric("Prepaid Discounts Disbursed", f"₹{total_discounts:,.2f}")

    col1, col2 = st.columns(2)
    col1.metric("Net Prepaid Benefit", f"₹{estimated_prepaid_benefit:,.2f}")
    col2.metric("Foregone Margin + Sunk CAC (₹300)", f"₹{estimated_margin_and_cac_foregone:,.2f}")

    st.divider()
    st.metric("Net Realized Financial Impact", f"₹{estimated_net_impact:,.2f}")

    st.divider()
    st.subheader("Financial Unit Economics Parameters")

    assumptions = pd.DataFrame(
        {
            "Parameter": [
                "Forward Shipping Cost",
                "Return Shipping Cost",
                "Packaging & Handling",
                "Product Damage Allowance (8% * ₹180)",
                "Total Loss Per RTO",
                "Marketing Meta Ad CAC",
                "Delivered Gross Margin %",
                "Prepaid RTO Rate Benchmark"
            ],
            "Value": [
                "₹65.00",
                "₹65.00",
                "₹25.00",
                "₹14.40",
                "₹169.40",
                "₹300.00",
                "62%",
                "4%"
            ]
        }
    )
    show_table(assumptions)


# ============================================================
# PAGE 6: ORDER LOGS
# ============================================================

elif page == "Order Logs":

    st.header("Order and Decision Logs")
    st.caption("Search and review final decisions, risk scores and address validation results.")

    search_order = st.text_input("Search by Order ID", placeholder="Enter an order ID...")

    filtered_data = dashboard_data.copy()
    if search_order:
        filtered_data = filtered_data[
            filtered_data["order_id"].astype(str).str.contains(search_order, case=False, na=False)
        ]

    st.subheader("Final Decision Log")
    decision_log_columns = [
        "order_id",
        "order_value",
        "rto_risk_percent",
        "original_decision",
        "decision",
        "prepaid_discount",
        "address_status",
        "risk_level",
        "manual_review",
        "explanation"
    ]
    show_table(filtered_data[decision_log_columns])

    st.download_button(
        label="⬇ Download Final Decision Log",
        data=filtered_data.to_csv(index=False).encode("utf-8"),
        file_name="final_decision_log.csv",
        mime="text/csv"
    )

    st.divider()
    st.subheader("WhatsApp Simulation Log")
    show_table(whatsapp_data[["order_id", "language", "reply", "simulated_outcome", "discount"]])

    st.download_button(
        label="⬇ Download WhatsApp Simulation",
        data=whatsapp_data.to_csv(index=False).encode("utf-8"),
        file_name="whatsapp_simulation.csv",
        mime="text/csv"
    )


# ============================================================
# 7. FOOTER
# ============================================================

st.divider()
st.markdown(
    f"""
    <div style="text-align:center; color:{theme['muted']}; font-size:12px; padding:12px;">
        COD Risk Intelligence | AI + Machine Learning Prototype
        <br>
        Historical Data • Simulated Communication • Estimated Impact
    </div>
    """,
    unsafe_allow_html=True
)