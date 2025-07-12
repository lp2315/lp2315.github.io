import requests
import json
from datetime import datetime
import time
import os
from typing import List, Dict, Any


class SystembolagetScraper:
    def __init__(self):
        # Option 1: Use the unofficial but working API
        self.product_search_url = "https://api-extern.systembolaget.se/sb-api-ecommerce/v1/productsearch"
        self.stores_url = "https://api-extern.systembolaget.se/sb-api-ecommerce/v1/store"
        self.api_key = "cfc702aed3094c86b92d6d4ff7a54c84"

        # Option 2: Community API fallback
        self.community_api_url = "https://api.systembolaget.io/products"

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Ocp-Apim-Subscription-Key': self.api_key
        }
        self.output_dir = "data"
        self.ensure_output_directory()

    def ensure_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def fetch_stores(self) -> List[Dict[str, Any]]:
        """Fetch all store information"""
        try:
            print("Fetching store information...")
            response = requests.get(self.stores_url, headers = self.headers)
            response.raise_for_status()

            data = response.json()
            stores = data.get('data', [])
            print(f"Found {len(stores)} stores")
            return stores[:5]  # Limit to first 5 stores for testing

        except Exception as e:
            print(f"Error fetching stores: {e}")
            return []

    def fetch_products_from_unofficial_api(self) -> List[Dict[str, Any]]:
        """Fetch products using the unofficial API"""
        all_products = []
        stores = self.fetch_stores()

        if not stores:
            print("No stores found, cannot fetch products")
            return []

        for store in stores:
            store_id = store.get('siteId', '')
            store_name = store.get('name', 'Unknown')

            print(f"Fetching products for store: {store_name} (ID: {store_id})")

            page = 0
            while True:
                try:
                    params = {
                        'storeId': store_id,
                        'size': 30,
                        'page': page
                    }

                    response = requests.get(self.product_search_url,
                                            params = params,
                                            headers = self.headers)
                    response.raise_for_status()

                    data = response.json()
                    products = data.get('products', [])

                    if not products:
                        break

                    all_products.extend(products)
                    print(f"  Fetched page {page + 1}, got {len(products)} products")

                    page += 1
                    time.sleep(0.5)  # Be nice to the API

                    # Safety limit per store
                    if page >= 10:  # Max 300 products per store for testing
                        print(f"  Reached page limit for {store_name}")
                        break

                except Exception as e:
                    print(f"  Error fetching page {page} for store {store_name}: {e}")
                    break

        # Remove duplicates based on product ID
        seen_ids = set()
        unique_products = []
        for product in all_products:
            product_id = product.get('productId')
            if product_id and product_id not in seen_ids:
                seen_ids.add(product_id)
                unique_products.append(product)

        print(f"Total unique products fetched: {len(unique_products)}")
        return unique_products

    def fetch_products_from_community_api(self) -> List[Dict[str, Any]]:
        """Fetch products from community-maintained API as fallback"""
        try:
            print("Trying community API as fallback...")
            response = requests.get(self.community_api_url,
                                    headers = {'User-Agent': self.headers['User-Agent']})
            response.raise_for_status()

            data = response.json()
            products = data if isinstance(data, list) else data.get('products', [])
            print(f"Fetched {len(products)} products from community API")
            return products

        except Exception as e:
            print(f"Community API also failed: {e}")
            return []

    def fetch_excel_data(self) -> List[Dict[str, Any]]:
        """Fetch data from Systembolaget's Excel file"""
        try:
            print("Trying to fetch Excel data from Systembolaget...")
            # This URL might change, but Systembolaget usually provides Excel downloads
            excel_url = "https://www.systembolaget.se/api/assortment/products/xml"

            response = requests.get(excel_url, headers = self.headers)
            response.raise_for_status()

            # Save the raw data for manual processing if needed
            with open(os.path.join(self.output_dir, "systembolaget_raw.xml"), 'wb') as f:
                f.write(response.content)

            print("Excel/XML data saved. You may need to process this manually.")
            return []

        except Exception as e:
            print(f"Excel data fetch failed: {e}")
            return []

    def create_mock_data(self) -> List[Dict[str, Any]]:
        """Create comprehensive mock data for testing"""
        mock_products = [
            {
                "productId": "1001", "productNameBold": "Vodka Explorer", "price": 299.0,
                "volume": 700, "alcoholPercentage": 40.0, "categoryLevel1": "Sprit",
                "categoryLevel2": "Vodka", "producerName": "Nordic Distillery",
                "country": "Sverige", "region": "Skåne"
            },
            {
                "productId": "1002", "productNameBold": "Red Wine Estate Reserve", "price": 159.0,
                "volume": 750, "alcoholPercentage": 13.5, "categoryLevel1": "Rött vin",
                "categoryLevel2": "Bordeaux", "producerName": "Château Mock",
                "country": "Frankrike", "region": "Bordeaux"
            },
            {
                "productId": "1003", "productNameBold": "Craft IPA Supreme", "price": 45.0,
                "volume": 500, "alcoholPercentage": 6.2, "categoryLevel1": "Öl",
                "categoryLevel2": "IPA", "producerName": "Micro Brewery",
                "country": "Sverige", "region": "Stockholm"
            },
            {
                "productId": "1004", "productNameBold": "Single Malt Highland", "price": 549.0,
                "volume": 700, "alcoholPercentage": 43.0, "categoryLevel1": "Whisky",
                "categoryLevel2": "Single Malt", "producerName": "Highland Distillery",
                "country": "Skottland", "region": "Highlands"
            },
            {
                "productId": "1005", "productNameBold": "London Dry Gin Premium", "price": 399.0,
                "volume": 700, "alcoholPercentage": 47.0, "categoryLevel1": "Gin",
                "categoryLevel2": "London Dry", "producerName": "London Spirits",
                "country": "England", "region": "London"
            },
            {
                "productId": "1006", "productNameBold": "Rosé Provence Style", "price": 129.0,
                "volume": 750, "alcoholPercentage": 12.5, "categoryLevel1": "Rosé",
                "categoryLevel2": "Provence", "producerName": "French Vineyard",
                "country": "Frankrike", "region": "Provence"
            },
            {
                "productId": "1007", "productNameBold": "Belgian Wheat Beer", "price": 39.0,
                "volume": 500, "alcoholPercentage": 4.8, "categoryLevel1": "Öl",
                "categoryLevel2": "Wheat Beer", "producerName": "Brussels Brewery",
                "country": "Belgien", "region": "Brussels"
            },
            {
                "productId": "1008", "productNameBold": "Tequila Silver 100%", "price": 429.0,
                "volume": 700, "alcoholPercentage": 40.0, "categoryLevel1": "Tequila",
                "categoryLevel2": "Silver", "producerName": "Agave Distillery",
                "country": "Mexico", "region": "Jalisco"
            },
            {
                "productId": "1009", "productNameBold": "Champagne Brut Reserve", "price": 489.0,
                "volume": 750, "alcoholPercentage": 12.0, "categoryLevel1": "Mousserande vin",
                "categoryLevel2": "Champagne", "producerName": "Champagne House",
                "country": "Frankrike", "region": "Champagne"
            },
            {
                "productId": "1010", "productNameBold": "Rum Dark Aged 12Y", "price": 599.0,
                "volume": 700, "alcoholPercentage": 43.0, "categoryLevel1": "Rom",
                "categoryLevel2": "Dark Rum", "producerName": "Caribbean Distillery",
                "country": "Jamaica", "region": "Kingston"
            },
            {
                "productId": "1011", "productNameBold": "Pilsner Czech Style", "price": 35.0,
                "volume": 500, "alcoholPercentage": 4.5, "categoryLevel1": "Öl",
                "categoryLevel2": "Pilsner", "producerName": "Prague Brewery",
                "country": "Tjeckien", "region": "Prague"
            },
            {
                "productId": "1012", "productNameBold": "Cognac VSOP Premium", "price": 799.0,
                "volume": 700, "alcoholPercentage": 40.0, "categoryLevel1": "Cognac",
                "categoryLevel2": "VSOP", "producerName": "French Cognac House",
                "country": "Frankrike", "region": "Cognac"
            },
            {
                "productId": "1013", "productNameBold": "Sauvignon Blanc Crisp", "price": 139.0,
                "volume": 750, "alcoholPercentage": 13.0, "categoryLevel1": "Vitt vin",
                "categoryLevel2": "Sauvignon Blanc", "producerName": "Valley Winery",
                "country": "Nya Zeeland", "region": "Marlborough"
            },
            {
                "productId": "1014", "productNameBold": "Porter Strong Dark", "price": 52.0,
                "volume": 500, "alcoholPercentage": 7.5, "categoryLevel1": "Öl",
                "categoryLevel2": "Porter", "producerName": "Craft Beer Co",
                "country": "Sverige", "region": "Göteborg"
            },
            {
                "productId": "1015", "productNameBold": "Bourbon Kentucky Straight", "price": 459.0,
                "volume": 700, "alcoholPercentage": 45.0, "categoryLevel1": "Bourbon",
                "categoryLevel2": "Straight Bourbon", "producerName": "Kentucky Distillery",
                "country": "USA", "region": "Kentucky"
            },
            {
                "productId": "1016", "productNameBold": "Riesling Sweet German", "price": 149.0,
                "volume": 750, "alcoholPercentage": 11.5, "categoryLevel1": "Vitt vin",
                "categoryLevel2": "Riesling", "producerName": "Rhine Vineyard",
                "country": "Tyskland", "region": "Rhein"
            },
            {
                "productId": "1017", "productNameBold": "Stout Imperial Russian", "price": 65.0,
                "volume": 500, "alcoholPercentage": 9.0, "categoryLevel1": "Öl",
                "categoryLevel2": "Stout", "producerName": "Dark Beer Brewery",
                "country": "Sverige", "region": "Stockholm"
            },
            {
                "productId": "1018", "productNameBold": "Aquavit Traditional Nordic", "price": 349.0,
                "volume": 700, "alcoholPercentage": 40.0, "categoryLevel1": "Akvavit",
                "categoryLevel2": "Traditional", "producerName": "Nordic Spirits",
                "country": "Sverige", "region": "Stockholm"
            },
            {
                "productId": "1019", "productNameBold": "Pinot Noir Elegant", "price": 229.0,
                "volume": 750, "alcoholPercentage": 13.5, "categoryLevel1": "Rött vin",
                "categoryLevel2": "Pinot Noir", "producerName": "Oregon Winery",
                "country": "USA", "region": "Oregon"
            },
            {
                "productId": "1020", "productNameBold": "Lager Light German", "price": 32.0,
                "volume": 500, "alcoholPercentage": 4.2, "categoryLevel1": "Öl",
                "categoryLevel2": "Lager", "producerName": "Munich Brewery",
                "country": "Tyskland", "region": "Bayern"
            }
        ]

        print(f"Using mock data with {len(mock_products)} products for demonstration")
        return mock_products

    def fetch_all_products(self) -> List[Dict[str, Any]]:
        """Try multiple methods to fetch products"""
        print("=" * 50)
        print("Starting product fetch with multiple fallback methods...")
        print("=" * 50)

        # Method 1: Try unofficial API
        print("\n1. Trying unofficial API...")
        products = self.fetch_products_from_unofficial_api()

        if products:
            return products

        # Method 2: Try community API
        print("\n2. Trying community API...")
        products = self.fetch_products_from_community_api()

        if products:
            return products

        # Method 3: Try Excel/XML data
        print("\n3. Trying Excel/XML data...")
        products = self.fetch_excel_data()

        if products:
            return products

        # Method 4: Use mock data
        print("\n4. All methods failed, using mock data for demonstration...")
        return self.create_mock_data()

    def calculate_alcohol_value(self, product: Dict[str, Any]) -> float:
        """Calculate price per unit of alcohol"""
        try:
            price = float(product.get('price', 0))
            volume_ml = float(product.get('volume', 0))
            alcohol_percentage = float(product.get('alcoholPercentage', 0))

            if price <= 0 or volume_ml <= 0 or alcohol_percentage <= 0:
                return float('inf')

            # Convert volume to liters
            volume_liters = volume_ml / 1000

            # Calculate actual alcohol content in liters
            alcohol_content_liters = (alcohol_percentage / 100) * volume_liters

            # Calculate price per unit of alcohol
            price_per_alcohol_unit = price / alcohol_content_liters

            return price_per_alcohol_unit

        except (ValueError, TypeError, ZeroDivisionError):
            return float('inf')

    def process_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process products and calculate alcohol values"""
        processed_products = []

        print("Processing products and calculating alcohol values...")

        for product in products:
            try:
                price_per_alcohol_unit = self.calculate_alcohol_value(product)

                if price_per_alcohol_unit == float('inf'):
                    continue

                processed_product = {
                    'name': product.get('productNameBold', product.get('name', 'Unknown')),
                    'price': float(product.get('price', 0)),
                    'volume': int(product.get('volume', 0)),
                    'alcoholPercentage': float(product.get('alcoholPercentage', 0)),
                    'pricePerAlcoholUnit': round(price_per_alcohol_unit, 2),
                    'category': product.get('categoryLevel1', product.get('category', 'Unknown')),
                    'subcategory': product.get('categoryLevel2', product.get('subcategory', 'Unknown')),
                    'producer': product.get('producerName', product.get('producer', 'Unknown')),
                    'productId': product.get('productId', ''),
                    'country': product.get('country', 'Unknown'),
                    'region': product.get('region', ''),
                    'vintage': product.get('vintage', ''),
                    'alcoholType': product.get('alcoholType', ''),
                    'packaging': product.get('packaging', ''),
                    'seal': product.get('seal', ''),
                    'origin': product.get('originLevel1', ''),
                    'taste': product.get('taste', ''),
                    'usage': product.get('usage', ''),
                    'lastUpdated': datetime.now().isoformat()
                }

                processed_products.append(processed_product)

            except Exception as e:
                print(f"Error processing product {product.get('productId', 'unknown')}: {e}")
                continue

        # Sort by price per alcohol unit (best value first)
        processed_products.sort(key = lambda x: x['pricePerAlcoholUnit'])

        print(f"Successfully processed {len(processed_products)} products")
        return processed_products

    def save_data(self, products: List[Dict[str, Any]]):
        """Save processed data to JSON files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save full dataset
        full_filename = os.path.join(self.output_dir, f"systembolaget_full_{timestamp}.json")
        with open(full_filename, 'w', encoding = 'utf-8') as f:
            json.dump(products, f, indent = 2, ensure_ascii = False)

        # Save top 100 best values for the website
        top_100_filename = os.path.join(self.output_dir, "systembolaget_top_100.json")
        top_100_data = {
            'lastUpdated': datetime.now().isoformat(),
            'totalProducts': len(products),
            'products': products[:100]
        }

        with open(top_100_filename, 'w', encoding = 'utf-8') as f:
            json.dump(top_100_data, f, indent = 2, ensure_ascii = False)

        # Save top 20 for quick loading
        top_20_filename = os.path.join(self.output_dir, "systembolaget_top_20.json")
        top_20_data = {
            'lastUpdated': datetime.now().isoformat(),
            'totalProducts': len(products),
            'products': products[:20]
        }

        with open(top_20_filename, 'w', encoding = 'utf-8') as f:
            json.dump(top_20_data, f, indent = 2, ensure_ascii = False)

        print(f"\nData saved:")
        print(f"  - Full dataset: {full_filename}")
        print(f"  - Top 100: {top_100_filename}")
        print(f"  - Top 20: {top_20_filename}")

        return top_20_filename, top_100_filename

    def generate_stats(self, products: List[Dict[str, Any]]):
        """Generate and save statistics about the data"""
        if not products:
            return

        stats = {
            'totalProducts': len(products),
            'lastUpdated': datetime.now().isoformat(),
            'bestValue': {
                'name': products[0]['name'],
                'pricePerAlcoholUnit': products[0]['pricePerAlcoholUnit'],
                'price': products[0]['price'],
                'alcoholPercentage': products[0]['alcoholPercentage']
            },
            'categories': {},
            'priceRanges': {
                'under_100': 0,
                '100_200': 0,
                '200_500': 0,
                'over_500': 0
            },
            'alcoholRanges': {
                'under_20': 0,
                '20_40': 0,
                '40_plus': 0
            }
        }

        # Calculate category distribution
        for product in products:
            category = product['category']
            stats['categories'][category] = stats['categories'].get(category, 0) + 1

            # Price ranges
            price = product['price']
            if price < 100:
                stats['priceRanges']['under_100'] += 1
            elif price < 200:
                stats['priceRanges']['100_200'] += 1
            elif price < 500:
                stats['priceRanges']['200_500'] += 1
            else:
                stats['priceRanges']['over_500'] += 1

            # Alcohol ranges
            alcohol = product['alcoholPercentage']
            if alcohol < 20:
                stats['alcoholRanges']['under_20'] += 1
            elif alcohol < 40:
                stats['alcoholRanges']['20_40'] += 1
            else:
                stats['alcoholRanges']['40_plus'] += 1

        # Save stats
        stats_filename = os.path.join(self.output_dir, "systembolaget_stats.json")
        with open(stats_filename, 'w', encoding = 'utf-8') as f:
            json.dump(stats, f, indent = 2, ensure_ascii = False)

        print(f"Statistics saved: {stats_filename}")
        return stats

    def run(self):
        """Main method to run the scraper"""
        print("=" * 60)
        print("Systembolaget Scraper Starting...")
        print("Note: Official API removed, using alternative methods")
        print("=" * 60)

        start_time = time.time()

        # Fetch all products using multiple fallback methods
        raw_products = self.fetch_all_products()

        if not raw_products:
            print("No products fetched from any method. Exiting.")
            return

        # Process products
        processed_products = self.process_products(raw_products)

        if not processed_products:
            print("No products processed successfully. Exiting.")
            return

        # Save data
        top_20_file, top_100_file = self.save_data(processed_products)

        # Generate statistics
        stats = self.generate_stats(processed_products)

        end_time = time.time()

        print("\n" + "=" * 60)
        print("Scraping completed successfully!")
        print(f"Total time: {end_time - start_time:.2f} seconds")
        print(f"Products processed: {len(processed_products)}")
        if processed_products:
            print(
                f"Best value: {processed_products[0]['name']} ({processed_products[0]['pricePerAlcoholUnit']} SEK/unit)")
        print("=" * 60)

        print("\nNext steps:")
        print("1. Copy the generated JSON files to your GitHub repository's 'data/' folder")
        print("2. Commit and push to update your website")
        print("3. Your website will now display the latest alcohol value data!")


if __name__ == "__main__":
    scraper = SystembolagetScraper()
    scraper.run()
