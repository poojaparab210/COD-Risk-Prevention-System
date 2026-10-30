import streamlit as st
import pandas as pd
import altair as alt
import html as html_lib
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DECISION_FILE = BASE_DIR / "reports" / "final_decision_log.csv"
WHATSAPP_FILE = BASE_DIR / "reports" / "whatsapp_simulation.csv"
ORDERS_FILE = BASE_DIR / "data" / "cleaned_orders.csv"

RTO_COST = 169.40
PREPAID_RTO_RATE = 0.04
GROSS_MARGIN_RATE = 0.62


st.set_page_config(
    page_title="COD Risk Intelligence",
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
# 3. SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 📦 COD Intelligence")
    st.caption("AI-powered RTO prevention system")

    st.divider()

    st.markdown("### Appearance")

    dark_mode = st.toggle(
        "🌙 Dark Mode",
        value=True
    )

    st.divider()

    st.markdown("### Dashboard Navigation")

    page = st.radio(
        "Navigate",
        [
            "Overview",
            "Decision Analysis",
            "WhatsApp Analysis",
            "Financial Impact",
            "Order Logs"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### Project Information")

    st.write("**ML Model:** Logistic Regression")
    st.write("**Address AI:** Llama 3.2")
    st.write("**Messaging:** Mock WhatsApp")
    st.write("**Data:** Historical order sample")

    st.divider()

    st.caption("COD Risk Prevention System | Prototype")



# ============================================================
# 4. THEME COLORS
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


# ============================================================
# 5. THEME-AWARE CSS
# ============================================================

st.markdown(
    f"""
    <style>

    /* Main application */

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {{
        background-color: {theme["background"]} !important;
        color: {theme["text"]} !important;
    }}

    [data-testid="stHeader"] {{
        background-color: {theme["background"]} !important;
    }}

    /* Sidebar */

    [data-testid="stSidebar"] {{
        background-color: {theme["sidebar"]} !important;
        border-right: 1px solid {theme["border"]};
    }}

    [data-testid="stSidebar"] > div {{
        background-color: {theme["sidebar"]} !important;
    }}

    [data-testid="stSidebar"] * {{
        color: {theme["text"]} !important;
    }}

    /* Main content spacing */

    .block-container {{
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}

    /* Headings */

    h1, h2, h3, h4, h5 {{
        color: {theme["text"]} !important;
        font-weight: 750 !important;
    }}

    /* Normal text */

    p,
    label,
    [data-testid="stCaptionContainer"] {{
        color: {theme["muted"]} !important;
    }}

    /* Metric cards */

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

    /* Input fields */

    input,
    textarea {{
        background-color: {theme["card"]} !important;
        color: {theme["text"]} !important;
        border-color: {theme["border"]} !important;
    }}

    [data-baseweb="select"] > div {{
        background-color: {theme["card"]} !important;
        border-color: {theme["border"]} !important;
        color: {theme["text"]} !important;
    }}

    [data-baseweb="popover"] {{
        background-color: {theme["card"]} !important;
    }}

    [role="listbox"],
    [role="option"] {{
        background-color: {theme["card"]} !important;
        color: {theme["text"]} !important;
    }}

    /* Radio buttons and checkboxes */

    [data-testid="stRadio"],
    [data-testid="stCheckbox"],
    [data-testid="stToggle"] {{
        color: {theme["text"]} !important;
    }}

    [data-testid="stRadio"] label,
    [data-testid="stCheckbox"] label {{
        color: {theme["text"]} !important;
    }}

    /* Radio: unselected circle */

    [data-baseweb="radio"]:has(input:not(:checked)) > div:first-child {{
        background-color: {theme["card"]} !important;
        border-color: {theme["muted"]} !important;
    }}

    /* Toggle: unselected track */

    [data-baseweb="checkbox"]:has(input:not(:checked)) > div:first-child {{
        background-color: {theme["muted"]} !important;
    }}

    /* Multiselect tags */

    [data-baseweb="tag"] {{
        background-color: {theme["accent"]} !important;
        color: #FFFFFF !important;
    }}

    [data-baseweb="tag"] * {{
        color: #FFFFFF !important;
    }}

    /* Dataframes */

    [data-testid="stDataFrame"] {{
        background-color: {theme["card"]} !important;
        border: 1px solid {theme["border"]} !important;
        border-radius: 12px;
    }}

    /* Buttons */

    .stDownloadButton button {{
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 9px;
        padding: 9px 16px;
    }}

    .stDownloadButton button:hover {{
        background-color: #1D4ED8 !important;
        color: #FFFFFF !important;
    }}

    /* Alerts */

    [data-testid="stAlert"] {{
        border-radius: 12px;
    }}

    /* Dividers */

    hr {{
        border-color: {theme["border"]} !important;
    }}

    /* Progress bars */

    [data-testid="stProgressBar"] > div {{
        background-color: {theme["track"]} !important;
    }}

    /* Chart containers */

    [data-testid="stVegaLiteChart"],
    [data-testid="stArrowVegaLiteChart"] {{
        background-color: {theme["card"]} !important;
        border: 1px solid {theme["border"]};
        border-radius: 12px;
        padding: 8px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 6. HELPER FUNCTIONS
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

        <div style="
            color: {theme['muted']};
            font-size: 13px;
            font-weight: 600;
        ">
            {label}
        </div>

        <div style="
            color: {color};
            font-size: 29px;
            font-weight: 800;
            margin-top: 8px;
        ">
            {value}
        </div>

        <div style="
            color: {theme['muted']};
            font-size: 11px;
            margin-top: 4px;
        ">
            {note}
        </div>

    </div>
    """

    st.html(card_html)


DECISION_PALETTE = [
    "#10B981",
    "#8B5CF6",
    "#F59E0B",
    "#EF4444",
    "#38BDF8",
    "#EC4899"
]


def themed_bar_chart(data, height=320):
    """Theme-aware replacement for st.bar_chart (Series or crosstab DataFrame)."""

    if isinstance(data, pd.Series):

        df = data.rename("count").rename_axis("category").reset_index()

        chart = alt.Chart(df).mark_bar(
            color=theme["accent"],
            cornerRadiusTopLeft=4,
            cornerRadiusTopRight=4
        ).encode(
            x=alt.X(
                "category:N",
                sort=None,
                title=None,
                axis=alt.Axis(labelAngle=-25)
            ),
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
            x=alt.X(
                f"{index_name}:N",
                title=None,
                axis=alt.Axis(labelAngle=-25)
            ),
            y=alt.Y("count:Q", title=None),
            color=alt.Color(
                f"{series_name}:N",
                scale=alt.Scale(
                    domain=list(data.columns),
                    range=DECISION_PALETTE[:len(data.columns)]
                )
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
        .configure_legend(
            labelColor=theme["text"],
            titleColor=theme["text"]
        )
    )

    st.altair_chart(chart, use_container_width=True, theme=None)


def show_table(df, height=460):
    """Fully theme-aware HTML table (replacement for st.dataframe)."""

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

        row_background = (
            theme["card"] if row_number % 2 == 0
            else theme["background"]
        )

        cells = []

        for value in row:

            if pd.isna(value):
                text = ""
            elif isinstance(value, float):
                text = f"{value:,.2f}"
            else:
                text = str(value)

            wrap = (
                "white-space:normal;min-width:260px;"
                if len(text) > 40
                else "white-space:nowrap;"
            )

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

        body_rows.append(
            f'<tr style="background:{row_background};">'
            + "".join(cells)
            + "</tr>"
        )

    table_html = f"""
    <div style="
        max-height:{height}px;
        overflow:auto;
        background:{theme['card']};
        border:1px solid {theme['border']};
        border-radius:12px;
        margin-bottom:12px;
    ">
        <table style="
            width:100%;
            border-collapse:collapse;
            font-family:inherit;
        ">
            <thead><tr>{header_cells}</tr></thead>
            <tbody>{"".join(body_rows)}</tbody>
        </table>
    </div>
    """

    st.html(table_html)


# ============================================================
# 7. PREPARE DASHBOARD DATA
# ============================================================

dashboard_data = decisions.merge(
    orders[
        [
            "order_id",
            "order_datetime",
            "city"
        ]
    ],
    on="order_id",
    how="left"
)

dashboard_data["risk_probability"] = (
    pd.to_numeric(
        dashboard_data["rto_risk_percent"],
        errors="coerce"
    ) / 100
)

whatsapp_data = whatsapp.merge(
    decisions[
        [
            "order_id",
            "order_value",
            "rto_risk_percent"
        ]
    ],
    on="order_id",
    how="left"
)

whatsapp_data["risk_probability"] = (
    pd.to_numeric(
        whatsapp_data["rto_risk_percent"],
        errors="coerce"
    ) / 100
)


# ============================================================
# 8. COMMON METRICS
# ============================================================

total_orders = len(dashboard_data)

decision_counts = dashboard_data["decision"].value_counts()

ship_count = int(
    decision_counts.get("Ship as-is", 0)
)

confirmation_count = int(
    decision_counts.get(
        "Ship after WhatsApp confirmation", 0
    )
)

prepaid_count = int(
    decision_counts.get("Nudge to prepaid", 0)
)

hold_count = int(
    decision_counts.get("Hold / cancel review", 0)
)

address_checked = int(
    dashboard_data["address_status"]
    .fillna("Not checked")
    .ne("Not checked")
    .sum()
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
# 9. DASHBOARD HEADER
# ============================================================

st.title("COD Risk Intelligence Dashboard")

st.caption(
    "Monitor COD order risk, customer responses, address reviews "
    "and estimated financial impact."
)


# ============================================================
# 10. OVERVIEW PAGE
# ============================================================

if page == "Overview":

    st.header("Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_kpi(
            "Total Orders",
            f"{total_orders:,}",
            "#3B82F6",
            "Orders analysed"
        )

    with col2:
        show_kpi(
            "Ship As-Is",
            f"{ship_count:,}",
            "#10B981",
            "Low-risk orders"
        )

    with col3:
        show_kpi(
            "WhatsApp Confirmation",
            f"{confirmation_count:,}",
            "#8B5CF6",
            "Confirmation required"
        )

    with col4:
        show_kpi(
            "Prepaid Nudge",
            f"{prepaid_count:,}",
            "#F59E0B",
            "Prepaid offer required"
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        show_kpi(
            "Hold / Manual Review",
            f"{hold_count:,}",
            "#EF4444",
            "Review before dispatch"
        )

    with col2:
        show_kpi(
            "WhatsApp Messages",
            f"{len(whatsapp_data):,}",
            "#06B6D4",
            "Simulated messages"
        )

    with col3:
        show_kpi(
            "Address Checks",
            f"{address_checked:,}",
            "#A78BFA",
            "LLM sample checks"
        )

    # --------------------------------------------------------
    # ORDER DECISION DISTRIBUTION
    # --------------------------------------------------------

    st.divider()

    st.subheader("Order Decision Distribution")

    decision_details = [
        ("Ship As-Is", ship_count, "#10B981"),
        ("WhatsApp Confirmation", confirmation_count, "#8B5CF6"),
        ("Prepaid Nudge", prepaid_count, "#F59E0B"),
        ("Hold / Review", hold_count, "#EF4444")
    ]

    max_count = max(
        [item[1] for item in decision_details] + [1]
    )

    left_column, right_column = st.columns([1.25, 1])

    # LEFT: HORIZONTAL DISTRIBUTION BARS

    with left_column:

        chart_rows = ""

        for label, count, color in decision_details:

            percentage = (
                count / total_orders * 100
                if total_orders else 0
            )

            bar_width = count / max_count * 100

            chart_rows += f"""
            <div style="margin-bottom:25px;">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    margin-bottom:9px;
                    gap:10px;
                ">

                    <span style="
                        color:{theme['text']};
                        font-size:14px;
                        font-weight:600;
                    ">
                        {label}
                    </span>

                    <span style="
                        color:{theme['muted']};
                        font-size:13px;
                        font-weight:700;
                        white-space:nowrap;
                    ">
                        {count:,} ({percentage:.1f}%)
                    </span>

                </div>

                <div style="
                    width:100%;
                    height:15px;
                    background:{theme['track']};
                    border-radius:20px;
                    overflow:hidden;
                ">

                    <div style="
                        width:{bar_width:.2f}%;
                        height:15px;
                        background:{color};
                        border-radius:20px;
                    ">
                    </div>

                </div>

            </div>
            """

        chart_html = f"""
        <div style="
            background:{theme['card']};
            border:1px solid {theme['border']};
            border-radius:15px;
            padding:24px;
            min-height:310px;
            box-sizing:border-box;
        ">

            <div style="
                color:{theme['text']};
                font-size:17px;
                font-weight:750;
                margin-bottom:25px;
            ">
                Order Distribution
            </div>

            {chart_rows}

            <div style="
                color:{theme['muted']};
                font-size:11px;
                margin-top:15px;
            ">
                Total orders: {total_orders:,}
            </div>

        </div>
        """

        st.html(chart_html)

    # RIGHT: DECISION SUMMARY CARDS

    with right_column:

        st.markdown("#### Decision Breakdown")

        for label, count, color in decision_details:

            percentage = (
                count / total_orders * 100
                if total_orders else 0
            )

            summary_html = f"""
            <div style="
                background:{theme['card']};
                border:1px solid {theme['border']};
                border-left:4px solid {color};
                border-radius:12px;
                padding:15px;
                margin-bottom:13px;
                box-sizing:border-box;
            ">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    align-items:center;
                    gap:8px;
                ">

                    <span style="
                        color:{theme['text']};
                        font-size:13px;
                        font-weight:650;
                    ">
                        {label}
                    </span>

                    <span style="
                        color:{color};
                        font-size:19px;
                        font-weight:800;
                    ">
                        {count:,}
                    </span>

                </div>

                <div style="
                    width:100%;
                    height:7px;
                    background:{theme['track']};
                    border-radius:20px;
                    margin-top:12px;
                    overflow:hidden;
                ">

                    <div style="
                        width:{percentage:.2f}%;
                        height:7px;
                        background:{color};
                        border-radius:20px;
                    ">
                    </div>

                </div>

                <div style="
                    color:{theme['muted']};
                    font-size:11px;
                    margin-top:8px;
                ">
                    {percentage:.1f}% of total orders
                </div>

            </div>
            """

            st.html(summary_html)

    # --------------------------------------------------------
    # ADDRESS VALIDATION OVERVIEW
    # --------------------------------------------------------

    st.divider()

    st.subheader("Address Validation Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Address Checks Completed",
        address_checked
    )

    col2.metric(
        "Not Checked",
        total_orders - address_checked
    )

    col3.metric(
        "Flagged for Review",
        address_review_count
    )

    st.warning(
        "The local LLM validator has checked only 10 orders. "
        "The remaining orders are marked Not checked. "
        "Address validation is a prototype feature."
    )

    # --------------------------------------------------------
    # LATEST DATASET ACTIVITY
    # --------------------------------------------------------

    st.divider()

    st.subheader("Latest Available Dataset Activity")

    valid_dates = dashboard_data.dropna(
        subset=["order_datetime"]
    )

    if not valid_dates.empty:

        latest_date = (
            valid_dates["order_datetime"].max().date()
        )

        latest_orders = valid_dates[
            valid_dates["order_datetime"].dt.date == latest_date
        ]

        col1, col2 = st.columns(2)

        col1.metric(
            "Latest Dataset Date",
            str(latest_date)
        )

        col2.metric(
            "Orders on Latest Date",
            len(latest_orders)
        )

        themed_bar_chart(
            latest_orders["decision"].value_counts()
        )

        st.caption(
            "This is the latest date in the historical dataset, "
            "not yesterday's live order activity."
        )


# ============================================================
# 11. DECISION ANALYSIS PAGE
# ============================================================

elif page == "Decision Analysis":

    st.header("Decision Analysis")

    st.caption(
        "Explore how the system distributes orders across four actions."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Ship As-Is", ship_count)
    col2.metric("WhatsApp Confirmation", confirmation_count)
    col3.metric("Prepaid Nudge", prepaid_count)
    col4.metric("Hold / Review", hold_count)

    st.divider()

    st.subheader("Decisions by City")

    city_data = dashboard_data.dropna(
        subset=["city"]
    )

    if not city_data.empty:

        city_decisions = pd.crosstab(
            city_data["city"],
            city_data["decision"]
        )

        themed_bar_chart(
            city_decisions
        )

    st.divider()

    st.subheader("Filter Order Decisions")

    available_decisions = (
        dashboard_data["decision"]
        .dropna()
        .unique()
        .tolist()
    )

    selected_decisions = st.multiselect(
        "Select decision categories",
        options=available_decisions,
        default=available_decisions
    )

    filtered_decisions = dashboard_data[
        dashboard_data["decision"].isin(selected_decisions)
    ]

    decision_columns = [
        "order_id",
        "order_value",
        "rto_risk_percent",
        "decision",
        "prepaid_discount",
        "address_status",
        "explanation"
    ]

    show_table(
        filtered_decisions[decision_columns]
    )


# ============================================================
# 12. WHATSAPP ANALYSIS PAGE
# ============================================================

elif page == "WhatsApp Analysis":

    st.header("WhatsApp Simulation Analysis")

    st.caption(
        "Explore simulated English and Hinglish messages "
        "and customer responses."
    )

    outcome_counts = (
        whatsapp_data["simulated_outcome"].value_counts()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Messages",
        len(whatsapp_data)
    )

    col2.metric(
        "COD Confirmed",
        int(outcome_counts.get("COD Confirmed - Ship", 0))
    )

    col3.metric(
        "Prepaid Accepted",
        int(outcome_counts.get("Prepaid Accepted - Ship", 0))
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Customer Cancelled",
        int(outcome_counts.get("Customer Cancelled", 0))
    )

    col2.metric(
        "No Reply",
        int(outcome_counts.get("No Reply - Hold for Review", 0))
    )

    col3.metric(
        "Manual Follow-up",
        int(outcome_counts.get("Manual Follow-up Required", 0))
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Customer Reply Distribution")

        themed_bar_chart(
            whatsapp_data["reply"].value_counts()
        )

    with col2:

        st.subheader("WhatsApp Outcomes")

        themed_bar_chart(
            outcome_counts
        )

    st.divider()

    st.subheader("Language Distribution")

    themed_bar_chart(
        whatsapp_data["language"].value_counts()
    )

    st.info(
        "Messages and customer replies are simulated using "
        "configured probabilities. No real WhatsApp messages were sent."
    )

    st.divider()

    st.subheader("WhatsApp Message History")

    show_table(
        whatsapp_data[
            [
                "order_id",
                "decision",
                "language",
                "message",
                "reply",
                "simulated_outcome",
                "discount"
            ]
        ]
    )


# ============================================================
# 13. FINANCIAL IMPACT PAGE
# ============================================================

elif page == "Financial Impact":

    st.header("Estimated Financial Impact")

    st.caption(
        "Illustrative calculations based on model risk scores "
        "and the assignment's financial assumptions."
    )

    prepaid_accepted = whatsapp_data[
        whatsapp_data["simulated_outcome"] == "Prepaid Accepted - Ship"
    ].copy()

    prepaid_accepted["expected_rto_reduction"] = (
        prepaid_accepted["risk_probability"] - PREPAID_RTO_RATE
    ).clip(lower=0)

    expected_avoided_rtos = (
        prepaid_accepted["expected_rto_reduction"].sum()
    )

    estimated_rto_savings = (
        expected_avoided_rtos * RTO_COST
    )

    total_discounts = (
        prepaid_accepted["discount"].sum()
    )

    estimated_prepaid_benefit = (
        estimated_rto_savings - total_discounts
    )

    cancelled_orders = whatsapp_data[
        whatsapp_data["simulated_outcome"] == "Customer Cancelled"
    ].copy()

    cancelled_orders["estimated_margin_foregone"] = (
        (1 - cancelled_orders["risk_probability"])
        * cancelled_orders["order_value"]
        * GROSS_MARGIN_RATE
    )

    estimated_margin_foregone = (
        cancelled_orders["estimated_margin_foregone"].sum()
    )

    estimated_net_impact = (
        estimated_prepaid_benefit - estimated_margin_foregone
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Estimated RTO Cost Avoided",
        f"₹{estimated_rto_savings:,.2f}"
    )

    col2.metric(
        "Prepaid Discounts Given",
        f"₹{total_discounts:,.2f}"
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Estimated Prepaid Benefit",
        f"₹{estimated_prepaid_benefit:,.2f}"
    )

    col2.metric(
        "Estimated Margin Foregone",
        f"₹{estimated_margin_foregone:,.2f}"
    )

    st.divider()

    st.metric(
        "Illustrative Net Financial Impact",
        f"₹{estimated_net_impact:,.2f}"
    )

    st.divider()

    st.subheader("Financial Assumptions")

    assumptions = pd.DataFrame(
        {
            "Assumption": [
                "Forward Shipping Cost",
                "Return Shipping Cost",
                "Packaging and Handling",
                "Expected Damage Cost",
                "Expected COD RTO Cost",
                "Prepaid RTO Rate",
                "Gross Margin"
            ],
            "Value": [
                "₹65",
                "₹65",
                "₹25",
                "₹14.40",
                "₹169.40",
                "4%",
                "62%"
            ]
        }
    )

    show_table(assumptions)

    st.warning(
        "These figures are estimates, not verified savings or actual profit. "
        "They assume prepaid orders have a 4% RTO rate. Model scores were "
        "generated on the same historical dataset used for training. "
        "The actual impact of discounts and cancellations has not been "
        "validated through a real experiment."
    )


# ============================================================
# 14. ORDER LOGS PAGE
# ============================================================

elif page == "Order Logs":

    st.header("Order and Decision Logs")

    st.caption(
        "Search and review final decisions, risk scores "
        "and address validation results."
    )

    search_order = st.text_input(
        "Search by Order ID",
        placeholder="Enter an order ID..."
    )

    filtered_data = dashboard_data.copy()

    if search_order:

        filtered_data = filtered_data[
            filtered_data["order_id"]
            .astype(str)
            .str.contains(
                search_order,
                case=False,
                na=False
            )
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

    show_table(
        filtered_data[decision_log_columns]
    )

    st.download_button(
        label="⬇ Download Final Decision Log",
        data=filtered_data.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="final_decision_log.csv",
        mime="text/csv"
    )

    st.divider()

    st.subheader("WhatsApp Simulation Log")

    show_table(
        whatsapp_data[
            [
                "order_id",
                "language",
                "reply",
                "simulated_outcome",
                "discount"
            ]
        ]
    )

    st.download_button(
        label="⬇ Download WhatsApp Simulation",
        data=whatsapp_data.to_csv(
            index=False
        ).encode("utf-8"),
        file_name="whatsapp_simulation.csv",
        mime="text/csv"
    )


# ============================================================
# 15. FOOTER
# ============================================================

st.divider()

st.markdown(
    f"""
    <div style="
        text-align:center;
        color:{theme['muted']};
        font-size:12px;
        padding:12px;
    ">
        COD Risk Intelligence | AI + Machine Learning Prototype
        <br>
        Historical Data • Simulated Communication • Estimated Impact
    </div>
    """,
    unsafe_allow_html=True
)