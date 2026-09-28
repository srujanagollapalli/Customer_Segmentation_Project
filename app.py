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
    "Budget":"Cluster 0",
    "Regular":"Cluster 1",
    "Premium":"Cluster 2",
    "VIP":"Cluster 3"
}

df["KMeans_Cluster"] = df["Customer_Segment"].map(cluster_map)

tips = {
    "Budget":"Offer affordable deals and discount coupons.",
    "Regular":"Provide loyalty rewards and seasonal discounts.",
    "Premium":"Offer premium membership and exclusive benefits.",
    "VIP":"Give exclusive access and premium benefits."
}

df["Marketing_Suggestion"] = df["Customer_Segment"].map(tips)

if "customer_id" not in st.session_state:
    st.session_state.customer_id = df["CustomerID"].iloc[0]

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "predicted" not in st.session_state:
    st.session_state.predicted = False

st.markdown("""
<style>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}

[data-testid="stSidebar"]{
    background:#081733;
}

.metric{
    background:white;
    padding:18px;
    border-radius:16px;
    border:1px solid #E5E7EB;
}

.profile{
    background:white;
    padding:18px;
    border-radius:14px;
    border:1px solid #E5E7EB;
}

.tip{
    padding:15px;
    border-radius:12px;
    border:1px solid #E5E7EB;
}

div.stButton>button{
    width:100%;
    height:45px;
    border-radius:10px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:

    st.markdown("""
    <div style="text-align:center">
        <h2 style="color:white;">👥 Customer Segmentation Platform</h2>
        <p style="color:#CBD5E1;">Personalized Marketing Analytics</p>
    </div>
    <hr>
    """, unsafe_allow_html=True)

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

if st.session_state.page == "Home":

    st.title("Customer Segmentation & Personalized Marketing Analytics")

    if st.session_state.predicted:
        st.success("🎉 Prediction Successful! Customer details loaded successfully.")
        st.session_state.predicted = False

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="metric">
            <h4>💎 Customer Segment</h4>
            <h2>{customer["Customer_Segment"]}</h2>
            <p>Confidence: {customer["SpendingScore"]}%</p>
        </div>
        """, unsafe_allow_html=True)
        st.progress(int(customer["SpendingScore"])/100)

    with c2:
        st.markdown(f"""
        <div class="metric">
            <h4>👥 Cluster</h4>
            <h2>{customer["KMeans_Cluster"]}</h2>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric">
            <h4>⭐ Marketing Priority</h4>
            <h2>High</h2>
            <p>{customer["Marketing_Suggestion"]}</p>
        </div>
        """, unsafe_allow_html=True)

    left,right = st.columns([1,1.4])

    with left:
        st.subheader("👤 Customer Profile")
        st.markdown(f"""
        <div class="profile">
            <p><b>ID:</b> {customer["CustomerID"]}</p>
            <p><b>Age:</b> {customer["Age"]}</p>
            <p><b>Income:</b> ₹{customer["AnnualIncome"]:,}</p>
            <p><b>Purchase:</b> {customer["PurchaseHistory"]}</p>
            <p><b>Spending:</b> {customer["SpendingScore"]}/100</p>
            <p><b>Segment:</b> {customer["Customer_Segment"]}</p>
            <p><b>Cluster:</b> {customer["KMeans_Cluster"]}</p>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.subheader("📊 Cluster Visualization")

        fig,ax = plt.subplots(figsize=(8,5))

        colors = {
            "Budget":"red",
            "Regular":"green",
            "Premium":"blue",
            "VIP":"purple"
        }

        for seg,data in df.groupby("Customer_Segment"):
            ax.scatter(
                data["AnnualIncome"],
                data["SpendingScore"],
                color=colors.get(seg,"gray"),
                label=seg,
                s=35
            )

        ax.scatter(
            customer["AnnualIncome"],
            customer["SpendingScore"],
            marker="*",
            s=280,
            color="black",
            label="Selected Customer"
        )

        ax.legend()
        ax.grid(alpha=.2)
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

elif st.session_state.page=="About":
    st.title("About Project")
    st.write("Customer Segmentation and Personalized Marketing Analytics using K-Means Clustering.")

else:
    st.title("👥 Project Team")
    for item in [
        "Member 1 – Data Collection & Database",
        "Member 2 – Data Preprocessing & EDA",
        "Member 3 – K-Means Clustering",
        "Member 4 – Marketing Analysis",
        "Member 5 – Frontend & Integration"
    ]:
        st.write(item)
