#!/usr/bin/env python3
"""
Asia2TV Scraper - 2025-2026 Only (FAST VERSION)
Scrapes ONLY first 10 pages of each category for speed
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from datetime import datetime
from typing import List, Dict, Optional
import unicodedata


class Asia2TV_Fast_Scraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'ar,en-US;q=0.9,en;q=0.8'
        }
        self.dramas = []
        self.seen_titles = set()
        self.base_url = 'https://asia2tv.com'
        
    def normalize_title(self, title: str) -> str:
        """Normalize title for duplicate detection"""
        title = unicodedata.normalize('NFKD', title.lower())
        title = re.sub(r'[^\w\s]', '', title)
        title = re.sub(r'\s+', ' ', title).strip()
        return title

    def extract_year_from_text(self, text: str) -> Optional[int]:
        """Extract 4-digit year from text"""
        years = re.findall(r'\b(202[56])\b', text)
        return int(years[0]) if years else None

    def scrape_drama_page(self, url: str, country: str) -> Optional[Dict]:
        """Scrape full details from a drama page - FAST VERSION"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get page text for year check FIRST
            page_text = soup.get_text()
            
            # Extract year - FAST METHOD
            year = None
            year_match = re.search(r'سنة العرض\s*:\s*(202[56])', page_text)
            if year_match:
                year = int(year_match.group(1))
            else:
                # Try finding in page
                year = self.extract_year_from_text(page_text)
            
            # SKIP if not 2025/2026
            if year not in [2025, 2026]:
                return None
            
            # Initialize drama data
            drama_data = {
                'url': url,
                'title': None,
                'title_arabic': None,
                'title_original': None,
                'country': country,
                'total_episodes': None,
                'episode_duration': 60,
                'release_year': year,
                'status': 'completed',
                'genres': [],
                'thumbnail_url': None,
                'description': None,
                'description_arabic': None,
                'watch_links': []
            }

            # Extract title
            title_elem = soup.find('h1')
            if title_elem:
                title_text = title_elem.get_text(strip=True)
                drama_data['title'] = title_text
                drama_data['title_arabic'] = title_text
            
            # Original title
            subtitle_elem = soup.find('h4')
            if subtitle_elem:
                drama_data['title_original'] = subtitle_elem.get_text(strip=True)
            
            # Episodes
            episode_match = re.search(r'عدد الحلقات\s*:\s*(\d+)', page_text)
            if episode_match:
                drama_data['total_episodes'] = int(episode_match.group(1))
            
            # Genres
            genre_links = soup.find_all('a', href=re.compile(r'/series/tags/'))
            for link in genre_links[:5]:  # Max 5 genres
                genre = link.get_text(strip=True)
                if genre:
                    drama_data['genres'].append(genre)
            
            # Description
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                text = p.get_text(strip=True)
                if len(text) > 50 and 'الاسم' not in text and 'البلد' not in text:
                    drama_data['description'] = text
                    drama_data['description_arabic'] = text
                    break
            
            # Thumbnail
            img_elem = soup.find('img', class_='img-fluid')
            if img_elem and img_elem.get('src'):
                drama_data['thumbnail_url'] = img_elem['src']
            
            # Watch link
            episode_links = soup.find_all('a', href=re.compile(r'/episode/'))
            if episode_links:
                first_ep_link = episode_links[-1].get('href', '')
                if first_ep_link:
                    if not first_ep_link.startswith('http'):
                        first_ep_link = self.base_url + first_ep_link
                    drama_data['watch_links'].append({
                        'server': 'Asia2TV',
                        'url': first_ep_link,
                        'quality': 'HD'
                    })
            
            # Status
            if 'يبث' in page_text:
                drama_data['status'] = 'ongoing'
            elif 'قادم' in page_text:
                drama_data['status'] = 'upcoming'
            
            return drama_data

        except Exception as e:
            return None

    def scrape_category(self, category_name: str, category_url: str, max_pages: int = 10):
        """Scrape category - FAST VERSION"""
        print(f"\n{'='*60}")
        print(f"📂 {category_name}")
        print(f"{'='*60}")
        
        country_map = {
            'Korean': 'South Korea',
            'Chinese': 'China',
            'Japanese': 'Japan'
        }
        country = country_map.get(category_name, 'unknown')
        
        for page in range(1, max_pages + 1):
            try:
                page_url = category_url if page == 1 else f"{category_url}?page={page}"
                
                print(f"\n→ Page {page}/{max_pages}")
                response = requests.get(page_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find drama links
                drama_links = soup.find_all('a', href=re.compile(r'/serie/[^/]+$'))
                
                if not drama_links:
                    print(f"  ⚠️ No links, stopping")
                    break
                
                # Get unique URLs
                unique_urls = set()
                for link in drama_links:
                    url = link.get('href', '')
                    if url and '/serie/' in url:
                        if not url.startswith('http'):
                            url = self.base_url + url
                        unique_urls.add(url)
                
                print(f"  📋 {len(unique_urls)} dramas to check")
                
                page_count = 0
                for drama_url in unique_urls:
                    drama_slug = drama_url.split('/')[-1]
                    
                    if drama_slug in self.seen_titles:
                        continue
                    
                    # Scrape
                    drama_data = self.scrape_drama_page(drama_url, country)
                    
                    if drama_data:
                        normalized_title = self.normalize_title(drama_data.get('title', ''))
                        if normalized_title not in self.seen_titles:
                            self.dramas.append(drama_data)
                            self.seen_titles.add(normalized_title)
                            self.seen_titles.add(drama_slug)
                            page_count += 1
                            print(f"  ✅ {drama_data['title']} ({drama_data['release_year']})")
                    
                    time.sleep(0.5)  # Fast but polite
                
                print(f"  📊 Added {page_count} dramas from page {page}")
                time.sleep(1)
                
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                continue

    def scrape_all_categories(self, max_pages: int = 10):
        """Scrape all categories"""
        print("🎬 ASIA2TV FAST SCRAPER (2025-2026)")
        print("="*60)
        print(f"⚡ Scraping {max_pages} pages per category")
        print("="*60)
        
        categories = {
            'Korean': '/serie/genre/الدراما-الكورية',
            'Chinese': '/serie/genre/chinese',
            'Japanese': '/serie/genre/japanese'
        }
        
        for cat_name, cat_path in categories.items():
            cat_url = self.base_url + cat_path
            self.scrape_category(cat_name, cat_url, max_pages)
        
        print("\n" + "="*60)
        print("✅ DONE!")
        print("="*60)

    def save_to_json(self, filename: str = 'asia2tv_2025_2026.json'):
        """Save to JSON"""
        output = {
            'scrape_date': datetime.now().isoformat(),
            'total_dramas': len(self.dramas),
            'year_filter': '2025-2026',
            'source': 'asia2tv.com',
            'dramas': self.dramas
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Saved {len(self.dramas)} dramas to {filename}")
        return filename

    def print_summary(self):
        """Print summary"""
        print("\n" + "="*60)
        print(f"📊 TOTAL: {len(self.dramas)} dramas")
        print("="*60)
        
        if len(self.dramas) == 0:
            return
        
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
    scraper = Asia2TV_Fast_Scraper()
    
    # FAST: Only 10 pages per category
    scraper.scrape_all_categories(max_pages=10)
    
    # Save
    filename = scraper.save_to_json('asia2tv_2025_2026.json')
    
    # Summary
    scraper.print_summary()
    
    print("\n🎯 NEXT:")
    print(f"python manage.py import_scraped_dramas {filename}")


if __name__ == '__main__':
    main()