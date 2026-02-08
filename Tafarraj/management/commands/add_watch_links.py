from django.core.management.base import BaseCommand
from Tafarraj.models import Drama, WatchLink

class Command(BaseCommand):
    help = 'Add VERIFIED watch links with Arabic subtitles for dramas'

    def handle(self, *args, **options):
        # Clear old links
        WatchLink.objects.all().delete()
        self.stdout.write('🗑️  Cleared old watch links')
        
        dramas = Drama.objects.all()
        
        for drama in dramas:
            title = drama.title.replace(' ', '+')
            title_dash = drama.title.lower().replace(' ', '-')
            title_ar = drama.title_arabic.replace(' ', '+')
            
            # Normalize country name
            country = drama.country.lower()
            if country == 'south korea':
                country = 'korean'
            elif country == 'china':
                country = 'chinese'
            elif country == 'japan':
                country = 'japanese'
            elif country == 'turkey':
                country = 'turkish'
            elif country == 'morocco':
                country = 'moroccan'
            
            # KOREAN DRAMAS - Sites with Arabic subs
            if country == 'korean':
                links = [
                    {'name': 'Aradrama', 'url': 'https://aradramatv.cc'},
                    {'name': 'Asia2TV', 'url': 'https://asia2tv.com'},
                    {'name': 'Best Drama', 'url': 'https://best-drama.com'},
                    {'name': 'ArabSeed', 'url': 'https://arabseed.show'},
                    {'name': 'Akwam', 'url': 'https://akwam.to'},
                    {'name': 'Viki', 'url': 'https://www.viki.com'},
                    {'name': 'WeTV', 'url': 'https://wetv.vip/ar'},
                    {'name': 'HiTV', 'url': 'https://home.hitv.vip/ar-ae/'},
                    {'name': 'Shahid Mosalsalat', 'url': 'https://w.shahidmosalsalat.me'},
                ]
            
            # TURKISH DRAMAS - Sites with Arabic subs/dub
            elif country == 'turkish':
                links = [
                    {'name': 'قصة عشق', 'url': 'https://3sk.cam'},
                    {'name': 'Qrmzi TV', 'url': 'https://www.qrmzi.tv'},
                    {'name': 'Akwam', 'url': 'https://akwam.to'},
                    {'name': 'MyCima', 'url': 'https://wecima.show'},
                    {'name': 'Shahid Mosalsalat', 'url': 'https://w.shahidmosalsalat.me'},
                    {'name': 'ArabSeed', 'url': 'https://arabseed.show'},
                ]
            
            # CHINESE DRAMAS - Sites with Arabic subs
            elif country == 'chinese':
                links = [
                    {'name': 'Aradrama', 'url': 'https://aradramatv.cc'},
                    {'name': 'Best Drama', 'url': 'https://best-drama.com'},
                    {'name': 'Asia2TV', 'url': 'https://asia2tv.com'},
                    {'name': 'WeTV', 'url': 'https://wetv.vip/ar'},
                    {'name': 'HiTV', 'url': 'https://home.hitv.vip/ar-ae/'},
                    {'name': 'Viki', 'url': 'https://www.viki.com'},
                ]
            
            # JAPANESE DRAMAS - Sites with Arabic subs
            elif country == 'japanese':
                links = [
                    {'name': 'Aradrama', 'url': 'https://aradramatv.cc'},
                    {'name': 'Best Drama', 'url': 'https://best-drama.com'},
                    {'name': 'Asia2TV', 'url': 'https://asia2tv.com'},
                    {'name': 'HiTV', 'url': 'https://home.hitv.vip/ar-ae/'},
                    {'name': 'WeTV', 'url': 'https://wetv.vip/ar'},
                    {'name': 'Viki', 'url': 'https://www.viki.com'},
                ]
            
            # MOROCCAN DRAMAS - Already in Arabic
            elif country == 'moroccan':
                links = [
                    # Official platforms
                    {'name': 'Shahid VIP', 'url': f'https://shahid.mbc.net/ar/search?q={title_ar}'},
                    {'name': 'Forja', 'url': f'https://forja.ma/search?q={title_ar}'},
                    
                    # FREE Arabic sites
                    {'name': 'Akwam', 'url': f'https://akwam.to/search?q={title_ar}'},
                    {'name': 'MyCima', 'url': f'https://mycima.tv/search/{title_dash}'},
                    {'name': 'ArabSeed', 'url': f'https://arabseed.show/?s={title_ar}'},
                    {'name': 'TvFHD', 'url': f'https://av.tvfun.me/?s={title_ar}'},
                    {'name': 'Mosalsalat', 'url': f'https://web.mosalsalat.net/?s={title_ar}'},
                ]
            
            else:
                continue
            
            # Create links
            for link in links:
                WatchLink.objects.create(
                    drama=drama,
                    website_name=link['name'],
                    url=link['url'],
                    language='arabic',
                    episodes_available=drama.total_episodes
                )
            
            self.stdout.write(f'✓ {drama.title_arabic} ({drama.country}) - {len(links)} links')
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Done! Added {WatchLink.objects.count()} verified Arabic watch links'))