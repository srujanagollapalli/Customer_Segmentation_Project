import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Customer Segmentation & Marketing",
    page_icon="👥",
    layout="wide"
)


# ============================================================
# MYSQL CONNECTION
# ============================================================

def get_mysql_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="MySQL@0915",
        database="customer_segmentation_db"
    )


# ============================================================
# LOAD CUSTOMER DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "customer_segmentation_exact.csv")
    )

    return df


try:

    df = load_data()

except Exception as e:

    st.error(f"Unable to load dataset: {e}")
    st.stop()


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Home",
        "📊 Dashboard",
        "👥 Customer Segments",
        "👤 Customer Analysis",
        "💡 Marketing Suggestions"
    ]
)


# ============================================================
# HOME PAGE
# ============================================================

if page == "🏠 Home":

    st.title("👥 Customer Segmentation & Marketing")

    st.subheader(
        "Customer Segmentation and Personalized Marketing Analysis Platform"
    )

    st.write(
        """
        This project analyzes customer information and divides customers
        into different segments based on their purchasing behavior.
        """
    )

    st.divider()

    # Project overview

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Customers",
            len(df)
        )

    with col2:

        st.metric(
            "Customer Segments",
            df["Customer_Segment"].nunique()
        )

    with col3:

        st.metric(
            "Average Spending Score",
            f"{df['SpendingScore'].mean():.2f}"
        )

    st.divider()

    st.subheader("🎯 Project Objectives")

    st.write(
        """
        • Analyze customer purchasing behavior

        • Divide customers into meaningful customer segments

        • Understand spending patterns

        • Identify high-value customers

        • Provide personalized marketing suggestions
        """
    )

    st.subheader("📂 Customer Segments")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info("💰 **Budget**\n\nPrice-sensitive customers")

    with col2:
        st.info("🛍️ **Regular**\n\nModerate spending customers")

    with col3:
        st.info("💎 **Premium**\n\nHigh-value customers")

    with col4:
        st.info("👑 **VIP**\n\nMost valuable customers")


# ============================================================
# DASHBOARD
# ============================================================

elif page == "📊 Dashboard":

    st.title("📊 Customer Segmentation Dashboard")

    st.write(
        "Overview of customer demographics, income and spending behavior."
    )

    st.divider()

    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Customers",
            len(df)
        )

    with col2:

        st.metric(
            "Average Income",
            f"{df['AnnualIncome'].mean():,.0f}"
        )

    with col3:

        st.metric(
            "Average Spending Score",
            f"{df['SpendingScore'].mean():.2f}"
        )

    with col4:

        st.metric(
            "Number of Segments",
            df["Customer_Segment"].nunique()
        )

    st.divider()

    # ========================================================
    # SEGMENT DISTRIBUTION
    # ========================================================

    st.subheader("👥 Customer Segment Distribution")

    segment_counts = df["Customer_Segment"].value_counts()

    col1, col2 = st.columns(2)

    with col1:

        fig, ax = plt.subplots(figsize=(7, 5))

        segment_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title("Customers by Segment")
        ax.set_xlabel("Customer Segment")
        ax.set_ylabel("Number of Customers")

        plt.xticks(rotation=0)

        st.pyplot(fig)

        plt.close(fig)

    with col2:

        fig, ax = plt.subplots(figsize=(7, 5))

        segment_counts.plot(
            kind="pie",
            autopct="%1.1f%%",
            ax=ax
        )

        ax.set_title("Segment Distribution")
        ax.set_ylabel("")

        st.pyplot(fig)

        plt.close(fig)

    st.divider()

    # ========================================================
    # INCOME VS SPENDING
    # ========================================================

    st.subheader("💰 Annual Income vs Spending Score")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.scatter(
        df["AnnualIncome"],
        df["SpendingScore"]
    )

    ax.set_title("Income vs Spending Score")
    ax.set_xlabel("Annual Income")
    ax.set_ylabel("Spending Score")

    st.pyplot(fig)

    plt.close(fig)

    st.divider()

    # ========================================================
    # AVERAGE INCOME BY SEGMENT
    # ========================================================

    st.subheader("📈 Average Income by Segment")

    avg_income = (
        df.groupby("Customer_Segment")["AnnualIncome"]
        .mean()
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    avg_income.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Average Annual Income by Segment")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Average Annual Income")

    plt.xticks(rotation=0)

    st.pyplot(fig)

    plt.close(fig)

    st.divider()

    # ========================================================
    # AVERAGE SPENDING BY SEGMENT
    # ========================================================

    st.subheader("🛍️ Average Spending Score by Segment")

    avg_spending = (
        df.groupby("Customer_Segment")["SpendingScore"]
        .mean()
        .sort_values()
    )

    fig, ax = plt.subplots(figsize=(10, 5))

    avg_spending.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Average Spending Score by Segment")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Average Spending Score")

    plt.xticks(rotation=0)

    st.pyplot(fig)

    plt.close(fig)

    st.divider()

    # ========================================================
    # COMPLETE DATASET
    # ========================================================

    st.subheader("📋 Complete Customer Dataset")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# CUSTOMER SEGMENTS
# ============================================================

