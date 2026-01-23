from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Fetch all 2025-2026 dramas for all countries'

    def handle(self, *args, **options):
        countries = ['KR', 'TR', 'CN']
        years = [2025, 2026]
        
        for country in countries:
            for year in years:
                self.stdout.write(f'\n{"="*50}')
                self.stdout.write(f'FETCHING {country} {year}')
                self.stdout.write(f'{"="*50}\n')
                
                call_command('fetch_by_year', country, year, '--pages', 20)
        
        self.stdout.write(self.style.SUCCESS('\n🎉 ALL DONE! ALL 2025-2026 DRAMAS ADDED!'))