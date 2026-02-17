import requests
from bs4 import BeautifulSoup
import time
import sqlite3
from urllib.parse import quote

def search_google_images(drama_title, year):
    """Search Google Images and return first result"""
    
    search_term = f"{drama_title} {year} drama poster"
    encoded_search = quote(search_term)
    
    url = f"https://www.google.com/search?q={encoded_search}&tbm=isch"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        img_tags = soup.find_all('img')
        
        for img in img_tags[1:]:
            src = img.get('src') or img.get('data-src')
            if src and src.startswith('http'):
                return src
        
        return None
    except:
        return None

def fix_all_thumbnails():
    """Fix all 341 dramas"""
    
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, title_original, title_arabic, release_year 
        FROM Tafarraj_drama 
        WHERE (thumbnail IS NULL OR thumbnail = '')
    """)
    
    dramas = cursor.fetchall()
    total = len(dramas)
    updated = 0
    failed = []
    
    print(f"Starting to fix {total} dramas...\n")
    
    for i, (drama_id, title_orig, title_ar, year) in enumerate(dramas, 1):
        search_title = title_orig or title_ar
        
        print(f"[{i}/{total}] {search_title} ({year})")
        
        thumbnail = search_google_images(search_title, year)
        
        if thumbnail:
            cursor.execute(
                "UPDATE Tafarraj_drama SET thumbnail = ? WHERE id = ?",
                (thumbnail, drama_id)
            )
            conn.commit()
            updated += 1
            print(f"  ✓ Found")
        else:
            failed.append(f"{search_title} ({year})")
            print(f"  ✗ Failed")
        
        time.sleep(2)
        
        if i % 50 == 0:
            print(f"\n--- Progress: {updated}/{i} ---\n")
    
    print(f"\n{'='*60}")
    print(f"RESULTS:")
    print(f"✓ Updated: {updated}/{total}")
    print(f"✗ Failed: {len(failed)}/{total}")
    print(f"{'='*60}")
    
    if failed:
        with open("failed_thumbnails.txt", "w", encoding="utf-8") as f:
            for drama in failed:
                f.write(f"{drama}\n")
        print("\nFailed dramas saved to: failed_thumbnails.txt")
    
    conn.close()

if __name__ == "__main__":
    fix_all_thumbnails()