elif page == "👥 Customer Segments":

    st.title("👥 Customer Segmentation")

    st.write(
        "Customers are grouped into four segments based on their purchasing behavior."
    )

    # ========================================================
    # CSS
    # ========================================================

    st.markdown(
        """
        <style>

        .segment-card {
            padding: 22px;
            border-radius: 12px;
            border: 1px solid #d9d9d9;
            background-color: black;
            text-align: center;
            min-height: 145px;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
        }

        .segment-title {
            font-size: 21px;
            font-weight: 700;
            margin-bottom: 12px;
        }

        .segment-count {
            font-size: 30px;
            font-weight: 700;
        }

        .segment-label {
            font-size: 14px;
            color: #666;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # CREATE SEGMENTS
    # ========================================================

    budget = df[
        df["Customer_Segment"] == "Budget"
    ]

    regular = df[
        df["Customer_Segment"] == "Regular"
    ]

    premium = df[
        df["Customer_Segment"] == "Premium"
    ]

    vip = df[
        df["Customer_Segment"] == "VIP"
    ]


    # ========================================================
    # TOP SEGMENT CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            f"""
            <div class="segment-card">
                <div class="segment-title">💰 Budget</div>
                <div class="segment-count">{len(budget)}</div>
                <div class="segment-label">Customers</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="segment-card">
                <div class="segment-title">🛍️ Regular</div>
                <div class="segment-count">{len(regular)}</div>
                <div class="segment-label">Customers</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            f"""
            <div class="segment-card">
                <div class="segment-title">💎 Premium</div>
                <div class="segment-count">{len(premium)}</div>
                <div class="segment-label">Customers</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            f"""
            <div class="segment-card">
                <div class="segment-title">👑 VIP</div>
                <div class="segment-count">{len(vip)}</div>
                <div class="segment-label">Customers</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.divider()


    # ========================================================
    # FUNCTION TO DISPLAY SEGMENT
    # ========================================================

    def display_segment(segment_name, segment_data):

        st.subheader(
            f"Customers - {segment_name}"
        )

        st.dataframe(
            segment_data[
                [
                    "CustomerID",
                    "Age",
                    "AnnualIncome",
                    "PurchaseHistory",
                    "SpendingScore"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("**💡 Marketing Strategy**")

        if not segment_data.empty:

            suggestion = (
                segment_data["Marketing_Suggestion"]
                .dropna()
                .unique()
            )

            for item in suggestion:

                st.info(item)


    # ========================================================
    # BUDGET + REGULAR
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 💰 Budget Customers")

        st.dataframe(
            budget[
                [
                    "CustomerID",
                    "Age",
                    "AnnualIncome",
                    "PurchaseHistory",
                    "SpendingScore"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("**💡 Marketing Strategy**")

        if not budget.empty:

            st.info(
                budget["Marketing_Suggestion"].iloc[0]
            )


    with col2:

        st.markdown("### 🛍️ Regular Customers")

        st.dataframe(
            regular[
                [
                    "CustomerID",
                    "Age",
                    "AnnualIncome",
                    "PurchaseHistory",
                    "SpendingScore"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("**💡 Marketing Strategy**")

        if not regular.empty:

            st.info(
                regular["Marketing_Suggestion"].iloc[0]
            )


    st.divider()


    # ========================================================
    # PREMIUM + VIP
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 💎 Premium Customers")

        st.dataframe(
            premium[
                [
                    "CustomerID",
                    "Age",
                    "AnnualIncome",
                    "PurchaseHistory",
                    "SpendingScore"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("**💡 Marketing Strategy**")

        if not premium.empty:

            st.info(
                premium["Marketing_Suggestion"].iloc[0]
            )


    with col2:

        st.markdown("### 👑 VIP Customers")

        st.dataframe(
            vip[
                [
                    "CustomerID",
                    "Age",
                    "AnnualIncome",
                    "PurchaseHistory",
                    "SpendingScore"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.markdown("**💡 Marketing Strategy**")

        if not vip.empty:

            st.info(
                vip["Marketing_Suggestion"].iloc[0]
            )


# ============================================================
# CUSTOMER ANALYSIS
# ============================================================

elif page == "👤 Customer Analysis":

    st.title("👤 Customer Analysis")

    st.write(
        "Select a Customer ID to view complete customer details."
    )

    customer_ids = sorted(
        df["CustomerID"].dropna().unique().tolist()
    )

    selected_customer_id = st.selectbox(
        "Select Customer ID",
        customer_ids
    )

    customer_data = df[
        df["CustomerID"] == selected_customer_id
    ]

    if not customer_data.empty:

        customer = customer_data.iloc[0]

        st.success(
            f"Customer found: {customer['CustomerID']}"
        )

        st.subheader("📋 Complete Customer Details")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "**Customer ID:**",
                customer["CustomerID"]
            )

            st.write(
                "**Age:**",
                int(customer["Age"])
            )

            st.write(
                "**Annual Income:**",
                f"{float(customer['AnnualIncome']):,.2f}"
            )

            st.write(
                "**Purchase History:**",
                int(customer["PurchaseHistory"])
            )

            st.write(
                "**Spending Score:**",
                float(customer["SpendingScore"])
            )

        with col2:

            st.write(
                "**Cluster:**",
                customer["Cluster"]
            )

            st.write(
                "**K-Means Cluster:**",
                customer["KMeans_Cluster"]
            )

            st.write(
                "**Customer Segment:**",
                customer["Customer_Segment"]
            )

        st.divider()

        st.subheader("💡 Marketing Suggestion")

        st.info(
            customer["Marketing_Suggestion"]
        )
# ============================================================
# MARKETING SUGGESTIONS
# ============================================================

elif page == "💡 Marketing Suggestions":

    st.title("💡 Marketing Suggestions")

    st.write(
        "Recommended marketing strategies for each customer segment."
    )

    st.divider()

    segments = [
        "Budget",
        "Regular",
        "Premium",
        "VIP"
    ]

    for segment in segments:

        segment_data = df[
            df["Customer_Segment"] == segment
        ]

        if not segment_data.empty:

            st.subheader(
                f"👥 {segment} Customers"
            )

            st.write(
                f"Total Customers: **{len(segment_data)}**"
            )

            suggestions = (
                segment_data["Marketing_Suggestion"]
                .dropna()
                .unique()
            )

            for suggestion in suggestions:

                st.info(suggestion)

            st.divider()