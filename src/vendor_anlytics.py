import csv
import os
import datetime
from collections import defaultdict
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipelines

# Load NER model and tokenizer
model_dir = "model/"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForTokenClassification.from_pretrained(model_dir)
ner = pipelines.pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple") # type: ignore
def parse_date(date_str):
    # Adjust this if your date format is different
    try:
        return datetime.datetime.fromisoformat(date_str)
    except Exception:
        # Try parsing common formats if needed
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

def extract_price(entities):
    for ent in entities:
        if ent['entity_group'].lower() == 'price':
            try:
                # Remove non-numeric characters except dot
                price = ''.join(c for c in ent['word'] if c.isdigit() or c == '.')
                return float(price)
            except Exception:
                continue
    return None

def extract_product(entities):
    for ent in entities:
        if ent['entity_group'].lower() == 'product':
            return ent['word']
    return None

def analyze_vendor(csv_path):
    vendor_posts = defaultdict(list)
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            vendor = row['Channel Username']
            vendor_posts[vendor].append(row)

    results = []
    for vendor, posts in vendor_posts.items():
        # Activity & Consistency
        dates = []
        for p in posts:
            try:
                dates.append(parse_date(p['Date']))
            except Exception:
                continue
        if not dates:
            continue
        min_date, max_date = min(dates), max(dates)
        weeks = max((max_date - min_date).days / 7, 1)
        posting_freq = len(posts) / weeks

        # Market Reach & Engagement
        views = []
        for p in posts:
            try:
                views.append(int(p.get('Views', 0)))
            except Exception:
                views.append(0)
        avg_views = sum(views) / len(views) if views else 0
        top_idx = views.index(max(views)) if views else 0
        top_post = posts[top_idx]

        # Business Profile (NER)
        prices = []
        products = []
        for p in posts:
            text = p['Message']
            entities = ner(text)
            price = extract_price(entities)
            product = extract_product(entities)
            if price:
                prices.append(price)
            if product:
                products.append(product)
        avg_price = sum(prices) / len(prices) if prices else 0

        # Lending Score (simple weighted sum)
        lending_score = (avg_views * 0.5) + (posting_freq * 0.5)

        results.append({
            "Vendor": vendor,
            "Channel Title": posts[0]['Channel Title'],
            "Posts": len(posts),
            "Posting Frequency (per week)": round(posting_freq, 2),
            "Average Views": round(avg_views, 2),
            "Top Post ID": top_post['ID'],
            "Top Product": extract_product(ner(top_post['Message'])),
            "Top Price": extract_price(ner(top_post['Message'])),
            "Average Price": round(avg_price, 2),
            "Lending Score": round(lending_score, 2)
        })
    return results

if __name__ == "__main__":
    csv_path = "data/telegram_data.csv"
    analytics = analyze_vendor(csv_path)
    # Print or save results
    for vendor in analytics:
        print(vendor)