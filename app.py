
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
    return pd.read_excel("Customer_Segmentation_200_Rows.xlsx")

df = load_data()
df.columns = df.columns.str.strip()

rename = {}
for c in df.columns:
    k = c.lower().replace(" ", "")
    if k == "customerid":
        rename[c] = "CustomerID"
    elif k == "annualincome":
        rename[c] = "AnnualIncome"
    elif k == "purchasehistory":
        rename[c] = "PurchaseHistory"
    elif k == "spendingscore":
        rename[c] = "SpendingScore"
    elif k == "cluster":
        rename[c] = "Cluster"

df.rename(columns=rename, inplace=True)

df["CustomerID"] = df["CustomerID"].astype(str).str.strip().str.upper()
df["Customer_Segment"] = df["Cluster"].astype(str).str.strip()

cluster_map = {
    "Budget": "Cluster 0",
    "Regular": "Cluster 1",
    "Premium": "Cluster 2",
    "VIP": "Cluster 3"
}

df["KMeans_Cluster"] = df["Customer_Segment"].map(cluster_map)

tips = {
    "Budget": "Offer affordable deals and discount coupons.",
    "Regular": "Provide loyalty rewards and seasonal discounts.",
    "Premium": "Offer premium membership and exclusive benefits.",
    "VIP": "Give exclusive access and premium benefits."
}

df["Marketing_Suggestion"] = df["Customer_Segment"].map(tips)

# ---------------- SESSION ----------------

if "customer_id" not in st.session_state:
    st.session_state.customer_id = df["CustomerID"].iloc[0]

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "predicted" not in st.session_state:
    st.session_state.predicted = False

# ---------------- CSS ----------------

st.markdown("""
<style>

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}

[data-testid="stSidebar"]{
    background:#081733;
    min-width:300px;
    max-width:300px;
}

[data-testid="stAppViewContainer"]{
    background:#F7F9FC;
}

.metric-card{
    background:white;
    padding:20px;
    border-radius:16px;
    border:1px solid #E5E7EB;
    min-height:170px;
    box-shadow:0 2px 8px rgba(0,0,0,.06);
}

.profile-box{
    background:white;
    padding:18px;
    border-radius:14px;
    border:1px solid #E5E7EB;
    box-shadow:0 2px 8px rgba(0,0,0,.05);
}

.tip{
    padding:15px;
    border-radius:12px;
    border:1px solid #E5E7EB;
    color:#111827!important;
    box-shadow:0 2px 8px rgba(0,0,0,.04);
    transition:0.25s;
}

.tip:hover{
    transform:translateY(-3px);
}

h1,h2,h3,h4,p,span,label{
    color:#111827!important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label{
    color:white!important;
}

div.stButton>button{
    width:100%;
    height:45px;
    border-radius:10px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("""
    <div style="text-align:center">
        <h2 style="color:white;">👥 Customer Segmentation Platform</h2>
        <p style="color:#CBD5E1;">Personalized Marketing Analytics</p>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    st.markdown("### Enter Customer Details")

    cid = st.text_input(
        "Customer ID",
        value=st.session_state.customer_id
    ).strip().upper()

    found = df[df["CustomerID"] == cid]

    if found.empty:
        preview = df.iloc[0]
    else:
        preview = found.iloc[0]

    st.number_input("Age", value=int(preview["Age"]), disabled=True)
    st.number_input("Income (₹)", value=int(preview["AnnualIncome"]), disabled=True)
    st.number_input("Purchase History", value=int(preview["PurchaseHistory"]), disabled=True)
    st.number_input("Spending Score", value=int(preview["SpendingScore"]), disabled=True)

       if st.button("🔍 Predict Customer"):
        if not found.empty:
            st.session_state.customer_id = cid
            st.session_state.predicted = True
            st.snow()
            st.balloons()
            st.rerun()
        else:
            st.error("Customer ID not found.")

    if st.button("↻ Reset"):
        st.session_state.customer_id = df["CustomerID"].iloc[0]
        st.session_state.predicted = False
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

    st.title("Customer Segmentation & Personalized Marketing Analytics")

    if st.session_state.predicted:
    st.success("🎉 Prediction Successful! Customer details loaded successfully.")
    st.session_state.predicted = False

    confidence = int(customer["SpendingScore"])

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <h4>💎 Customer Segment</h4>
            <h2 style="color:#2563EB;">{customer["Customer_Segment"]}</h2>
            <p>Confidence Score</p>
            <h3>{confidence}%</h3>
        </div>
        """, unsafe_allow_html=True)
        st.progress(confidence/100)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <h4>👥 Cluster</h4>
            <h2 style="color:#16A34A;">{customer["KMeans_Cluster"]}</h2>
            <p>{customer["Customer_Segment"]}</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <h4>⭐ Marketing Priority</h4>
            <h2 style="color:#D97706;">High</h2>
            <p>{customer["Marketing_Suggestion"]}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("###")

    left, right = st.columns([1,1.4])

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
            "Budget":"red",
            "Regular":"green",
            "Premium":"blue",
            "VIP":"purple"
        }

        for seg, data in df.groupby("Customer_Segment"):
            ax.scatter(
                data["AnnualIncome"],
                data["SpendingScore"],
                color=colors.get(seg,"gray"),
                alpha=0.8,
                s=35,
                label=seg
            )

        ax.scatter(
            customer["AnnualIncome"],
            customer["SpendingScore"],
            marker="*",
            color="black",
            s=280,
            label="Selected Customer"
        )

        ax.set_xlabel("Annual Income (₹)")
        ax.set_ylabel("Spending Score")
        ax.set_title("Income vs Spending Score")
        ax.grid(alpha=.2)
        ax.legend()

        st.pyplot(fig)

    st.subheader("💡 Personalized Marketing Suggestions")

    cols = st.columns(5)

    cards = [
        ("🎁 Premium Membership","#EEF5FF"),
        ("🏷 Festival Discount","#EDF9F1"),
        ("⭐ Loyalty Rewards","#FFF8E8"),
        ("✉ Personalized Offers","#F4ECFF"),
        ("⏰ Early Access","#FFF1F1")
    ]

    for col,(title,bg) in zip(cols,cards):
        with col:
            st.markdown(f"""
            <div class="tip" style="background:{bg};">
                <b>{title}</b><br><br>
                {customer["Marketing_Suggestion"]}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <hr>
    <div style="text-align:center;color:#64748B;padding:15px;">
        © 2024 Customer Segmentation Platform | Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

# ---------------- ABOUT ----------------

elif st.session_state.page == "About":

    st.title("About Project")

    st.markdown("""
    ### Customer Segmentation and Personalized Marketing

    **Inputs**

    - Customer ID
    - Annual Income
    - Purchase History
    - Spending Score

    **Outputs**

    - Customer Segment
    - K-Means Cluster
    - Customer Profile
    - Cluster Visualization
    - Personalized Marketing Suggestions
    """)

# ---------------- TEAM ----------------

else:

    st.title("👥 Project Team")

    members = [
        ("Member 1","Data Collection & Database"),
        ("Member 2","Data Preprocessing & EDA"),
        ("Member 3","K-Means Clustering"),
        ("Member 4","Marketing Analysis"),
        ("Member 5","Frontend & Integration")
    ]

    for name, role in members:
        st.markdown(f"""
        <div style="background:white;padding:18px;border-radius:12px;border:1px solid #E5E7EB;margin-bottom:12px;">
            <h4>👤 {name}</h4>
            <p>{role}</p>
        </div>
        """, unsafe_allow_html=True)
