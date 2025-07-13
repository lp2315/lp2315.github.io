import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options


class SystembolagetScraper:
    def __init__(self, headless = True, wait_time = 0.2):
        self.wait_time = wait_time
        self.driver = self._setup_driver(headless)
        self.wait = WebDriverWait(self.driver, 0.2)

    def _setup_driver(self, headless):
        options = Options()
        options.page_load_strategy = 'normal'
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        return webdriver.Chrome(options = options)

    def _handle_age_verification(self):
        try:
            time.sleep(2)  # Let page load

            # Handle cookie consent first
            cookie_selectors = [
                "button[id*='accept']",
                "button[class*='accept']",
                "[data-testid*='accept']",
                "//button[contains(text(), 'acceptera')]"
            ]

            for selector in cookie_selectors:
                try:
                    if selector.startswith('//'):
                        button = self.driver.find_element(By.XPATH, selector)
                    else:
                        button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    button.click()
                    time.sleep(1)
                    break
                except:
                    continue

            # Handle age verification - avoid anything with "under 20" or leading to "/under-20/"
            all_clickable = self.driver.find_elements(By.XPATH, "//button | //a | //div[@role='button']")

            for element in all_clickable:
                try:
                    text = element.text.lower()
                    href = element.get_attribute('href') or ""

                    # Skip if contains "under 20" or leads to under-20 page
                    if "under 20" in text or "/under-20/" in href:
                        continue

                    # Click if it looks like age verification (contains age-related text)
                    if any(keyword in text for keyword in ["fyllt", "20", "år", "ja"]):
                        element.click()
                        time.sleep(2)
                        print("Age verification complete\n")
                        break

                except:
                    continue

        except Exception as e:
            print(f"Age verification handling failed: {e}")

    def scrape_products(self, base_url):
        # Handle initial setup
        self.driver.get("https://www.systembolaget.se")
        self._handle_age_verification()

        product_urls = set()  # Use set to avoid duplicates
        page = 1
        previous_page_urls = set()

        # First pass: collect all product URLs
        while True:
            url = f"{base_url}&p={page}"
            print(f"Collecting URLs from page {page}...")

            try:
                self.driver.get(url)
                time.sleep(self.wait_time)

                # Find all product links
                product_links = self.driver.find_elements(By.CSS_SELECTOR, 'a[href*="/produkt/"]')

                if not product_links:
                    break

                page_urls = [link.get_attribute('href') for link in product_links]
                current_page_urls = set(page_urls)

                # Check if current page is identical to previous page
                if page > 1 and current_page_urls == previous_page_urls:
                    print("Reached last page (identical to previous)")
                    break

                initial_count = len(product_urls)
                product_urls.update(page_urls)  # Set automatically handles duplicates
                new_count = len(product_urls) - initial_count

                print(f"Found {new_count} new products - total {len(product_urls)}")

                previous_page_urls = current_page_urls
                page += 1
                time.sleep(0.2)

            except Exception as e:
                print(f"Error on page {page}: {e}")
                break

        print(f"Total unique product URLs: {len(product_urls)}")

        # Second pass: scrape each product page
        products = []
        for i, product_url in enumerate(product_urls):
            try:
                print(f"Scraping product {i + 1}/{len(product_urls)}")
                product_data = self._scrape_individual_product(product_url)
                if product_data:
                    print(product_data)
                    products.append(product_data)
                time.sleep(self.wait_time)

            except Exception as e:
                print(f"Error scraping {product_url}: {e}")
                continue

        return products

    def _scrape_individual_product(self, url):
        try:
            self.driver.get(url)
            time.sleep(0.2)

            # Extract data using specific XPATHs
            name = self._safe_extract_xpath(
                '/html/body/div[1]/div/main/div[2]/div[1]/div[3]/div[1]/div[1]/div[1]/h1/span[1]')
            if not name:
                name = self._safe_extract_xpath(
                    '/html/body/div[1]/div/main/div[2]/div[1]/div[3]/div[1]/div[1]/h1/span[1]'
                )

            volume = self._safe_extract_xpath(
                '/html/body/div[1]/div/main/div[2]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/p[3]')
            if not volume:
                volume = (
                    self._safe_extract_xpath('/html/body/div[1]/div/main/div[2]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/select/option[1]'))
            if not volume:
                volume = (
                    self._safe_extract_xpath('/html/body/div[1]/div/main/div[2]/div[1]/div[3]/div[1]/div[3]/div[1]/p[3]'))

            alcohol = self._safe_extract_xpath(
                '/html/body/div[1]/div/main/div[2]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/p[5]')
            if not alcohol:
                alcohol = self._safe_extract_xpath(
                    '/html/body/div[1]/div/main/div[2]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/p')
            if not alcohol:
                alcohol = self._safe_extract_xpath('/html/body/div[1]/div/main/div[2]/div[1]/div[3]/div[1]/div[3]/div[1]/p[5]')


            price = self._safe_extract_xpath('/html/body/div[1]/div/main/div[2]/div[1]/div[3]/div[1]/div[1]/div[4]/p')

            type = self._safe_extract_xpath('/html/body/div[1]/div/main/div[2]/div[1]/div[1]/div/a[3]')

            return {
                'name': name,
                'type': type,
                'price': price,
                'volume': volume,
                'alcohol_content': alcohol,
                'url': url
            }

        except Exception as e:
            print(f"Failed to scrape {url}: {e}")
            return None

    def _safe_extract_xpath(self, xpath):
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            return self.driver.execute_script("return arguments[0].textContent;", element).strip()
        except:
            return None

    def _safe_extract_js(self, selector):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return self.driver.execute_script("return arguments[0].textContent;", element).strip()
        except:
            return None

    def save_data(self, products, filename = 'systembolaget_data.json'):
        with open(filename, 'w', encoding = 'utf-8') as f:
            json.dump(products, f, ensure_ascii = False, indent = 2)
        print(f"Saved {len(products)} products to {filename}")

    def close(self):
        self.driver.quit()


# Usage
if __name__ == "__main__":
    url = "https://www.systembolaget.se/sortiment/fast-sortiment/?pris-till=499&volym-fran=1&alkoholhalt-fran=1"

    scraper = SystembolagetScraper(headless = True, wait_time = 0.2)

    try:
        products = scraper.scrape_products(url)
        scraper.save_data(products)
        print(f"Scraping complete. Total products: {len(products)}")
        input('Press any key to exit...')
    finally:
        scraper.close()
