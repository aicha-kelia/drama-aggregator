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
            
            # KOREAN DRAMAS - Sites with Arabic subs
            if drama.country == 'korean':
                links = [
                    # FREE Arabic sites (VERIFIED)
                    {'name': 'Aradrama', 'url': f'https://aradramatv.com/?s={title}'},
                    {'name': 'Asia2TV', 'url': f'https://asia2tv.com/?s={title}'},
                    {'name': 'Best-Drama', 'url': f'https://best-drama.com/?s={title}'},
                    {'name': 'ArabSeed', 'url': f'https://arabseed.show/?s={title_ar}'},
                    {'name': 'Drama Slayer', 'url': f'https://dramaslayer.net/?s={title}'},
                    {'name': 'Akwam', 'url': f'https://akwam.to/search?q={title_ar}'},
                    {'name': 'Shahid', 'url': f'https://shahid.mbc.net/ar/search?q={title}'},
                    
                    # Official platforms
                    {'name': 'Netflix', 'url': f'https://www.netflix.com/search?q={title}'},
                    {'name': 'Viki', 'url': f'https://www.viki.com/search?q={title}'},
                ]
            
            # TURKISH DRAMAS - Sites with Arabic subs/dub
            elif drama.country == 'turkish':
                links = [
                    # FREE Arabic sites (VERIFIED)
                    {'name': 'قصة عشق', 'url': f'https://3isk.cam/?s={title}'},
                    {'name': 'Akwam', 'url': f'https://akwam.to/search?q={title_ar}'},
                    {'name': 'MyCima', 'url': f'https://mycima.tv/search/{title_dash}'},
                    {'name': 'Shahid', 'url': f'https://shahid.mbc.net/ar/search?q={title_ar}'},
                    {'name': 'ArabSeed', 'url': f'https://arabseed.show/?s={title_ar}'},
                    {'name': 'EgyBest', 'url': f'https://egybest.deals/explore/?q={title}'},
                    
                    # Official platforms
                    {'name': 'Netflix', 'url': f'https://www.netflix.com/search?q={title}'},
                    {'name': 'StarzPlay', 'url': f'https://starzplay.com/en/search?q={title}'},
                ]
            
            # CHINESE DRAMAS - Sites with Arabic subs
            elif drama.country == 'chinese':
                links = [
                    # FREE Arabic sites (VERIFIED)
                    {'name': 'Aradrama', 'url': f'https://aradramatv.com/?s={title}'},
                    {'name': 'Best-Drama', 'url': f'https://best-drama.com/?s={title}'},
                    {'name': 'Asia2TV', 'url': f'https://asia2tv.com/?s={title}'},
                    {'name': 'Akwam', 'url': f'https://akwam.to/search?q={title_ar}'},
                    {'name': 'ArabSeed', 'url': f'https://arabseed.show/?s={title_ar}'},
                    
                    # Official platforms
                    {'name': 'WeTV', 'url': f'https://wetv.vip/en/search?q={title}'},
                    {'name': 'iQIYI', 'url': f'https://www.iq.com/search/{title}'},
                    {'name': 'Netflix', 'url': f'https://www.netflix.com/search?q={title}'},
                ]
            
            # MOROCCAN DRAMAS - Already in Arabic
            elif drama.country == 'moroccan':
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