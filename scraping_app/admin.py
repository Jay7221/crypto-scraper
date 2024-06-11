from django.contrib import admin
from .models import ScrapingJob, ScrapingTask

# Register your models here.
admin.site.register(ScrapingJob)
admin.site.register(ScrapingTask)
