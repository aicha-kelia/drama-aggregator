from django.db import models

class Drama(models.Model):
    # Basic Info
    title = models.CharField(max_length=200)
    title_arabic = models.CharField(max_length=200, blank=True)
    title_original = models.CharField(max_length=200, blank=True)
    
    # Visual
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)  # ADD THIS
   
    # Details
    description = models.TextField()
    description_arabic = models.TextField(blank=True)
    country = models.CharField(max_length=50, choices=[
    ('korean', 'كوري'),
    ('turkish', 'تركي'),
    ('indian', 'هندي'),
    ('chinese', 'صيني'),
    ('moroccan', 'مغربي'),
])

    
    # Episodes
    total_episodes = models.IntegerField()
    episode_duration = models.IntegerField()
    release_year = models.IntegerField()
    status = models.CharField(max_length=20, choices=[
    ('ongoing', 'مستمر'),
    ('completed', 'مكتمل'),
])
    
    next_episode_date = models.DateTimeField(blank=True, null=True)
    current_episode_number = models.IntegerField(default=0)  # FIX 1: add default
    
    # Categories
    genres = models.ManyToManyField('Genre')
    
    # FIX 2: Add this
    def __str__(self):
        return self.title_arabic or self.title


class WatchLink(models.Model):
    drama = models.ForeignKey(Drama, on_delete=models.CASCADE, related_name='links')
    website_name = models.CharField(max_length=100)
    url = models.URLField()
    language = models.CharField(max_length=20, choices=[
        ('arabic', 'Arabic Subs'),
        ('english', 'English Subs'),
    ])
    episodes_available = models.IntegerField()

    
    # FIX 3: Add this
    def __str__(self):
        return f"{self.website_name} - {self.drama.title}"


class Genre(models.Model):
    name = models.CharField(max_length=50)
    name_arabic = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name_arabic or self.name