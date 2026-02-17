#!/usr/bin/env python3
"""
FIXED Arabic Drama Scraper
Uses CORRECT selectors based on actual HTML structure
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime
from typing import List, Dict, Optional
import unicodedata


class DramaScraper:
    def __init__(self):
        self.scraped_dramas = []
        self.seen_titles = set()
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ar,en-US;q=0.7,en;q=0.3',
        }
        
        # Genre mapping
        self.genre_map = {
            'رومانسي': 'romance',
            'كوميدي': 'comedy',
            'دراما': 'drama',
            'إثارة': 'thriller',
            'غموض': 'mystery',
            'جريمة': 'crime',
            'تاريخي': 'historical',
            'فانتازيا': 'fantasy',
            'أكشن': 'action',
            'رعب': 'horror',
            'طبي': 'medical',
        }
        
        # Country mapping
        self.country_map = {
            'كوري': 'korean',
            'كوريا': 'korean',
            'صيني': 'chinese',
            'الصين': 'chinese',
            'تايوان': 'taiwanese',
            'تركي': 'turkish',
            'تركيا': 'turkish',
            'ياباني': 'japanese',
            'اليابان': 'japanese',
            'تايلندي': 'thai',
            'تايلند': 'thai',
        }
    
    def normalize_title(self, title: str) -> str:
        """Normalize title for duplicate detection"""
        title = ''.join(c for c in unicodedata.normalize('NFD', title)
                       if unicodedata.category(c) != 'Mn')
        title = re.sub(r'[^\w\s]', '', title.lower()).strip()
        title = ' '.join(title.split())
        return title
    
    def is_duplicate(self, title: str, year: int, country: str) -> bool:
        """Check if drama already exists"""
        key = f"{self.normalize_title(title)}_{year}_{country}"
        if key in self.seen_titles:
            return True
        self.seen_titles.add(key)
        return False
    
    def extract_year(self, text: str) -> int:
        """Extract year from text"""
        match = re.search(r'(20\d{2})', text)
        return int(match.group(1)) if match else datetime.now().year
    
    def map_genre(self, arabic_genres: List[str]) -> List[str]:
        """Map Arabic genres to English"""
        english_genres = []
        for genre in arabic_genres:
            genre = genre.strip()
            if genre in self.genre_map:
                english_genres.append(self.genre_map[genre])
        return english_genres if english_genres else ['drama']
    
    def map_country(self, text: str) -> str:
        """Map Arabic country to English"""
        text_lower = text.lower()
        for arabic, english in self.country_map.items():
            if arabic in text_lower:
                return english
        return 'unknown'
    
    def scrape_aradrama_tv(self, max_dramas: int = 100):
        """Scrape ArabDrama TV using CORRECT selectors"""
        print("\n🔍 Scraping ArabDrama TV...")
        
        base_url = "https://aradramatv.cc"
        
        # Scrape multiple pages
        categories = [
            ('/category/serie/korea/', 'korean'),
            ('/category/serie/chinese-taiwan/', 'chinese'),
            ('/category/serie/japanese/', 'japanese'),
        ]
        
        drama_count = 0
        
        for category_url, default_country in categories:
            if drama_count >= max_dramas:
                break
                
            print(f"\n  📂 Category: {category_url}")
            
            # Scrape multiple pages in each category
            for page in range(1, 6):  # Pages 1-5
                if drama_count >= max_dramas:
                    break
                
                try:
                    if page == 1:
                        url = f"{base_url}{category_url}"
                    else:
                        url = f"{base_url}{category_url}page/{page}/"
                    
                    print(f"    → Page {page}: {url}")
                    
                    response = requests.get(url, headers=self.headers, timeout=15)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # CORRECT SELECTOR: Find all post-row divs
                    drama_cards = soup.find_all('div', class_='post-row')
                    
                    print(f"      Found {len(drama_cards)} drama cards")
                    
                    for card in drama_cards:
                        if drama_count >= max_dramas:
                            break
                        
                        try:
                            # Extract drama link
                            link = card.find('a')
                            if not link:
                                continue
                            
                            drama_url = link.get('href', '')
                            if not drama_url.startswith('http'):
                                drama_url = base_url + drama_url
                            
                            # Extract title from b_title div
                            title_div = card.find('div', class_='b_title')
                            if not title_div:
                                continue
                            
                            title_text = title_div.get_text(strip=True)
                            
                            # Extract thumbnail
                            img = card.find('img')
                            thumbnail = img.get('src', '') if img else ''
                            if thumbnail and not thumbnail.startswith('http'):
                                thumbnail = base_url + thumbnail
                            
                            # Extract filter info (genre/year)
                            filter_div = card.find('div', class_='filter')
                            filter_text = filter_div.get_text(strip=True) if filter_div else ''
                            
                            # Now visit the drama page for full details
                            drama_data = self.scrape_drama_page(
                                drama_url, 
                                title_text, 
                                thumbnail,
                                filter_text,
                                default_country
                            )
                            
                            if drama_data:
                                if not self.is_duplicate(
                                    drama_data['title'],
                                    drama_data['release_year'],
                                    drama_data['country']
                                ):
                                    self.scraped_dramas.append(drama_data)
                                    drama_count += 1
                                    print(f"      ✅ [{drama_count}] {drama_data['title_arabic'][:50]}")
                                else:
                                    print(f"      ⏭️  Duplicate: {title_text[:30]}")
                            
                            time.sleep(0.5)
                            
                        except Exception as e:
                            print(f"      ⚠️  Error processing card: {e}")
                            continue
                    
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"    ❌ Error on page {page}: {e}")
                    continue
        
        print(f"\n✅ Scraped {drama_count} dramas from ArabDrama TV")
    
    def scrape_drama_page(self, url: str, title: str, thumbnail: str, filter_text: str, default_country: str) -> Optional[Dict]:
        """Scrape individual drama page for full details"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Initialize data
            drama_data = {
                'title': '',
                'title_arabic': '',
                'title_original': '',
                'description': '',
                'description_arabic': '',
                'country': default_country,
                'total_episodes': 0,
                'episode_duration': 60,
                'release_year': datetime.now().year,
                'status': 'completed',
                'genres': ['drama'],
                'thumbnail_url': thumbnail,
                'watch_links': [{
                    'website_name': 'ArabDrama TV',
                    'url': url,
                    'language': 'arabic',
                    'episodes_available': 0
                }],
                'scraped_from_site': 'ArabDrama TV',
            }
            
            # Parse title (format: "Arabic Title English Title" or just Arabic)
            title = title.strip()
            
            # Check if title contains both Arabic and English
            # Split by common patterns
            if ' - ' in title:
                parts = title.split(' - ', 1)
                drama_data['title_arabic'] = parts[0].strip()
                drama_data['title'] = parts[1].strip()
            elif re.search(r'[\u0600-\u06FF]', title):
                # Has Arabic characters
                drama_data['title_arabic'] = title
                drama_data['title'] = title
            else:
                drama_data['title'] = title
                drama_data['title_arabic'] = title
            
            # Extract info from page content
            content_div = soup.find('div', class_='entry-content')
            if content_div:
                content_text = content_div.get_text()
                
                # Extract year
                year = self.extract_year(content_text)
                drama_data['release_year'] = year
                
                # Extract episodes
                ep_match = re.search(r'عدد الحلقات[:\s]*(\d+)', content_text)
                if ep_match:
                    drama_data['total_episodes'] = int(ep_match.group(1))
                    drama_data['watch_links'][0]['episodes_available'] = drama_data['total_episodes']
                
                # Extract genre
                genre_match = re.search(r'النوع[:\s]*([^\n]+)', content_text)
                if genre_match:
                    genres_text = genre_match.group(1).strip()
                    genres_list = [g.strip() for g in re.split(r'[،,/]', genres_text)]
                    drama_data['genres'] = self.map_genre(genres_list)
                
                # Extract country
                country_match = re.search(r'البلد[:\s]*([^\n]+)', content_text)
                if country_match:
                    drama_data['country'] = self.map_country(country_match.group(1))
                
                # Extract description (القصة)
                desc_match = re.search(r'القصة[:\s]*([^\n]{50,})', content_text)
                if desc_match:
                    drama_data['description_arabic'] = desc_match.group(1).strip()
                    drama_data['description'] = drama_data['description_arabic']
                
                # Status
                if 'مستمر' in content_text or 'يعرض' in content_text:
                    drama_data['status'] = 'ongoing'
            
            return drama_data
            
        except Exception as e:
            print(f"        ⚠️  Error scraping page: {e}")
            return None
    
    def save_to_json(self, filename: str = 'scraped_dramas.json'):
        """Save to JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.scraped_dramas, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Saved {len(self.scraped_dramas)} dramas to {filename}")
        return filename
    
    def print_summary(self):
        """Print summary"""
        print(f"\n" + "="*60)
        print(f"📊 SCRAPING SUMMARY")
        print(f"="*60)
        print(f"Total dramas: {len(self.scraped_dramas)}")
        
        # By country
        countries = {}
        for drama in self.scraped_dramas:
            country = drama['country']
            countries[country] = countries.get(country, 0) + 1
        
        print(f"\n📍 By Country:")
        for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True):
            print(f"  {country}: {count}")
        
        # By year
        years = {}
        for drama in self.scraped_dramas:
            year = drama['release_year']
            years[year] = years.get(year, 0) + 1
        
        print(f"\n📅 By Year:")
        for year, count in sorted(years.items(), reverse=True):
            print(f"  {year}: {count}")
        
        print(f"="*60)


def main():
    print("🎬 ARABIC DRAMA SCRAPER (FIXED VERSION)")
    print("="*60)
    
    scraper = DramaScraper()
    
    # Scrape dramas (adjust max_dramas as needed)
    scraper.scrape_aradrama_tv(max_dramas=100)  # Change to 500 for more
    
    # Print summary
    scraper.print_summary()
    
    # Save to JSON
    output_file = scraper.save_to_json('scraped_dramas_FIXED.json')
    
    print(f"\n✅ DONE!")
    print(f"\n💡 NEXT: Import this file into Django:")
    print(f"   python manage.py import_dramas {output_file}")


if __name__ == '__main__':
    main()