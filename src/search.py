import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_products(path='data/products.json'):
    with open(path, 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['text'] = (df['name'].astype(str) + ' ' + df['description'].astype(str) + ' ' +
                  df['category'].astype(str))
    return df

class SemanticSearcher:
    def __init__(self, corpus_texts):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.doc_matrix = self.vectorizer.fit_transform(corpus_texts)

    def rank(self, query: str):
        q_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(q_vec, self.doc_matrix).ravel()
        return sims

def filter_rank(df, sims, price_max=None, rating_min=None, category=None):
    out = df.copy()
    out['score'] = sims
    if price_max is not None:
        out = out[out['price'] <= price_max]
    if rating_min is not None:
        out = out[out['rating'] >= rating_min]
    if category is not None:
        out = out[out['category'] == category]
    out = out.sort_values(['score','rating'], ascending=[False, False])
    return out
