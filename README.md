# FinTech Vendor Analytics Engine for Micro-Lending

This project helps EthioMart identify its most active and promising vendors on Telegram to offer small business loans (micro-lending). It combines business activity data scraped from Telegram with product and price information extracted using a trained NER (Named Entity Recognition) model.

## Features

- **Vendor Activity & Consistency:** Calculates posting frequency (posts per week) for each vendor.
- **Market Reach & Engagement:** Computes average views per post and identifies the top-performing post.
- **Business Profile:** Uses an NER model to extract product and price information from each post.
- **Lending Score:** Combines engagement and activity metrics into a simple, weighted score to help prioritize vendors for micro-lending.

## Project Structure

```
.
├── data/
│   └── telegram_data.csv         # Scraped Telegram posts (CSV)
├── model/                        # Trained NER model directory
├── src/
│   ├── telegram_scraper.py       # Telegram scraping script
│   ├── label_data.py             # Rule-based data labeling script
│   └── vendor_anlytics.py        # Vendor analytics engine (main script)
└── README.md
```

## Requirements

- Python 3.8+
- [transformers](https://huggingface.co/transformers/)
- [telethon](https://docs.telethon.dev/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. **Scrape Telegram Data**
   - Configure your Telegram API credentials in a `.env` file.
   - Run the scraper:
     ```bash
     python3 src/telegram_scraper.py
     ```
   - This will create `data/telegram_data.csv` with posts and metadata.

2. **Label Data (Optional)**
   - Use `src/label_data.py` to label data for NER model training.

3. **Train or Place Your NER Model**
   - Place your trained NER model files in the `model/` directory.

4. **Run Vendor Analytics**
   - Analyze vendors and compute lending scores:
     ```bash
     python3 src/vendor_anlytics.py
     ```
   - The script prints a summary for each vendor, including posting frequency, average views, top product/price, and the final lending score.

## Output Example

```
{'Vendor': '@Shageronlinestore', 
 'Channel Title': 'Shager Online Store', 
 'Posts': 120, 
 'Posting Frequency (per week)': 8.5, 
 'Average Views': 350.2, 
 'Top Post ID': '12345', 
 'Top Product': 'Laptop', 
 'Top Price': 15000.0, 
 'Average Price': 12000.0, 
 'Lending Score': 179.35}
```

## Customization

- Adjust the `Lending Score` formula in `vendor_anlytics.py` as needed for your business logic.
- If your CSV or NER model uses different field names, update the script accordingly.

## License

MIT License

---

**Contact:**  
For questions or support, please contact the project maintainer.