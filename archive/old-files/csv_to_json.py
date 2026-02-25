#!/usr/bin/env python3
"""
Atlas Creator Database - CSV to JSON Converter
Converts the creator CSV export to JSON format for the website
"""

import csv
import json
import sys
from pathlib import Path

def convert_csv_to_json(csv_path, json_path=None):
    """
    Convert creator CSV to JSON format
    
    Args:
        csv_path: Path to input CSV file
        json_path: Path to output JSON file (optional, defaults to same name with .json)
    """
    # Default output path
    if json_path is None:
        json_path = Path(csv_path).with_suffix('.json')
    
    creators = []
    
    with open(csv_path, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # Clean up the data
            creator = {
                'name': row.get('t', '').strip(),
                'link': row.get('Link', '').strip(),
                'originList': row.get('Origin List', '').strip(),
                'moved': row.get('Moved', '').strip().upper() == 'YES'
            }
            
            # Only add if name and link exist
            if creator['name'] and creator['link']:
                creators.append(creator)
    
    # Write to JSON
    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump(creators, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"✅ Converted {len(creators)} creators")
    print(f"📄 Input:  {csv_path}")
    print(f"📄 Output: {json_path}")
    
    return len(creators)

def main():
    if len(sys.argv) < 2:
        print("Usage: python csv_to_json.py <input.csv> [output.json]")
        print("\nExample:")
        print("  python csv_to_json.py creators.csv")
        print("  python csv_to_json.py creators.csv creators-data.json")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    json_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(csv_path).exists():
        print(f"❌ Error: File not found: {csv_path}")
        sys.exit(1)
    
    try:
        count = convert_csv_to_json(csv_path, json_path)
        print(f"\n🎉 Success! {count} creators converted to JSON.")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
