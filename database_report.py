#!/usr/bin/env python3
"""
Database Analysis Report
Shows exact state of your drama database and watch links
"""

import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dramahere.settings')
django.setup()

from Tafarraj.models import Drama, WatchLink
from django.db.models import Count
from collections import defaultdict


def generate_report():
    print("="*70)
    print("📊 DRAMA DATABASE ANALYSIS REPORT")
    print("="*70)
    
    # Total dramas
    total_dramas = Drama.objects.count()
    total_links = WatchLink.objects.count()
    
    print(f"\n📚 TOTAL DRAMAS: {total_dramas}")
    print(f"🔗 TOTAL WATCH LINKS: {total_links}")
    print(f"📊 AVERAGE LINKS PER DRAMA: {total_links/total_dramas:.1f}")
    
    # Dramas by link count
    print("\n" + "="*70)
    print("📊 DRAMAS BY LINK COUNT")
    print("="*70)
    
    dramas_with_links = Drama.objects.annotate(link_count=Count('links'))
    
    link_distribution = {
        '0 links': dramas_with_links.filter(link_count=0).count(),
        '1 link': dramas_with_links.filter(link_count=1).count(),
        '2 links': dramas_with_links.filter(link_count=2).count(),
        '3 links': dramas_with_links.filter(link_count=3).count(),
        '4 links': dramas_with_links.filter(link_count=4).count(),
        '5 links': dramas_with_links.filter(link_count=5).count(),
        '6+ links': dramas_with_links.filter(link_count__gte=6).count(),
    }
    
    for category, count in link_distribution.items():
        if count > 0:
            percentage = (count / total_dramas) * 100
            print(f"{category:15} : {count:5} dramas ({percentage:5.1f}%)")
    
    # Links by website
    print("\n" + "="*70)
    print("🌐 LINKS BY WEBSITE")
    print("="*70)
    
    links_by_website = WatchLink.objects.values('website_name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    for item in links_by_website:
        website = item['website_name'] or 'Unknown'
        count = item['count']
        print(f"{website:20} : {count:5} links")
    
    # Check for duplicates
    print("\n" + "="*70)
    print("🔍 DUPLICATE LINKS CHECK")
    print("="*70)
    
    duplicates_found = 0
    duplicate_examples = []
    
    # Check each drama for duplicate URLs
    for drama in Drama.objects.all()[:100]:  # Sample first 100
        urls = list(drama.links.values_list('url', flat=True))
        if len(urls) != len(set(urls)):
            duplicates_found += 1
            if len(duplicate_examples) < 5:
                duplicate_examples.append({
                    'title': drama.title_arabic or drama.title,
                    'total_links': len(urls),
                    'unique_links': len(set(urls)),
                    'duplicates': len(urls) - len(set(urls))
                })
    
    if duplicates_found > 0:
        print(f"⚠️  Found duplicates in {duplicates_found} dramas (from 100 sampled)")
        print("\nExamples:")
        for ex in duplicate_examples:
            print(f"  • {ex['title'][:40]}")
            print(f"    Total: {ex['total_links']}, Unique: {ex['unique_links']}, Duplicates: {ex['duplicates']}")
    else:
        print("✅ No duplicates found in sample")
    
    # Check for same website duplicates
    print("\n" + "="*70)
    print("🔍 SAME-WEBSITE DUPLICATE LINKS")
    print("="*70)
    
    same_website_duplicates = 0
    duplicate_website_examples = []
    
    for drama in Drama.objects.all()[:100]:
        website_counts = defaultdict(int)
        for link in drama.links.all():
            website_counts[link.website_name] += 1
        
        for website, count in website_counts.items():
            if count > 1:
                same_website_duplicates += 1
                if len(duplicate_website_examples) < 5:
                    duplicate_website_examples.append({
                        'title': drama.title_arabic or drama.title,
                        'website': website,
                        'count': count
                    })
                break
    
    if same_website_duplicates > 0:
        print(f"⚠️  Found {same_website_duplicates} dramas with duplicate links from SAME website")
        print("\nExamples:")
        for ex in duplicate_website_examples:
            print(f"  • {ex['title'][:40]}")
            print(f"    {ex['website']}: {ex['count']} links (should be 1)")
    else:
        print("✅ No same-website duplicates found")
    
    # Dramas without thumbnails
    print("\n" + "="*70)
    print("🖼️  THUMBNAILS")
    print("="*70)
    
    dramas_with_thumbnails = Drama.objects.exclude(thumbnail_url='').exclude(thumbnail_url=None).count()
    dramas_without_thumbnails = total_dramas - dramas_with_thumbnails
    
    print(f"✅ Dramas WITH thumbnails: {dramas_with_thumbnails} ({dramas_with_thumbnails/total_dramas*100:.1f}%)")
    print(f"❌ Dramas WITHOUT thumbnails: {dramas_without_thumbnails} ({dramas_without_thumbnails/total_dramas*100:.1f}%)")
    
    # Sample dramas needing attention
    print("\n" + "="*70)
    print("⚠️  DRAMAS NEEDING ATTENTION (Sample)")
    print("="*70)
    
    print("\n🔴 NO LINKS (showing first 10):")
    no_links = dramas_with_links.filter(link_count=0)[:10]
    for drama in no_links:
        print(f"  ID {drama.id}: {drama.title_arabic or drama.title}")
    
    print("\n🟡 1-2 LINKS (showing first 10):")
    few_links = dramas_with_links.filter(link_count__range=(1,2))[:10]
    for drama in few_links:
        link_count = drama.links.count()
        print(f"  ID {drama.id}: {drama.title_arabic or drama.title} ({link_count} links)")
    
    # Summary and recommendations
    print("\n" + "="*70)
    print("💡 RECOMMENDATIONS")
    print("="*70)
    
    need_links = dramas_with_links.filter(link_count__lt=3).count()
    
    if need_links > 0:
        print(f"\n1. 📌 ADD LINKS: {need_links} dramas have fewer than 3 links")
        print(f"   Run: python add_watch_links_NO_DUPLICATES.py")
    
    if same_website_duplicates > 0:
        print(f"\n2. 🧹 CLEAN DUPLICATES: ~{same_website_duplicates} dramas have duplicate links")
        print(f"   Need cleanup script")
    
    if dramas_without_thumbnails > 100:
        print(f"\n3. 🖼️  ADD THUMBNAILS: {dramas_without_thumbnails} dramas missing thumbnails")
        print(f"   Can be added when adding links")
    
    print("\n" + "="*70)
    print("✅ REPORT COMPLETE")
    print("="*70)


if __name__ == '__main__':
    generate_report()