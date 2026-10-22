import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["figure.facecolor"]= "#0E1B2A"
plt.rcParams["axes.facecolor"] = "#0E1B2A"
plt.rcParams["text.color"] = "#E6EAF0"
plt.rcParams["axes.labelcolor"] = "#A9B7C6"
plt.rcParams["xtick.color"] = "#A9B7C6"
plt.rcParams["ytick.color"] = "#A9B7C6"
st.set_page_config(
    page_title="FinTrack",
    page_icon="💳",
    layout="wide"
)
st.markdown("""
<style>
.stApp{
    background-color: #0E1117;
}

h1 {
    color: #FFFFFF;
}
h2, h3 {
    color: #E6EAF0;
}
[data-testid="stMetric"] {
    background : linear-gradient(135deg, #0F1F3D, #111A2E);
    border: 1px solid rgba(59, 130, 246, 0.35);
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 0 20px rgba(37, 99, 235, 0.15);
    min-height: 120px
    }
[data-testid="sMetricLabel"] {color: #A9B7C6, font-size: 14px;}
[data-testid="sMetricvalue"] {color: #FFFFFF: font-size: 28px; font-weight: 700;}

.sidebar-brand {
    padding: 10px 8px 20px 8px;
}

.brand-icon {
    color: #3B82F6;
    font-size: 28px;
    font-weight: 900;
    display: inline-block;
    margin-right: 8px;
}

.brand-name {
    color: #FFFFFF;
    font-size: 24px;
    font-weight: 700;
    display: inline-block;
}

.brand-tagline {
    color: #7F91AA;
    font-size: 11px;
    line-height: 1.5;
    margin-top: 5px;
    margin-left: 2px;
}

.sidebar-section-title {
    color: #5F7390;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
    margin-top: 10px;
    margin-bottom: 8px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #071426 0%, #0B1930 100%);
    border-right: 1px solid rgba(59, 130, 246, 0.20);
}

[data-testid="stSidebarContent"] {
    padding: 1.2rem 1rem;
}

.dashboard-header {
    margin-bottom: 24px;
}

.dashboard-title {
    color: #FFFFFF;
    font-size: 32px;
    font-weight: 700;
    letter-spacing: -0.5px;
}

.dashboard-subtitle {
    color: #8FA3BF;
    font-size: 14px;
    margin-top: 6px;
}


</style>
""", unsafe_allow_html=True)


data = pd.read_csv("transactions.csv")

# Data quality checks
st.sidebar.markdown("---")
st.sidebar.subheader("Data Quality")

missing_values = data.isnull().sum().sum()
duplicate_ids = data["Transaction ID"].duplicated().sum()

st.sidebar.metric("Missing Values", int(missing_values))
st.sidebar.metric("Duplicate IDs", int(duplicate_ids))

data["Timestamp"] = pd.to_datetime(data["Timestamp"])
st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="brand-icon">▮▮</div>
        <div class="brand-name">FinTrack</div>
        <div class="brand-tagline">
            Smarter Transactions.<br>
            Safer Tomorrow.
        </div>
    </div>

    <div class="sidebar-section-title">
        DASHBOARD
    </div>
    """,
    unsafe_allow_html=True
)
payment_filter =  st.sidebar.selectbox("Payment Method Filter", ["All"] + list(data["Payment Method"].unique()))
location_filter = st.sidebar.selectbox(
    "Location Filter",
    ["All"] + list(data["Location"].unique())
)

if payment_filter == "All" and location_filter == "All":
    filtered_data = data

elif payment_filter != "All" and location_filter == "All":
    filtered_data = data[
        data["Payment Method"] == payment_filter
    ]

elif payment_filter == "All" and location_filter != "All":
    filtered_data = data[
        data["Location"] == location_filter
    ]

else:
    filtered_data = data[
        (data["Payment Method"] == payment_filter) &
        (data["Location"] == location_filter)
    ]

st.markdown(
    """
    <div class="dashboard-header">
        <div class="dashboard-title">Transaction Analytics</div>
        <div class="dashboard-subtitle">
            Monitor transaction activity and discover key patterns
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

col1 , col2, col3 = st.columns(3)
total_amount = filtered_data["Amount"].sum()
average_amount = filtered_data["Amount"].mean()

with col1 :
    st.metric("Total Transactions", len(filtered_data))
with col2:
    st.metric("Total Transaction Value", f"₹{total_amount:,.0f}")
with col3:
    st.metric("Average Transaction Amount", f"₹{average_amount:,.0f}")

#charts section...

col1, col2 = st.columns(2)
with col1:

    status_counts = filtered_data["Status"].value_counts()

    status_colors = {
        "Success": "#10B981",
        "Failed": "#EF4444",
        "Pending": "#F59E0B"
    }

    colors = [
        status_colors.get(status, "#22D3EE")
        for status in status_counts.index
    ]

    fig, ax = plt.subplots(figsize=(5, 4.5))

    wedges, _ = ax.pie(
        status_counts,
        startangle=90,
        colors=colors,
        wedgeprops={
            "width": 0.38,
            "edgecolor": "#0E1B2A",
            "linewidth": 3
        }
    )

    ax.set_title(
        "Transaction Status",
        fontsize=14,
        fontweight="bold",
        pad=15
    )

    legend_labels = [
        f"{status}  {count / status_counts.sum() * 100:.1f}%"
        for status, count in status_counts.items()
    ]

    ax.legend(
        wedges,
        legend_labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.02),
        ncol=3,
        frameon=False, fontsize = 9
    )

    ax.set_aspect("equal")

    st.pyplot(fig, use_container_width=True)

