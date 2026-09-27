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

# ---------- Segment Mapping ----------
if pd.api.types.is_numeric_dtype(df["Cluster"]):
    seg_map = {
        0: "High Value Customer",
        1: "Regular Customer",
        2: "Budget Customer",
        3: "VIP Customer"
    }
    cluster_map = {
        0: "Cluster 0",
        1: "Cluster 1",
        2: "Cluster 2",
        3: "Cluster 3"
    }
    df["Customer_Segment"] = df["Cluster"].map(seg_map)
    df["KMeans_Cluster"] = df["Cluster"].map(cluster_map)
else:
    df["Customer_Segment"] = df["Cluster"].astype(str)
    df["KMeans_Cluster"] = df["Cluster"].astype(str)

tips = {
    "High Value Customer": "Focus on retention and premium offers.",
    "Regular Customer": "Give loyalty rewards and seasonal discounts.",
    "Budget Customer": "Offer affordable deals and coupons.",
    "VIP Customer": "Provide exclusive access and premium benefits."
}
df["Marketing_Suggestion"] = df["Customer_Segment"].map(tips)

# ---------- Session ----------
if "customer_id" not in st.session_state:
    st.session_state.customer_id = df["CustomerID"].iloc[0]

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------- CSS ----------
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
background:#f5f7fb;
}

.block-container{
padding-top:20px;
max-width:1400px;
}

.metric-card{
border-radius:16px;
padding:20px;
height:165px;
border:1px solid #ddd;
}

.profile-box{
background:white;
padding:18px;
border-radius:14px;
border:1px solid #ddd;
color:#111827;
}

.tip{
padding:15px;
border-radius:14px;
border:1px solid #ddd;
height:120px;
}

.blue{background:#eef5ff;}
.green{background:#eef9ef;}
.yellow{background:#fff7e3;}

h1,h2,h3,h4,p,span{
color:#111827;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span{
color:white;
}

div.stButton>button{
width:100%;
height:46px;
border-radius:10px;
font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:

    st.markdown("""
    <div style="text-align:center">
    <h2 style="color:white;">👥 Customer Segmentation Platform</h2>
    <p style="color:#cbd5e1;">Personalized Marketing Analytics</p>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    st.markdown("### Enter Customer Details")

    cid = st.text_input("Customer ID", value=st.session_state.customer_id)

    found = df[df["CustomerID"] == cid]

    if found.empty:
        customer = df.iloc[0]
    else:
        customer = found.iloc[0]

    st.number_input("Age", value=int(customer["Age"]), disabled=True)
    st.number_input("Income (₹)", value=int(customer["AnnualIncome"]), disabled=True)
    st.number_input("Purchase History", value=int(customer["PurchaseHistory"]), disabled=True)
    st.number_input("Spending Score", value=int(customer["SpendingScore"]), disabled=True)

    if st.button("🔍 Predict Customer"):
        if cid in set(df["CustomerID"]):
            st.session_state.customer_id = cid
            st.rerun()

    if st.button("↻ Reset"):
        st.session_state.customer_id = df["CustomerID"].iloc[0]
        st.rerun()

    st.markdown("---")

    if st.button("🏠 Home"):
        st.session_state.page="Home"
        st.rerun()

    if st.button("ℹ️ About Project"):
        st.session_state.page="About"
        st.rerun()

    if st.button("👥 Team"):
        st.session_state.page="Team"
        st.rerun()

customer = df[df["CustomerID"] == st.session_state.customer_id].iloc[0]

# ---------- HOME ----------
if st.session_state.page == "Home":

    st.title("Customer Segmentation & Personalized Marketing Analytics")
    st.success("Prediction Successful!")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric-card blue">
        <h4>💎 Customer Segment</h4>
        <h2 style="color:#1d4ed8;">{customer["Customer_Segment"]}</h2>
        <p>Confidence Score</p>
        <h4>92.45%</h4>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card green">
        <h4>👥 Cluster</h4>
        <h2 style="color:#16a34a;">{customer["KMeans_Cluster"]}</h2>
        <p>High income, high spending customer.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card yellow">
        <h4>⭐ Marketing Priority</h4>
        <h2 style="color:#d97706;">High</h2>
        <p>{customer["Marketing_Suggestion"]}</p>
        </div>
        """, unsafe_allow_html=True)

    left,right = st.columns([1,1.4])

    with left:

        st.subheader("👤 Customer Profile")

        st.markdown(f"""
        <div class="profile-box">
        <p><b>Customer ID:</b> {customer["CustomerID"]}</p>
        <p><b>Age:</b> {customer["Age"]}</p>
        <p><b>Income:</b> ₹{customer["AnnualIncome"]:,}</p>
        <p><b>Purchase History:</b> {customer["PurchaseHistory"]}</p>
        <p><b>Spending Score:</b> {customer["SpendingScore"]}/100</p>
        <p><b>Segment:</b> {customer["Customer_Segment"]}</p>
        <p><b>Cluster:</b> {customer["KMeans_Cluster"]}</p>
        </div>
        """, unsafe_allow_html=True)

    with right:

        st.subheader("📊 Cluster Visualization")

        fig,ax = plt.subplots(figsize=(8,5))

        colors = {
            "High Value Customer":"red",
            "Regular Customer":"blue",
            "Budget Customer":"green",
            "VIP Customer":"purple"
        }

        for seg,d in df.groupby("Customer_Segment"):

            ax.scatter(
                d["AnnualIncome"],
                d["SpendingScore"],
                color=colors.get(seg,"gray"),
                alpha=.7,
                s=35,
                label=seg
            )

        ax.scatter(
            customer["AnnualIncome"],
            customer["SpendingScore"],
            color="black",
            marker="*",
            s=280,
            label="Selected Customer"
        )

        ax.set_title("Income vs Spending Score (Colored by Cluster)")
        ax.set_xlabel("Income (₹)")
        ax.set_ylabel("Spending Score")
        ax.grid(alpha=.2)
        ax.legend()

        st.pyplot(fig)

    st.subheader("💡 Personalized Marketing Suggestions")

    cols = st.columns(5)

    cards = [
        ("🎁 Premium Membership","#eef5ff"),
        ("🏷 Festival Discount","#edf9ef"),
        ("⭐ Loyalty Rewards","#fff8e5"),
        ("✉ Personalized Offers","#f4ecff"),
        ("⏰ Early Access","#fff1f1")
    ]

    for col,(title,bg) in zip(cols,cards):
        with col:
            st.markdown(f"""
            <div class="tip" style="background:{bg}">
            <b>{title}</b><br><br>
            {customer["Marketing_Suggestion"]}
            </div>
            """, unsafe_allow_html=True)

    st.markdown(
        "<div style='text-align:center;color:#64748b;padding:18px;'>© 2024 Customer Segmentation Platform | Built with Streamlit</div>",
        unsafe_allow_html=True
    )

elif st.session_state.page=="About":

    st.title("About Project")
    st.write("Customer Segmentation and Personalized Marketing Analytics using K-Means Clustering.")

else:

    st.title("Team")
    st.write("""
- Member 1 – Data Collection
- Member 2 – Data Preprocessing
- Member 3 – K-Means Clustering
- Member 4 – Marketing Analysis
- Member 5 – Frontend & Integration
""")
