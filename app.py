import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Customer Segmentation Platform", page_icon="👥", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data():
    return pd.read_excel("Customer_Segmentation_200_Rows.xlsx")

df = load_data()
df.columns = df.columns.str.strip()

# normalize columns
rename = {}
for c in df.columns:
    t=c.lower().replace(" ","")
    if t=="customerid": rename[c]="CustomerID"
    elif t=="annualincome": rename[c]="AnnualIncome"
    elif t=="purchasehistory": rename[c]="PurchaseHistory"
    elif t=="spendingscore": rename[c]="SpendingScore"
    elif t=="cluster": rename[c]="Cluster"
df.rename(columns=rename,inplace=True)
df["CustomerID"]=df["CustomerID"].astype(str)

# segment mapping
if "Customer_Segment" not in df.columns:
    if df["Cluster"].dtype==object:
        df["Customer_Segment"]=df["Cluster"]
    else:
        mp={0:"Budget",1:"Regular",2:"Premium",3:"VIP"}
        df["Customer_Segment"]=df["Cluster"].map(mp)
if "KMeans_Cluster" not in df.columns:
    df["KMeans_Cluster"]=df["Customer_Segment"]

tips={
"Budget":"Offer discount coupons and budget-friendly deals.",
"Regular":"Provide loyalty rewards and seasonal offers.",
"Premium":"Offer premium membership with exclusive benefits.",
"VIP":"Give exclusive early access and VIP services."
}
df["Marketing_Suggestion"]=df["Customer_Segment"].map(tips).fillna("Focus on retention and personalized offers.")

if "customer_id" not in st.session_state:
    st.session_state.customer_id=df["CustomerID"].iloc[0]
if "page" not in st.session_state:
    st.session_state.page="Home"

st.markdown("""
<style>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

[data-testid="stAppViewContainer"]{
    background:#F7F9FC;
}

[data-testid="stSidebar"]{
    background:#0F1D3B;
}

.block-container{
    max-width:1400px;
    padding-top:1.5rem;
}

h1,h2,h3,h4,p,span,label{
    color:#111827 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label{
    color:white !important;
}

.metric{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:14px;
    padding:20px;
    color:#111827 !important;
}

.profile{
    background:white;
    border:1px solid #E5E7EB;
    border-radius:14px;
    padding:18px;
    color:#111827 !important;
}

.tip{
    border-radius:12px;
    padding:14px;
    color:#111827 !important;
}

div.stButton > button{
    width:100%;
    height:46px;
    border-radius:10px;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

customer=df[df["CustomerID"]==st.session_state.customer_id].iloc[0]

with st.sidebar:
    st.markdown("<div style='text-align:center;color:white'><h2>👥 Customer Segmentation Platform</h2><p>Personalized Marketing Analytics</p></div><hr>",unsafe_allow_html=True)
    st.markdown("### Enter Customer Details")
    cid=st.text_input("Customer ID",value=st.session_state.customer_id)
    f=df[df["CustomerID"]==cid]
    p=f.iloc[0] if not f.empty else customer
    st.number_input("Age",value=int(p["Age"]),disabled=True)
    st.number_input("Income (₹)",value=int(p["AnnualIncome"]),disabled=True)
    st.number_input("Purchase History",value=int(p["PurchaseHistory"]),disabled=True)
    st.number_input("Spending Score",value=int(p["SpendingScore"]),disabled=True)
    if st.button("🔍 Predict Customer"):
        if cid in set(df["CustomerID"]):
            st.session_state.customer_id=cid
            st.rerun()
    if st.button("↻ Reset"):
        st.session_state.customer_id=df["CustomerID"].iloc[0]
        st.rerun()
    st.markdown("---")
    if st.button("🏠 Home"):
        st.session_state.page="Home"; st.rerun()
    if st.button("ℹ️ About Project"):
        st.session_state.page="About"; st.rerun()
    if st.button("👥 Team"):
        st.session_state.page="Team"; st.rerun()

if st.session_state.page=="Home":
    customer=df[df["CustomerID"]==st.session_state.customer_id].iloc[0]
    st.title("Customer Segmentation & Personalized Marketing Analytics")
    st.success("Prediction Successful!")
    c1,c2,c3=st.columns(3)
    with c1:
        st.markdown(f"<div class='metric blue'><h4>💎 Customer Segment</h4><h2>{customer['Customer_Segment']}</h2><b>{customer['SpendingScore']}/100</b></div>",unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric green'><h4>👥 Cluster</h4><h2>{customer['KMeans_Cluster']}</h2><p>{customer['Customer_Segment']} Customer</p></div>",unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric yellow'><h4>⭐ Marketing Priority</h4><h2>High</h2><p>{customer['Marketing_Suggestion']}</p></div>",unsafe_allow_html=True)
    left,right=st.columns([1,1.4])
    with left:
        st.subheader("👤 Customer Profile")
        st.markdown(f"""<div class='profile'>
        <p><b>Customer ID:</b> {customer['CustomerID']}</p>
        <p><b>Age:</b> {customer['Age']} Years</p>
        <p><b>Income:</b> ₹{customer['AnnualIncome']:,}</p>
        <p><b>Purchase History:</b> {customer['PurchaseHistory']}</p>
        <p><b>Spending Score:</b> {customer['SpendingScore']}/100</p>
        <p><b>Segment:</b> {customer['Customer_Segment']}</p>
        <p><b>Cluster:</b> {customer['KMeans_Cluster']}</p>
        </div>""",unsafe_allow_html=True)
    with right:
        st.subheader("📊 Cluster Visualization")
        fig,ax=plt.subplots(figsize=(7,5))
        colors={"Budget":"red","Regular":"green","Premium":"blue","VIP":"purple"}
        for s,d in df.groupby("Customer_Segment"):
            ax.scatter(d["AnnualIncome"],d["SpendingScore"],label=f"Cluster {s}",color=colors.get(str(s),"gray"),alpha=.7,s=35)
        ax.scatter(customer["AnnualIncome"],customer["SpendingScore"],marker="*",s=260,color="black",label="Selected Customer")
        ax.set_xlabel("Income (₹)"); ax.set_ylabel("Spending Score"); ax.grid(alpha=.2); ax.legend()
        st.pyplot(fig)
    st.subheader("📊 Cluster Visualization")

fig, ax = plt.subplots(figsize=(8,5))

colors = {
    "Budget":"red",
    "Regular":"green",
    "Premium":"blue",
    "VIP":"purple"
}

for seg in ["Budget","Regular","Premium","VIP"]:
    d = df[df["Customer_Segment"] == seg]
    if not d.empty:
        ax.scatter(
            d["AnnualIncome"],
            d["SpendingScore"],
            color=colors[seg],
            alpha=0.7,
            s=40,
            label=seg
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
plt.close(fig)
