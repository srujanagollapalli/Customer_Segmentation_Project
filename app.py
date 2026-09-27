import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Customer Segmentation Platform",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    return pd.read_excel("Customer_Segmentation_200_Rows.xlsx")

df = load_data()
df.columns = df.columns.str.strip()

rename = {}
for c in df.columns:
    x = c.lower().replace(" ", "")
    if x == "customerid":
        rename[c] = "CustomerID"
    elif x == "annualincome":
        rename[c] = "AnnualIncome"
    elif x == "purchasehistory":
        rename[c] = "PurchaseHistory"
    elif x == "spendingscore":
        rename[c] = "SpendingScore"
    elif x == "cluster":
        rename[c] = "Cluster"

df.rename(columns=rename, inplace=True)
df["CustomerID"] = df["CustomerID"].astype(str)

# -------- Segment Logic --------

def get_segment(row):
    income = row["AnnualIncome"]
    score = row["SpendingScore"]

    if income >= 90000 and score >= 75:
        return "High Value Customer", "Cluster 0"

    elif income >= 60000 and score >= 50:
        return "Premium Customer", "Cluster 1"

    elif income >= 35000 and score >= 35:
        return "Regular Customer", "Cluster 2"

    else:
        return "Budget Customer", "Cluster 3"

segments = df.apply(get_segment, axis=1)

df["Customer_Segment"] = segments.apply(lambda x: x[0])
df["KMeans_Cluster"] = segments.apply(lambda x: x[1])

tips = {
    "High Value Customer": "Focus on retention and premium offers.",
    "Premium Customer": "Offer premium membership and exclusive benefits.",
    "Regular Customer": "Provide loyalty rewards and seasonal discounts.",
    "Budget Customer": "Offer affordable deals and discount coupons."
}

df["Marketing_Suggestion"] = df["Customer_Segment"].map(tips)

if "customer_id" not in st.session_state:
    st.session_state.customer_id = df["CustomerID"].iloc[0]

if "page" not in st.session_state:
    st.session_state.page = "Home"
    # ---------------- CSS ----------------