with col2:

    payment_method_counts = filtered_data["Payment Method"].value_counts()

    fig, ax = plt.subplots(figsize=(5, 4))

    bars = ax.bar(
        payment_method_counts.index,
        payment_method_counts.values,
        color="#3B82F6"
    )

    ax.set_title(
        "Payment Methods",
        fontsize=14,
        fontweight="bold",
        pad=15
    )

    ax.set_xlabel("")
    ax.set_ylabel("Transactions")

    ax.tick_params(axis="x", labelsize=9)
    ax.tick_params(axis="y", labelsize=9)

    plt.xticks(rotation=25, ha="right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    st.pyplot(fig, use_container_width=True)


amount_col, customer_col = st.columns(2)

with amount_col:

    amount_bins = [0, 5000, 20000, 60000, 150000]

    amount_ranges = pd.cut(
        filtered_data["Amount"],
        bins=amount_bins,
        labels=["Small", "Medium", "Large", "Unusual"]
    )

    amount_counts = amount_ranges.value_counts().sort_index()

    fig, ax = plt.subplots(figsize=(5, 3.5))

    ax.bar(
        amount_counts.index,
        amount_counts.values,
        color="#8B5CF6",
        width=0.6
    )

    ax.set_title(
        "Transaction Amount Ranges",
        fontsize=14,
        fontweight="bold",
        pad=12
    )

    ax.set_xlabel("")
    ax.set_ylabel("Transactions")

    ax.tick_params(axis="x", labelsize=9)
    ax.tick_params(axis="y", labelsize=9)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    amount_col.pyplot(fig, use_container_width=True)


with customer_col:

    customer_counts = filtered_data["Customer Type"].value_counts()

    fig, ax = plt.subplots(figsize=(5, 3.5))

    ax.bar(
        customer_counts.index,
        customer_counts.values,
        color="#22D3EE",
        width=0.6
    )

    ax.set_title(
        "Customer Type",
        fontsize=14,
        fontweight="bold",
        pad=12
    )

    ax.set_xlabel("")
    ax.set_ylabel("Transactions")

    ax.tick_params(axis="x", labelsize=9)
    ax.tick_params(axis="y", labelsize=9)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    customer_col.pyplot(fig, use_container_width=True)

#transaction activity over time.......


daily_transactions =  filtered_data.groupby(filtered_data["Timestamp"].dt.date).size()

st.subheader("Transaction Activity Over Time")

fig, ax = plt.subplots(figsize=(10,4))
ax.plot(daily_transactions.index, daily_transactions.values, color="#22D3EE", linewidth = 2)

ax.set_xlabel("")
ax.set_ylabel("Transactions")

ax.set_title("Transaction Over Time", fontsize=14, fontweight="bold", pad=12)
ax.tick_params(axis="x", labelrotation=45, labelsize=8)
ax.tick_params(axis="y", labelsize=9)
st.pyplot(fig, use_container_width=True)

#row 4 = merchants & locations..

merchant_col, location_col= st.columns(2)

with merchant_col:
    merchant_counts = (filtered_data["Merchant"].value_counts().head(5))
    fig, ax= plt.subplots(figsize = (5,3.5))
    ax.bar(merchant_counts.index, merchant_counts.values, color="#3B82F6", width=0.6)
    ax.set_title("Top Five Merchants", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("")
    ax.set_ylabel("Merchants")
    ax.tick_params(axis="x", labelsize=9)
    ax.tick_params(axis="y", labelsize=9)
    plt.xticks(rotation=25, ha="right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    merchant_col.pyplot(fig, use_container_width=True)

with location_col:
    location_counts = (filtered_data["Location"].value_counts().head(5))
    fig, ax = plt.subplots(figsize=(5,3.5))
    ax.bar(location_counts.index, location_counts.values, color="#8B5CF6", width=0.6)
    ax.set_title("Top Five Locations", fontsize=14, fontweight = "bold", pad = 12)
    ax.set_xlabel("")
    ax.set_ylabel("Transactions")
    
    ax.tick_params(axis="x", labelsize=9)
    ax.tick_params(axis="y", labelsize=9)

    plt.xticks(rotation=25, ha="right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    location_col.pyplot(fig, use_container_width=True)

st.subheader("Potentially Unusual Transactions")


st.subheader("Quick Insights")

total_count = len(filtered_data)

if total_count > 0:
    success_count = (filtered_data["Status"] == "Success").sum()
    failed_count = (filtered_data["Status"] == "Failed").sum()
    unusual_count = (filtered_data["Amount"] > 60000).sum()

    success_rate = success_count / total_count * 100
    failure_rate = failed_count / total_count * 100

    insight1, insight2, insight3 = st.columns(3)

    insight1.metric(
        "Success Rate",
        f"{success_rate:.1f}%"
    )

    insight2.metric(
        "Failed Transactions",
        f"{failed_count}",
        f"{failure_rate:.1f}% of filtered transactions"
    )

    insight3.metric(
        "Flagged Transactions",
        f"{unusual_count}"
    )
else:
    st.info("No transactions match the selected filters.")

unusual_transactions = filtered_data[filtered_data["Amount"]>60000]
st.write("transactions above 60000 are flagged for further review.")
st.dataframe(unusual_transactions)


