from django.core.management.base import BaseCommand
from Tafarraj.models import Drama, Genre, WatchLink
import cloudinary
import cloudinary.uploader
import requests
from django.core.files.base import ContentFile
import time

# Configure Cloudinary
cloudinary.config(
    cloud_name="dobqw9fa9",
    api_key="971324672167161",
    api_secret="_Yuhs0gVWh8pAWAOVSI0MQJsaYc"
)

class Command(BaseCommand):
    help = 'Add Moroccan Ramadan 2026 dramas to database'

    def handle(self, *args, **options):
        self.stdout.write('🇲🇦 Adding Moroccan Ramadan 2026 Dramas...\n')
        
        # First, add 'moroccan' to country choices if needed
        # You need to update your model.py Drama.country choices to include:
        # ('moroccan', 'مغربي'),
        
        # Define all Moroccan Ramadan 2026 dramas
        moroccan_dramas = [
            {
                'title': 'Al Hayba: Ra\'s Al Jabal',
                'title_arabic': 'الهيبة - رأس الجبل',
                'title_original': 'الهيبة - رأس الجبل',
                'description': 'Moroccan adaptation of the popular Syrian crime drama series. A powerful family drama involving crime, loyalty, and mountain conflicts.',
                'description_arabic': 'النسخة المغربية من المسلسل السوري الشهير. دراما عائلية قوية تتضمن الجريمة والولاء والصراعات الجبلية.',
                'total_episodes': 30,
                'episode_duration': 45,
                'release_year': 2026,
                'status': 'ongoing',
                'genres': ['Drama', 'Action', 'Crime', 'Family'],
                'cast': 'Assaad Bouab, Hiba Bennani, Nora Skali, Amine Ennaji',
                'director': 'Ayoub Lahnoud',
                'channels': ['MBC 5', 'Shahid'],
                'poster_url': 'https://core.elcinema.com/uploads/photo/file/124657674/_315x420_a5ce5dbf585dabbe97108233d50d959240c8c8ccc1b0131faed7e90c1cf68f05.jpg'  # Real poster from elcinema.com
            },
            {
                'title': 'Rahma 2',
                'title_arabic': 'رحمة الموسم الثاني',
                'title_original': 'رحمة 2',
                'description': 'Second season of the popular social drama series exploring complex family relationships and social issues in modern Moroccan society.',
                'description_arabic': 'الموسم الثاني من المسلسل الاجتماعي الشهير الذي يستكشف العلاقات الأسرية المعقدة والقضايا الاجتماعية في المجتمع المغربي الحديث.',
                'total_episodes': 30,
                'episode_duration': 45,
                'release_year': 2026,
                'status': 'ongoing',
                'genres': ['Drama', 'Family', 'Romance'],
                'cast': 'Abdullah Didan, Sanaa Akroud, Karima Ghaith, Farah El Fassi',
                'director': 'Mohamed Ali Al-Majboud',
                'channels': ['MBC 5', 'Shahid'],
                'poster_url': 'https://media0093.elcinema.com/uploads/_315x420_12b31023c090bfb3edab0dd6c92a2e1d0997d2ea047ab2dcb46662945b443418.jpg'  # Real poster from elcinema.com
            },
            {
                'title': 'Imarat Al-Saada',
                'title_arabic': 'عمارة السعادة',
                'title_original': 'عمارة السعادة',
                'description': 'A comedy series about the daily lives and hilarious interactions of residents living in the same apartment building.',
                'description_arabic': 'مسلسل كوميدي عن الحياة اليومية والتفاعلات المضحكة للسكان الذين يعيشون في نفس المبنى السكني.',
                'total_episodes': 30,
                'episode_duration': 45,
                'release_year': 2026,
                'status': 'ongoing',
                'genres': ['Comedy', 'Family'],
                'cast': 'Aziz Dadas, Soukaina Darabil',
                'director': 'Hisham Al-Jebbari',
                'channels': ['MBC 5', 'Shahid'],
                'poster_url': 'https://via.placeholder.com/500x750/C9A24D/0B0B0B?text=Imarat+Al-Saada'
            },
            {
                'title': 'Banat Lalla Menana 3',
                'title_arabic': 'بنات لالة منانة 3',
                'title_original': 'بنات لالة منانة الموسم الثالث',
                'description': 'Third season returns after 13-year hiatus. Popular family drama series about the daughters of Lalla Menana and their modern life challenges.',
                'description_arabic': 'الموسم الثالث يعود بعد غياب 13 عامًا. مسلسل عائلي شهير عن بنات لالة منانة وتحديات حياتهن العصرية.',
                'total_episodes': 30,
                'episode_duration': 45,
                'release_year': 2026,
                'status': 'ongoing',
                'genres': ['Drama', 'Family', 'Comedy'],
                'cast': 'Original cast returning',
                'director': 'TBA',
                'channels': ['2M', 'Chouf Drama'],
                'poster_url': 'https://media0093.elcinema.com/uploads/_315x420_a4bc0df304951951e73df24c973fa611184449738c5e63b0891d99718a39f906.jpg'  # Real poster from elcinema.com
            },
            {
                'title': 'Lili Twil (A Long Night)',
                'title_arabic': 'ليلي طويل',
                'title_original': 'ليلي طويل',
                'description': 'A 15-episode drama exploring the dark side of social media influence and the lives of digital influencers in Morocco.',
                'description_arabic': 'دراما من 15 حلقة تستكشف الجانب المظلم لتأثير وسائل التواصل الاجتماعي وحياة المؤثرين الرقميين في المغرب.',
                'total_episodes': 15,
                'episode_duration': 45,
                'release_year': 2026,
                'status': 'ongoing',
                'genres': ['Drama', 'Thriller'],
                'cast': 'Salma Salaheddine, Maria Lalouaz, Ayoub Gretaa, Nasser Akabab',
                'director': 'Alaa Akaaboune',
                'channels': ['2M'],
                'poster_url': 'https://via.placeholder.com/500x750/C9A24D/0B0B0B?text=Lili+Twil'
            },
            {
                'title': 'Hikayat Shama',
                'title_arabic': 'حكايات شامة',
                'title_original': 'حكايات شامة',
                'description': 'A drama series telling multiple intertwined stories about Moroccan women and their daily struggles and triumphs.',
                'description_arabic': 'مسلسل درامي يروي قصصًا متعددة متشابكة عن النساء المغربيات وصراعاتهن اليومية وانتصاراتهن.',
                'total_episodes': 30,
                'episode_duration': 45,
                'release_year': 2026,
                'status': 'ongoing',
                'genres': ['Drama', 'Family'],
                'cast': 'TBA',
                'director': 'TBA',
                'channels': ['2M'],
                'poster_url': 'https://via.placeholder.com/500x750/C9A24D/0B0B0B?text=Hikayat+Shama'
            },
            {
                'title': 'Yawmiyat Mahjouba Wal Tabariya',
                'title_arabic': 'يوميات محجوبة والتبارية',
                'title_original': 'يوميات محجوبة والتبارية',
                'description': 'A comedy-drama series about the daily diaries and adventures of two contrasting Moroccan women characters.',
                'description_arabic': 'مسلسل كوميدي درامي عن اليوميات والمغامرات اليومية لشخصيتين نسائيتين مغربيتين متناقضتين.',
                'total_episodes': 30,
                'episode_duration': 45,
                'release_year': 2026,
                'status': 'ongoing',
                'genres': ['Comedy', 'Drama', 'Family'],
                'cast': 'TBA',
                'director': 'TBA',
                'channels': ['2M'],
                'poster_url': 'https://via.placeholder.com/500x750/C9A24D/0B0B0B?text=Yawmiyat+Mahjouba'
            },
            {
                'title': 'Habibi Hatta Al-Maut',
                'title_arabic': 'حبيبي حتى الموت',
                'title_original': 'حبيبي حتى الموت',
                'description': 'A 10-episode comedy-drama about love, relationships, and daily life in modern Morocco. A light-hearted take on Moroccan romance.',
                'description_arabic': 'كوميديا درامية من 10 حلقات عن الحب والعلاقات والحياة اليومية في المغرب الحديث. نظرة خفيفة على الرومانسية المغربية.',
                'total_episodes': 10,
                'episode_duration': 45,
                'release_year': 2026,
                'status': 'ongoing',
                'genres': ['Comedy', 'Romance', 'Drama'],
                'cast': 'Aziz Hattab, Samia Aqriou, Rashid Al-Wali, Hisham Al-Wali',
                'director': 'Hisham Al-Jebbari',
                'channels': ['Al Aoula'],
                'poster_url': 'https://via.placeholder.com/500x750/C9A24D/0B0B0B?text=Habibi+Hatta+Al-Maut'
            },
        ]
        
        added_count = 0
        
        for drama_data in moroccan_dramas:
            # Check if drama already exists
            if Drama.objects.filter(title_arabic=drama_data['title_arabic']).exists():
                self.stdout.write(f"⏭️  SKIP: {drama_data['title_arabic']} (already exists)")
                continue
            
            self.stdout.write(f"\n📺 Adding: {drama_data['title_arabic']}")
            
            # Create the drama
            drama = Drama.objects.create(
                title=drama_data['title'],
                title_arabic=drama_data['title_arabic'],
                title_original=drama_data['title_original'],
                description=drama_data['description'],
                description_arabic=drama_data['description_arabic'],
                country='moroccan',  # Make sure you add this to your model choices!
                total_episodes=drama_data['total_episodes'],
                episode_duration=drama_data['episode_duration'],
                release_year=drama_data['release_year'],
                status=drama_data['status'],
                current_episode_number=0,
                next_episode_date=None  # Will start Feb 17-18, 2026
            )
            
            # Add genres
            for genre_name in drama_data['genres']:
                try:
                    # Try to find existing genre by English name
                    genre = Genre.objects.get(name=genre_name)
                except Genre.DoesNotExist:
                    # Create genre if it doesn't exist
                    genre_arabic_map = {
                        'Drama': 'دراما',
                        'Action': 'أكشن',
                        'Crime': 'جريمة',
                        'Family': 'عائلي',
                        'Romance': 'رومانسية',
                        'Comedy': 'كوميديا',
                        'Thriller': 'إثارة'
                    }
                    genre = Genre.objects.create(
                        name=genre_name,
                        name_arabic=genre_arabic_map.get(genre_name, genre_name)
                    )
                    self.stdout.write(f"  ➕ Created genre: {genre_name}")
                
                drama.genres.add(genre)
            
            # Download and upload thumbnail to Cloudinary
            try:
                self.stdout.write(f"  📷 Downloading poster from: {drama_data['poster_url'][:50]}...")
                img_response = requests.get(drama_data['poster_url'], timeout=10)
                
                if img_response.status_code == 200:
                    # Upload to Cloudinary
                    result = cloudinary.uploader.upload(
                        img_response.content,
                        folder="dramahere_thumbnails",
                        public_id=f"moroccan_{drama.id}_{drama_data['title'].replace(' ', '_')}",
                        overwrite=True
                    )
                    cloudinary_url = result['secure_url']
                    self.stdout.write(f"  ✅ Uploaded to Cloudinary: {cloudinary_url}")
                    
                    # Save to drama model
                    drama.thumbnail.save(
                        f'moroccan_{drama.id}.jpg',
                        ContentFile(img_response.content),
                        save=True
                    )
                    self.stdout.write(f"  ✅ Thumbnail saved to database")
                else:
                    self.stdout.write(f"  ⚠️  Failed to download image (status: {img_response.status_code})")
                
            except Exception as e:
                self.stdout.write(f"  ⚠️  Thumbnail upload failed: {e}")
                self.stdout.write(f"  ℹ️  Drama added without thumbnail, you can add it manually later")
            
            # Add watch links based on channels
            channel_urls = {
                'MBC 5': {
                    'url': f'https://shahid.mbc.net/ar/search?q={drama_data["title_arabic"].replace(" ", "+")}',
                    'name': 'MBC 5'
                },
                'Shahid': {
                    'url': f'https://shahid.mbc.net/ar/search?q={drama_data["title_arabic"].replace(" ", "+")}',
                    'name': 'Shahid'
                },
                '2M': {
                    'url': f'https://www.2m.ma/ar/search?q={drama_data["title_arabic"].replace(" ", "+")}',
                    'name': '2M'
                },
                'Al Aoula': {
                    'url': f'https://www.snrt.ma/ar/search?q={drama_data["title_arabic"].replace(" ", "+")}',
                    'name': 'Al Aoula'
                },
                'Chouf Drama': {
                    'url': f'https://choufdrama.com/search?q={drama_data["title_arabic"].replace(" ", "+")}',
                    'name': 'Chouf Drama'
                }
            }
            
            # Additional Arabic platforms
            arabic_platforms = [
                {'name': 'Akwam', 'url': f'https://akwam.to/search?q={drama_data["title_arabic"].replace(" ", "+")}'},
                {'name': 'Faselhd', 'url': f'https://faselhd.io/?s={drama_data["title_arabic"].replace(" ", "+")}'},
                {'name': 'MyCima', 'url': f'https://mycima.tv/search/{drama_data["title"].lower().replace(" ", "-")}'},
            ]
            
            # Add main channel links
            for channel in drama_data['channels']:
                if channel in channel_urls:
                    WatchLink.objects.create(
                        drama=drama,
                        website_name=channel_urls[channel]['name'],
                        url=channel_urls[channel]['url'],
                        language='arabic',
                        episodes_available=drama_data['total_episodes']
                    )
                    self.stdout.write(f"  🔗 Added link: {channel_urls[channel]['name']}")
            
            # Add additional Arabic platform links
            for platform in arabic_platforms:
                WatchLink.objects.create(
                    drama=drama,
                    website_name=platform['name'],
                    url=platform['url'],
                    language='arabic',
                    episodes_available=drama_data['total_episodes']
                )
                self.stdout.write(f"  🔗 Added link: {platform['name']}")
            
            added_count += 1
            self.stdout.write(self.style.SUCCESS(f"✅ Successfully added: {drama_data['title_arabic']}"))
            
            # Small delay to avoid overwhelming the system
            time.sleep(0.5)
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'🎉 DONE! Added {added_count} Moroccan Ramadan 2026 dramas'))
        self.stdout.write(f'📊 Total dramas in database: {Drama.objects.count()}')
        self.stdout.write(f'🔗 Total watch links: {WatchLink.objects.count()}')
        self.stdout.write('='*50)