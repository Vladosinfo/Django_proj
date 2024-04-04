from django.urls import path, re_path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('tag/', views.tag, name='tag'),
    path('author/', views.author, name='author'),
    path('quote/', views.quote, name='quote'),
    path('detail/<int:quote_id>', views.detail, name='detail'),
    path('author_detail/<int:author_id>', views.author_detail, name='author_detail'),
    path('delete/<int:quote_id>', views.delete_quote, name='delete'),
    path('scrapy/', views.scrapy, name='scrapy'),
    path('scrapyng_quotes/', views.scrapyng_quotes, name='scrapyng_quotes'),
    path('', views.main, name='main'),
    re_path('', views.main, name='main'),
]
