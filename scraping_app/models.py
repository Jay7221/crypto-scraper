# scraping_app/models.py
import uuid
from django.db import models


class ScrapingJob(models.Model):
    job_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)


class ScrapingTask(models.Model):
    job = models.ForeignKey(
        ScrapingJob, related_name='tasks', on_delete=models.CASCADE)
    coin = models.CharField(max_length=100)
    output = models.JSONField(null=True)
