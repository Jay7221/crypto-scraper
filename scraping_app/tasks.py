# scraping_app/tasks.py
from celery import shared_task
from .models import ScrapingJob, ScrapingTask
from .coinmarketcap import CoinMarketCapScraper  # Import the scraping logic


@shared_task
def start_scraping_job(job_id):
    # Retrieve the scraping job from the database
    job = ScrapingJob.objects.get(job_id=job_id)

    # Retrieve all tasks associated with the job
    tasks = ScrapingTask.objects.filter(job=job)

    # Iterate over each task and perform scraping for the corresponding coin
    for task in tasks:
        coin = task.coin

        # Perform scraping for the coin and update the task output
        scraper = CoinMarketCapScraper(
            url=f"https://coinmarketcap.com/currencies/{coin}/")
        output = scraper.fetch_all_values()  # Extract all data for the coin
        task.output = output  # Save the scraped data to the task
        task.status = 'COMPLETED'  # Update task status to completed
        task.save()

    # Update the job status to indicate that all tasks are completed
    job.status = 'COMPLETED'
    job.save()

    return f"Scraping job with ID {job_id} completed successfully."
