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
#MainMenu{visibility:hidden;}footer{visibility:hidden;}header{visibility:hidden;}
[data-testid="stAppViewContainer"]{background:#f6f8fc;}
[data-testid="stSidebar"]{background:#081733;min-width:310px;max-width:310px;}
.block-container{max-width:1400px;padding-top:1.2rem;}
h1,h2,h3{color:#111827!important;}
.metric{padding:20px;border-radius:15px;border:1px solid #ddd;height:150px;}
.blue{background:#eef5ff;}.green{background:#edf9f1;}.yellow{background:#fff8e8;}
.profile{background:white;border:1px solid #ddd;border-radius:15px;padding:16px;color:#111827!important;}
.tip{padding:14px;border-radius:12px;border:1px solid #ddd;height:120px;}
div.stButton>button{width:100%;height:46px;border-radius:10px;font-weight:700;}
</style>
""",unsafe_allow_html=True)

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
    if st.session_state.page == "Home":

    customer = df[df["CustomerID"] == st.session_state.customer_id].iloc[0]

    st.title("Customer Segmentation & Personalized Marketing Analytics")
    st.success("Prediction Successful!")

    # Top Cards
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="metric blue">
                <h4>💎 Customer Segment</h4>
                <h2>{customer["Customer_Segment"]}</h2>
                <b>{customer["SpendingScore"]}/100</b>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric green">
                <h4>👥 Cluster</h4>
                <h2>{customer["KMeans_Cluster"]}</h2>
                <p>{customer["Customer_Segment"]} Customer</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric yellow">
                <h4>⭐ Marketing Priority</h4>
                <h2>High</h2>
                <p>{customer["Marketing_Suggestion"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    left, right = st.columns([1, 1.4])

    with left:
        st.subheader("👤 Customer Profile")
        st.markdown(
            f"""
            <div class="profile">
                <p><b>Customer ID:</b> {customer["CustomerID"]}</p>
                <p><b>Age:</b> {customer["Age"]} Years</p>
                <p><b>Income:</b> ₹{customer["AnnualIncome"]:,}</p>
                <p><b>Purchase History:</b> {customer["PurchaseHistory"]}</p>
                <p><b>Spending Score:</b> {customer["SpendingScore"]}/100</p>
                <p><b>Segment:</b> {customer["Customer_Segment"]}</p>
                <p><b>Cluster:</b> {customer["KMeans_Cluster"]}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.subheader("📊 Cluster Visualization")

        fig, ax = plt.subplots(figsize=(7, 5))

        colors = {
            "Budget": "red",
            "Regular": "green",
            "Premium": "blue",
            "VIP": "purple",
        }

        for seg, d in df.groupby("Customer_Segment"):
            ax.scatter(
                d["AnnualIncome"],
                d["SpendingScore"],
                color=colors.get(seg, "gray"),
                label=f"Cluster {seg}",
                alpha=0.7,
                s=35,
            )

        ax.scatter(
            customer["AnnualIncome"],
            customer["SpendingScore"],
            marker="*",
            s=260,
            color="black",
            label="Selected Customer",
        )

        ax.set_xlabel("Income (₹)")
        ax.set_ylabel("Spending Score")
        ax.grid(alpha=0.2)
        ax.legend()

        st.pyplot(fig)

    st.subheader("💡 Personalized Marketing Suggestions")

    cols = st.columns(5)

    cards = [
        ("🎁 Premium Membership", "#eef5ff"),
        ("🏷 Festival Discount", "#edf9f1"),
        ("⭐ Loyalty Rewards", "#fff8e8"),
        ("✉ Personalized Offers", "#f6efff"),
        ("⏰ Early Access", "#fff0f0"),
    ]

    for col, (title, bg) in zip(cols, cards):
        with col:
            st.markdown(
                f"""
                <div class="tip" style="background:{bg}">
                    <b>{title}</b>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        "<div style='text-align:center;color:#64748b;padding:18px;'>© 2024 Customer Segmentation Platform | Built with Streamlit</div>",
        unsafe_allow_html=True,
    )

elif st.session_state.page == "About":

    st.title("About Project")
    st.write(
        "Customer Segmentation and Personalized Marketing Analytics using Income, Purchase History, Spending Score and K-Means Clustering."
    )

else:

    st.title("Team")
    st.write(
        "- Member 1 – Data Collection\n"
        "- Member 2 – Data Preprocessing\n"
        "- Member 3 – K-Means Clustering\n"
        "- Member 4 – Marketing Analysis\n"
        "- Member 5 – Frontend & Integration"
    )
