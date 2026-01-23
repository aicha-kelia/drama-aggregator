from django.core.management.base import BaseCommand
from Tafarraj.models import Drama, WatchLink

class Command(BaseCommand):
    help = 'Add reliable watch links for dramas'

    def handle(self, *args, **options):
        # Clear old links
        WatchLink.objects.all().delete()
        self.stdout.write('🗑️  Cleared old watch links')
        
        dramas = Drama.objects.all()
        
        for drama in dramas:
            title = drama.title.replace(' ', '+')
            title_dash = drama.title.lower().replace(' ', '-')
            title_ar = drama.title_arabic.replace(' ', '+')
            
            # KOREAN DRAMAS - Most reliable sources
            if drama.country == 'korean':
                links = [
                    # International platforms (most reliable)
                    {'name': 'Viki', 'url': f'https://www.viki.com/search?q={title}'},
                    {'name': 'Netflix', 'url': f'https://www.netflix.com/search?q={title}'},
                    {'name': 'MyDramaList', 'url': f'https://mydramalist.com/search?q={title}'},
                    
                    # Arabic platforms
                    {'name': 'Shahid', 'url': f'https://shahid.mbc.net/ar/search?q={title}'},
                    {'name': 'Akwam', 'url': f'https://akwam.to/search?q={title_ar}'},
                    {'name': 'Faselhd', 'url': f'https://faselhd.io/?s={title_ar}'},
                ]
            
            # TURKISH DRAMAS
            elif drama.country == 'turkish':
                links = [
                    # Turkish drama specialists
                    {'name': 'قصة عشق', 'url': f'https://3isk.cam/?s={title}'},
                    {'name': 'قصة عشق الاصلي', 'url': f'https://www.3sk.tv/?s={title}'},
                    
                    # Arabic platforms
                    {'name': 'Shahid', 'url': f'https://shahid.mbc.net/ar/search?q={title_ar}'},
                    {'name': 'Akwam', 'url': f'https://akwam.to/search?q={title_ar}'},
                    {'name': 'MyCima', 'url': f'https://mycima.tv/search/{title_dash}'},
                    {'name': 'Egybest', 'url': f'https://egybest.deals/explore/?q={title}'},
                ]
            
            # CHINESE DRAMAS
            elif drama.country == 'chinese':
                links = [
                    # International platforms
                    {'name': 'Viki', 'url': f'https://www.viki.com/search?q={title}'},
                    {'name': 'WeTV', 'url': f'https://wetv.vip/en/search?q={title}'},
                    {'name': 'iQIYI', 'url': f'https://www.iq.com/search/{title}'},
                    {'name': 'Netflix', 'url': f'https://www.netflix.com/search?q={title}'},
                    
                    # Arabic platforms
                    {'name': 'Akwam', 'url': f'https://akwam.to/search?q={title_ar}'},
                    {'name': 'Shahid', 'url': f'https://shahid.mbc.net/ar/search?q={title_ar}'},
                ]
            
            # INDIAN DRAMAS
            elif drama.country == 'indian':
                links = [
                    # Indian platforms
                    {'name': 'Hotstar', 'url': f'https://www.hotstar.com/in/search?q={title}'},
                    {'name': 'Zee5', 'url': f'https://www.zee5.com/search?q={title}'},
                    
                    # Arabic platforms
                    {'name': 'Shahid', 'url': f'https://shahid.mbc.net/ar/search?q={title_ar}'},
                    {'name': 'Akwam', 'url': f'https://akwam.to/search?q={title_ar}'},
                    {'name': 'MyCima', 'url': f'https://mycima.tv/search/{title_dash}'},
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
            
            self.stdout.write(f'✓ {drama.title_arabic} ({drama.country})')
        
        self.stdout.write(self.style.SUCCESS(f'✅ Done! Added {WatchLink.objects.count()} watch links'))