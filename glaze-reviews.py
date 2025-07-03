name: Scrape Yandex Reviews

on:
  schedule:
    - cron: "0 3 * * *"  # Каждый день в 3:00 утра по UTC
  workflow_dispatch:

jobs:
  run-scraper:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.10

      - name: Install dependencies
        run: |
          pip install playwright
          playwright install chromium

      - name: Run scraper
        run: python glaze-reviews.py

      - name: Commit and push reviews.json
        run: |
          git config user.name "github-actions"
          git config user.email "github-actions@github.com"
          git add reviews.json
          git commit -m "Update reviews" || echo "No changes to commit"
          git push
