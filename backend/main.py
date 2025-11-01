from fastapi import FastAPI
from recommender import ProductRecommender

app = FastAPI(title="Product Recommendation API")

# Initialize recommender
recommender = ProductRecommender()

@app.get("/")
def root():
    return {"message": "Welcome to the Product Recommendation API"}

@app.get("/recommend")
def recommend(product_name: str, top_n: int = 5):
    recommendations = recommender.recommend(product_name, top_n)
    return {"product": product_name, "recommendations": recommendations}
