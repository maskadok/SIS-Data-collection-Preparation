import asyncio
import csv
import re
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
OUTPUT = DATA_DIR / "row_data.csv"

BASE_URL = (
    "https://www.technodom.kz/catalog/smartfony-i-gadzhety/"
    "smartfony-i-telefony/smartfony"
)


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Начинаю скрапинг...")

        with OUTPUT.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "name",
                    "rating",
                    "reviews",
                    "price",
                    "product_url",
                    "category",
                    "raw_text",
                ]
            )

            total = 0
            seen_urls = set()

            for page_num in range(1, 6):
                url = f"{BASE_URL}?page={page_num}"
                print(f"Скрап страницы {page_num}: {url}")

                await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                await page.wait_for_timeout(2000)
                await page.wait_for_selector("a[href^='/p/']")

                cards = page.locator("a[href^='/p/']")
                count = await cards.count()
                print(f"  найдено ссылок: {count}")

                collected_on_page = 0

                for i in range(count):
                    if collected_on_page >= 24 or total >= 120:
                        break

                    card = cards.nth(i)

                    href = await card.get_attribute("href")
                    if not href:
                        continue

                    if href.startswith("/"):
                        product_url = "https://www.technodom.kz" + href
                    else:
                        product_url = href

                    if product_url in seen_urls:
                        continue
                    seen_urls.add(product_url)

                    raw_text = " ".join((await card.inner_text()).split())

                    m_rating = re.search(r"([0-5](?:\.\d)?)\s*\((\d+)\)", raw_text)
                    rating = m_rating.group(1) if m_rating else ""
                    reviews = m_rating.group(2) if m_rating else ""

                    m_price = re.search(r"(\d[\d\s]+)\s*₸", raw_text)
                    price = m_price.group(1).replace(" ", "") if m_price else ""

                    name_start = raw_text.find("Смартфон")
                    if name_start == -1:
                        name_start = 0
                    name_end = m_rating.start() if m_rating else len(raw_text)
                    name = raw_text[name_start:name_end].strip(" -")

                    writer.writerow(
                        [
                            name,
                            rating,
                            reviews,
                            price,
                            product_url,
                            "smartphones",
                            raw_text,
                        ]
                    )

                    collected_on_page += 1
                    total += 1

                print(f"  собрано с страницы: {collected_on_page}, всего: {total}")

                if total >= 120:
                    break

        await browser.close()
        print(f"Готово. Результат сохранён в {OUTPUT}")


if __name__ == "__main__":
    asyncio.run(main())
