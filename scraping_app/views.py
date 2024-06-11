# scraping_app/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ScrapingJob, ScrapingTask
from .serializers import ScrapingJobSerializer
from .tasks import start_scraping_job  # Import the Celery task


class StartScrapingView(APIView):
    def post(self, request, format=None):
        # Extract the list of coins from the request data
        coins = request.data.get("coins", [])

        # Create a new scraping job
        job = ScrapingJob.objects.create()

        # Create tasks for each coin and associate them with the job
        for coin in coins:
            ScrapingTask.objects.create(job=job, coin=coin)

        # Start the Celery task to perform the scraping asynchronously
        # Delayed execution of the Celery task
        start_scraping_job.delay(job.job_id)

        # Return the job_id in the response
        return Response({"job_id": job.job_id}, status=status.HTTP_200_OK)


class ScrapingStatusView(APIView):
    def get(self, request, job_id, format=None):
        # Retrieve job and tasks for the given job_id from the database
        try:
            job = ScrapingJob.objects.get(job_id=job_id)
        except ScrapingJob.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the job and its associated tasks
        serializer = ScrapingJobSerializer(job)
        return Response(serializer.data)
