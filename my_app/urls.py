from django.contrib import admin
from django.urls import path

from my_app import views

urlpatterns = [
    path('', views.Home, name='home_page'),
    path('search', views.search, name='new_search')
]