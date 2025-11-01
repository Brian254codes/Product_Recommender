import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ProductRecommender:
    def __init__(self, data_path="data/all_products.csv"):
        self.df = pd.read_csv(data_path, encoding="utf-8")
        self.df['Product Description'] = self.df['Product Description'].fillna('').str.lower()
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['Product Description'])
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def recommend(self, product_name, top_n=5):
        # Find the index of the product
        idx = self.df[self.df['Product Description'] == product_name.lower()].index
        if len(idx) == 0:
            return []
        idx = idx[0]

        # Compute similarity
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]
        indices = [i[0] for i in sim_scores]

        results = self.df.iloc[indices][['Product Description', 'Price(Dollar)', 'category']].to_dict(orient="records")
        return results
