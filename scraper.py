from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from collections import Counter
from bs4 import BeautifulSoup
import requests
import json
import time


def build_dynamic_brand_list(descriptions, min_occurrences=2):
    brand_candidates = []
    for desc in descriptions:
        tokens = desc.split()
        brand = " ".join(tokens[:3])
        brand_candidates.append(brand)
    #return [brand for brand, count in Counter(brand_candidates).items() if count >= min_occurrences]
    return brand_candidates

def extract_brand_from_desc(desc, brand_list):
    for brand in brand_list:
        if brand.lower() in desc.lower():
            return brand
    return "Unknown"

def scroll_down(driver, steps=5, pause=2):
    for _ in range(steps):
        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(pause)



def scrape_nykaa_offers():
    offers = []

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://www.nykaa.com/sp/pink-sale-offers/pink-sale-offers")
        time.sleep(5)
        scroll_down(driver, steps=5, pause=2)

        cards = driver.find_elements(By.CSS_SELECTOR, ".css-lwzvs1")
        for card in cards:
            try:
                desc = card.find_element(By.CLASS_NAME, "header").text.strip()
            except:
                desc = None
            try:
                price = card.find_element(By.CLASS_NAME, "sale-price").text.strip()
            except:
                price = None
            try:
                mrp = card.find_element(By.CLASS_NAME, "mrp-price").text.strip()
            except:
                mrp = None
            try:
                discount = card.find_element(By.CLASS_NAME, "discounted-price").text.strip()
            except:
                discount = None
            try:
                link_el = card.find_element(By.CLASS_NAME, "a")
                product_link = link_el.get_attribute("href")
            except:
                product_link = driver.current_url

            offers.append({
                "source": "Nykaa",
                "description": desc,
                "price": price,
                "mrp": mrp,
                "discount": discount,
                "link": product_link
            })

    except Exception as e:
        print("Nykaa scraping error:", e)
    finally:
        driver.quit()

    return offers


def scrape_hm_offers():
    base_url = "https://www2.hm.com/en_in/{category}/sale/view-all.html"
    categories = ["women", "men", "kids", "home"]
    headers = {"User-Agent": "Mozilla/5.0"}

    all_offers = []

    for category in categories:
        url = base_url.format(category=category)
        try:
            res = requests.get(url, headers=headers, timeout=20)
            soup = BeautifulSoup(res.text, "html.parser")
            script_tag = soup.find("script", {
                "id": "product-list-carousel-schema",
                "type": "application/ld+json"
            })

            if not script_tag:
                print(f"No product data found for category: {category}")
                continue

            data = json.loads(script_tag.string)
            items = data.get("itemListElement", [])

            for item in items:
                product = item.get("item", {})
                offer = product.get("offers", {})

                name = product.get("name")
                low = offer.get("lowPrice")
                high = offer.get("highPrice")

                if name and low and high:
                    discount = f"{round((1 - float(low) / float(high)) * 100)}% off"
                else:
                    discount = "N/A"

                all_offers.append({
                    "source": f"H&M - {category.capitalize()}",
                    "title": f"{discount} - {name}",
                    "brand": "H&M",
                    "description": name,
                    "price": f"₹{low}" if low else None,
                    "mrp": f"₹{high}" if high else None,
                    "discount": discount,
                    "link": product.get("url")
                })

        except Exception as e:
            print(f"Error scraping {category}: {e}")

    return all_offers


def scrape_all_offers():
    all_offers = []

    # Scrape each source
    nykaa_raw = scrape_nykaa_offers()
    hm_offers = scrape_hm_offers()

    # Process Nykaa
    descriptions = [o["description"] for o in nykaa_raw if o["description"]]
    brand_list = build_dynamic_brand_list(descriptions)

    nykaa_enriched = []
    for offer in nykaa_raw:
        desc = offer["description"]
        brand = extract_brand_from_desc(desc, brand_list)
        title = f"{offer['discount'] or 'No offer'} - {desc}"
        nykaa_enriched.append({
            "title": title,
            "brand": brand,
            **offer
        })

    all_offers.extend(nykaa_enriched)
    all_offers.extend(hm_offers)
    return all_offers



if __name__ == "__main__":
    offers = scrape_all_offers()
    for offer in offers:
        print(offer)

