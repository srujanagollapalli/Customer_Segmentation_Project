import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Customer Segmentation Platform", page_icon="👥", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data():
    return pd.read_excel("Customer_Segmentation_200_Rows.xlsx")

df = load_data()
df.columns = df.columns.str.strip()

rename={}
for c in df.columns:
    k=c.lower().replace(" ","")
    if k=="customerid": rename[c]="CustomerID"
    elif k=="annualincome": rename[c]="AnnualIncome"
    elif k=="purchasehistory": rename[c]="PurchaseHistory"
    elif k=="spendingscore": rename[c]="SpendingScore"
    elif k=="cluster": rename[c]="Cluster"
df.rename(columns=rename,inplace=True)
df["CustomerID"]=df["CustomerID"].astype(str)

if df["Cluster"].dtype==object:
    df["Customer_Segment"]=df["Cluster"]
else:
    df["Customer_Segment"]=df["Cluster"].map({0:"Budget",1:"Regular",2:"Premium",3:"VIP"}).fillna("Regular")

df["KMeans_Cluster"]=df["Customer_Segment"]
tips={"Budget":"Offer discount coupons and budget-friendly deals.","Regular":"Provide loyalty rewards and seasonal offers.","Premium":"Offer premium membership with exclusive benefits.","VIP":"Give exclusive early access and VIP services."}
df["Marketing_Suggestion"]=df["Customer_Segment"].map(tips)

if "customer_id" not in st.session_state:
    st.session_state.customer_id=df["CustomerID"].iloc[0]
if "page" not in st.session_state:
    st.session_state.page="Home"

st.markdown("""
<style>
#MainMenu,footer,header{visibility:hidden;}
[data-testid="stAppViewContainer"]{background:#f6f8fc;}
[data-testid="stSidebar"]{background:#081733;}
h1,h2,h3{color:#111827!important;}
.card{padding:18px;border-radius:14px;border:1px solid #ddd;background:white}
</style>""",unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h2 style='color:white;text-align:center'>👥 Customer Segmentation Platform</h2>",unsafe_allow_html=True)
    cid=st.text_input("Customer ID",value=st.session_state.customer_id)
    r=df[df["CustomerID"]==cid]
    p=r.iloc[0] if not r.empty else df.iloc[0]
    st.number_input("Age",value=int(p["Age"]),disabled=True)
    st.number_input("Income (₹)",value=int(p["AnnualIncome"]),disabled=True)
    st.number_input("Purchase History",value=int(p["PurchaseHistory"]),disabled=True)
    st.number_input("Spending Score",value=int(p["SpendingScore"]),disabled=True)
    if st.button("🔍 Predict Customer") and not r.empty:
        st.session_state.customer_id=cid
        st.rerun()
    if st.button("↻ Reset"):
        st.session_state.customer_id=df["CustomerID"].iloc[0]
        st.rerun()
    st.markdown("---")
    if st.button("🏠 Home"): st.session_state.page="Home"; st.rerun()
    if st.button("ℹ️ About Project"): st.session_state.page="About"; st.rerun()
    if st.button("👥 Team"): st.session_state.page="Team"; st.rerun()

customer=df[df["CustomerID"]==st.session_state.customer_id].iloc[0]

if st.session_state.page=="Home":
    st.title("Customer Segmentation & Personalized Marketing Analytics")
    st.success("Prediction Successful!")
    c1,c2,c3=st.columns(3)
    with c1: st.metric("Customer Segment",customer["Customer_Segment"])
    with c2: st.metric("Cluster",customer["KMeans_Cluster"])
    with c3: st.metric("Spending Score",f"{customer['SpendingScore']}/100")
    l,r=st.columns([1,1.3])
    with l:
        st.subheader("Customer Profile")
        st.write(f"**Customer ID:** {customer['CustomerID']}")
        st.write(f"**Age:** {customer['Age']}")
        st.write(f"**Income:** ₹{customer['AnnualIncome']:,}")
        st.write(f"**Purchase History:** {customer['PurchaseHistory']}")
    with r:
        fig,ax=plt.subplots(figsize=(6,4))
        colors={"Budget":"red","Regular":"green","Premium":"blue","VIP":"purple"}
        for s,d in df.groupby("Customer_Segment"):
            ax.scatter(d["AnnualIncome"],d["SpendingScore"],label=s,color=colors.get(s,"gray"),alpha=.7)
        ax.scatter(customer["AnnualIncome"],customer["SpendingScore"],marker="*",s=250,color="black")
        ax.set_xlabel("Income"); ax.set_ylabel("Spending Score"); ax.legend()
        st.pyplot(fig)
elif st.session_state.page=="About":
    st.title("About Project")
    st.write("Customer Segmentation and Personalized Marketing Analytics project using K-Means Clustering.")
else:
    st.title("Team")
    st.write("- Member 1\n- Member 2\n- Member 3\n- Member 4\n- Member 5")
