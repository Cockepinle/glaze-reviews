import json
from playwright.sync_api import sync_playwright

YANDEX_URL = "https://yandex.ru/maps/org/glaze/194103090849/"

def scrape_reviews():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(YANDEX_URL, timeout=60000)
        page.wait_for_timeout(5000)

        for _ in range(5):
            page.mouse.wheel(0, 500)
            page.wait_for_timeout(1500)

        reviews = []
        blocks = page.query_selector_all('[data-testid="review-card"]')

        for block in blocks:
            try:
                name = block.query_selector('[data-testid="reviewer-name"]').inner_text()
                rating = int(block.query_selector('[data-testid="rating"]').get_attribute("aria-label")[0])
                text = block.query_selector('[data-testid="review-text"]').inner_text()
                date = block.query_selector('[data-testid="review-date"]').inner_text()
                reviews.append({
                    "name": name,
                    "rating": rating,
                    "text": text,
                    "date": date
                })
            except Exception:
                continue

        browser.close()

        with open("reviews.json", "w", encoding="utf-8") as f:
            json.dump(reviews, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape_reviews()
