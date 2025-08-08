# AI E-commerce Catalog (Streamlit)

A small e-commerce catalog with basic filters and an **AI smart search** that understands natural language (e.g., “running shoes under $100 with good reviews”).  
The AI uses **TF-IDF semantic similarity** plus a **rule-based intent parser** for price/rating/category constraints.  
Optional **Dynamic Pricing** demo included.

## How to run
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install streamlit scikit-learn pandas numpy
streamlit run app.py
```

## AI Feature
**Smart Product Search (NLP):**  
TF-IDF vectorization + cosine similarity ranks products by semantic relevance to the user query.  
A tiny parser extracts numeric and categorical constraints (price caps like “under $100”, ratings like “4+ stars”, categories like “shoes”).

## Tools / Libraries
- Python
- Streamlit
- scikit-learn
- pandas
- numpy

## Assumptions
- Static JSON product catalog (12 items)
- No external APIs (offline)
- Intent parser handles common phrases (“under”, “below”, “stars”, category keywords)
- Dynamic pricing is a demo (rule-based) to illustrate how signals could affect prices

## Bonus: Blockchain Integration (idea)
- **Token-gated pricing:** users holding a loyalty token/NFT receive automatic price adjustments at checkout
- **On-chain preferences:** users opt-in to store category/budget preferences on-chain, and the app reads them to personalize recommendations without centralized profiles
- **Loyalty smart contracts:** purchases mint points as on-chain rewards redeemable for discounts or early product drops
