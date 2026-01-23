from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from .models import Drama, Genre

def drama_list(request):
    """Show all dramas with filters and search"""
    dramas = Drama.objects.all()
    
    # Filter by country
    country = request.GET.get('country')
    if country:
        dramas = dramas.filter(country=country)
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        dramas = dramas.filter(status=status)
    
    # Filter by genre
    genre = request.GET.get('genre')
    if genre:
        try:
            genre_id = int(genre)
            print(f"DEBUG: Filtering by genre ID: {genre_id}")
            print(f"DEBUG: Total dramas BEFORE filter: {dramas.count()}")
            dramas = dramas.filter(genres__id=genre_id)
            print(f"DEBUG: Total dramas AFTER filter: {dramas.count()}")
        except ValueError:
            print(f"DEBUG: Invalid genre value: {genre}")
    
    # Filter by release year
    year = request.GET.get('year')
    if year:
        dramas = dramas.filter(release_year=year)
    
    # Search by title (arabic, english, original)
    search = request.GET.get('search')
    if search:
        dramas = dramas.filter(
            Q(title__icontains=search) |
            Q(title_arabic__icontains=search) |
            Q(title_original__icontains=search)
        )
    
    # Get all genres and years for filter dropdowns
    genres = Genre.objects.annotate(drama_count=Count('drama')).filter(drama_count__gt=0)
    years = Drama.objects.values_list('release_year', flat=True).distinct().order_by('-release_year')
    
    context = {
        'dramas': dramas,
        'genres': genres,
        'years': years,
    }
    return render(request, 'tafarraj/drama_list.html', context)

def drama_detail(request, pk):
    """Show single drama with watch links"""
    drama = get_object_or_404(Drama, pk=pk)
    
    context = {
        'drama': drama,
    }
    return render(request, 'tafarraj/drama_detail.html', context)