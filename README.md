<div align="center">

# 🎭 TAFARRAJ | تفرّج

### *Your Ultimate Arabic Drama Destination*

![Django](https://img.shields.io/badge/Django-6.0.1-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)

**[Live Demo](https://tafarraj.pythonanywhere.com)** • **[Report Bug](https://github.com/aicha-kelia/drama-aggregator/issues)** • **[Request Feature](https://github.com/aicha-kelia/drama-aggregator/issues)**

*A comprehensive drama streaming platform featuring **1,906+ dramas** from Korea, Turkey, India, China, and Morocco with automatic Arabic translations and multiple streaming sources.*

</div>

---

## 📋 Table of Contents

- [About](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Database Stats](#database-stats)
- [Management Commands](#management-commands)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## About The Project

**Tafarraj** (تفرّج - meaning "watch" in Arabic) is a full-stack web application that aggregates Asian and Middle Eastern dramas with Arabic translations. Built with Django, it provides a Netflix-like browsing experience for Arabic-speaking drama enthusiasts.

### Why Tafarraj?

- **Multi-Region Content**: Access dramas from 5 different countries in one place
- **Arabic-First**: All titles and descriptions automatically translated to Arabic
- **Multiple Sources**: Find your favorite shows on Netflix, Viki, and other platforms
- **Smart Filtering**: Filter by country, genre, year, and status
- **Responsive Design**: Beautiful UI that works on all devices

---

## ✨ Features

### Multi-Country Support
Browse dramas from:
- 🇰🇷 Korean (K-Dramas)
- 🇹🇷 Turkish (Dizi)
- 🇮🇳 Indian (Hindi/Tamil shows)
- 🇨🇳 Chinese (C-Dramas)
- 🇲🇦 Moroccan (Ramadan specials)

### Advanced Filtering & Search
- Filter by **genre** (17+ categories: Romance, Action, Comedy, Thriller, etc.)
- Filter by **country** and **year**
- Filter by **status** (Completed/Ongoing)
- Real-time **search** functionality
- Sort by **popularity** and **release date**

### Automatic Arabic Translation
- Titles translated to Arabic using deep-translator
- Descriptions and plot summaries in Arabic
- Genre names localized

### Rich Metadata
- Episode counts and durations
- Release years and status
- IMDB-style ratings
- High-quality thumbnails from TMDB
- Genre classification

### Streaming Links
- Netflix integration (with episode count)
- Viki integration (with subtitle info)
- Direct links to watch platforms
- Arabic subtitle availability

### TMDB Integration
- Real-time data from The Movie Database API
- Automatic metadata fetching
- Professional poster images via Cloudinary CDN

---

## 🛠 Tech Stack

| Technology | Purpose | Version |
|-----------|---------|---------|
| Django | Backend framework | 6.0.1 |
| Python | Core language | 3.11+ |
| SQLite | Database | 3.37+ |
| TMDB API | Drama metadata & images | v3 |
| Cloudinary | Image CDN & storage | Latest |
| deep-translator | Arabic translations | 1.11.4 |
| BeautifulSoup4 | Web scraping | 4.14.3 |
| Requests | HTTP library | 2.32.5 |
| Gunicorn | WSGI server | 24.1.0 |
| WhiteNoise | Static file serving | 6.11.0 |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+ installed
- pip package manager
- TMDB API Key (free) - [Get yours here](https://www.themoviedb.org/settings/api)
- Cloudinary Account (free) - [Sign up here](https://cloudinary.com/)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aicha-kelia/drama-aggregator.git
   cd drama-aggregator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-django-secret-key
   TMDB_API_KEY=your-tmdb-api-key
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   DEBUG=True
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Populate database** *(Optional - to fetch your own dataset)*
   ```bash
   # Fetch Korean dramas from 2024
   python manage.py fetch_by_year KR 2024 --pages 10
   
   # Or fetch all recent content (2024-2026)
   python manage.py fetch_all_recent
   ```

8. **Start the development server**
   ```bash
   python manage.py runserver
   ```

9. **Open your browser**
   
   Visit: `http://127.0.0.1:8000`

---

## 📊 Database Stats

Current statistics (approximate, February 2026):

> **Note**: This repository includes a pre-populated SQLite database for demo purposes only.

| Metric | Count |
|--------|-------|
| Total Dramas | 1,906 |
| Korean Dramas | ~750 |
| Turkish Dramas | ~500 |
| Indian Dramas | ~400 |
| Chinese Dramas | ~250 |
| Moroccan Dramas | 8 |
| Total Genres | 17 |
| Streaming Links | 2,000+ |

---

## 📝 Management Commands

### Fetch Dramas by Year
```bash
# Fetch Korean dramas from 2025 (20 pages)
python manage.py fetch_by_year KR 2025 --pages 20

# Fetch Chinese dramas from 2024
python manage.py fetch_by_year CN 2024 --pages 15

# Countries: KR (Korea), CN (China), TR (Turkey), IN (India)
```

### Fix Missing Data
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

### Add Moroccan Ramadan Dramas
```bash
# Add 2026 Moroccan Ramadan dramas
python manage.py add_moroccan_ramadan_2026
```

### Add Watch Links
```bash
# Add streaming platform links
python manage.py add_watch_links
```

---

## 🚢 Deployment

### Deploy to PythonAnywhere

1. **Create account** at [PythonAnywhere](https://www.pythonanywhere.com)

2. **Upload your code**
   ```bash
   git clone https://github.com/aicha-kelia/drama-aggregator.git
   cd drama-aggregator
   ```

3. **Set up virtual environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.11 drama-env
   pip install -r requirements.txt
   ```

4. **Configure WSGI**
   
   Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
   ```python
   import os
   import sys
   
   path = '/home/yourusername/drama-aggregator'
   if path not in sys.path:
       sys.path.append(path)
   
   os.environ['DJANGO_SETTINGS_MODULE'] = 'dramahere.settings'
   
   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

5. **Set environment variables** in Web tab

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Reload web app**

---

## 📁 Project Structure

```
drama-aggregator/
├── Tafarraj/                 # Main Django app
│   ├── models.py            # Drama, Genre, WatchLink models
│   ├── views.py             # Frontend views
│   ├── utils.py             # TMDB integration, translation
│   ├── management/
│   │   └── commands/        # Custom Django commands
│   │       ├── fetch_by_year.py
│   │       ├── fetch_all_recent.py
│   │       ├── add_moroccan_ramadan_2026.py
│   │       └── fix_missing_data.py
│   ├── migrations/          # Database migrations
│   └── templates/
│       └── tafarraj/        # HTML templates
├── dramahere/               # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/               # Global templates
├── requirements.txt        # Python dependencies
├── Procfile               # Deployment config
├── .gitignore
└── README.md
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourusername.pythonanywhere.com

TMDB_API_KEY=your-tmdb-api-key

CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

DATABASE_URL=sqlite:///db.sqlite3
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Write clear commit messages
- Add docstrings to new functions
- Test before submitting PR

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

**Aicha Kelia** - Developer & Maintainer

- GitHub: [@aicha-kelia](https://github.com/aicha-kelia)
- Project Link: [https://github.com/aicha-kelia/drama-aggregator](https://github.com/aicha-kelia/drama-aggregator)
- Live Demo: [https://tafarraj.pythonanywhere.com](https://tafarraj.pythonanywhere.com)

---

## Acknowledgments

- [TMDB](https://www.themoviedb.org/) - Drama metadata and images
- [Cloudinary](https://cloudinary.com/) - Image CDN and storage
- [Django](https://www.djangoproject.com/) - Web framework
- [deep-translator](https://github.com/nidhaloff/deep-translator) - Arabic translation
- [PythonAnywhere](https://www.pythonanywhere.com/) - Hosting platform

---

<div align="center">

**Built by Aicha Kelia**

⭐ Star this repo if you find it helpful

[⬆ Back to Top](#-tafarraj--تفرّج)

</div>