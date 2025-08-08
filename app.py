import streamlit as st
import pandas as pd
import numpy as np

from src.search import load_products, SemanticSearcher, filter_rank
from src.utils import parse_query

st.set_page_config(page_title="AI Catalog", page_icon="🛒", layout="wide")
st.title("🛒 E-commerce Catalog (AI Search)")

# Load products
df = load_products().copy()

# --- Optional Dynamic Pricing (demo) ---
# Keep a copy of original prices to show delta when adjusted
if 'base_price' not in df.columns:
    df['base_price'] = df['price']

with st.sidebar:
    st.header("Filters")
    # We'll add the dynamic pricing toggle below a divider so it's visually separate
    cat = st.selectbox("Category", ["All"] + sorted(df['category'].unique().tolist()))
    price_max = st.slider("Max Price", 0, 300, 300)
    rating_min = st.slider("Min Rating", 0.0, 5.0, 0.0, 0.1)
    st.markdown("---")
    dyn = st.checkbox("Enable Dynamic Pricing (demo)")

# Apply dynamic pricing if enabled
if dyn:
    # Mock demand: Shoes & Electronics are "hot"
    demand_boost = df['category'].isin(['Shoes', 'Electronics']).astype(int)

    # Adjustment formula:
    # +5% if high-demand category
    # +1% per 0.1 rating above 4.2 (only positive part)
    # -5% if rating < 4.0 (clearance)
    adj = 1 + 0.05 * demand_boost + np.clip((df['rating'] - 4.2), 0, None) * 0.10
    adj = np.where(df['rating'] < 4.0, 0.95, adj)

    df['price'] = (df['base_price'] * adj).round(2)  # recompute from base each time
else:
    df['price'] = df['base_price']  # reset to original when toggle off

# Build searcher AFTER final df['text'] exists
searcher = SemanticSearcher(df['text'].tolist())

st.subheader("Natural Language Search")
q = st.text_input("Try: 'show me running shoes under $100 with good reviews'")

if st.button("Search") or q:
    parsed = parse_query(q or "")
    # sync sidebar constraints with parsed intent but don't override user's sidebar choices
    pmax = min(price_max, parsed['price_max']) if parsed['price_max'] else price_max
    rmin = max(rating_min, parsed['rating_min']) if parsed['rating_min'] else rating_min
    cat_eff = parsed['category'] if parsed['category'] and cat == "All" else (None if cat == "All" else cat)

    sims = searcher.rank(q or " ")
    results = filter_rank(
        df, sims,
        price_max=pmax if pmax < 300 else None,
        rating_min=rmin if rmin > 0 else None,
        category=cat_eff
    )
else:
    # default: just apply basic filters and show by rating
    results = df.copy().sort_values('rating', ascending=False)
    results = results[(results['price'] <= price_max) & (results['rating'] >= rating_min)]
    if cat != "All":
        results = results[results['category'] == cat]

st.caption(f"Showing {len(results)} products")

def product_card(row):
    # show strikethrough if dynamic pricing changed the price
    show_discount = ('base_price' in row) and (row['price'] != row['base_price'])
    if show_discount:
        price_line = f"~~${row['base_price']:.2f}~~ ${row['price']:.2f}"
    else:
        price_line = f"${row['price']:.2f}"

    st.markdown(f"""
**{row['name']}**  
Category: {row['category']} · ⭐ {row['rating']} · {price_line}  
_{row['description']}_
""")

if len(results) == 0:
    st.info("No products match your filters/search. Try widening your filters.")
else:
    cols = st.columns(3)
    for i, (_, row) in enumerate(results.iterrows()):
        with cols[i % 3]:
            product_card(row)
