import os
import sys
import django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dramahere.settings")
django.setup()

from Tafarraj.models import Drama, WatchLink
from django.db.models import Count

def verify_dramas():
    print("\n" + "="*80)
    print("DRAMA DATABASE VERIFICATION REPORT")
    print("="*80 + "\n")
    
    # Get all dramas
    all_dramas = Drama.objects.all()
    total_count = all_dramas.count()
    
    print(f"📊 TOTAL DRAMAS IN DATABASE: {total_count}\n")
    
    # Check dramas without thumbnails
    no_thumbnail = Drama.objects.filter(thumbnail__isnull=True) | Drama.objects.filter(thumbnail='')
    
    print("="*80)
    print(f"🖼️  DRAMAS WITHOUT THUMBNAILS: {no_thumbnail.count()}")
    print("="*80)
    
    if no_thumbnail.exists():
        # Group by country
        countries = no_thumbnail.values_list('country', flat=True).distinct()
        
        for country in countries:
            country_dramas = no_thumbnail.filter(country=country)
            count = country_dramas.count()
            display_name = dict(Drama._meta.get_field('country').choices).get(country, country)
            
            print(f"\n{display_name} ({country}): {count} dramas")
            print("-" * 40)
            
            for drama in country_dramas:
                print(f"  • {drama.title_arabic or drama.title}")
                print(f"    ID: {drama.id} | Year: {drama.release_year}")
    else:
        print("✅ All dramas have thumbnails!\n")
    
    # Check dramas without watch links
    no_links = Drama.objects.annotate(link_count=Count('links')).filter(link_count=0)
    
    print("\n" + "="*80)
    print(f"🔗 DRAMAS WITHOUT WATCH LINKS: {no_links.count()}")
    print("="*80)
    
    if no_links.exists():
        # Group by country
        countries = no_links.values_list('country', flat=True).distinct()
        
        for country in countries:
            country_dramas = no_links.filter(country=country)
            count = country_dramas.count()
            display_name = dict(Drama._meta.get_field('country').choices).get(country, country)
            
            print(f"\n{display_name} ({country}): {count} dramas")
            print("-" * 40)
            
            for drama in country_dramas:
                print(f"  • {drama.title_arabic or drama.title}")
                print(f"    ID: {drama.id} | Year: {drama.release_year}")
    else:
        print("✅ All dramas have watch links!\n")
    
    # Summary by country
    print("\n" + "="*80)
    print("📈 SUMMARY BY COUNTRY")
    print("="*80 + "\n")
    
    countries = Drama.objects.values_list('country', flat=True).distinct()
    
    for country in countries:
        country_dramas = Drama.objects.filter(country=country)
        total = country_dramas.count()
        with_links = country_dramas.annotate(link_count=Count('links')).filter(link_count__gt=0).count()
        with_thumb = country_dramas.exclude(thumbnail__isnull=True).exclude(thumbnail='').count()
        display_name = dict(Drama._meta.get_field('country').choices).get(country, country)
        
        print(f"{display_name} ({country}):")
        print(f"  Total: {total}")
        print(f"  ✓ With Thumbnails: {with_thumb}/{total} ({int(with_thumb/total*100) if total > 0 else 0}%)")
        print(f"  ✓ With Watch Links: {with_links}/{total} ({int(with_links/total*100) if total > 0 else 0}%)")
        print()
    
    print("="*80)
    print("END OF REPORT")
    print("="*80 + "\n")


if __name__ == "__main__":
    verify_dramas()