import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dramahere.settings')
django.setup()

from tafarraj.models import Drama

# Read URLs from file
url_mapping = {}
with open('cloudinary_urls.txt', 'r') as f:
    for line in f:
        if '|' in line:
            filename, url = line.strip().split('|')
            # Extract ID from filename (e.g., "1.jpg" → 1)
            drama_id = int(filename.split('.')[0])
            url_mapping[drama_id] = url

# Update database
for drama_id, url in url_mapping.items():
    try:
        drama = Drama.objects.get(id=drama_id)
        drama.thumbnail_url = url
        drama.save()
        print(f"✅ Updated Drama {drama_id}")
    except Drama.DoesNotExist:
        print(f"❌ Drama {drama_id} not found")

print(f"\n🎉 {len(url_mapping)} dramas updated!")