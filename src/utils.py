import re

def parse_query(q: str):
    q = q.lower()
    price_max = None
    rating_min = None
    category = None

    # Price patterns
    m = re.search(r'(under|below|<=|<)\s*\$?(\d+(\.\d+)?)', q)
    if m:
        price_max = float(m.group(2))
    else:
        m2 = re.search(r'\$?(\d+(\.\d+)?)\s*(or less|and under)?', q)
        if m2 and ('under' in q or 'less' in q):
            price_max = float(m2.group(1))

    # Rating patterns
    if 'good reviews' in q or 'highly rated' in q or '4+ stars' in q:
        rating_min = 4.0
    m = re.search(r'(\d(\.\d+)?)\s*\+?\s*stars', q)
    if m:
        rating_min = float(m.group(1))
    m = re.search(r'(>=|at least)\s*(\d(\.\d+)?)\s*stars?', q)
    if m:
        rating_min = float(m.group(2))

    # Category patterns
    for c in ['shoes','apparel','electronics','fitness','accessories']:
        if c in q:
            category = c.capitalize()
            break

    return {"price_max": price_max, "rating_min": rating_min, "category": category}
