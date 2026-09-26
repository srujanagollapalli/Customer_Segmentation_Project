import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title="Customer Segmentation Platform",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- DATA ----------------
@st.cache_data
def load_data():
    return pd.read_excel("Customer_Segmentation_200_Rows.xlsx")

df = load_data()
df.columns = df.columns.str.strip()

rename_map = {}
for c in df.columns:
    t = c.lower().replace(" ", "")
    if t == "customerid":
        rename_map[c] = "CustomerID"
    elif t == "annualincome":
        rename_map[c] = "AnnualIncome"
    elif t == "purchasehistory":
        rename_map[c] = "PurchaseHistory"
    elif t == "spendingscore":
        rename_map[c] = "SpendingScore"
    elif t == "cluster":
        rename_map[c] = "Cluster"

df.rename(columns=rename_map, inplace=True)
df["CustomerID"] = df["CustomerID"].astype(str)

if "Customer_Segment" not in df.columns:
    seg_map = {0:"Budget",1:"Regular",2:"Premium",3:"VIP"}
    df["Customer_Segment"] = df["Cluster"].map(seg_map)

if "KMeans_Cluster" not in df.columns:
    df["KMeans_Cluster"] = df["Cluster"]

if "Marketing_Suggestion" not in df.columns:
    tips = {
        "Budget":"Offer discount coupons and budget-friendly deals.",
        "Regular":"Provide loyalty rewards and seasonal offers.",
        "Premium":"Offer premium membership and exclusive benefits.",
        "VIP":"Give early access and VIP services."
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

[data-testid="stAppViewContainer"]{
background:#f5f7fb;
}

[data-testid="stSidebar"]{
background:#081733;
min-width:310px;
max-width:310px;
}

.block-container{
padding-top:1.2rem;
max-width:1450px;
}

[data-testid="stSidebar"] label{
color:white !important;
font-weight:600;
font-size:16px;
}

[data-testid="stSidebar"] input{
font-size:16px;
}

div.stButton>button{
width:100%;
height:48px;
border-radius:10px;
font-size:16px;
font-weight:700;
}

.metric-card{
padding:20px;
border-radius:14px;
border:1px solid #dfe6ef;
min-height:170px;
}

.blue{background:#eef5ff;}
.green{background:#edf9f1;}
.yellow{background:#fff8e8;}

.profile-box{
background:white;
padding:16px;
border-radius:14px;
border:1px solid #e2e8f0;
}

.profile-row{
display:flex;
justify-content:space-between;
padding:10px 0;
border-bottom:1px solid #edf0f5;
font-size:15px;
}

.profile-row:last-child{
border-bottom:none;
}

.tip-card{
padding:14px;
border-radius:12px;
border:1px solid #dfe6ef;
min-height:120px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- CURRENT CUSTOMER ----------------
customer = df[df["CustomerID"]==st.session_state.customer_id].iloc[0]

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown("""
    <div style="text-align:center;padding:10px;">
    <div style="font-size:36px;">👥</div>
    <div style="color:white;font-size:26px;font-weight:800;">
    Customer Segmentation Platform
    </div>
    <div style="color:#cbd5e1;margin-top:8px;">
    Personalized Marketing Analytics
    </div>
    </div>
    <hr>
    """, unsafe_allow_html=True)

    st.markdown("### Enter Customer Details")

    cid = st.text_input("Customer ID", value=st.session_state.customer_id)

    found = df[df["CustomerID"]==cid]

    if not found.empty:
        preview = found.iloc[0]
    else:
        preview = customer

    st.number_input("Age", value=int(preview["Age"]), disabled=True)
    st.number_input("Income (₹)", value=int(preview["AnnualIncome"]), disabled=True)
    st.number_input("Purchase History", value=int(preview["PurchaseHistory"]), disabled=True)
    st.number_input("Spending Score", value=int(preview["SpendingScore"]), disabled=True)

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
if st.session_state.page == "Home":

    customer = df[df["CustomerID"] == st.session_state.customer_id].iloc[0]

    st.title("Customer Segmentation & Personalized Marketing Analytics")

    st.markdown("""
    <div style="background:#edf9f1;border:1px solid #c9efd9;
    padding:14px;border-radius:10px;color:#177245;
    font-weight:700;margin-bottom:18px;">
    ✅ Prediction Successful!
    </div>
    """, unsafe_allow_html=True)

    # ---------- TOP CARDS ----------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card blue">
        <div style="font-size:15px;font-weight:700;color:#475569;">
        💎 Customer Segment
        </div>
        <div style="font-size:34px;font-weight:800;color:#2456d8;margin-top:8px;">
        {customer["Customer_Segment"]}
        </div>

        <div style="margin-top:16px;color:#475569;">
        Spending Score
        </div>

        <div style="font-size:22px;font-weight:800;color:#2456d8;">
        {customer["SpendingScore"]}/100
        </div>

        <div style="height:8px;background:#dbe7ff;border-radius:20px;margin-top:10px;">
            <div style="width:{customer['SpendingScore']}%;height:8px;background:#2456d8;border-radius:20px;"></div>
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card green">
        <div style="font-size:15px;font-weight:700;color:#475569;">
        👥 Cluster
        </div>

        <div style="font-size:34px;font-weight:800;color:#15945b;margin-top:8px;">
        Cluster {customer["KMeans_Cluster"]}
        </div>

        <div style="margin-top:16px;color:#178555;font-size:15px;line-height:1.5;">
        Customer belongs to the
        {customer["Customer_Segment"]} segment.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card yellow">
        <div style="font-size:15px;font-weight:700;color:#475569;">
        ⭐ Marketing Priority
        </div>

        <div style="font-size:34px;font-weight:800;color:#d99416;margin-top:8px;">
        High
        </div>

        <div style="margin-top:16px;color:#5f4b22;font-size:15px;line-height:1.5;">
        {customer["Marketing_Suggestion"]}
        </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ---------- PROFILE + GRAPH ----------
    left, right = st.columns([1, 1.4])

    with left:

        st.subheader("👤 Customer Profile")

        st.markdown(f"""
        <div class="profile-box">

        <div class="profile-row"><span>Customer ID</span><b>{customer["CustomerID"]}</b></div>

        <div class="profile-row"><span>Age</span><b>{customer["Age"]} Years</b></div>

        <div class="profile-row"><span>Income</span><b>₹{customer["AnnualIncome"]:,}</b></div>

        <div class="profile-row"><span>Purchase History</span><b>{customer["PurchaseHistory"]}</b></div>

        <div class="profile-row"><span>Spending Score</span><b>{customer["SpendingScore"]}/100</b></div>

        <div class="profile-row"><span>Segment</span><b>{customer["Customer_Segment"]}</b></div>

        <div class="profile-row"><span>Cluster</span><b>{customer["KMeans_Cluster"]}</b></div>

        </div>
        """, unsafe_allow_html=True)

    with right:

        st.subheader("📊 Cluster Visualization")

        fig, ax = plt.subplots(figsize=(7,5))

        colors = {
            0:"#dc2626",
            1:"#16a34a",
            2:"#2563eb",
            3:"#9333ea"
        }

        for cl in sorted(df["KMeans_Cluster"].unique()):

            d = df[df["KMeans_Cluster"] == cl]

            ax.scatter(
                d["AnnualIncome"],
                d["SpendingScore"],
                color=colors.get(cl,"gray"),
                alpha=0.7,
                s=35,
                label=f"Cluster {cl}"
            )

        ax.scatter(
            customer["AnnualIncome"],
            customer["SpendingScore"],
            color="black",
            marker="*",
            s=280,
            label="Selected Customer"
        )

        ax.set_xlabel("Income (₹)")
        ax.set_ylabel("Spending Score")
        ax.grid(alpha=.2)
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

    st.markdown("<br>", unsafe_allow_html=True)
        # ---------- MARKETING CARDS ----------
    st.subheader("💡 Personalized Marketing Suggestions")

    m1, m2, m3, m4, m5 = st.columns(5)

    cards = [
        ("🎁 Premium Membership", "#eef5ff",
         "Offer premium membership with exclusive benefits."),

        ("🏷 Festival Discount", "#edf9f1",
         "Provide seasonal discounts and promotional deals."),

        ("⭐ Loyalty Rewards", "#fff8e8",
         "Reward repeat customers with loyalty points."),

        ("✉ Personalized Offers", "#f6efff",
         "Send personalized emails and SMS offers."),

        ("⏰ Early Access", "#fff0f0",
         "Give early access to new products.")
    ]

    for col, (title, bg, text) in zip([m1, m2, m3, m4, m5], cards):
        with col:
            st.markdown(f"""
            <div class="tip-card" style="background:{bg};">
            <div style="font-weight:700;font-size:16px;margin-bottom:10px;">
            {title}
            </div>
            <div style="font-size:14px;color:#475569;line-height:1.5;">
            {text}
            </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;
    color:#64748b;
    font-size:13px;
    padding:20px;
    border-top:1px solid #e2e8f0;">
    © 2024 Customer Segmentation Platform | Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

# ---------------- ABOUT PAGE ----------------
elif st.session_state.page == "About":

    st.title("ℹ️ About Project")

    st.subheader("Customer Segmentation & Personalized Marketing Analytics")

    st.write("""
    This project analyzes customer behavior using Income,
    Purchase History and Spending Score.

    Customers are grouped into Budget, Regular,
    Premium and VIP segments.

    Personalized marketing strategies are generated
    for every customer segment.
    """)

    st.subheader("🎯 Project Objectives")

    st.markdown("""
    - Analyze customer purchasing behavior
    - Identify valuable customer segments
    - Understand spending patterns
    - Improve customer retention
    - Generate personalized marketing recommendations
    """)

    st.subheader("🛠 Technologies Used")

    st.markdown("""
    - Python
    - Pandas
    - Matplotlib
    - Streamlit
    - K-Means Clustering
    """)

# ---------------- TEAM PAGE ----------------
elif st.session_state.page == "Team":

    st.title("👥 Project Team")

    st.info("Customer Segmentation & Personalized Marketing Project")

    st.markdown("""
    ### Team Members

    - Member 1 – Data Collection
    - Member 2 – Data Preprocessing
    - Member 3 – K-Means Clustering
    - Member 4 – Marketing Analysis
    - Member 5 – Frontend & Integration
    """)

    st.markdown("""
    ---
    Built for BCA Data Science Final Year Project.
    """)
