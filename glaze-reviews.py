import json
from playwright.sync_api import sync_playwright

YANDEX_URL = "https://yandex.ru/maps/org/glaze/194103090849/"

def scrape_reviews():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(YANDEX_URL, timeout=60000)
        page.wait_for_timeout(7000)

        # Прокручиваем больше раз
        for _ in range(10):
            page.mouse.wheel(0, 800)
            page.wait_for_timeout(1500)

        reviews = []
        blocks = page.query_selector_all('[data-testid="review-card"]')

        for i, block in enumerate(blocks):
            try:
                name = block.query_selector('[data-testid="reviewer-name"]').inner_text()
                rating_str = block.query_selector('[data-testid="rating"]').get_attribute("aria-label")
                rating = int(rating_str[0]) if rating_str else 0
                text = block.query_selector('[data-testid="review-text"]').inner_text()
                date = block.query_selector('[data-testid="review-date"]').inner_text()
                reviews.append({
                    "name": name.strip(),
                    "rating": rating,
                    "text": text.strip(),
                    "date": date.strip()
                })
            except Exception as e:
                print(f"Ошибка в блоке {i}: {e}")
                continue

        browser.close()

        # Лог для проверки
        print(f"Собрано отзывов: {len(reviews)}")

        # Записываем результат
        with open("reviews.json", "w", encoding="utf-8") as f:
            json.dump(reviews, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scrape_reviews()
