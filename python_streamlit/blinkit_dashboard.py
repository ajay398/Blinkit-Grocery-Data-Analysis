import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="🛒 Blinkit Grocery Dashboard", layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("BlinkIT Grocery Data.csv")

df = load_data()

st.title("🛒 Blinkit Grocery Sales Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters")
category_filter = st.sidebar.multiselect("Select Item Categories", df['Item Type'].unique(), default=df['Item Type'].unique())
filtered_df = df[df['Item Type'].isin(category_filter)]

# --- Show Raw Data ---
with st.expander("📄 Show Raw Data"):
    st.dataframe(filtered_df.head())

# --- Overview Metrics ---
st.subheader("📊 Dataset Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Rows", df.shape[0])
col2.metric("Total Columns", df.shape[1])
col3.metric("Total Sales", f"{df['Sales'].sum():,.0f}")

# --- Tabs for Charts ---
tab1, tab2, tab3, tab4 = st.tabs(["📌 Summary Charts", "📈 Time Trends", "📍 Location Insights", "📦 Product Insights"])

with tab1:
    st.markdown("### Sales by Category")
    if 'Category' in df.columns and 'Sales' in df.columns:
        category_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
        st.bar_chart(category_sales)

    st.markdown("### Sales by Outlet Size")
    if 'Outlet Size' in df.columns and 'Sales' in df.columns:
        outlet_sales = df.groupby('Outlet Size')['Sales'].sum()
        fig, ax = plt.subplots()
        ax.pie(outlet_sales, labels=outlet_sales.index, autopct='%.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

    st.markdown("### Sales by Item Fat Content")
    if 'Item Fat Content' in df.columns and 'Sales' in df.columns:
        fat_sales = df.groupby('Item Fat Content')['Sales'].sum()
        fig, ax = plt.subplots()
        ax.pie(fat_sales, labels=fat_sales.index, autopct='%.1f%%', startangle=90, colors=['#6A5ACD','#FFD700','#FF7F50'])
        ax.axis('equal')
        st.pyplot(fig)

with tab2:
    st.markdown("### Sales Over Years")
    if 'Outlet Establishment Year' in df.columns:
        yearly_sales = df.groupby('Outlet Establishment Year')['Sales'].sum()
        fig, ax = plt.subplots()
        ax.plot(yearly_sales.index, yearly_sales.values, marker='o', linestyle='-', color='purple')
        for x, y in zip(yearly_sales.index, yearly_sales.values):
            ax.text(x, y, f'{y:,.0f}', ha='center', va='bottom', fontsize=8)
        ax.set_xlabel("Year")
        ax.set_ylabel("Sales")
        ax.set_title("Total Sales by Year")
        st.pyplot(fig)

with tab3:
    st.markdown("### Sales by Outlet Location Type")
    location_sales = df.groupby('Outlet Location Type')['Sales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots()
    location_sales.plot(kind='bar', ax=ax, color='teal')
    ax.set_ylabel("Total Sales")
    ax.set_xlabel("Location Type")
    ax.set_title("Sales by Outlet Location Type")
    st.pyplot(fig)

    st.markdown("### Sales by Fat Content & Location")
    fat_by_loc = df.groupby(['Item Fat Content', 'Outlet Location Type'])['Sales'].sum().unstack()
    fig, ax = plt.subplots(figsize=(8,6))
    fat_by_loc.plot(kind='bar', stacked=True, ax=ax, colormap='Set2')
    ax.set_title("Sales by Fat Content and Location Type")
    ax.set_ylabel("Sales")
    for container in ax.containers:
        ax.bar_label(container, label_type='center', fontsize=8)
    st.pyplot(fig)

with tab4:
    st.markdown("### Total Sales by Item Type")
    item_type_sales = df.groupby('Item Type')['Sales'].sum().sort_values()
    fig, ax = plt.subplots(figsize=(10, 6))
    item_type_sales.plot(kind='barh', ax=ax, colormap='Dark2')
    for i in ax.patches:
        ax.text(i.get_width() + 100, i.get_y() + 0.3, f'{i.get_width():.0f}', fontsize=9)
    ax.set_xlabel("Total Sales")
    ax.set_title("Sales by Item Type")
    st.pyplot(fig)
