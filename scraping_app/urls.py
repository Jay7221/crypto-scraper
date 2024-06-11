# scraping_app/urls.py
from django.urls import path
from .views import StartScrapingView, ScrapingStatusView

urlpatterns = [
    path('start-scraping/', StartScrapingView.as_view(), name='start_scraping'),
    path('scraping-status/<uuid:job_id>/',
         ScrapingStatusView.as_view(), name='scraping_status'),
]
