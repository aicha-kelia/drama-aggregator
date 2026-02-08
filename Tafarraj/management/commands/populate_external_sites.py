"""
Management command to populate external streaming sites
Run with: python manage.py populate_external_sites
"""

from django.core.management.base import BaseCommand
from Tafarraj.models import ExternalStreamingSite


class Command(BaseCommand):
    help = 'Populate external streaming sites database'

    def handle(self, *args, **kwargs):
        
        sites = [
            # Sites we tested
            {
                "name": "ArabDrama TV",
                "url": "https://aradramatv.cc",
                "description": "Korean, Chinese, Japanese dramas with Arabic subtitles",
                "countries": ["KR", "CN", "JP", "TH"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
            {
                "name": "WeTV",
                "url": "https://wetv.vip/ar",
                "description": "Official streaming platform for Chinese and Korean dramas",
                "countries": ["KR", "CN", "TH"],
                "has_arabic_subs": True,
                "requires_subscription": True,
            },
            {
                "name": "HiTV",
                "url": "https://home.hitv.vip/ar-ae/",
                "description": "Asian dramas with Arabic subtitles",
                "countries": ["KR", "CN", "JP"],
                "has_arabic_subs": True,
                "requires_subscription": True,
            },
            {
                "name": "Qrmzi TV",
                "url": "https://www.qrmzi.tv/all-turkish-series/",
                "description": "Turkish series with Arabic subtitles",
                "countries": ["TR"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
            {
                "name": "Esheaq",
                "url": "https://n.esheaq.onl",
                "description": "Korean and Turkish dramas",
                "countries": ["KR", "TR"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
            {
                "name": "Best Drama",
                "url": "https://best-drama.com",
                "description": "Chinese, Korean, and Japanese dramas",
                "countries": ["KR", "CN", "JP", "TH"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
            {
                "name": "Shahid Mosalsalat",
                "url": "https://w.shahidmosalsalat.me",
                "description": "Turkish and Korean series",
                "countries": ["KR", "TR"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
            {
                "name": "Akwam",
                "url": "https://akwam.to",
                "description": "Asian dramas and series",
                "countries": ["KR", "CN", "JP", "TR"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
            {
                "name": "Asia2TV",
                "url": "https://asia2tv.com",
                "description": "Asian movies and series",
                "countries": ["KR", "CN", "JP", "TH"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
            {
                "name": "Dramacool",
                "url": "https://dramacool.asia",
                "description": "Korean, Chinese, Japanese dramas with English subs (some Arabic)",
                "countries": ["KR", "CN", "JP", "TH"],
                "has_arabic_subs": False,
                "requires_subscription": False,
            },
            {
                "name": "3isk (قصة عشق)",
                "url": "https://3isk.biz",
                "description": "Turkish and Korean series",
                "countries": ["KR", "TR"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
            {
                "name": "Shahid4U",
                "url": "https://shahid4u.casa",
                "description": "Movies and series",
                "countries": ["ALL"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
            {
                "name": "FaselHD",
                "url": "https://faselhd.cloud",
                "description": "Asian dramas and movies",
                "countries": ["KR", "CN", "JP", "TR"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
            {
                "name": "EgyBest",
                "url": "https://egybest.red",
                "description": "Movies and series",
                "countries": ["ALL"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
            
            # Additional popular Arabic sites
            {
                "name": "Arabseed",
                "url": "https://arabseed.ink",
                "description": "Asian dramas with Arabic subtitles",
                "countries": ["KR", "CN", "JP", "TR", "TH"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
            {
                "name": "Cima4u",
                "url": "https://cima4u.cam",
                "description": "Movies and series",
                "countries": ["ALL"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
            {
                "name": "Mycima",
                "url": "https://mycima.tube",
                "description": "Asian dramas and movies",
                "countries": ["KR", "CN", "JP", "TR"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
            {
                "name": "Movizland",
                "url": "https://movizland.online",
                "description": "Movies and series",
                "countries": ["ALL"],
                "has_arabic_subs": True,
                "requires_subscription": False,
            },
        ]
        
        created_count = 0
        updated_count = 0
        
        for idx, site_data in enumerate(sites, 1):
            site, created = ExternalStreamingSite.objects.update_or_create(
                name=site_data["name"],
                defaults={
                    "url": site_data["url"],
                    "description": site_data["description"],
                    "countries": site_data["countries"],
                    "has_arabic_subs": site_data["has_arabic_subs"],
                    "requires_subscription": site_data["requires_subscription"],
                    "is_active": True,
                    "display_order": idx,
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {site.name}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'⟳ Updated: {site.name}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Done! Created: {created_count}, Updated: {updated_count}'))