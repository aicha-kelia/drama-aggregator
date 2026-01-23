from django.urls import path
from . import views

app_name = 'tafarraj' 

urlpatterns = [
    path('', views.drama_list, name='drama_list'),
    path('drama/<int:pk>/', views.drama_detail, name='drama_detail'),
]