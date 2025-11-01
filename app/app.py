import streamlit as st
import requests
import pandas as pd

# -------------------------------------------
# API Configuration
# -------------------------------------------
API_URL = "http://127.0.0.1:8000/recommend"

# -------------------------------------------
# Load Local Data (for product list)
# -------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/all_products.csv", encoding="utf-8")
    df['Product Description'] = df['Product Description'].fillna('').str.lower()
    df['Image'] = "https://via.placeholder.com/200x200.png?text=Product"
    return df

df = load_data()

# -------------------------------------------
# Streamlit UI
# -------------------------------------------
st.set_page_config(page_title="SmartShop", layout="wide")
st.title("🛍️ SmartShop — Intelligent Product Recommender")
st.write("Now powered by a real FastAPI backend 🚀")

category_list = sorted(df['category'].unique())
selected_category = st.selectbox("Select a category:", category_list)

category_df = df[df['category'] == selected_category]
selected_product = st.selectbox(
    "Choose a product to get recommendations:",
    category_df['Product Description'].head(100).tolist()
)

top_n = st.slider("How many recommendations?", 1, 15, 5)

if st.button("🔍 Get Recommendations"):
    try:
        with st.spinner("Fetching recommendations from API..."):
            response = requests.get(API_URL, params={"product_name": selected_product, "top_n": top_n})
            if response.status_code == 200:
                data = response.json()
                recs = pd.DataFrame(data["recommendations"])
                
                st.subheader(f"🧠 Recommended Products for: {selected_product.title()}")
                cols = st.columns(3)
                for i, (_, row) in enumerate(recs.iterrows()):
                    with cols[i % 3]:
                        st.image("https://via.placeholder.com/200x200.png?text=Product", width=200)
                        st.markdown(f"**{row['Product Description'].title()}**")
                        st.write(f"💰 **${row['Price(Dollar)']:.2f}**")
                        st.caption(f"🏷️ {row['category']}")
            else:
                st.error("⚠️ Error fetching data from API.")
    except Exception as e:
        st.error(f"Something went wrong: {e}")
