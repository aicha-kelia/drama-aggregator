# 🎬 Drama Aggregator

![Django](https://img.shields.io/badge/Django-5.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

> A comprehensive Asian drama streaming platform featuring **1,898+ dramas** from Korea, China, Turkey, and India with automatic Arabic translations.

## ✨ Features

- 🌏 **Multi-Country Support** - Korean, Chinese, Turkish, and Indian dramas
- 🔍 **Advanced Filtering** - Filter by genre, country, year, and status
- 🌐 **Arabic Translations** - Automatic title and description translation
- 📺 **Rich Metadata** - Episode counts, durations, release years
- 🎯 **Genre Classification** - 17+ genres including Drama, Romance, Action, Mystery
- 🚀 **TMDB Integration** - Real-time data from The Movie Database API

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [TMDB API Key](https://www.themoviedb.org/settings/api) (free)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/aicha-kelia/drama-aggregator.git
cd drama-aggregator
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your TMDB_API_KEY
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Fetch dramas** (optional - takes ~30 minutes)
```bash
python manage.py fetch_by_year KR 2025 --pages 10
```

7. **Start the server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` 🎉

## 📊 Database Stats

- **Total Dramas**: 1,898
- **Korean**: 735 dramas
- **Chinese**: 653 dramas
- **Turkish**: 510 dramas
- **Genres**: 17 categories

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Django 5.1 | Backend framework |
| PostgreSQL | Production database |
| TMDB API | Drama metadata & images |
| WhiteNoise | Static file serving |
| Gunicorn | WSGI server |

## 📝 Management Commands

### Fetch Dramas by Year
```bash
# Fetch Korean dramas from 2025 (20 pages)
python manage.py fetch_by_year KR 2025 --pages 20

# Fetch Chinese dramas from 2024
python manage.py fetch_by_year CN 2024 --pages 15

# Countries: KR (Korea), CN (China), TR (Turkey), IN (India)
```

### Fix Missing Genres
```bash
# Diagnose database issues
python manage.py diagnose_data

# Fix dramas without genres (Korean only)
python manage.py fix_missing_data --country KR

# Fix all dramas
python manage.py fix_missing_data
```

### Fetch All Recent Content
```bash
# Automatically fetches 2024-2026 content from all countries
python manage.py fetch_all_recent
```

## 🚢 Deployment

### Deploy to Railway

1. Push to GitHub
2. Connect Railway to your repository
3. Add environment variables:
   - `SECRET_KEY` - Django secret key
   - `TMDB_API_KEY` - Your TMDB API key
   - `DEBUG` - Set to `False`
   - `ALLOWED_HOSTS` - Your Railway domain
4. Railway auto-provides `DATABASE_URL` for PostgreSQL

The `Procfile` is already configured for automatic deployment.

## 📁 Project Structure

```
drama-aggregator/
├── Tafarraj/              # Main Django app
│   ├── models.py          # Drama, Genre, Episode models
│   ├── views.py           # Frontend views
│   ├── utils.py           # TMDB integration, translation
│   └── management/
│       └── commands/      # Custom Django commands
├── dramahere/             # Project settings
│   ├── settings.py
│   └── urls.py
├── media/                 # Drama thumbnails
├── static/                # CSS, JS, images
├── templates/             # HTML templates
├── requirements.txt
├── Procfile              # Railway deployment
└── README.md
```

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
TMDB_API_KEY=your-tmdb-api-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app
DATABASE_URL=sqlite:///db.sqlite3  # Railway provides PostgreSQL URL
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [TMDB](https://www.themoviedb.org/) - Drama metadata and images
- [Django](https://www.djangoproject.com/) - Web framework
- Arabic translation via Google Translate API

---

**Built by [Aicha Kelia](https://github.com/aicha-kelia)** | 📍 Ankara, Turkey