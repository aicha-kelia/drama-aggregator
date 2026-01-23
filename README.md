# DramaHere 🎬

A comprehensive drama streaming platform featuring Korean, Chinese, Turkish, and Indian dramas with Arabic translations.

## Features

- 🌍 Multi-country drama database (Korean, Chinese, Turkish, Indian)
- 🔍 Advanced filtering by genre, country, and year
- 🌐 Arabic translations for titles and descriptions
- 📺 Episode tracking and watchlist
- 🎯 Genre-based recommendations
- 📱 Responsive design

## Tech Stack

- **Backend**: Django 5.1
- **Database**: SQLite (development) / PostgreSQL (production)
- **API**: TMDB (The Movie Database)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Railway

## Installation

### Prerequisites
- Python 3.11+
- TMDB API Key

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/dramahere.git
cd dramahere
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```env
SECRET_KEY=your-secret-key
TMDB_API_KEY=your-tmdb-api-key
DEBUG=True
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Fetch dramas:
```bash
python manage.py fetch_by_year KR 2025 --pages 10
```

7. Run server:
```bash
python manage.py runserver
```

## Management Commands

### Fetch Dramas
```bash
# Fetch Korean dramas from 2025
python manage.py fetch_by_year KR 2025 --pages 20

# Fetch all recent dramas (2024-2026)
python manage.py fetch_all_recent
```

### Fix Missing Genres
```bash
# Diagnose data issues
python manage.py diagnose_data

# Fix missing genres
python manage.py fix_missing_data --country KR
```

## Deployment (Railway)

1. Push to GitHub
2. Connect Railway to your repository
3. Add environment variables in Railway dashboard
4. Railway will auto-deploy

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Django secret key |
| `TMDB_API_KEY` | TMDB API key |
| `DEBUG` | Set to False in production |
| `DATABASE_URL` | PostgreSQL URL (Railway provides this) |

## Database

Currently supports:
- **1,898+ dramas** across 4 countries
- **17 genres**
- Automatic translation to Arabic

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Acknowledgments

- Drama data provided by [TMDB](https://www.themoviedb.org/)
- Arabic translations via Google Translate API