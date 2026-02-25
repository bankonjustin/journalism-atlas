#!/usr/bin/env python3
"""
Independent Journalism Atlas - Data Conversion Script
Converts mega_list_2_7_clean.csv to creators-data.json
Version: 1.0
Date: February 7, 2026
"""

import pandas as pd
import json
import sys
from pathlib import Path

def validate_url(url):
    """Ensure URL has proper protocol"""
    if pd.isna(url):
        return None
    url = str(url).strip()
    if not url:
        return None
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url

def clean_text(text):
    """Clean text fields of extra whitespace and handle NaN"""
    if pd.isna(text):
        return ""
    return str(text).strip()

def main():
    # File paths
    input_file = 'mega_list_2_7_clean.csv'
    output_file = 'creators-data-new.json'
    backup_file = 'creators-data-backup.json'
    
    print("=" * 60)
    print("INDEPENDENT JOURNALISM ATLAS - DATA CONVERSION")
    print("=" * 60)
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f"❌ ERROR: Input file '{input_file}' not found!")
        print("   Make sure the CSV file is in the current directory.")
        sys.exit(1)
    
    # Load CSV
    print(f"\n📂 Loading {input_file}...")
    df = pd.read_csv(input_file)
    print(f"   ✓ Loaded {len(df)} rows")
    
    # Show columns
    print(f"\n📋 Columns found: {list(df.columns)}")
    
    # Drop internal/private columns
    columns_to_drop = ['Platform Secondary', 'Origin List', 'New Tags', 
                       'Special Lists', 'Notes']
    existing_drops = [col for col in columns_to_drop if col in df.columns]
    if existing_drops:
        df = df.drop(existing_drops, axis=1)
        print(f"\n🗑️  Dropped internal columns: {existing_drops}")
    
    # Rename columns to match current JSON structure
    df = df.rename(columns={
        'Creator Name': 'name',
        'Creator Channel': 'channel',
        'Link Primary': 'link',
        'Platform Primary': 'platform',
        'Topic/Category': 'topic',
        'Geography': 'geography',
        'Groups': 'group'
    })
    
    print(f"\n✓ Renamed columns to standard format")
    
    # Data cleaning and validation
    print(f"\n🧹 Cleaning and validating data...")
    
    # Clean text fields
    for col in ['name', 'channel', 'platform', 'topic', 'geography', 'group']:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)
    
    # Validate and clean URLs
    df['link'] = df['link'].apply(validate_url)
    
    # Remove rows with missing critical data
    before_count = len(df)
    df = df.dropna(subset=['name', 'link'])
    after_count = len(df)
    if before_count != after_count:
        print(f"   ⚠️  Removed {before_count - after_count} rows with missing name or link")
    
    # Convert to records format
    creators = df.to_dict('records')
    
    # Generate statistics
    print(f"\n📊 DATA STATISTICS:")
    print(f"   Total creators: {len(creators)}")
    print(f"\n   Unique groups: {df['group'].nunique()}")
    for group in sorted(df['group'].unique()):
        count = len(df[df['group'] == group])
        print(f"      • {group}: {count} creators")
    
    print(f"\n   Unique platforms: {df['platform'].nunique()}")
    platform_counts = df['platform'].value_counts().head(10)
    for platform, count in platform_counts.items():
        print(f"      • {platform}: {count} creators")
    
    print(f"\n   Unique topics: {df['topic'].nunique()}")
    
    # Show sample entry
    print(f"\n📄 SAMPLE ENTRY:")
    print(json.dumps(creators[0], indent=2))
    
    # Backup existing file if it exists
    if Path('creators-data.json').exists():
        print(f"\n💾 Backing up existing creators-data.json...")
        with open('creators-data.json', 'r') as f:
            backup_data = json.load(f)
        with open(backup_file, 'w') as f:
            json.dump(backup_data, f, indent=2)
        print(f"   ✓ Backup saved as {backup_file}")
        print(f"   (Previous version had {len(backup_data)} entries)")
    
    # Write new JSON file
    print(f"\n💾 Writing {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(creators, f, indent=2, ensure_ascii=False)
    print(f"   ✓ File saved successfully")
    
    # Validation checks
    print(f"\n✅ VALIDATION CHECKS:")
    
    # Check for empty groups
    empty_groups = df[df['group'] == ''].shape[0]
    if empty_groups > 0:
        print(f"   ⚠️  WARNING: {empty_groups} creators have no group assigned")
    else:
        print(f"   ✓ All creators have groups assigned")
    
    # Check for HTTPS
    http_count = sum(1 for c in creators if c['link'].startswith('http://'))
    if http_count > 0:
        print(f"   ⚠️  WARNING: {http_count} creators use HTTP (not HTTPS)")
    else:
        print(f"   ✓ All links use HTTPS")
    
    # Check for duplicate creators
    duplicates = df[df.duplicated(subset=['name', 'channel'], keep=False)]
    if len(duplicates) > 0:
        print(f"   ⚠️  WARNING: {len(duplicates)} potential duplicate entries")
        print(f"   Check: {duplicates[['name', 'channel']].values[:5]}")
    else:
        print(f"   ✓ No duplicate creators found")
    
    print(f"\n" + "=" * 60)
    print(f"✅ CONVERSION COMPLETE!")
    print(f"=" * 60)
    print(f"\nNext steps:")
    print(f"1. Review {output_file} for accuracy")
    print(f"2. Test locally before deploying")
    print(f"3. Replace creators-data.json on live site")
    print(f"4. Verify all visualizations load correctly")
    print(f"\nNote: If anything goes wrong, restore from {backup_file}")
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
