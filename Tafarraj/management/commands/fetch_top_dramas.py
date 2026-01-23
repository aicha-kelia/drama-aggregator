from django.core.management.base import BaseCommand
from Tafarraj.models import Drama, Genre
from Tafarraj.utils import translate_to_arabic, TMDB_API_KEY, TMDB_BASE_URL
import requests
from django.core.files.base import ContentFile
import time

class Command(BaseCommand):
    help = 'Fetch dramas from TMDB with genres'

    def add_arguments(self, parser):
        parser.add_argument('country', type=str, help='KR, TR, CN, IN')
        parser.add_argument('--pages', type=int, default=5)

    def handle(self, *args, **options):
        country = options['country'].upper()
        pages = options['pages']
        
        country_map = {'KR': 'korean', 'TR': 'turkish', 'CN': 'chinese', 'IN': 'indian'}
        
        if country not in country_map:
            self.stdout.write('ERROR: Use KR, TR, CN, or IN')
            return
        
        country_name = country_map[country]
        added = 0
        
        # Fetch TMDB genre list ONCE at the start
        self.stdout.write('Fetching TMDB genre list...')
        genre_resp = requests.get(f"{TMDB_BASE_URL}/genre/tv/list", params={'api_key': TMDB_API_KEY})
        tmdb_genres = {g['id']: g['name'] for g in genre_resp.json().get('genres', [])}
        self.stdout.write(f'Loaded {len(tmdb_genres)} genres from TMDB')
        
        # Create a mapping of TMDB genre IDs to YOUR Genre database IDs
        genre_mapping = {}
        for tmdb_id, tmdb_name in tmdb_genres.items():
            try:
                # Try to find exact match in your database
                db_genre = Genre.objects.get(name=tmdb_name)
                genre_mapping[tmdb_id] = db_genre
            except Genre.DoesNotExist:
                # Create it if doesn't exist
                db_genre = Genre.objects.create(
                    name=tmdb_name,
                    name_arabic=translate_to_arabic(tmdb_name)
                )
                genre_mapping[tmdb_id] = db_genre
                self.stdout.write(f'Created genre: {tmdb_name}')
        
        for page in range(1, pages + 1):
            self.stdout.write(f'--- PAGE {page} ---')
            
            url = f"{TMDB_BASE_URL}/discover/tv"
            params = {
                'api_key': TMDB_API_KEY,
                'with_origin_country': country,
                'sort_by': 'popularity.desc',
                'page': page
            }
            
            resp = requests.get(url, params=params)
            
            if resp.status_code != 200:
                self.stdout.write(f'API ERROR: {resp.status_code}')
                continue
            
            shows = resp.json().get('results', [])
            self.stdout.write(f'Found {len(shows)} shows')
            
            for show in shows:
                name = show.get('name', '')
                
                if Drama.objects.filter(title=name).exists():
                    self.stdout.write(f'SKIP: {name}')
                    continue
                
                # Get details
                detail_url = f"{TMDB_BASE_URL}/tv/{show['id']}"
                detail_resp = requests.get(detail_url, params={'api_key': TMDB_API_KEY})
                detail = detail_resp.json()
                
                # Translate
                title_ar = translate_to_arabic(name) or name
                overview = show.get('overview', '')
                desc_ar = translate_to_arabic(overview) if overview else 'لا يوجد وصف'
                
                # Create drama
                drama = Drama.objects.create(
                    title=name,
                    title_arabic=title_ar,
                    title_original=show.get('original_name', ''),
                    description=show.get('overview', 'No description available'),
                    description_arabic=desc_ar,
                    country=country_name,
                    release_year=int((show.get('first_air_date') or '2000')[:4]),
                    total_episodes=detail.get('number_of_episodes') or 0,
                    episode_duration=detail.get('episode_run_time', [45])[0] if detail.get('episode_run_time') else 45,
                    status='completed' if detail.get('status') == 'Ended' else 'ongoing',
                    current_episode_number=0
                )
                
                # Add genres using the mapping
                genre_ids = show.get('genre_ids', [])
                genres_added = []
                for tmdb_genre_id in genre_ids:
                    if tmdb_genre_id in genre_mapping:
                        db_genre = genre_mapping[tmdb_genre_id]
                        drama.genres.add(db_genre)
                        genres_added.append(db_genre.name_arabic)
                
                # Image
                if show.get('poster_path'):
                    img_url = f"https://image.tmdb.org/t/p/w500{show['poster_path']}"
                    img = requests.get(img_url)
                    drama.thumbnail.save(f'{drama.id}.jpg', ContentFile(img.content), save=True)
                
                genres_str = ", ".join(genres_added) if genres_added else "لا توجد أنواع"
                self.stdout.write(self.style.SUCCESS(f'ADDED: {title_ar} | {genres_str}'))
                added += 1
                time.sleep(0.5)
        
        self.stdout.write(f'\nTOTAL ADDED: {added}')