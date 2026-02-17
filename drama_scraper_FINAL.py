#!/usr/bin/env python3
"""
FINAL FIXED Arabic Drama Scraper
Uses CORRECT selectors verified from actual drama pages
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime
from typing import List, Dict, Optional
import unicodedata


class ArabicDramaScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.dramas = []
        self.seen_titles = set()

    def normalize_title(self, title: str) -> str:
        """Normalize title for duplicate detection"""
        title = unicodedata.normalize('NFKD', title.lower())
        title = re.sub(r'[^\w\s]', '', title)
        title = re.sub(r'\s+', ' ', title).strip()
        return title

    def scrape_drama_details(self, url: str) -> Optional[Dict]:
        """Scrape full details from a drama page"""
        try:
            print(f"    📄 Fetching: {url}")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract data from the actual HTML structure
            drama_data = {
                'url': url,
                'title': None,
                'title_arabic': None,
                'title_original': None,
                'country': 'unknown',
                'total_episodes': None,
                'episode_duration': 60,
                'release_year': None,
                'status': 'completed',
                'genres': [],
                'thumbnail_url': None,
                'description': None,
                'description_arabic': None,
                'watch_links': []
            }

            # Title - from <h3> tag with format "العنوان الإنجليزي Arabic Title"
            title_tag = soup.find('h3')
            if title_tag:
                title_text = title_tag.get_text(strip=True)
                # Split English and Arabic titles
                parts = title_text.split(' ', 1)
                if len(parts) >= 2:
                    # English title is usually first few words
                    english_match = re.match(r'^([A-Za-z\s\'\?\!]+)', title_text)
                    if english_match:
                        drama_data['title'] = english_match.group(1).strip()
                        # Rest is Arabic
                        arabic_part = title_text[len(drama_data['title']):].strip()
                        drama_data['title_arabic'] = arabic_part
                else:
                    drama_data['title'] = title_text
                    drama_data['title_arabic'] = title_text

            # Extract from "معلومات عن المسلسل" section
            info_section = soup.find('h3', string=re.compile(r'معلومات عن المسلسل'))
            if info_section:
                # Get the next <p> tag which contains all info
                info_p = info_section.find_next_sibling()
                if info_p:
                    info_text = info_p.get_text(separator='\n')
                    
                    # Extract original name
                    original_match = re.search(r'اسم المسلسل\s*:\s*(.+?)(?:\n|$)', info_text)
                    if original_match:
                        drama_data['title_original'] = original_match.group(1).strip()
                    
                    # Extract alternative name
                    alt_match = re.search(r'الاسم العربي\s*:\s*(.+?)(?:\n|$)', info_text)
                    if alt_match and not drama_data['title_arabic']:
                        drama_data['title_arabic'] = alt_match.group(1).strip()
                    
                    # Extract genre
                    genre_match = re.search(r'النوع\s*:\s*(.+?)(?:\n|$)', info_text)
                    if genre_match:
                        genres = [g.strip() for g in genre_match.group(1).split('،')]
                        drama_data['genres'] = genres
                    
                    # Extract episodes
                    ep_match = re.search(r'عدد الحلقات\s*:\s*(\d+)', info_text)
                    if ep_match:
                        drama_data['total_episodes'] = int(ep_match.group(1))
                    
                    # Extract country
                    country_match = re.search(r'البلد المنتج\s*:\s*(.+?)(?:\n|$)', info_text)
                    if country_match:
                        country = country_match.group(1).strip()
                        if 'كوريا' in country:
                            drama_data['country'] = 'korean'
                        elif 'الصين' in country or 'تايوان' in country:
                            drama_data['country'] = 'chinese'
                        elif 'اليابان' in country:
                            drama_data['country'] = 'japanese'
                        elif 'تايلاند' in country:
                            drama_data['country'] = 'thai'
                    
                    # Extract air date to determine year
                    date_match = re.search(r'موعد البث\s*:\s*(.+?)(?:\n|$)', info_text)
                    if date_match:
                        date_str = date_match.group(1).strip()
                        year_match = re.search(r'(\d{4})', date_str)
                        if year_match:
                            drama_data['release_year'] = int(year_match.group(1))
                    
                    # Check if ongoing
                    if 'أيام العرض' in info_text:
                        drama_data['status'] = 'ongoing'

            # Extract description from "القصة" section
            story_section = soup.find('h3', string=re.compile(r'القصة'))
            if story_section:
                story_p = story_section.find_next_sibling('p')
                if story_p:
                    description = story_p.get_text(strip=True)
                    drama_data['description_arabic'] = description
                    drama_data['description'] = description  # Same for now

            # Extract thumbnail
            thumbnail = soup.find('img', src=re.compile(r'wp-content/uploads'))
            if thumbnail:
                drama_data['thumbnail_url'] = thumbnail.get('src', '')

            # Find watch link (link to episodes page)
            watch_link = soup.find('a', string=re.compile(r'مشاهدة حلقات'))
            if watch_link:
                episodes_url = watch_link.get('href', '')
                if episodes_url:
                    drama_data['watch_links'].append({
                        'website_name': 'ArabDrama TV',
                        'url': episodes_url,
                        'language': 'arabic',
                        'episodes_available': drama_data['total_episodes'] or 0
                    })

            # Validation - must have at least a title
            if not drama_data['title'] and not drama_data['title_arabic']:
                print(f"      ⚠️  No title found, skipping")
                return None

            # Use title for deduplication
            check_title = drama_data['title'] or drama_data['title_arabic']
            normalized = self.normalize_title(check_title)
            
            if normalized in self.seen_titles:
                print(f"      ⏭️  Duplicate: {check_title}")
                return None
            
            self.seen_titles.add(normalized)
            print(f"      ✅ Extracted: {check_title}")
            return drama_data

        except Exception as e:
            print(f"      ❌ Error: {str(e)}")
            return None

    def scrape_aradrama_tv(self, max_dramas: int = 100):
        """Scrape dramas from ArabDrama TV"""
        print("🔍 Scraping ArabDrama TV...")
        
        categories = [
            '/category/serie/korea/',
            '/category/serie/chinese-taiwan/',
            '/category/serie/japanese/'
        ]
        
        base_url = 'https://aradramatv.cc'
        
        for category in categories:
            if len(self.dramas) >= max_dramas:
                break
                
            print(f"  📂 Category: {category}")
            
            for page_num in range(1, 6):  # Pages 1-5
                if len(self.dramas) >= max_dramas:
                    break
                
                if page_num == 1:
                    url = f"{base_url}{category}"
                else:
                    url = f"{base_url}{category}page/{page_num}/"
                
                try:
                    print(f"    → Page {page_num}: {url}")
                    response = requests.get(url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Find drama cards using correct selector
                    drama_cards = soup.find_all('div', class_='post-row')
                    print(f"      Found {len(drama_cards)} drama cards")
                    
                    for card in drama_cards:
                        if len(self.dramas) >= max_dramas:
                            break
                        
                        # Extract drama URL from the card
                        link = card.find('a', href=True)
                        if not link:
                            continue
                        
                        drama_url = link['href']
                        if not drama_url.startswith('http'):
                            drama_url = base_url + drama_url
                        
                        # Scrape full details
                        drama_data = self.scrape_drama_details(drama_url)
                        if drama_data:
                            self.dramas.append(drama_data)
                        
                        time.sleep(0.5)  # Be polite
                    
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"    ❌ Error on page {page_num}: {str(e)}")
                    continue
        
        print(f"✅ Scraped {len(self.dramas)} dramas from ArabDrama TV")

    def save_to_json(self, filename: str = 'scraped_dramas_FINAL.json'):
        """Save scraped data to JSON"""
        output = {
            'scrape_date': datetime.now().isoformat(),
            'total_dramas': len(self.dramas),
            'dramas': self.dramas
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved {len(self.dramas)} dramas to {filename}")

    def print_summary(self):
        """Print scraping summary"""
        print("\n" + "="*60)
        print("📊 SCRAPING SUMMARY")
        print("="*60)
        print(f"Total dramas: {len(self.dramas)}")
        
        # Count by country
        countries = {}
        years = {}
        for drama in self.dramas:
            country = drama.get('country', 'unknown')
            countries[country] = countries.get(country, 0) + 1
            
            year = drama.get('release_year')
            if year:
                years[year] = years.get(year, 0) + 1
        
        print("\n📍 By Country:")
        for country, count in sorted(countries.items()):
            print(f"  {country}: {count}")
        
        print("\n📅 By Year:")
        for year, count in sorted(years.items(), reverse=True):
            print(f"  {year}: {count}")
        
        print("="*60)


def main():
    print("🎬 ARABIC DRAMA SCRAPER (FINAL VERSION)")
    print("="*60)
    
    scraper = ArabicDramaScraper()
    
    # Scrape dramas
    scraper.scrape_aradrama_tv(max_dramas=100)
    
    # Print summary
    scraper.print_summary()
    
    # Save to JSON
    scraper.save_to_json()
    
    print("\n✅ DONE!")
    print("💡 NEXT: Import this file into Django:")
    print("   python manage.py import_scraped_dramas scraped_dramas_FINAL.json")


if __name__ == '__main__':
    main()