from django.core.management.base import BaseCommand
from Tafarraj.models import Drama, Genre
from Tafarraj.utils import TMDB_API_KEY, TMDB_BASE_URL
import requests
import time
from django.db.models import Count

class Command(BaseCommand):
    help = 'Fix dramas missing genres by fetching from TMDB'

    def add_arguments(self, parser):
        parser.add_argument('--country', type=str, help='Fix specific country (KR, TR, CN, IN)')
        parser.add_argument('--limit', type=int, default=0, help='Limit number of dramas to fix (0 = all)')
        parser.add_argument('--dry-run', action='store_true', help='Show what would be fixed without making changes')

    def handle(self, *args, **options):
        country = options.get('country')
        limit = options['limit']
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made\n'))
        
        # Get all TMDB genres first
        try:
            genre_resp = requests.get(
                f"{TMDB_BASE_URL}/genre/tv/list", 
                params={'api_key': TMDB_API_KEY},
                timeout=10
            )
            tmdb_genres = {g['id']: g['name'] for g in genre_resp.json().get('genres', [])}
            self.stdout.write(f'Loaded {len(tmdb_genres)} genres from TMDB\n')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to fetch genres: {e}'))
            return
        
        # Find dramas without genres
        query = Drama.objects.annotate(genre_count=Count('genres')).filter(genre_count=0)
        
        if country:
            country_map = {'KR': 'korean', 'TR': 'turkish', 'CN': 'chinese', 'IN': 'indian'}
            country_name = country_map.get(country.upper())
            if country_name:
                query = query.filter(country=country_name)
                self.stdout.write(f'Filtering by country: {country_name}\n')
        
        if limit > 0:
            dramas = query[:limit]
            self.stdout.write(f'Processing {limit} dramas\n')
        else:
            dramas = query
            self.stdout.write(f'Processing all {query.count()} dramas without genres\n')
        
        fixed = 0
        failed = 0
        skipped = 0
        
        for drama in dramas:
            self.stdout.write(f'\nProcessing: {drama.title} ({drama.country}, {drama.release_year})')
            
            # Search for drama on TMDB
            try:
                # First try searching by title
                search_resp = requests.get(
                    f"{TMDB_BASE_URL}/search/tv",
                    params={
                        'api_key': TMDB_API_KEY,
                        'query': drama.title_original or drama.title,
                        'first_air_date_year': drama.release_year
                    },
                    timeout=10
                )
                
                results = search_resp.json().get('results', [])
                
                if not results:
                    self.stdout.write('  ⚠️  Not found on TMDB')
                    skipped += 1
                    continue
                
                # Get the first result (most relevant)
                show = results[0]
                show_id = show['id']
                
                # Get full details including genres
                detail_resp = requests.get(
                    f"{TMDB_BASE_URL}/tv/{show_id}",
                    params={'api_key': TMDB_API_KEY},
                    timeout=10
                )
                
                detail = detail_resp.json()
                genre_ids = [g['id'] for g in detail.get('genres', [])]
                
                if not genre_ids:
                    self.stdout.write('  ℹ️  No genres found on TMDB')
                    skipped += 1
                    continue
                
                # Map to genre names
                genre_names = [tmdb_genres[gid] for gid in genre_ids if gid in tmdb_genres]
                
                if not dry_run:
                    # Add genres to drama
                    for genre_name in genre_names:
                        genre, created = Genre.objects.get_or_create(name=genre_name)
                        drama.genres.add(genre)
                    
                    self.stdout.write(self.style.SUCCESS(f'  ✓ Added genres: {", ".join(genre_names)}'))
                else:
                    self.stdout.write(f'  [DRY RUN] Would add: {", ".join(genre_names)}')
                
                fixed += 1
                time.sleep(0.3)  # Rate limiting
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Failed: {e}'))
                failed += 1
                time.sleep(1)
        
        # Summary
        self.stdout.write('\n' + '='*60)
        self.stdout.write('SUMMARY')
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS(f'✓ Fixed: {fixed}'))
        self.stdout.write(self.style.WARNING(f'⚠️  Skipped: {skipped}'))
        self.stdout.write(self.style.ERROR(f'✗ Failed: {failed}'))
        
        if dry_run:
            self.stdout.write('\nRun without --dry-run to apply changes')