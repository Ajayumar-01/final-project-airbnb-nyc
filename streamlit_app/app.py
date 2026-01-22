import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

st.set_page_config(page_title="NYC Airbnb - 11 Visualizations", layout="wide")
plt.style.use('seaborn-v0_8-whitegrid')

@st.cache_data
def load_data():
    possible_paths = ['data/AB_NYC_2019.csv', '../data/AB_NYC_2019.csv']
    for path in possible_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            # Exact same cleaning as notebook
            df_clean = df[df['price'] > 0].copy()
            price_threshold = df_clean['price'].quantile(0.99)
            df_clean = df_clean[df_clean['price'] <= price_threshold]
            df_clean['last_review'] = pd.to_datetime(df_clean['last_review'], errors='coerce')
            df_clean['price_per_review'] = df_clean['price'] / (df_clean['number_of_reviews'] + 1)
            return df_clean
    st.error("Put AB_NYC_2019.csv in data/ folder")
    st.stop()

df = load_data()
st.success(f" Loaded {len(df):,} listings | Same data as notebook")

# Sidebar
st.sidebar.header("🔍 Filters")
price_range = st.sidebar.slider("Price ($)", 10, 800, (10, 300))
room_types = st.sidebar.multiselect("Room type", df['room_type'].unique(), default=df['room_type'].unique())
boroughs = st.sidebar.multiselect("Borough", df['neighbourhood_group'].unique(), default=df['neighbourhood_group'].unique())

filtered_df = df[(df['price'].between(*price_range)) & 
                 df['room_type'].isin(room_types) & 
                 df['neighbourhood_group'].isin(boroughs)]

# Title + metrics
st.title("🏠 NYC Airbnb Analysis - 11 Visualizations")
col1, col2, col3 = st.columns(3)
col1.metric("Listings", len(filtered_df))
col2.metric("Avg Price", f"${filtered_df['price'].mean():.0f}")
col3.metric("Median Price", f"${filtered_df['price'].median():.0f}")

st.markdown("---")

# 11 VISUALIZATIONS FROM YOUR NOTEBOOK (interactive!)
tab1, tab2, tab3 = st.tabs([" Price Analysis", " Location", "👥 Hosts & Types"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Q1: Price distribution
        fig1, ax1 = plt.subplots(figsize=(7,5))
        sns.histplot(filtered_df['price'], bins=30, kde=True, ax=ax1)
        ax1.set_title("Q1: Price Distribution")
        st.pyplot(fig1)
    
    with col2:
        # Q2: Price by room type
        fig2, ax2 = plt.subplots(figsize=(7,5))
        price_room = filtered_df.groupby('room_type')['price'].mean()
        sns.barplot(x=price_room.index, y=price_room.values, 
                    hue=price_room.index, palette='viridis', legend=False, ax=ax2)
        ax2.set_title("Q2: Avg Price by Room Type")
        st.pyplot(fig2)

    col3, col4 = st.columns(2)
    with col3:
        # Q4: Price by borough
        fig4, ax4 = plt.subplots(figsize=(7,5))
        price_borough = filtered_df.groupby('neighbourhood_group')['price'].median()
        sns.barplot(x=price_borough.index, y=price_borough.values,
                    hue=price_borough.index, palette='coolwarm', legend=False, ax=ax4)
        ax4.set_title("Q4: Median Price by Borough")
        st.pyplot(fig4)
    
    with col4:
        # Q8: Min nights vs price
        fig8, ax8 = plt.subplots(figsize=(7,5))
        short_stays = filtered_df[filtered_df['minimum_nights'] <= 30]
        sns.scatterplot(data=short_stays, x='minimum_nights', y='price', ax=ax8)
        ax8.set_title("Q8: Price vs Min Nights")
        st.pyplot(fig8)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # Q6: Availability
        fig6, ax6 = plt.subplots(figsize=(7,5))
        avail_borough = filtered_df.groupby('neighbourhood_group')['availability_365'].mean()
        sns.barplot(x=avail_borough.index, y=avail_borough.values,
                    hue=avail_borough.index, palette='plasma', legend=False, ax=ax6)
        ax6.set_title("Q6: Avg Availability by Borough")
        st.pyplot(fig6)
    
    with col2:
        # Q9: Room types by borough
        fig9, ax9 = plt.subplots(figsize=(7,5))
        ct = pd.crosstab(filtered_df['neighbourhood_group'], filtered_df['room_type'], normalize='index') * 100
        ct.plot(kind='bar', stacked=True, ax=ax9)
        ax9.set_title("Q9: Room Types by Borough (%)")
        ax9.legend(bbox_to_anchor=(1.05, 1))
        st.pyplot(fig9)

    # Q10: Top neighbourhoods
    fig10, (ax1, ax2) = plt.subplots(1, 2, figsize=(14,5))
    top_n = filtered_df['neighbourhood'].value_counts().head(6)
    sns.barplot(x=top_n.values, y=top_n.index, hue=top_n.index, palette='tab10', legend=False, ax=ax1)
    ax1.set_title("Q10: Top Neighbourhoods")
    
    top_df = filtered_df[filtered_df['neighbourhood'].isin(top_n.index)]
    price_top = top_df.groupby('neighbourhood')['price'].median()
    sns.barplot(x=price_top.index, y=price_top.values, hue=price_top.index, palette='tab10', legend=False, ax=ax2)
    ax2.set_title("Median Price - Top Neighbourhoods")
    st.pyplot(fig10)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        # Q5: Reviews vs price
        fig5, ax5 = plt.subplots(figsize=(7,5))
        reviews_cap = filtered_df[filtered_df['number_of_reviews'] <= 100]
        sns.scatterplot(data=reviews_cap, x='number_of_reviews', y='price', ax=ax5)
        ax5.set_title("Q5: Price vs Reviews")
        st.pyplot(fig5)
    
    with col2:
        # Q7: Top hosts
        fig7, ax7 = plt.subplots(figsize=(7,5))
        top_hosts = filtered_df['host_name'].value_counts().head(8)
        sns.barplot(x=top_hosts.values, y=top_hosts.index, 
                    hue=top_hosts.index, palette='plasma', legend=False, ax=ax7)
        ax7.set_title("Q7: Top Hosts")
        st.pyplot(fig7)

# Interactive bonus
st.header(" Interactive Charts")
col1, col2 = st.columns(2)

with col1:
    fig_scatter = px.scatter(filtered_df, x='number_of_reviews', y='price', 
                            color='neighbourhood_group', hover_data=['room_type', 'neighbourhood'],
                            title="Interactive: Price vs Reviews")
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    fig_map = px.scatter_mapbox(filtered_df.sample(2000), lat='latitude', lon='longitude',
                               color='price', hover_name='neighbourhood',
                               mapbox_style="carto-positron", zoom=10,
                               title="Map: Listings by Price")
    st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")
st.markdown("*Final Project | 11 notebook visualizations → interactive dashboard*")
