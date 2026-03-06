"""
Alternative scraper using Selenium for JavaScript-rendered content
Use this if the regular scraper doesn't get all 377+ products
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"

def setup_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def scrape_with_selenium():
    """Scrape SHL catalog using Selenium"""
    print("Starting Selenium-based scraping...")
    print("This will take a few minutes...")
    
    driver = setup_driver()
    assessments = []
    
    try:
        driver.get(BASE_URL)
        print(f"Loaded page: {BASE_URL}")
        
        # Wait for page to load
        time.sleep(5)
        
        # Try to click "Show All" or load more buttons
        try:
            show_all_buttons = driver.find_elements(By.XPATH, 
                "//*[contains(text(), 'Show All') or contains(text(), 'Load More') or contains(text(), 'View All')]")
            for button in show_all_buttons:
                try:
                    button.click()
                    time.sleep(2)
                except:
                    pass
        except:
            pass
        
        # Scroll to load lazy-loaded content
        last_height = driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scrolls = 10
        
        while scroll_attempts < max_scrolls:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            scroll_attempts += 1
            print(f"Scrolled {scroll_attempts} times...")
        
        # Get page source and parse
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find all product links
        all_links = set()
        
        # Strategy 1: Find all links with product-related patterns
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Build full URL
            if href.startswith('/'):
                full_url = 'https://www.shl.com' + href
            elif href.startswith('http'):
                full_url = href
            else:
                continue
            
            # Filter for individual assessments
            if '/product-catalog/view/' in full_url:
                if not any(exclude in full_url.lower() for exclude in ['job-solution', 'package', 'bundle']):
                    all_links.add(full_url)
        
        print(f"Found {len(all_links)} unique product URLs")
        
        # Extract details for each product
        for i, url in enumerate(sorted(all_links), 1):
            try:
                # Extract name from URL
                name = url.rstrip('/').split('/')[-1].replace('-', ' ').title()
                
                # Try to find the link in the soup for better info
                link_elem = soup.find('a', href=lambda x: x and url in ('https://www.shl.com' + x if x.startswith('/') else x))
                
                if link_elem:
                    # Get text from link or parent
                    link_text = link_elem.get_text(strip=True)
                    if link_text and len(link_text) > 2:
                        name = link_text
                    
                    # Try to get description
                    parent = link_elem.find_parent(['div', 'article', 'section'])
                    description = name
                    if parent:
                        desc_elem = parent.find('p')
                        if desc_elem:
                            description = desc_elem.get_text(strip=True)
                else:
                    description = name
                
                # Determine test type
                name_lower = name.lower()
                if any(word in name_lower for word in ['personality', 'behavior', 'behaviour', 'opq', 'mq']):
                    test_type = "Personality & Behavior"
                elif any(word in name_lower for word in ['verify', 'cognitive', 'reasoning', 'aptitude', 'numerical', 'verbal']):
                    test_type = "Cognitive"
                else:
                    test_type = "Knowledge & Skills"
                
                assessments.append({
                    "name": name,
                    "url": url,
                    "description": description,
                    "duration": None,
                    "test_type": test_type,
                    "remote_support": "Yes",
                    "adaptive_support": "No"
                })
                
                if i % 50 == 0:
                    print(f"Processed {i}/{len(all_links)} assessments...")
                
            except Exception as e:
                print(f"Error processing {url}: {e}")
                continue
        
    finally:
        driver.quit()
    
    # Create DataFrame
    df = pd.DataFrame(assessments)
    df = df.drop_duplicates(subset=["url"])
    df = df.drop_duplicates(subset=["name"])
    
    print(f"\n{'='*60}")
    print(f"Scraping Complete!")
    print(f"{'='*60}")
    print(f"Total assessments: {len(df)}")
    print(f"\nTest type breakdown:")
    print(df['test_type'].value_counts())
    
    # Save
    df.to_csv("data/raw/shl_catalog_raw.csv", index=False)
    print(f"\nSaved to data/raw/shl_catalog_raw.csv")
    
    return df

if __name__ == "__main__":
    scrape_with_selenium()
