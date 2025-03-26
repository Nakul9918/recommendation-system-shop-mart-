import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from collections import Counter
import plotly.express as px

# Load data
df = pd.read_csv('DMart.csv')
df_purchases = pd.read_csv('Purchases.csv')  # Purchase history

# Data Cleaning & Preprocessing
df['Name'] = df['Name'].fillna('Kitchen Appliance')
df['Brand'] = df['Brand'].fillna('Local/Unknown')
df['Category'] = df['Category'].fillna('Home & Kitchen')
df['SubCategory'] = df['SubCategory'].fillna('Home Appliances')
df['Price'] = df['Price'].fillna(0)

# GST Calculation
gst_rate = 18
df['GST_Amount'] = df['Price'] * (gst_rate / 100)
df['Final_Price_After_GST'] = df['Price'] + df['GST_Amount']

# Function to get top trending products
def get_top_trending_products(df_purchases, top_n=5):
    """Returns the top N trending products based on total sales."""
    product_counts = Counter(df_purchases["Product Name"])
    return product_counts.most_common(top_n)

# 🔥 **MOVE TRENDING PRODUCTS SECTION TO THE TOP**
st.subheader("🔥 Top Trending Products")
with st.container():
    trending_products = get_top_trending_products(df_purchases)

    if trending_products:
        trending_df = pd.DataFrame(trending_products, columns=['Product', 'Sales'])

        # Create an interactive bar chart using Plotly
        fig = px.bar(
            trending_df,
            x=trending_df.index,  # Use index instead of product names
            y="Sales",
            title="Top Trending Products",
            labels={"Sales": "Sales Count"},
            text="Sales",  # Display sales count on bars
            hover_data={"Product": True, "Sales": True},  # Tooltip on hover
            color="Sales",
            color_continuous_scale="reds"
        )

        fig.update_traces(textposition="outside")  # Move text outside bars

        fig.update_layout(
            xaxis=dict(
                showticklabels=False,  # Hide product names below bars
                title=None
            ),
            yaxis=dict(title="Sales Count")
        )

        # Display interactive Plotly chart
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.write("No trending products found.")
# Initialize session cart
if "cart" not in st.session_state:
    st.session_state.cart = {}

# Display available categories
categories = df["Category"].dropna().unique()
selected_category = st.selectbox("Select a category", categories)

# Show available products in the selected category
category_products = df[df["Category"] == selected_category][["Name", "Final_Price_After_GST"]].dropna()
selected_product = st.selectbox(f"Products in '{selected_category}'", category_products["Name"].unique())

# Function to add products to cart
# Function to add products to cart without showing messages
def add_to_cart(product_name):
    product_price = df[df["Name"] == product_name]["Final_Price_After_GST"].values[0]
    
    if product_name in st.session_state.cart:
        st.session_state.cart[product_name]["Quantity"] += 1
    else:
        st.session_state.cart[product_name] = {"Quantity": 1, "Price": product_price}
    
    # Remove success message (no st.success or st.write)


# Add selected product to cart
if st.button("🛒 Add Selected Product to Cart"):
    add_to_cart(selected_product)

# Function to predict related products with sales count
def predict_related_products(selected_product, selected_category, df_purchases):
    """Predicts top 5 related products based on past purchases in the same category with sales count."""
    category_purchases = df_purchases[df_purchases["Category"] == selected_category]
    
    if category_purchases.empty:
        return []
    
    product_counts = Counter(category_purchases["Product Name"])
    product_counts.pop(selected_product, None)  # Remove selected product

    return [(product, count) for product, count in product_counts.most_common(5)]

# 🚀 **Show Recommendations After Trending Section**
related_products = predict_related_products(selected_product, selected_category, df_purchases)

st.subheader(f"📌 Recommended Products for '{selected_product}'")
if related_products:
    for product, count in related_products:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{product}** (Sold {count} times)")
        with col2:
            if st.button("🛒", key=product):  # Only the cart icon
                add_to_cart(product)
else:
    st.write("No related products found.")

# 🚀 **Cart Section**
st.subheader("🛒 Your Cart")
if st.session_state.cart:
    cart_df = pd.DataFrame([
        {"Product": prod, "Quantity": details["Quantity"], "Price": details["Price"], "Total": details["Quantity"] * details["Price"]}
        for prod, details in st.session_state.cart.items()
    ])

    st.table(cart_df)

    # Total Price
    total_price = cart_df["Total"].sum()
    total_items = cart_df["Quantity"].sum()

    # Submit Order Button
    if st.button("✅ Submit Order"):
        st.success(f"Order placed successfully! 🎉")
        st.write(f"**Total Items:** {total_items}")
        st.write(f"**Total Price:** ₹{total_price:.2f}")

        # Clear the cart after submitting
        st.session_state.cart = {}

else:
    st.write("Your cart is empty.")
