import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json
import re
from urllib.parse import urljoin

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"

def extract_assessment_details(url, headers):
    """Extract detailed information from individual assessment page"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        details = {}
        
        # Extract duration
        duration_elem = soup.find(text=re.compile(r'\d+\s*(?:min|minutes)', re.I))
        if duration_elem:
            duration_match = re.search(r'(\d+)', duration_elem)
            details['duration'] = int(duration_match.group(1)) if duration_match else None
        
        # Extract remote/adaptive support
        content_text = soup.get_text().lower()
        details['remote_support'] = "Yes" if "remote" in content_text else "No"
        details['adaptive_support'] = "Yes" if "adaptive" in content_text else "No"
        
        return details
    except Exception as e:
        return {}

def scrape_shl_catalog():
    """Scrape SHL catalog for Individual Test Solutions only"""
    print("Starting SHL catalog scraping...")
    print(f"Target URL: {BASE_URL}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    
    try:
        response = requests.get(BASE_URL, headers=headers, timeout=15)
        response.raise_for_status()
        print(f"Successfully fetched page (status: {response.status_code})")
    except Exception as e:
        print(f"Error fetching page: {e}")
        return pd.DataFrame()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    assessments = []
    
    # Strategy 1: Look for product cards with various class patterns
    selectors = [
        "a.product-card",
        "div.product-card a",
        "a[href*='/product-catalog/view/']",
        "a[href*='/solutions/products/']",
        ".product-item a",
        ".assessment-card a",
        "div[class*='product'] a",
        "div[class*='card'] a[href*='product']"
    ]
    
    all_links = set()
    
    for selector in selectors:
        elements = soup.select(selector)
        for elem in elements:
            href = elem.get('href', '')
            if href:
                full_url = urljoin(BASE_URL, href)
                if '/product-catalog/view/' in full_url or '/solutions/products/' in full_url:
                    all_links.add(full_url)
    
    # Strategy 2: Find all links containing product-related keywords
    all_page_links = soup.find_all('a', href=True)
    for link in all_page_links:
        href = link.get('href', '')
        full_url = urljoin(BASE_URL, href)
        
        # Include links that look like individual assessments
        if any(pattern in full_url for pattern in ['/product-catalog/view/', '/solutions/products/product-catalog/view/']):
            # Exclude job solutions and packages
            if not any(exclude in full_url.lower() for exclude in ['job-solution', 'package', 'bundle']):
                all_links.add(full_url)
    
    print(f"Found {len(all_links)} unique product URLs")
    
    # Extract information from each link
    for i, url in enumerate(sorted(all_links), 1):
        try:
            # Extract name from URL
            name_from_url = url.rstrip('/').split('/')[-1].replace('-', ' ').title()
            
            # Try to find the link element for better name extraction
            link_elem = soup.find('a', href=lambda x: x and url.endswith(x) if x else False)
            
            if link_elem:
                # Try to get name from link text or nearby heading
                name = link_elem.get_text(strip=True)
                if not name or len(name) < 3:
                    parent = link_elem.find_parent(['div', 'article', 'section'])
                    if parent:
                        heading = parent.find(['h1', 'h2', 'h3', 'h4', 'h5'])
                        name = heading.get_text(strip=True) if heading else name_from_url
                    else:
                        name = name_from_url
            else:
                name = name_from_url
            
            # Extract description
            description = name  # Default to name
            if link_elem:
                parent = link_elem.find_parent(['div', 'article', 'section'])
                if parent:
                    desc_elem = parent.find('p')
                    if desc_elem:
                        description = desc_elem.get_text(strip=True)
            
            # Determine test type from name/URL
            name_lower = name.lower()
            url_lower = url.lower()
            
            if any(word in name_lower or word in url_lower for word in 
                   ['personality', 'behavior', 'behaviour', 'motivation', 'opq', 'mq']):
                test_type = "Personality & Behavior"
            elif any(word in name_lower or word in url_lower for word in 
                     ['verify', 'cognitive', 'reasoning', 'aptitude', 'ability', 'numerical', 'verbal']):
                test_type = "Cognitive"
            else:
                test_type = "Knowledge & Skills"
            
            assessments.append({
                "name": name,
                "url": url,
                "description": description,
                "duration": None,  # Will be filled if we scrape individual pages
                "test_type": test_type,
                "remote_support": "Yes",
                "adaptive_support": "No"
            })
            
            if i % 50 == 0:
                print(f"Processed {i}/{len(all_links)} assessments...")
            
        except Exception as e:
            print(f"Error parsing URL {url}: {e}")
            continue
    
    # Create DataFrame
    df = pd.DataFrame(assessments)
    
    # Remove duplicates
    df = df.drop_duplicates(subset=["url"])
    df = df.drop_duplicates(subset=["name"])
    
    # Clean up names
    df['name'] = df['name'].str.strip()
    df = df[df['name'].str.len() > 2]  # Remove very short names
    
    print(f"\n{'='*60}")
    print(f"Scraping Complete!")
    print(f"{'='*60}")
    print(f"Total assessments scraped: {len(df)}")
    print(f"Test type breakdown:")
    print(df['test_type'].value_counts())
    
    # Save raw data
    df.to_csv("data/raw/shl_catalog_raw.csv", index=False)
    print(f"\nSaved to data/raw/shl_catalog_raw.csv")
    
    # Show sample
    print(f"\nSample assessments:")
    print(df[['name', 'test_type']].head(10))
    
    return df

if __name__ == "__main__":
    scrape_shl_catalog()
