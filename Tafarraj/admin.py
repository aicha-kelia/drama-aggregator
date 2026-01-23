from django.contrib import admin
from .models import Drama, WatchLink, Genre

@admin.register(Drama)
class DramaAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_arabic', 'country', 'total_episodes', 'status', 'release_year')
    list_filter = ('country', 'status', 'release_year')
    search_fields = ('title', 'title_arabic', 'title_original')

@admin.register(WatchLink)
class WatchLinkAdmin(admin.ModelAdmin):
    list_display = ('drama', 'website_name', 'language', 'episodes_available')
    list_filter = ('language', 'website_name')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_arabic')