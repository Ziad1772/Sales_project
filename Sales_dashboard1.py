import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

# ================= Page Mode =================
st.set_page_config(page_title= 'Sales Dashboard',
                    layout="wide",
                    page_icon= None,
                    initial_sidebar_state= 'expanded')

# loading data
df = pd.read_csv('Sales Dataset.csv')

# orange themes 
color_theme = ['#FFA500', '#FF8C00', '#FF7F50', '#FFB347']

# ================= CSS for Responsive =================
st.markdown("""
<style>
/* Responsive text sizes */
@media (max-width: 768px) {
    h2, h4 { font-size: 16px !important; }
    div[data-testid="stMetricValue"] { font-size: 18px !important; }
}
@media (min-width: 769px) {
    h2, h4 { font-size: 22px !important; }
    div[data-testid="stMetricValue"] { font-size: 26px !important; }
}

/* Sidebar style */
[data-testid="stSidebar"] {
    background-color: #FFA500;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ================= Sidebar =================
st.sidebar.markdown(
    """
    <h2 style='text-align: center; border-bottom: 5px solid red; padding-bottom: 5px;'>
        Sales Dashboard
    </h2>
    """,
    unsafe_allow_html=True
)
st.sidebar.write('')
st.sidebar.image("salee.jpg", use_container_width=True)
st.sidebar.write('')
st.sidebar.header('Filter your data : ')

# filters
Num_filter = st.sidebar.selectbox('Numerical : ', ['Amount', 'Profit', 'Quantity'])
Cat_filter = st.sidebar.selectbox('Categorical : ', ['Category', 'Sub-Category', 'State'])

# values filter
cat_values = st.sidebar.multiselect(f"Select {Cat_filter}:", df[Cat_filter].unique())
filtered_df = df.copy()
if cat_values:
    filtered_df = filtered_df[filtered_df[Cat_filter].isin(cat_values)]

st.sidebar.write('')
st.sidebar.markdown('Made with :heart_eyes: by Eng.[Ziad Essam](https://www.linkedin.com/in/ziad-essam-684680255/)')


# ================= Body =================
st.markdown(
    """
    <h2 style='text-align: center; border-bottom: 5px solid orange; padding-bottom: 5px;'>
        Sales Analyses
    </h2>
    """,
    unsafe_allow_html=True
)

st.dataframe(filtered_df.sample(6), use_container_width=True)

st.markdown(
    """
    <h2 style='border-top: 5px solid orange;'>
    </h2>
    """,
    unsafe_allow_html=True
)

# ================= Row A (KPIs) =================
a1, a2, a3 = st.columns([1,1,1])

# ----------
total = filtered_df[Num_filter].sum() 
a1.markdown(f"""
    <div style="
        background-color: #FFA500;
        padding: 20px;
        border-radius: 30px;
        text-align: center;
        color: white;
        font-family: Arial, sans-serif;
    ">
        <h4 style="margin: 0;">Total of {Num_filter}</h4>
        <h2 style="margin: 0;">{round(total)}</h2>
    </div>
""", unsafe_allow_html=True)

# -----------
count = filtered_df[Num_filter].count()
a2.markdown(f"""
    <div style="
        background-color: #FFA500;
        padding: 20px;
        border-radius: 30px;
        text-align: center;
        color: white;
        font-family: Arial, sans-serif;
    ">
        <h4 style="margin: 0;">Count of {Num_filter}</h4>
        <h2 style="margin: 0;">{round(count)}</h2>
    </div>
""", unsafe_allow_html=True)

# ----------
avg = filtered_df[Num_filter].mean()
a3.markdown(f"""
    <div style="
        background-color: #FFA500;
        padding: 20px;
        border-radius: 30px;
        text-align: center;
        color: white;
        font-family: Arial, sans-serif;
    ">
        <h4 style="margin: 0;">Avg of {Num_filter}</h4>
        <h2 style="margin: 0;">{round(avg)}</h2>
    </div>
""", unsafe_allow_html=True)


# ================= Row B =================
b1, b2 = st.columns([1,1])

# Pie (Category Distribution)
category_counts = filtered_df['Category'].value_counts().reset_index()
category_counts.columns = ['Category', 'Count']

fig1 = px.pie(
    data_frame=category_counts,
    names='Category',
    values='Count',
    title='Goods distribution by category',
    hole=0.6,
    color_discrete_sequence=color_theme
)
fig1.update_traces(textinfo='percent+label')
b1.plotly_chart(fig1, use_container_width=True)

# Bar (Profit by Category)
category_profit = (
    filtered_df.groupby('Category', as_index=False)['Profit']
    .sum()
    .sort_values(by='Profit', ascending=False)
)

fig2 = px.bar(
    data_frame=category_profit,
    x='Category',
    y='Profit',
    text='Profit',
    color='Category',
    color_discrete_sequence=color_theme
)
fig2.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig2.update_layout(yaxis_title="Total Profit", xaxis_title="Category")
b2.plotly_chart(fig2, use_container_width=True)


# ================= Row C =================
c1, c2 = st.columns([1,1])

# Line (Sales Trend)
sales_trend = filtered_df.groupby('Year-Month')['Amount'].sum().reset_index()
fig3 = px.line(
    sales_trend, x='Year-Month', y='Amount',
    title="Sales Trend Over Time",
    markers=True,
    color_discrete_sequence=color_theme
)
c1.plotly_chart(fig3, use_container_width=True)

# Scatter (Quantity vs Profit)
fig4 = px.scatter(
    filtered_df, x='Quantity', y='Profit',
    size='Amount', color='Category',
    title="Quantity vs Profit",
    color_discrete_sequence=color_theme
)
c2.plotly_chart(fig4, use_container_width=True)


# ================= Row D =================
st.markdown(
    """
    <h2 style='text-align: center; border-top: 3px solid orange; padding-top: 10px;'>
        Amount vs Profit (Detailed Scatter)
    </h2>
    """,
    unsafe_allow_html=True
)

fig5 = px.scatter(
    filtered_df,
    x='Amount',
    y='Profit',
    color='Category',
    size='Quantity',
    hover_data=['CustomerName', 'City'],
    color_discrete_sequence=color_theme,
    title="Amount vs Profit by Category"
)

st.plotly_chart(fig5)
