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
    else:
        st.error("Customer_Segmentation_200_Rows.xlsx file not found.")
        st.stop()

df = load_data()
df.columns = df.columns.str.strip()

# Column names normalize
rename_map = {}
for c in df.columns:
    low = c.lower().replace(" ", "")
    if low == "annualincome":
        rename_map[c] = "AnnualIncome"
    elif low == "purchasehistory":
        rename_map[c] = "PurchaseHistory"
    elif low == "spendingscore":
        rename_map[c] = "SpendingScore"
    elif low == "customerid":
        rename_map[c] = "CustomerID"
    elif low == "age":
        rename_map[c] = "Age"
    elif low == "cluster":
        rename_map[c] = "Cluster"

df.rename(columns=rename_map, inplace=True)

df["CustomerID"] = df["CustomerID"].astype(str)

# Create missing columns
if "Customer_Segment" not in df.columns:
    def make_segment(r):
        s = r["SpendingScore"]
        i = r["AnnualIncome"]
        if s >= 80 and i >= 100000:
            return "VIP"
        elif s >= 60:
            return "Premium"
        elif s >= 40:
            return "Regular"
        else:
            return "Budget"
    df["Customer_Segment"] = df.apply(make_segment, axis=1)

if "KMeans_Cluster" not in df.columns:
    mapping = {"Budget":0,"Regular":1,"Premium":2,"VIP":3}
    df["KMeans_Cluster"] = df["Customer_Segment"].map(mapping)

if "Marketing_Suggestion" not in df.columns:
    tips = {
        "Budget":"Offer discounts and coupons.",
        "Regular":"Provide loyalty rewards.",
        "Premium":"Offer premium membership.",
        "VIP":"Give exclusive early access."
    }
    df["Marketing_Suggestion"] = df["Customer_Segment"].map(tips)

# ---------------- SESSION ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "customer_id" not in st.session_state:
    st.session_state.customer_id = df["CustomerID"].iloc[0]

# ---------------- CSS ----------------
st.markdown("""
<style>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

[data-testid="stSidebar"]{
background:#0f1d3b;
}

[data-testid="stAppViewContainer"]{
background:#f8f9fb;
}

[data-testid="stSidebar"] label{
color:white !important;
font-weight:600;
}

div.stButton > button{
width:100%;
height:45px;
border-radius:10px;
font-weight:bold;
}

.card{
padding:18px;
border-radius:15px;
border:1px solid #ddd;
height:100%;
}

.blue{background:#eef5ff;}
.green{background:#eefbf4;}
.yellow{background:#fff8e8;}
</style>
""", unsafe_allow_html=True)

# ---------------- CUSTOMER ----------------
customer = df[df["CustomerID"] == st.session_state.customer_id].iloc[0]

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown("""
    <div style="text-align:center;padding:10px;">
    <h2 style="color:white;">👥 Customer Segmentation Platform</h2>
    <p style="color:#cbd5e1;">Personalized Marketing Analytics</p>
    </div>
    """, unsafe_allow_html=True)

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

# ---------------- HOME ----------------
if st.session_state.page=="Home":

    customer = df[df["CustomerID"]==st.session_state.customer_id].iloc[0]

    st.title("Customer Segmentation & Personalized Marketing Analytics")
    st.success("Prediction Successful!")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="card blue">
        <h4>💎 Customer Segment</h4>
        <h2 style="color:#2563eb;">{customer["Customer_Segment"]}</h2>
        <p>Spending Score</p>
        <b>{customer["SpendingScore"]}/100</b>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card green">
        <h4>👥 Cluster</h4>
        <h2 style="color:#15945b;">Cluster {customer["KMeans_Cluster"]}</h2>
        <p>High income & spending customers</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card yellow">
        <h4>⭐ Marketing Priority</h4>
        <h2 style="color:#d99416;">High</h2>
        <p>{customer["Marketing_Suggestion"]}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left,right = st.columns([1,1.4])

    with left:
        st.subheader("👤 Customer Profile")
        st.markdown(f"""
        <div style="background:white;padding:15px;border-radius:15px;border:1px solid #ddd;">
        <table width="100%">
        <tr><td><b>Customer ID</b></td><td>{customer["CustomerID"]}</td></tr>
        <tr><td><b>Age</b></td><td>{customer["Age"]} Years</td></tr>
        <tr><td><b>Income</b></td><td>₹{customer["AnnualIncome"]:,}</td></tr>
        <tr><td><b>Purchase History</b></td><td>{customer["PurchaseHistory"]}</td></tr>
        <tr><td><b>Spending Score</b></td><td>{customer["SpendingScore"]}/100</td></tr>
        <tr><td><b>Segment</b></td><td>{customer["Customer_Segment"]}</td></tr>
        <tr><td><b>Cluster</b></td><td>{customer["KMeans_Cluster"]}</td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.subheader("📊 Cluster Visualization")

        fig,ax = plt.subplots(figsize=(7,5))

        colors={0:"red",1:"green",2:"blue",3:"purple"}

        for c in sorted(df["KMeans_Cluster"].unique()):
            d=df[df["KMeans_Cluster"]==c]
            ax.scatter(
                d["AnnualIncome"],
                d["SpendingScore"],
                color=colors.get(c,"gray"),
                alpha=.7,
                s=30,
                label=f'Cluster {c}'
            )

        ax.scatter(
            customer["AnnualIncome"],
            customer["SpendingScore"],
            color="black",
            marker="*",
            s=260,
            label="Selected Customer"
        )

        ax.set_xlabel("Income (₹)")
        ax.set_ylabel("Spending Score")
        ax.grid(alpha=.2)
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("💡 Personalized Marketing Suggestions")

    m1,m2,m3,m4,m5 = st.columns(5)

    cards=[
        ("🎁 Premium Membership","#eef5ff","Offer premium membership with exclusive benefits."),
        ("🏷 Festival Discount","#edf9f1","Provide seasonal discounts."),
        ("⭐ Loyalty Rewards","#fff8e8","Reward repeat customers."),
        ("✉ Personalized Offers","#f6efff","Send personalized emails."),
        ("⏰ Early Access","#fff0f0","Give early access to products.")
    ]

    for col,(title,bg,text) in zip([m1,m2,m3,m4,m5],cards):
        with col:
            st.markdown(f"""
            <div style="background:{bg};padding:14px;border-radius:12px;border:1px solid #ddd;height:130px;">
            <b>{title}</b>
            <p>{text}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown(
        "<div style='text-align:center;color:gray;padding:20px;'>© 2024 Customer Segmentation Platform | Built with Streamlit</div>",
        unsafe_allow_html=True
    )

# ---------------- ABOUT ----------------
elif st.session_state.page=="About":

    st.title("About Project")

    st.write("""
This project groups customers into Budget, Regular, Premium and VIP segments
using Income, Purchase History and Spending Score.
""")

# ---------------- TEAM ----------------
elif st.session_state.page=="Team":

    st.title("Team")

    st.info("Add your team member names here.")
