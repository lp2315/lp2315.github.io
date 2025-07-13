import json
import re
from datetime import datetime


class SystembolagetDataProcessor:
    def __init__(self, input_file = 'systembolaget_data.json'):
        self.input_file = input_file
        self.processed_data = []
        self.faulty_count = 0

    def load_data(self):
        with open(self.input_file, 'r', encoding = 'utf-8') as f:
            return json.load(f)

    def clean_price(self, price_str):
        if not price_str:
            return None
        # Convert "17:50" to 17.50
        price_clean = re.sub(r'[^\d:,.-]', '', price_str)
        price_clean = price_clean.replace(':-', '.00').replace(':', '.').replace(',', '.')
        try:
            return float(price_clean)
        except:
            return None

    def clean_volume(self, volume_str):
        if not volume_str:
            return None
        # Extract number from "330 ml"
        volume_str = volume_str.replace(' ', '')
        volume_match = re.search(r'(\d+)', volume_str)
        if volume_match:
            try:
                return float(volume_match.group(1))
            except:
                return None
        return None

    def clean_alcohol(self, alcohol_str):
        if not alcohol_str:
            return None
        # Extract number from "4,5 % vol." and handle comma as decimal
        alcohol_clean = re.search(r'(\d+[,.]?\d*)', alcohol_str)
        if alcohol_clean:
            try:
                alcohol_val = alcohol_clean.group(1).replace(',', '.')
                return float(alcohol_val)
            except:
                return None
        return None

    def calculate_apk(self, price, volume, alcohol):
        # APK = (alcohol_percentage * volume) / price
        # This gives you total alcohol units per krona
        if price and volume and alcohol and price > 0:
            total_alcohol = (alcohol / 100) * volume  # ml of pure alcohol
            return round(total_alcohol / price, 2)
        return None

    def is_valid_entry(self, entry):
        required_fields = ['name', 'price', 'volume', 'alcohol_content']
        return all(entry.get(field) for field in required_fields)

    def process_data(self):
        raw_data = self.load_data()

        for item in raw_data:
            if not self.is_valid_entry(item):
                self.faulty_count += 1
                continue

            # Clean data
            price = self.clean_price(item['price'])
            volume = self.clean_volume(item['volume'])
            alcohol = self.clean_alcohol(item['alcohol_content'])

            # Skip if any cleaning failed
            if None in [price, volume, alcohol]:
                self.faulty_count += 1
                continue

            # Calculate APK
            apk = self.calculate_apk(price, volume, alcohol)
            if apk is None:
                self.faulty_count += 1
                continue

            # Create processed entry
            processed_item = {
                'name': item['name'].strip(),
                'type': item.get('type', '').strip(),
                'price': price,
                'volume': volume,
                'alcohol_content': alcohol,
                'apk': apk,
                'url': item.get('url', '')
            }

            self.processed_data.append(processed_item)

        # Sort by APK (highest first - best value)
        self.processed_data.sort(key = lambda x: x['apk'], reverse = True)

        # Add rank
        for i, item in enumerate(self.processed_data, 1):
            item['rank'] = i

    def create_summary(self):
        if not self.processed_data:
            return None

        apk_values = [item['apk'] for item in self.processed_data]
        avg_apk = round(sum(apk_values) / len(apk_values), 2)

        top_3 = [item['name'] + " " + str(item['apk']) for item in self.processed_data[:3]]

        summary = {
            'scan_date': datetime.now().strftime('%Y-%m-%d'),
            'total_processed': len(self.processed_data),
            'faulty_entries': self.faulty_count,
            'average_apk': avg_apk,
            'top_3_products': top_3
        }

        return summary

    def save_processed_data(self, output_file = 'processed_systembolaget_data.json'):
        with open(output_file, 'w', encoding = 'utf-8') as f:
            json.dump(self.processed_data, f, ensure_ascii = False, indent = 2)
        print(f"Processed data saved to {output_file}")

    def save_summary(self, summary_file = 'scan_summary.json'):
        summary = self.create_summary()
        if summary:
            with open(summary_file, 'a', encoding = 'utf-8') as f:
                json.dump(summary, f, ensure_ascii = False, indent = 0)
            print(f"Summary saved to {summary_file}")

            # Also print summary
            print(f"\nScan Summary:")
            print(f"Date: {summary['scan_date']}")
            print(f"Products processed: {summary['total_processed']}")
            print(f"Faulty entries: {summary['faulty_entries']}")
            print(f"Average APK: {summary['average_apk']} ml alkohol/krona")
            print(f"Top 3 products:")
            for i, product in enumerate(summary['top_3_products'], 1):
                print(f"  {i}. {product}")

    def run(self):
        print("Processing Systembolaget data...")
        self.process_data()

        if self.processed_data:
            self.save_processed_data()
            self.save_summary()
            print(f"\nProcessing complete!")
        else:
            print("No valid data to process.")


# Usage
if __name__ == "__main__":
    processor = SystembolagetDataProcessor()
    processor.run()
