import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Customer Segmentation Platform",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    if os.path.exists("Customer_Segmentation_200_Rows.xlsx"):
        return pd.read_excel("Customer_Segmentation_200_Rows.xlsx")
    elif os.path.exists("customer_segmentation_exact.csv"):
        return pd.read_csv("customer_segmentation_exact.csv")
    else:
        st.error("Dataset file not found.")
        st.stop()

df = load_data()
df["CustomerID"] = df["CustomerID"].astype(str)

# Column names ni project ki match cheyyadam
df.columns = df.columns.str.strip()

if "Cluster" in df.columns and "Customer_Segment" not in df.columns:
    segment_map = {
        0: "High Value Customer",
        1: "Regular Customer",
        2: "Budget Customer",
        3: "VIP Customer"
    }
    df["Customer_Segment"] = df["Cluster"].map(segment_map)

if "KMeans_Cluster" not in df.columns and "Cluster" in df.columns:
    df["KMeans_Cluster"] = df["Cluster"]

if "Marketing_Suggestion" not in df.columns:
    df["Marketing_Suggestion"] = "Focus on retention and personalized offers."

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "customer_id" not in st.session_state:
    st.session_state.customer_id = df["CustomerID"].iloc[0]

# ---------------- CSS ----------------
st.markdown("""
<style>
#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

[data-testid="stAppViewContainer"]{
background:#f8f9fb;
}

[data-testid="stSidebar"]{
background:#111d36;
}

[data-testid="stSidebar"] label{
color:white !important;
font-weight:600;
}

div.stButton > button{
width:100%;
height:45px;
border-radius:10px;
font-weight:700;
}
</style>
""", unsafe_allow_html=True)

# ---------------- CUSTOMER ----------------
customer = df[df["CustomerID"] == st.session_state.customer_id].iloc[0]

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;">
        <h2 style="color:white;">👥 Customer Segmentation Platform</h2>
        <p style="color:#cbd5e1;">Personalized Marketing Analytics</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("### Enter Customer Details")

    cid = st.text_input("Customer ID", value=st.session_state.customer_id)

    found = df[df["CustomerID"] == cid]

    if not found.empty:
        p = found.iloc[0]
    else:
        p = customer

    st.number_input("Age", value=int(p["Age"]), disabled=True)
    st.number_input("Income (₹)", value=int(p["AnnualIncome"]), disabled=True)
    st.number_input("Purchase History", value=int(p["PurchaseHistory"]), disabled=True)
    st.number_input("Spending Score", value=int(p["SpendingScore"]), disabled=True)

    if st.button("🔍 Predict Customer"):
        if cid in set(df["CustomerID"]):
            st.session_state.customer_id = cid
            st.rerun()
        else:
            st.error("Customer ID not found")

    if st.button("↻ Reset"):
        st.session_state.customer_id = df["CustomerID"].iloc[0]
        st.rerun()

    st.markdown("---")

    if st.button("🏠 Home"):
        st.session_state.page = "Home"
        st.rerun()

    if st.button("ℹ️ About Project"):
        st.session_state.page = "About"
        st.rerun()

    if st.button("👥 Team"):
        st.session_state.page = "Team"
        st.rerun()

# ---------------- HOME ----------------
if st.session_state.page == "Home":

    st.title("Customer Segmentation & Personalized Marketing Analytics")
    st.success("Prediction Successful!")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Customer Segment", customer["Customer_Segment"])

    with c2:
        st.metric("Cluster", f'Cluster {customer["KMeans_Cluster"]}')

    with c3:
        st.metric("Marketing Priority", "High")

    left, right = st.columns([1, 1.2])

    with left:
        st.subheader("Customer Profile")

        st.write(f"**Customer ID:** {customer['CustomerID']}")
        st.write(f"**Age:** {customer['Age']} Years")
        st.write(f"**Income:** ₹{customer['AnnualIncome']:,}")
        st.write(f"**Purchase History:** {customer['PurchaseHistory']}")
        st.write(f"**Spending Score:** {customer['SpendingScore']}/100")
        st.write(f"**Segment:** {customer['Customer_Segment']}")

    with right:
        st.subheader("Cluster Visualization")

        fig, ax = plt.subplots(figsize=(7,5))

        colors = ["red", "blue", "green", "purple"]

        for i, cl in enumerate(sorted(df["KMeans_Cluster"].unique())):
            d = df[df["KMeans_Cluster"] == cl]
            ax.scatter(
                d["AnnualIncome"],
                d["SpendingScore"],
                color=colors[i % 4],
                alpha=0.7,
                label=f"Cluster {cl}"
            )

        ax.scatter(
            customer["AnnualIncome"],
            customer["SpendingScore"],
            marker="*",
            color="black",
            s=250,
            label="Selected Customer"
        )

        ax.set_xlabel("Income")
        ax.set_ylabel("Spending Score")
        ax.legend()

        st.pyplot(fig)

    st.subheader("Personalized Marketing Suggestions")

    m1, m2, m3, m4, m5 = st.columns(5)

    m1.info("🎁 Premium Membership")
    m2.info("🏷 Festival Discount")
    m3.info("⭐ Loyalty Rewards")
    m4.info("✉ Personalized Offers")
    m5.info("⏰ Early Access")

# ---------------- ABOUT ----------------
elif st.session_state.page == "About":

    st.title("About Project")

    st.write("""
Customer Segmentation and Personalized Marketing Analytics

This project groups customers using K-Means Clustering based on
Income, Purchase History and Spending Score.
""")

# ---------------- TEAM ----------------
elif st.session_state.page == "Team":

    st.title("Team")

    st.info("Add your team member names here.")
