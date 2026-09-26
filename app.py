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
    if os.path.exists("customer_segmentation_exact.csv"):
        return pd.read_csv("customer_segmentation_exact.csv")
    return pd.read_csv("data/customer_segmentation_exact.csv")

df = load_data()
df["CustomerID"] = df["CustomerID"].astype(str)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page="Home"

if "customer_id" not in st.session_state:
    st.session_state.customer_id=df["CustomerID"].iloc[0]

# ---------------- CSS ----------------
st.markdown("""
<style>

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

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

[data-testid="stSidebar"] button{
border-radius:10px;
}

div.stButton > button{
width:100%;
height:46px;
font-weight:700;
border-radius:10px;
border:none;
}

.predbtn button{
background:linear-gradient(90deg,#2563eb,#9333ea);
color:white;
}

.card{
background:white;
padding:18px;
border-radius:14px;
border:1px solid #e6e8ef;
height:100%;
}

.blue{
background:#eef5ff;
}

.green{
background:#eefbf4;
}

.yellow{
background:#fff8e8;
}

.feature{
padding:15px;
border-radius:12px;
border:1px solid #e3e5ec;
height:120px;
}

</style>
""",unsafe_allow_html=True)

# ---------------- SELECT CUSTOMER ----------------
row=df[df["CustomerID"]==str(st.session_state.customer_id)]

if row.empty:
    row=df.iloc[[0]]

customer=row.iloc[0]

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown("""
    <div style="text-align:center;padding:10px;">
    <div style="font-size:35px;">👥</div>
    <h2 style="color:white;margin:0;">Customer Segmentation Platform</h2>
    </div>
    <hr>
    """,unsafe_allow_html=True)

    st.markdown("### Enter Customer Details")

    cid=st.text_input("Customer ID",value=st.session_state.customer_id)

    found=df[df["CustomerID"]==cid.strip()]

    if not found.empty:
        preview=found.iloc[0]
    else:
        preview=customer

    st.number_input("Age",value=int(preview["Age"]),disabled=True)
    st.number_input("Income (₹)",value=int(preview["AnnualIncome"]),disabled=True)
    st.number_input("Purchase History",value=int(preview["PurchaseHistory"]),disabled=True)
    st.number_input("Spending Score",value=int(preview["SpendingScore"]),disabled=True)

    if st.button("🔍 Predict Customer"):
        if cid.strip() in set(df["CustomerID"]):
            st.session_state.customer_id=cid.strip()
            st.rerun()
        else:
            st.error("Customer ID not found")

    if st.button("↻ Reset"):
        st.session_state.customer_id=df["CustomerID"].iloc[0]
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

# ---------------- HOME ----------------
if st.session_state.page=="Home":

    st.title("Customer Segmentation & Personalized Marketing Analytics")

    st.success("Prediction Successful!")

    col1,col2,col3=st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card blue">
        <h4>💎 Customer Segment</h4>
        <h2 style="color:#2456d8;">{customer["Customer_Segment"]}</h2>
        <p>Spending Score</p>
        <h3>{customer["SpendingScore"]}/100</h3>
        </div>
        """,unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card green">
        <h4>👥 Cluster</h4>
        <h2 style="color:#15945b;">Cluster {customer["KMeans_Cluster"]}</h2>
        <p>High income & spending behaviour</p>
        </div>
        """,unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card yellow">
        <h4>⭐ Marketing Priority</h4>
        <h2 style="color:#d99416;">High</h2>
        <p>{customer["Marketing_Suggestion"]}</p>
        </div>
        """,unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    left,right=st.columns([1,1.3])

    with left:

        st.subheader("👤 Customer Profile")

        st.markdown(f"""
        <div class="card">
        <table width="100%">
        <tr><td><b>Customer ID</b></td><td>{customer["CustomerID"]}</td></tr>
        <tr><td><b>Age</b></td><td>{customer["Age"]} Years</td></tr>
        <tr><td><b>Income</b></td><td>₹{customer["AnnualIncome"]:,}</td></tr>
        <tr><td><b>Purchase History</b></td><td>{customer["PurchaseHistory"]} Purchases</td></tr>
        <tr><td><b>Spending Score</b></td><td>{customer["SpendingScore"]}/100</td></tr>
        <tr><td><b>Segment</b></td><td>{customer["Customer_Segment"]}</td></tr>
        <tr><td><b>Cluster</b></td><td>{customer["KMeans_Cluster"]}</td></tr>
        </table>
        </div>
        """,unsafe_allow_html=True)

    with right:

        st.subheader("📊 Cluster Visualization")

        fig,ax=plt.subplots(figsize=(7,5))

        colors=["red","blue","green","purple","orange"]

        clusters=sorted(df["KMeans_Cluster"].unique())

        for i,c in enumerate(clusters):
            d=df[df["KMeans_Cluster"]==c]
            ax.scatter(
                d["AnnualIncome"],
                d["SpendingScore"],
                label=f"Cluster {c}",
                alpha=.7,
                color=colors[i%len(colors)],
                s=22
            )

        ax.scatter(
            customer["AnnualIncome"],
            customer["SpendingScore"],
            marker="*",
            color="black",
            s=250,
            label=f'Customer ({customer["CustomerID"]})'
        )

        ax.set_xlabel("Income (₹)")
        ax.set_ylabel("Spending Score")
        ax.legend()
        ax.grid(alpha=.2)

        st.pyplot(fig)
        plt.close(fig)

    st.markdown("<br>",unsafe_allow_html=True)

    st.subheader("💡 Personalized Marketing Suggestions")

    c1,c2,c3,c4,c5=st.columns(5)

    with c1:
        st.markdown("""
        <div class="feature blue">
        <b>🎁 Premium Membership</b>
        <p>Offer premium membership with exclusive benefits.</p>
        </div>
        """,unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature green">
        <b>🏷 Festival Discount</b>
        <p>Offer seasonal discounts.</p>
        </div>
        """,unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="feature yellow">
        <b>⭐ Loyalty Rewards</b>
        <p>Reward repeat customers.</p>
        </div>
        """,unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="feature" style="background:#f6efff;">
        <b>✉ Personalized Offers</b>
        <p>Send personalized emails.</p>
        </div>
        """,unsafe_allow_html=True)

    with c5:
        st.markdown("""
        <div class="feature" style="background:#fff0f0;">
        <b>⏰ Early Access</b>
        <p>Give early access to products.</p>
        </div>
        """,unsafe_allow_html=True)

    st.markdown("<br>",unsafe_allow_html=True)

    st.markdown(
        '<div style="text-align:center;color:gray;padding:20px;">© 2024 Customer Segmentation Platform | Built with Streamlit</div>',
        unsafe_allow_html=True
    )

# ---------------- ABOUT ----------------
elif st.session_state.page=="About":

    st.title("About Project")

    st.write("""
    Customer Segmentation & Personalized Marketing Analytics

    This project analyzes customer behaviour using K-Means Clustering.
    It groups customers based on Income, Purchase History and Spending Score.
    """)

    st.subheader("Technologies")

    st.write("""
    - Python
    - Pandas
    - Matplotlib
    - Streamlit
    - K-Means Clustering
    """)

# ---------------- TEAM ----------------
elif st.session_state.page=="Team":

    st.title("Team")

    st.info("Add your team member names here.")
