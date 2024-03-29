from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('tag/', views.tag, name='tag'),
    path('author/', views.author, name='author'),
    path('quote/', views.quote, name='quote'),
]
