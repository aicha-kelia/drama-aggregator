#!/usr/bin/env python3
"""
Django Management Command: import_scraped_dramas
Imports dramas from JSON file into database
Checks for duplicates and only adds new ones
"""

from django.core.management.base import BaseCommand
from Tafarraj.models import Drama, Genre, WatchLink
import json
from pathlib import Path


class Command(BaseCommand):
    help = 'Import scraped dramas from JSON file'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to JSON file with scraped dramas')

    def handle(self, *args, **options):
        json_file = options['json_file']
        
        # Load JSON
        self.stdout.write(f"📂 Loading {json_file}...")
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"❌ File not found: {json_file}"))
            return
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(f"❌ Invalid JSON: {e}"))
            return

        dramas = data.get('dramas', [])
        total = len(dramas)
        self.stdout.write(f"📊 Found {total} dramas in file")
        
        # Stats
        added = 0
        skipped = 0
        errors = 0
        
        for i, drama_data in enumerate(dramas, 1):
            try:
                # Check for duplicate
                title = drama_data.get('title') or drama_data.get('title_arabic')
                if not title:
                    self.stdout.write(f"  ⚠️  [{i}/{total}] No title, skipping")
                    skipped += 1
                    continue
                
                # Check if exists
                exists = Drama.objects.filter(
                    title__iexact=title
                ).exists() or Drama.objects.filter(
                    title_arabic__iexact=title
                ).exists()
                
                if exists:
                    self.stdout.write(f"  ⏭️  [{i}/{total}] Duplicate: {title}")
                    skipped += 1
                    continue
                
                # Use title_arabic as fallback if title is empty
                title_en = drama_data.get('title') or drama_data.get('title_arabic') or 'Unknown'
                title_ar = drama_data.get('title_arabic') or drama_data.get('title') or 'Unknown'
                
                # Create drama
                drama = Drama.objects.create(
                    title=title_en,
                    title_arabic=title_ar,
                    title_original=drama_data.get('title_original', ''),
                    description=drama_data.get('description', ''),
                    description_arabic=drama_data.get('description_arabic', ''),
                    country=drama_data.get('country', 'unknown'),
                    total_episodes=drama_data.get('total_episodes'),
                    episode_duration=drama_data.get('episode_duration', 60),
                    release_year=drama_data.get('release_year'),
                    status=drama_data.get('status', 'completed'),
                    thumbnail_url=drama_data.get('thumbnail_url', '')
                )
                
                # Add genres
                for genre_name in drama_data.get('genres', []):
                    if genre_name:
                        genre, _ = Genre.objects.get_or_create(
                            name=genre_name,
                            defaults={'name_arabic': genre_name}
                        )
                        drama.genres.add(genre)
                
                # Add watch links
                for link_data in drama_data.get('watch_links', []):
                    WatchLink.objects.create(
                        drama=drama,
                        website_name=link_data.get('website_name', 'Unknown'),
                        url=link_data.get('url', ''),
                        language=link_data.get('language', 'arabic'),
                        episodes_available=link_data.get('episodes_available', 0)
                    )
                
                self.stdout.write(self.style.SUCCESS(f"  ✅ [{i}/{total}] Added: {title}"))
                added += 1
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ❌ [{i}/{total}] Error: {str(e)}"))
                errors += 1
        
        # Summary
        self.stdout.write("\n" + "="*60)
        self.stdout.write(self.style.SUCCESS(f"✅ IMPORT COMPLETE"))
        self.stdout.write(f"📊 Total in file: {total}")
        self.stdout.write(self.style.SUCCESS(f"✅ Added: {added}"))
        self.stdout.write(self.style.WARNING(f"⏭️  Skipped (duplicates): {skipped}"))
        if errors:
            self.stdout.write(self.style.ERROR(f"❌ Errors: {errors}"))
        self.stdout.write("="*60)