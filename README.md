
# Crypto Scraper

The Crypto Scraper is a Django-based project that allows you to scrape cryptocurrency data and manage scraping jobs via an API. This guide will help you set up and run the project.

## Prerequisites

Ensure you have the following installed:
- Python 3.x
- pip (Python package installer)

## Installation

### Step 1: Install Required Packages

First, install the required Python packages using `pip`. Run the following command in your terminal:

```bash
pip install -r requirements.txt
```

### Step 2: Initialize the Database

After installing the dependencies, you need to initialize the database. Run the following commands to create the necessary migrations and apply them:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### Step 3: Start the Django Development Server

Once the database is set up, start the Django development server by running:

```bash
python3 manage.py runserver
```

This will start the server at `http://127.0.0.1:8000/`.

![Django Server Running](https://github.com/Jay7221/crypto-scraper/assets/96529359/7706f2af-0555-491e-9f7b-195752114e91)

### Step 4: Run Celery Worker

To handle asynchronous tasks, such as scraping jobs, start a Celery worker. Run the following command in a new terminal window or tab:

```bash
python3 -m celery -A crypto_scraper worker -l info
```

![Celery Worker Running](https://github.com/Jay7221/crypto-scraper/assets/96529359/e3e1d7a5-7e83-4464-b7fc-fba2f65d1784)

## Using the API

With the server and Celery worker running, you can now make API calls to manage scraping jobs.

### Start a Scraping Job

To start a new scraping job, make an API call to the appropriate endpoint. Example request:

![Start Scraping Job](https://github.com/Jay7221/crypto-scraper/assets/96529359/7897bec0-161a-41b0-a388-5f659a234f00)

### View Scraping Job Status

You can also check the status of a scraping job via an API call. Example response:

![Scraping Job Status](https://github.com/Jay7221/crypto-scraper/assets/96529359/0adc298e-0cf1-4e57-9032-a9bb8e449b9e)
