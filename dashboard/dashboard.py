import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_orders_df(df):
    # revenue for canceled and unavailable purchases wouldn't be counted
    filtered_df = df[~df['order_status'].isin(['canceled', 'unavailable'])]
    daily_orders_df = filtered_df.resample(rule='D', on='order_purchase_timestamp').agg({
        "order_id": "nunique",
        "price": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "price": "revenue"
    }, inplace=True)

    return daily_orders_df

def create_revenue_product_df(df):
    revenue_product_df = df[~df['order_status'].isin(['canceled', 'unavailable'])].groupby("product_category_name").price.sum().sort_values(ascending=False).reset_index()
    return revenue_product_df

def create_review_product_df(df):
    review_product_df = df[~df['order_status'].isin(['canceled', 'unavailable'])].groupby("product_category_name").review_score.mean().sort_values(ascending=False).reset_index()
    return review_product_df

def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    return bystate_df

def create_bypaymenttype_df(df):
    bypaytype_df = df.groupby(by="payment_type").agg({
        "customer_id": "nunique",
        "payment_installments": "mean"
    })
    bypaytype_df.rename(columns={
        "customer_id": "customer_count",
        "payment_installments": "avg_installments"
    }, inplace=True)
    bypaytype_df = bypaytype_df.reset_index()
    return bypaytype_df

def create_byinstallments_df(df):
    installments_df = df[df['payment_type'] == 'credit_card'].groupby('payment_installments')['order_id'].nunique().sort_values(ascending=False).reset_index()
    installments_df.columns = ['Installments', 'Customer Count']
    return installments_df

def create_bystatus_df(df):
    bystatus_df = df.groupby(by="order_status").customer_id.nunique().reset_index()
    bystatus_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    return bystatus_df

def create_bydeltime_df(df):
    delivery_time_order = ['1-7 days', '8-14 days', '15-21 days', '21+ days']

    bydeltime_df = df["delivery_time_range"].value_counts().reindex(delivery_time_order).reset_index()
    bydeltime_df.columns = ["Delivery Time Range", "Order Count"]
    return bydeltime_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_purchase_timestamp": "max",
        "order_id": "nunique",
        "price": "sum"
    })
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]

    rfm_df['customer_id'] = range(1, len(rfm_df) + 1)

    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = df["order_purchase_timestamp"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

    return rfm_df

ecom_df = pd.read_csv("ecommerce-data-analysis/dashboard/ecommerce_data.csv.gz")

datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
ecom_df.sort_values(by="order_purchase_timestamp", inplace=True)
ecom_df.reset_index(inplace=True)

for column in datetime_columns:
    ecom_df[column] = pd.to_datetime(ecom_df[column])

# filter component
min_date = ecom_df["order_purchase_timestamp"].min()
max_date = ecom_df["order_purchase_timestamp"].max()

with st.sidebar:
    # add company logo
    st.image("ecommerce-data-analysis/dashboard/logo.png")

    # extract start_date and end_date from date_input
    start_date, end_date = st.date_input(
        label = 'Range Date',
        min_value = min_date,
        max_value = max_date,
        value=[min_date,max_date]
    )

main_df = ecom_df[(ecom_df["order_purchase_timestamp"]>=str(start_date)) & (ecom_df["order_purchase_timestamp"]<=str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
revenue_product_df = create_revenue_product_df(main_df)
review_product_df = create_review_product_df(main_df)
bystate_df = create_bystate_df(main_df)
bypaytype_df = create_bypaymenttype_df(main_df)
installments_df = create_byinstallments_df(main_df)
bystatus_df = create_bystatus_df(main_df)
bydeltime_df = create_bydeltime_df(main_df)
rfm_df = create_rfm_df(main_df)

# completing dashboard with data visualisation
st.header('E-Commerce Public Dashboard')

# daily orders
st.subheader('Daily Orders')
col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "USD", locale="en_US")
    st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16,8))
ax.plot(
    daily_orders_df["order_purchase_timestamp"],
    daily_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color='#90CAF9'
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20)
st.pyplot(fig)

# best and least performing products
st.subheader('Best-Performing and Least-Performing Products (Revenue)')

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="price", y="product_category_name", data=revenue_product_df.head(), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Revenue", fontsize=30)
ax[0].set_title("Best Performing Products", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="price", y="product_category_name", data=revenue_product_df.sort_values(by="price", ascending=True).head(), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Revenue", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Least Performing Products", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# best & worst reviewed product
st.subheader("Best and Worst Reviewed Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35,15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="review_score", y="product_category_name", data=review_product_df.head(), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Review Score", fontsize=30)
ax[0].set_title("Best Reviewed Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="review_score", y="product_category_name", data=review_product_df.sort_values(by="review_score", ascending=True).head(), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Review Score", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Reviewed Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# customer insights
st.subheader("Customer Insights")
 
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count", 
    y="customer_state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by States", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

col1, col2 = st.columns([1, 2])
 
with col1:
    fig, ax = plt.subplots(figsize=(12, 12))

    ax.pie(
        bypaytype_df["customer_count"],
        labels=bypaytype_df["payment_type"],
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("pastel"),
        textprops={'fontsize': 15} ,
        pctdistance=0.85
    )
    ax.set_title("Percentage of Customers by Payment Type", fontsize=35)
    st.pyplot(fig)
 
with col2:
    plt.figure(figsize=(12, 6))
    bars = plt.bar(installments_df["Installments"], installments_df["Customer Count"], color="skyblue")

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, str(int(height)), 
                ha='center', va='bottom', fontsize=10, color='black')
        
    plt.title("Number of Customers using Credit Card by Payment Installments", fontsize=15)
    plt.xlabel("Installments")
    plt.ylabel("Customer Count")
    st.pyplot(plt)

# RFM
st.subheader("Best Customer Based on RFM Parameters")
 
col1, col2, col3 = st.columns(3)
 
with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)
 
with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)
 
with col3:
    avg_monetary = format_currency(rfm_df.monetary.mean(), "USD", locale='en_US') 
    st.metric("Average Monetary", value=avg_monetary)
 
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]
 
sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)
 
sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)
 
st.pyplot(fig)

# delivery-related insights
st.subheader("Delivery Insights")

plt.figure(figsize=(12, 6))
bars = plt.bar(bystatus_df["order_status"], bystatus_df["customer_count"], color="skyblue")

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, str(int(height)), 
            ha='center', va='bottom', fontsize=10, color='black')

plt.title("Number of Orders based on Order Status")
plt.xlabel("Order Status")
plt.ylabel("Order Count")
plt.xticks(rotation=45)
st.pyplot(plt)

plt.figure(figsize=(12, 6))
plt.title('Delivery Time Spread of Delivered Orders')
bars = plt.bar(bydeltime_df['Delivery Time Range'], bydeltime_df['Order Count'], color='skyblue')

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, str(int(height)), 
            ha='center', va='bottom', fontsize=10, color='black')
    
plt.xlabel('Delivery Time Range')
plt.ylabel('Order Count')
plt.xticks(rotation=45)
st.pyplot(plt)
