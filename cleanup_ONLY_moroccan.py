#!/usr/bin/env python3
"""
Selective Link Cleanup - Keep Moroccan & Turkish, Delete Broken Korean/Chinese
"""
import os
import sys
import django

# Django setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE')
django.setup()

from Tafarraj.models import Drama, WatchLink
from django.db.models import Count


def analyze_links():
    """Show what will be deleted vs kept"""
    print("="*70)
    print("📊 LINK ANALYSIS - WHAT WILL BE DELETED VS KEPT")
    print("="*70)
    
    # Sites to KEEP (ONLY MOROCCAN)
    keep_sites = [
        'Unknown',
        'TvFHD', 
        'Forja',
        'Mosalsalat'
    ]
    
    # Get all links
    all_links = WatchLink.objects.all()
    
    # Links to KEEP
    keep_links = all_links.filter(server__in=keep_sites)
    
    # Links to DELETE (everything else - mostly broken Korean/Chinese search URLs)
    delete_links = all_links.exclude(server__in=keep_sites)
    
    print(f"\n✅ WILL KEEP: {keep_links.count()} links")
    keep_by_server = keep_links.values('server').annotate(count=Count('id')).order_by('-count')
    for item in keep_by_server:
        print(f"   {item['server']}: {item['count']} links")
    
    print(f"\n❌ WILL DELETE: {delete_links.count()} links")
    delete_by_server = delete_links.values('server').annotate(count=Count('id')).order_by('-count')
    for item in delete_by_server:
        print(f"   {item['server']}: {item['count']} links")
    
    # Check for search URLs in delete list
    search_urls = delete_links.filter(url__contains='?s=')
    print(f"\n🔍 Search URLs to delete: {search_urls.count()}")
    
    return keep_links, delete_links


def delete_broken_links(delete_links):
    """Delete everything except Moroccan links"""
    print("\n" + "="*70)
    print("🗑️  DELETING ALL NON-MOROCCAN LINKS...")
    print("="*70)
    
    count = delete_links.count()
    delete_links.delete()
    
    print(f"✅ Deleted {count} links")
    print("✅ Kept ONLY Moroccan drama links")
    

def show_dramas_needing_links():
    """Show which dramas now need links"""
    print("\n" + "="*70)
    print("📊 DRAMAS THAT NEED NEW LINKS")
    print("="*70)
    
    # Dramas by country
    turkish = Drama.objects.filter(country='Turkey').annotate(link_count=Count('links'))
    korean = Drama.objects.filter(country='South Korea').annotate(link_count=Count('links'))
    chinese = Drama.objects.filter(country='China').annotate(link_count=Count('links'))
    japanese = Drama.objects.filter(country='Japan').annotate(link_count=Count('links'))
    
    turkish_need = turkish.filter(link_count__lt=3).count()
    korean_need = korean.filter(link_count__lt=3).count()
    chinese_need = chinese.filter(link_count__lt=3).count()
    japanese_need = japanese.filter(link_count__lt=3).count()
    
    print(f"\n🇹🇷 Turkish dramas needing links: {turkish_need}/{turkish.count()}")
    print(f"🇰🇷 Korean dramas needing links: {korean_need}/{korean.count()}")
    print(f"🇨🇳 Chinese dramas needing links: {chinese_need}/{chinese.count()}")
    print(f"🇯🇵 Japanese dramas needing links: {japanese_need}/{japanese.count()}")
    print(f"\n📊 TOTAL needing links: {turkish_need + korean_need + chinese_need + japanese_need}")
    

def main():
    print("🎬 SELECTIVE LINK CLEANUP")
    print("="*70)
    print("✅ WILL KEEP: ONLY Moroccan drama links (Unknown, TvFHD, Forja, Mosalsalat)")
    print("❌ WILL DELETE: Everything else (Turkish, Korean, Chinese, Japanese)")
    print("="*70)
    
    # Step 1: Analyze
    keep_links, delete_links = analyze_links()
    
    # Step 2: Confirm
    print("\n" + "="*70)
    print("⚠️  CONFIRMATION")
    print("="*70)
    print(f"This will DELETE {delete_links.count()} links")
    print(f"This will KEEP {keep_links.count()} links (ONLY Moroccan)")
    print("\nMoroccan dramas will keep their links ✅")
    print("ALL other dramas (Turkish, Korean, Chinese, Japanese) will need new links ⚠️")
    
    response = input("\nType 'DELETE' to proceed: ")
    
    if response != 'DELETE':
        print("❌ Cancelled")
        return
    
    # Step 3: Delete
    delete_broken_links(delete_links)
    
    # Step 4: Show what needs links
    show_dramas_needing_links()
    
    print("\n" + "="*70)
    print("✅ CLEANUP COMPLETE!")
    print("="*70)
    print("\n🎯 NEXT STEP:")
    print("Run: python add_watch_links_NO_DUPLICATES.py")
    print("This will add fresh working links to Turkish/Korean/Chinese/Japanese dramas")
    print("="*70)


if __name__ == '__main__':
    main()