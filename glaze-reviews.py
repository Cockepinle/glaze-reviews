import json
from playwright.sync_api import sync_playwright

YANDEX_URL = "https://yandex.ru/maps/org/glaze/194103090849/"

def scrape_reviews():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Используем обычный браузер (не headless)
        context = browser.new_context(
            locale='ru-RU',
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.118 Safari/537.36",
            geolocation={"longitude": 44.4911, "latitude": 48.6867},
            permissions=["geolocation"],
        )

        # Загружаем cookies
        try:
            with open("cookies.json", "r", encoding="utf-8") as f:
                cookies = json.load(f)
                context.add_cookies(cookies)
        except Exception as e:
            print("Не удалось загрузить cookies:", e)

        page = context.new_page()
        page.goto(YANDEX_URL, timeout=60000)
        page.wait_for_timeout(8000)

        # Скроллим, чтобы подгрузить отзывы
        for _ in range(6):
            page.mouse.wheel(0, 800)
            page.wait_for_timeout(2000)

        blocks = page.query_selector_all('[data-testid="review-card"]')
        reviews = []

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
            except:
                continue

        with open("reviews.json", "w", encoding="utf-8") as f:
            json.dump(reviews, f, ensure_ascii=False, indent=2)

        context.close()
        browser.close()

if __name__ == "__main__":
    scrape_reviews()
