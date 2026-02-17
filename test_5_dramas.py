#!/usr/bin/env python3
"""
TEST SCRIPT - Test on FIRST 5 DRAMAS ONLY
Quick validation test
"""

import os
import django
import sys
import time
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import quote, urljoin

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dramahere.settings')
django.setup()

from Tafarraj.models import Drama, WatchLink
from django.db.models import Count


class WatchLinkFinderTest:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        self.websites = {
            'Asia2TV': {
                'base_url': 'https://asia2tv.com',
                'search_urls': [
                    'https://asia2tv.com/?s={}',
                    'https://asia2tv.com/search?q={}',
                    'https://asia2tv.com/search/{}'
                ],
                'enabled': True,
                'types': ['korean', 'japanese', 'chinese']
            },
            'ArabDrama TV': {
                'base_url': 'https://aradramatv.cc',
                'search_urls': [
                    'https://aradramatv.cc/?s={}',
                    'https://aradramatv.cc/search?q={}',
                    'https://aradramatv.cc/search/{}'
                ],
                'enabled': True,
                'types': ['korean', 'japanese', 'chinese']
            },
            'Dramacool': {
                'base_url': 'https://dramacool.asia',
                'search_urls': [
                    'https://dramacool.asia/search?keyword={}',
                    'https://dramacool.asia/search?q={}',
                    'https://dramacool.asia/?s={}'
                ],
                'enabled': True,
                'types': ['korean', 'japanese', 'chinese']
            },
            'Akwam': {
                'base_url': 'https://akwam.to',
                'search_urls': [
                    'https://akwam.to/search?q={}',
                    'https://akwam.to/?s={}',
                    'https://akwam.to/search/{}'
                ],
                'enabled': True,
                'types': ['turkish']
            },
            '3isk (قصة عشق)': {
                'base_url': 'https://3isk.biz',
                'search_urls': [
                    'https://3isk.biz/?s={}',
                    'https://3isk.biz/search?q={}',
                    'https://3isk.biz/search/{}'
                ],
                'enabled': True,
                'types': ['turkish']
            },
            'Shahid4U': {
                'base_url': 'https://shahid4u.casa',
                'search_urls': [
                    'https://shahid4u.casa/?s={}',
                    'https://shahid4u.casa/search?q={}',
                    'https://shahid4u.casa/search/{}'
                ],
                'enabled': True,
                'types': ['korean', 'japanese', 'chinese', 'turkish']
            },
            'FaselHD': {
                'base_url': 'https://faselhd.cloud',
                'search_urls': [
                    'https://faselhd.cloud/?s={}',
                    'https://faselhd.cloud/search?q={}',
                    'https://faselhd.cloud/search/{}'
                ],
                'enabled': True,
                'types': ['korean', 'japanese', 'chinese', 'turkish']
            },
            'EgyBest': {
                'base_url': 'https://egybest.red',
                'search_urls': [
                    'https://egybest.red/?s={}',
                    'https://egybest.red/search?q={}',
                    'https://egybest.red/search/{}'
                ],
                'enabled': True,
                'types': ['korean', 'japanese', 'chinese', 'turkish']
            }
        }
    
    
    def has_episode_links(self, soup) -> bool:
        """Check if page has ACTUAL episode links (requires at least 3)"""
        try:
            episode_links = soup.find_all('a', href=re.compile(r'(episode|ep-|ep_|الحلقة|حلقة-|حلقة_)', re.I))
            return len(episode_links) >= 3
        except:
            return False
    
    def has_episode_blocks(self, soup) -> bool:
        """Detect episode list blocks (JS-based, video players, Telegram embeds)"""
        try:
            blocks = soup.find_all(
                ['div', 'ul', 'section', 'table'],
                class_=re.compile(r'(episodes|servers|watch|play|list|video|player)', re.I)
            )
            return len(blocks) >= 1
        except:
            return False
    
    def is_valid_drama_page(self, page_content: str, drama_title: str, arabic_title: str) -> bool:
        """Validate if page actually contains the drama"""
        try:
            text = page_content.lower()
            score = 0
            
            if drama_title and len(drama_title) > 3:
                if drama_title.lower() in text:
                    score += 2
            
            if arabic_title and len(arabic_title) > 2:
                if arabic_title in page_content:
                    score += 2
            
            if "حلقة" in page_content or "الحلقة" in page_content:
                score += 1
            
            if "episode" in text or "ep." in text or "ep " in text:
                score += 1
            
            watch_keywords = ["مشاهدة", "watch", "play", "video", "stream"]
            if any(word in text for word in watch_keywords):
                score += 1
            
            if "مسلسل" in page_content or "drama" in text or "series" in text:
                score += 1
            
            return score >= 3
            
        except Exception as e:
            return False
    
    def get_drama_details_from_page(self, url: str, website_name: str) -> dict:
        """Get drama details (thumbnail, episodes)"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            details = {
                'thumbnail_url': None,
                'episodes_available': None
            }
            
            thumbnail = None
            
            og_image = soup.find('meta', property='og:image')
            if og_image:
                thumbnail = og_image.get('content')
            
            if not thumbnail:
                twitter_image = soup.find('meta', property='twitter:image')
                if twitter_image:
                    thumbnail = twitter_image.get('content')
            
            if not thumbnail:
                img = soup.find('img', class_=re.compile(r'(poster|thumbnail|drama|serie|cover|movie-image)', re.I))
                if img:
                    thumbnail = img.get('src') or img.get('data-src') or img.get('data-original')
            
            if not thumbnail:
                for img in soup.find_all('img'):
                    src = img.get('src') or img.get('data-src') or img.get('data-original')
                    if src:
                        src_lower = src.lower()
                        if any(keyword in src_lower for keyword in ['poster', 'cover', 'thumb', 'image']):
                            thumbnail = src
                            break
            
            if thumbnail and not thumbnail.startswith('http'):
                thumbnail = urljoin(url, thumbnail)
            
            details['thumbnail_url'] = thumbnail
            
            page_text = soup.get_text()
            
            episode_match = re.search(r'(\d+)\s*(حلقة|الحلقة)', page_text, re.IGNORECASE)
            if episode_match:
                details['episodes_available'] = int(episode_match.group(1))
            else:
                episode_match = re.search(r'(\d+)\s*(episodes?|eps)', page_text, re.IGNORECASE)
                if episode_match:
                    details['episodes_available'] = int(episode_match.group(1))
            
            return details
            
        except Exception as e:
            return {'thumbnail_url': None, 'episodes_available': None}
    
    def search_drama_on_website(self, drama_title: str, website_name: str, website_config: dict) -> list:
        """Returns LIST of candidate URLs - tries multiple search URLs"""
        search_query = quote(drama_title)
        all_candidates = []
        
        for search_url_template in website_config['search_urls']:
            try:
                search_url = search_url_template.format(search_query)
                response = requests.get(search_url, headers=self.headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Reject soft-404 / empty result pages
                page_text = soup.get_text().lower()
                if any(x in page_text for x in [
                    "no results",
                    "not found",
                    "لم يتم العثور",
                    "لا توجد نتائج",
                    "404"
                ]):
                    continue
                
                candidates = []
                
                for link in soup.find_all('a', href=re.compile(r'/(serie|series|drama|show)/', re.I)):
                    url = link.get('href', '')
                    if url:
                        if not url.startswith('http'):
                            url = urljoin(website_config['base_url'], url)
                        if url not in candidates and url != website_config['base_url']:
                            candidates.append(url)
                        if len(candidates) >= 8:
                            break
                
                if len(candidates) < 5:
                    for link in soup.find_all('a', href=re.compile(r'/\d{3,}')):
                        url = link.get('href', '')
                        if url:
                            if not url.startswith('http'):
                                url = urljoin(website_config['base_url'], url)
                            if url not in candidates and url != website_config['base_url']:
                                candidates.append(url)
                            if len(candidates) >= 8:
                                break
                
                if len(candidates) < 3:
                    for link in soup.find_all('a', href=True):
                        url = link.get('href', '')
                        if url and len(url) > 20:
                            if not url.startswith('http'):
                                url = urljoin(website_config['base_url'], url)
                            if url not in candidates and url != website_config['base_url']:
                                if not any(skip in url.lower() for skip in ['/tag/', '/category/', '/author/', '/page/', '?s=']):
                                    candidates.append(url)
                            if len(candidates) >= 8:
                                break
                
                all_candidates.extend(candidates)
                if len(all_candidates) >= 5:
                    break
                    
            except Exception as e:
                continue
        
        return list(dict.fromkeys(all_candidates))[:10]
    
    def add_watch_links_to_drama(self, drama_id: int):
        """Test on one drama"""
        try:
            drama = Drama.objects.get(id=drama_id)
            
            print(f"\n{'='*70}")
            print(f"📺 DRAMA: {drama.title_arabic or drama.title}")
            print(f"   ID: {drama.id}")
            print(f"   Country: {drama.country or 'Unknown'}")
            print(f"   Current thumbnail: {'✅ Yes' if drama.thumbnail_url else '❌ Missing'}")
            print(f"   Existing links: {WatchLink.objects.filter(drama=drama).count()}")
            print(f"{'='*70}")
            
            search_titles = []
            if drama.title_arabic:
                search_titles.append(drama.title_arabic)
            if drama.title and drama.title != drama.title_arabic:
                search_titles.append(drama.title)
            
            if not search_titles:
                print(f"    ⚠️  No valid titles to search")
                return
            
            # Generate normalized title variants
            variants = set()
            for t in search_titles:
                variants.add(t)
                cleaned = re.sub(r'[^a-zA-Z0-9\u0600-\u06FF\s]', '', t)
                if cleaned:
                    variants.add(cleaned)
                no_season = re.sub(r'(Season|الموسم)\s*\d+', '', t, flags=re.I).strip()
                if no_season and no_season != t:
                    variants.add(no_season)
                if ':' in t:
                    before_colon = t.split(':')[0].strip()
                    if before_colon:
                        variants.add(before_colon)
            
            search_titles = [v for v in variants if len(v) > 2]
            print(f"🔍 Search variants: {search_titles}")
            
            added_count = 0
            needs_thumbnail = not drama.thumbnail_url or drama.thumbnail_url == ''
            
            # Get drama type for website filtering
            drama_type = drama.country.lower() if drama.country else ""
            if drama_type:
                print(f"🏷️  Drama type: {drama_type}")
            
            for website_name, config in self.websites.items():
                if not config['enabled']:
                    continue
                
                # Filter websites by drama country type
                if drama_type and drama_type not in config['types']:
                    print(f"\n    ⏭️  {website_name}: Skipped (doesn't host {drama_type} dramas)")
                    continue
                
                if WatchLink.objects.filter(drama=drama, website_name=website_name).exists():
                    existing_link = WatchLink.objects.filter(drama=drama, website_name=website_name).first()
                    print(f"\n    🔄 {website_name}: Has existing link, validating...")
                    # Validate existing link
                    try:
                        response = requests.get(existing_link.url, headers=self.headers, timeout=10)
                        if self.is_valid_drama_page(response.text, drama.title or "", drama.title_arabic or ""):
                            print(f"       ✅ Existing link is VALID, keeping it")
                            continue
                        else:
                            print(f"       ❌ Existing link is BROKEN (homepage/category page)")
                            print(f"       🔄 Deleting and searching for new link...")
                            existing_link.delete()
                    except:
                        print(f"       ❌ Existing link is DEAD (can't fetch)")
                        print(f"       🔄 Deleting and searching for new link...")
                        existing_link.delete()
                
                print(f"\n    🌐 {website_name}")
                print(f"       Searching...")
                
                all_candidates = []
                for search_title in search_titles:
                    candidates = self.search_drama_on_website(search_title, website_name, config)
                    all_candidates.extend(candidates)
                    if len(all_candidates) >= 10:
                        break
                
                all_candidates = list(dict.fromkeys(all_candidates))
                
                if not all_candidates:
                    print(f"       ❌ No results found")
                    continue
                
                print(f"       📋 Found {len(all_candidates)} candidates")
                
                drama_url = None
                validated = False
                best_details = None
                fail_reasons = []
                
                for i, candidate_url in enumerate(all_candidates[:10], 1):
                    try:
                        print(f"       Testing #{i}: {candidate_url[:60]}...")
                        response = requests.get(candidate_url, headers=self.headers, timeout=10)
                        response.raise_for_status()
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        text_valid = self.is_valid_drama_page(
                            response.text,
                            drama.title or "",
                            drama.title_arabic or ""
                        )
                        has_episodes = self.has_episode_links(soup) or self.has_episode_blocks(soup)
                        
                        if text_valid and has_episodes:
                            drama_url = candidate_url
                            validated = True
                            best_details = self.get_drama_details_from_page(drama_url, website_name)
                            print(f"       ✅ VALID! (text + episodes)")
                            print(f"       📸 Thumbnail: {'✅ Found' if best_details.get('thumbnail_url') else '❌ Not found'}")
                            print(f"       📺 Episodes: {best_details.get('episodes_available') or 'Unknown'}")
                            break
                        else:
                            reasons = []
                            if not text_valid:
                                reasons.append("title mismatch")
                            if not has_episodes:
                                reasons.append("no episode links")
                            fail_reasons.append(f"#{i}: {', '.join(reasons)}")
                            print(f"       ❌ Failed: {', '.join(reasons)}")
                        
                        time.sleep(0.5)
                        
                    except Exception as e:
                        fail_reasons.append(f"#{i}: {str(e)[:30]}")
                        print(f"       ⚠️  Error: {str(e)[:40]}")
                        continue
                
                if not drama_url or not validated:
                    print(f"       ❌ No valid page found")
                    if fail_reasons:
                        print(f"       📋 Reasons: {' | '.join(fail_reasons[:3])}")
                    continue
                
                if needs_thumbnail and best_details and best_details['thumbnail_url']:
                    drama.thumbnail_url = best_details['thumbnail_url']
                    drama.save()
                    print(f"       🖼️  ✅ THUMBNAIL UPDATED!")
                    needs_thumbnail = False
                
                WatchLink.objects.create(
                    drama=drama,
                    website_name=website_name,
                    url=drama_url,
                    language='arabic',
                    episodes_available=(best_details.get('episodes_available') if best_details else None) or drama.total_episodes or 0
                )
                
                added_count += 1
                print(f"       ✅ LINK SAVED")
                
                time.sleep(1)
            
            print(f"\n{'='*70}")
            print(f"📊 SUMMARY FOR THIS DRAMA:")
            print(f"   ✅ Added {added_count} new links")
            print(f"   🖼️  Thumbnail: {'✅ Updated' if not needs_thumbnail and added_count > 0 else '❌ Still missing' if needs_thumbnail else '✅ Already had'}")
            print(f"{'='*70}")
            
        except Drama.DoesNotExist:
            print(f"  ❌ Drama ID {drama_id} not found")
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    def test_first_5(self):
        """Test on first 5 dramas"""
        print("\n" + "="*70)
        print("🧪 TEST MODE - FIRST 5 DRAMAS")
        print("="*70)
        
        dramas = Drama.objects.all().order_by('id')[:5]
        drama_ids = list(dramas.values_list('id', flat=True))
        
        if not drama_ids:
            print("❌ No dramas found in database!")
            return
        
        print(f"📋 Testing on drama IDs: {drama_ids}")
        print(f"🌐 Websites to test: {len([k for k, v in self.websites.items() if v['enabled']])}")
        print("="*70)
        
        input("\nPress ENTER to start test...")
        
        for i, drama_id in enumerate(drama_ids, 1):
            print(f"\n\n{'#'*70}")
            print(f"TEST {i}/5")
            print(f"{'#'*70}")
            self.add_watch_links_to_drama(drama_id)
            time.sleep(2)
        
        print("\n\n" + "="*70)
        print("✅ TEST COMPLETE!")
        print("="*70)
        print("\n📊 RESULTS:")
        for drama_id in drama_ids:
            drama = Drama.objects.get(id=drama_id)
            link_count = WatchLink.objects.filter(drama=drama).count()
            print(f"   Drama {drama_id} ({drama.title[:30]}...): {link_count} links")
        print("="*70)


def main():
    tester = WatchLinkFinderTest()
    tester.test_first_5()


if __name__ == '__main__':
    main()