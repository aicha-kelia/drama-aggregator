from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Drama, Genre, WatchLink


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
            dramas = dramas.filter(genres__id=genre_id)
        except ValueError:
            pass
    
    # Filter by release year
    year = request.GET.get('year')
    if year:
        dramas = dramas.filter(release_year=year)
    
    # Search by title
    search = request.GET.get('search')
    if search:
        dramas = dramas.filter(
            Q(title__icontains=search) |
            Q(title_arabic__icontains=search) |
            Q(title_original__icontains=search)
        )
    
    # PAGINATION - Added here
    paginator = Paginator(dramas, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    genres = Genre.objects.annotate(drama_count=Count('drama')).filter(drama_count__gt=0)
    years = Drama.objects.values_list('release_year', flat=True).distinct().order_by('-release_year')
    
    context = {
        'page_obj': page_obj,      # Changed from dramas
        'dramas': page_obj,         # Keep this so old template still works
        'genres': genres,
        'years': years,
        'country': country,
        'status': status,
        'genre': genre,
        'year': year,
        'search': search,
    }
    return render(request, 'Tafarraj/drama_list.html', context)


def drama_detail(request, pk):
    """Show single drama with watch links"""
    drama = get_object_or_404(Drama, pk=pk)
    
    context = {
        'drama': drama,
    }
    return render(request, 'Tafarraj/drama_detail.html', context)