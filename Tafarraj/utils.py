from deep_translator import GoogleTranslator
import requests
from .models import Drama, Genre


    
def translate_to_arabic(text):
    """Translate text to Arabic"""
    if not text or text.strip() == '':
        return "لا يوجد وصف"
    try:
        result = GoogleTranslator(source='auto', target='ar').translate(text)
        if not result or result.strip() == '':
            return "لا يوجد وصف"
        return result
    except Exception as e:
        print(f"Translation error: {e}")
        return text if text else "لا يوجد وصف"

TMDB_API_KEY = '00b22672f6e2dbae13b1d6f64bbfa54e'  # Get from https://www.themoviedb.org/settings/api
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

def fetch_drama_from_tmdb(tmdb_id, drama_type='tv'):
    """
    Fetch drama info from TMDB
    drama_type: 'tv' for series, 'movie' for movies
    """
    url = f"{TMDB_BASE_URL}/{drama_type}/{tmdb_id}"
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Create Drama object
        drama_data = {
            'title': data.get('name') or data.get('title'),
            'title_original': data.get('original_name') or data.get('original_title'),
            'description': data.get('overview'),
            'release_year': int(data.get('first_air_date', '2000')[:4]) if data.get('first_air_date') else 2000,
            'total_episodes': data.get('number_of_episodes', 0),
            'episode_duration': data.get('episode_run_time', [45])[0] if data.get('episode_run_time') else 45,
            'status': 'completed' if data.get('status') == 'Ended' else 'ongoing',
        }
        
        # Translate to Arabic
        drama_data['title_arabic'] = translate_to_arabic(drama_data['title'])
        drama_data['description_arabic'] = translate_to_arabic(drama_data['description'])
        
        # Determine country (you'll need to map origin_country)
        origin = data.get('origin_country', ['US'])[0]
        country_map = {
            'KR': 'korean',
            'TR': 'turkish',
            'IN': 'indian',
            'CN': 'chinese',
        }
        drama_data['country'] = country_map.get(origin, 'korean')
        
        # Get poster image URL
        if data.get('poster_path'):
            drama_data['thumbnail_url'] = f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        
        return drama_data
        
    except Exception as e:
        print(f"TMDB API error: {e}")
        return None


def search_tmdb_dramas(query, country='KR'):
    """Search for dramas on TMDB"""
    url = f"{TMDB_BASE_URL}/search/tv"
    params = {
        'api_key': TMDB_API_KEY,
        'query': query,
        'language': 'en-US',
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
    except Exception as e:
        print(f"TMDB search error: {e}")
        return []