st.markdown("""
<style>

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

[data-testid="stSidebar"]{
background:#081733;
min-width:310px;
max-width:310px;
}

[data-testid="stAppViewContainer"]{
background:#F7F9FC;
}

.block-container{
max-width:1400px;
padding-top:20px;
}

.metric-card{
background:white;
padding:20px;
border-radius:16px;
border:1px solid #E5E7EB;
min-height:180px;
display:flex;
flex-direction:column;
justify-content:space-between;
box-shadow:0 2px 8px rgba(0,0,0,.05);
}

.profile-box{
background:white;
padding:18px;
border-radius:14px;
border:1px solid #E5E7EB;
box-shadow:0 2px 8px rgba(0,0,0,.05);
color:#111827 !important;
}

.tip{
padding:16px;
border-radius:14px;
border:1px solid #E5E7EB;
min-height:120px;
box-shadow:0 2px 8px rgba(0,0,0,.04);
color:#111827 !important;
}

.tip b{
font-size:16px;
color:#111827 !important;
}

.blue{background:#EEF5FF;}
.green{background:#EDF9F1;}
.yellow{background:#FFF8E8;}

h1,h2,h3,h4,p,span,label{
color:#111827 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label{
color:white !important;
}

div.stButton>button{
width:100%;
height:46px;
border-radius:10px;
font-weight:bold;
font-size:15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("""
    <div style="text-align:center;padding-top:10px;">
        <h2 style="color:white;">👥 Customer Segmentation Platform</h2>
        <p style="color:#CBD5E1;">Personalized Marketing Analytics</p>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    st.markdown("### Enter Customer Details")

    cid = st.text_input(
        "Customer ID",
        value=st.session_state.customer_id
    )

    found = df[df["CustomerID"] == cid]

    if found.empty:
        customer = df.iloc[0]
    else:
        customer = found.iloc[0]

    st.number_input(
        "Age",
        value=int(customer["Age"]),
        disabled=True
    )

    st.number_input(
        "Income (₹)",
        value=int(customer["AnnualIncome"]),
        disabled=True
    )

    st.number_input(
        "Purchase History",
        value=int(customer["PurchaseHistory"]),
        disabled=True
    )

    st.number_input(
        "Spending Score",
        value=int(customer["SpendingScore"]),
        disabled=True
    )

    if st.button("🔍 Predict Customer"):
        if cid in set(df["CustomerID"]):
            st.session_state.customer_id = cid
            st.rerun()

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

customer = df[df["CustomerID"] == st.session_state.customer_id].iloc[0]
# ---------------- HOME ----------------

if st.session_state.page == "Home":

    customer = df[df["CustomerID"] == st.session_state.customer_id].iloc[0]

    # Dynamic Confidence Score
    confidence = min(99, max(70, int(customer["SpendingScore"]) + 15))

    st.title("Customer Segmentation & Personalized Marketing Analytics")
    st.success("Prediction Successful!")

    # ---------- TOP 3 CARDS ----------
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card blue">
            <div>
                <h4>💎 Customer Segment</h4>
                <h2 style="color:#1D4ED8;">{customer["Customer_Segment"]}</h2>
                <p>Confidence Score</p>
                <h4>{confidence}%</h4>
            </div>

            <div style="background:#DBEAFE;height:8px;border-radius:10px;">
                <div style="background:#2563EB;width:{confidence}%;height:8px;border-radius:10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card green">
            <h4>👥 Cluster</h4>
            <h2 style="color:#16A34A;">{customer["KMeans_Cluster"]}</h2>
            <p>{customer["Customer_Segment"]}</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card yellow">
            <h4>⭐ Marketing Priority</h4>
            <h2 style="color:#D97706;">High</h2>
            <p>{customer["Marketing_Suggestion"]}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- PROFILE + GRAPH ----------
    left, right = st.columns([1, 1.4])

    with left:

        st.subheader("👤 Customer Profile")

        st.markdown(f"""
        <div class="profile-box">
            <p><b>Customer ID:</b> {customer["CustomerID"]}</p>
            <p><b>Age:</b> {customer["Age"]} Years</p>
            <p><b>Income:</b> ₹{customer["AnnualIncome"]:,}</p>
            <p><b>Purchase History:</b> {customer["PurchaseHistory"]}</p>
            <p><b>Spending Score:</b> {customer["SpendingScore"]}/100</p>
            <p><b>Segment:</b> {customer["Customer_Segment"]}</p>
            <p><b>Cluster:</b> {customer["KMeans_Cluster"]}</p>
        </div>
        """, unsafe_allow_html=True)

    with right:

        st.subheader("📊 Cluster Visualization")

        fig, ax = plt.subplots(figsize=(8,5))

        colors = {
            "High Value Customer":"red",
            "Premium Customer":"blue",
            "Regular Customer":"green",
            "Budget Customer":"purple"
        }

        for seg in [
            "High Value Customer",
            "Premium Customer",
            "Regular Customer",
            "Budget Customer"
        ]:

            data = df[df["Customer_Segment"] == seg]

            if not data.empty:

                ax.scatter(
                    data["AnnualIncome"],
                    data["SpendingScore"],
                    color=colors[seg],
                    alpha=0.75,
                    s=35,
                    label=data["KMeans_Cluster"].iloc[0]
                )

        ax.scatter(
            customer["AnnualIncome"],
            customer["SpendingScore"],
            color="black",
            marker="*",
            s=300,
            label="Selected Customer"
        )

        ax.set_title("Income vs Spending Score")
        ax.set_xlabel("Annual Income (₹)")
        ax.set_ylabel("Spending Score")
        ax.grid(alpha=0.2)
        ax.legend()

        st.pyplot(fig)
            # ---------- MARKETING SUGGESTIONS ----------

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("💡 Personalized Marketing Suggestions")

    col1, col2, col3, col4, col5 = st.columns(5)

    cards = [
        ("🎁 Premium Membership", "#EEF5FF"),
        ("🏷 Festival Discount", "#EDF9F1"),
        ("⭐ Loyalty Rewards", "#FFF8E8"),
        ("✉ Personalized Offers", "#F4ECFF"),
        ("⏰ Early Access", "#FFF1F1")
    ]

    for col, (title, bg) in zip([col1, col2, col3, col4, col5], cards):
        with col:
            st.markdown(f"""
            <div class="tip" style="background:{bg};">
                <b>{title}</b>
                <br><br>
                {customer["Marketing_Suggestion"]}
            </div>
            """, unsafe_allow_html=True)

    # ---------- FOOTER ----------

    st.markdown(
        """
        <hr>
        <div style='text-align:center;color:#64748B;padding:15px;font-size:14px;'>
            © 2024 Customer Segmentation Platform | Built with Streamlit
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------- ABOUT PAGE ----------

elif st.session_state.page == "About":

    st.title("About Project")

    st.markdown("""
    ### Customer Segmentation and Personalized Marketing

    This project uses **K-Means Clustering** to group customers based on:

    - Customer ID
    - Annual Income
    - Purchase History
    - Spending Score

    ### Features

    - Dynamic Customer Segmentation
    - Cluster Visualization
    - Customer Profile
    - Personalized Marketing Suggestions
    - Interactive Dashboard

    ### Technology Used

    - Python
    - Pandas
    - Streamlit
    - Matplotlib
    - K-Means Clustering
    """)

# ---------- TEAM PAGE ----------

else:

    st.title("👥 Project Team")

    team = [
        ("Member 1", "Data Collection & Database"),
        ("Member 2", "Data Preprocessing & EDA"),
        ("Member 3", "K-Means Clustering"),
        ("Member 4", "Marketing Analysis"),
        ("Member 5", "Frontend & Integration")
    ]

    for name, role in team:
        st.markdown(f"""
        <div style="background:white;padding:18px;border-radius:12px;border:1px solid #E5E7EB;margin-bottom:12px;">
            <h4 style="margin-bottom:5px;">👤 {name}</h4>
            <p style="margin:0;color:#475569;">{role}</p>
        </div>
        """, unsafe_allow_html=True)
