#!/usr/bin/env python3
"""
Fix Watch Links - Convert Search URLs to Real Drama Page URLs
Goes through all existing links and updates them to actual drama pages
"""

import os
import django
import sys
import time
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dramahere.settings')
django.setup()

from Tafarraj.models import Drama, WatchLink


class LinkFixer:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.fixed_count = 0
        self.failed_count = 0
        self.already_good_count = 0
    
    def is_search_url(self, url):
        """Check if URL is a search page"""
        search_patterns = ['?s=', 'search?q=', '/search/', '?q=']
        return any(pattern in url for pattern in search_patterns)
    
    def extract_drama_page_from_search(self, search_url, drama_title):
        """Visit search page and extract actual drama page URL"""
        try:
            response = requests.get(search_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find drama links (common patterns)
            for link in soup.find_all('a', href=re.compile(r'/(serie|series|drama|episode|post)/')):
                href = link.get('href', '')
                if not href:
                    continue
                
                # Make absolute URL
                if not href.startswith('http'):
                    base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(search_url))
                    href = urljoin(base_url, href)
                
                # Skip if it's still a search URL
                if self.is_search_url(href):
                    continue
                
                # Skip episode pages, we want series page
                if '/episode/' in href or '/ep-' in href or '/الحلقة' in href:
                    continue
                
                # Return first valid drama page
                return href
            
            return None
            
        except Exception as e:
            return None
    
    def fix_link(self, link):
        """Fix a single watch link"""
        try:
            # Check if it's already a good link
            if not self.is_search_url(link.url):
                self.already_good_count += 1
                return True
            
            print(f"  🔧 Fixing: {link.website_name}")
            
            # Extract real drama page URL
            real_url = self.extract_drama_page_from_search(link.url, link.drama.title)
            
            if real_url:
                link.url = real_url
                link.save()
                self.fixed_count += 1
                print(f"    ✅ Fixed: {real_url[:60]}")
                return True
            else:
                self.failed_count += 1
                print(f"    ❌ Could not find drama page")
                return False
                
        except Exception as e:
            self.failed_count += 1
            print(f"    ❌ Error: {str(e)}")
            return False
    
    def fix_all_links(self, start_id=None, end_id=None, batch_size=50):
        """Fix all links in database"""
        print("="*70)
        print("🔧 FIXING WATCH LINKS - CONVERTING SEARCH URLS TO REAL PAGES")
        print("="*70)
        
        # Get all dramas
        dramas = Drama.objects.all().order_by('id')
        
        if start_id:
            dramas = dramas.filter(id__gte=start_id)
        if end_id:
            dramas = dramas.filter(id__lte=end_id)
        
        dramas = dramas[:batch_size]
        
        total_dramas = dramas.count()
        print(f"\n📊 Processing {total_dramas} dramas")
        print(f"⏱️  Estimated time: {total_dramas * 0.5:.0f} minutes")
        print("="*70)
        
        for i, drama in enumerate(dramas, 1):
            print(f"\n[{i}/{total_dramas}] 📺 {drama.title_arabic or drama.title}")
            
            links = drama.links.all()
            
            if links.count() == 0:
                print("  ⏭️  No links to fix")
                continue
            
            print(f"  📊 {links.count()} links to check")
            
            for link in links:
                self.fix_link(link)
                time.sleep(0.5)  # Be polite
            
            time.sleep(1)  # Pause between dramas
        
        # Print summary
        print("\n" + "="*70)
        print("📊 SUMMARY")
        print("="*70)
        print(f"✅ Fixed: {self.fixed_count} links")
        print(f"✓  Already good: {self.already_good_count} links")
        print(f"❌ Failed: {self.failed_count} links")
        print(f"📊 Total processed: {self.fixed_count + self.already_good_count + self.failed_count} links")
        print("="*70)


def main():
    """
    USAGE:
    
    Test with first 10 dramas:
        python fix_watch_links.py
    
    Process specific range:
        python fix_watch_links.py 1 100
    
    Process all (use carefully - takes hours):
        python fix_watch_links.py 1 2500
    """
    
    fixer = LinkFixer()
    
    if len(sys.argv) >= 3:
        start_id = int(sys.argv[1])
        end_id = int(sys.argv[2])
        batch_size = int(sys.argv[3]) if len(sys.argv) >= 4 else 1000
    else:
        # Default: Test with first 10 dramas
        start_id = 1
        end_id = None
        batch_size = 10
    
    print(f"\n⚙️  Configuration:")
    print(f"   Start ID: {start_id}")
    print(f"   End ID: {end_id or 'Auto'}")
    print(f"   Batch size: {batch_size}")
    
    # Calculate rough time estimate
    total_links = WatchLink.objects.filter(
        drama__id__gte=start_id
    )
    if end_id:
        total_links = total_links.filter(drama__id__lte=end_id)
    total_links = total_links[:batch_size * 10].count()  # Rough estimate
    
    estimated_minutes = (total_links * 0.5) / 60
    print(f"\n⏱️  Estimated time: {estimated_minutes:.1f} hours")
    print(f"   ({total_links} links × 0.5 sec each)")
    
    print("\n⚠️  WARNING: This will modify your database!")
    print("   - Search URLs will be replaced with actual drama pages")
    print("   - Links that can't be fixed will remain unchanged")
    print("   - Failed links can be deleted later")
    
    input("\nPress ENTER to start or Ctrl+C to cancel...")
    
    fixer.fix_all_links(start_id, end_id, batch_size)
    
    print("\n✅ DONE!")
    print("\n💡 NEXT STEPS:")
    print("   1. Review the failed links")
    print("   2. Run again on next batch of dramas")
    print("   3. Or delete failed links and add fresh ones")


if __name__ == '__main__':
    main()