# SerpAPI or RapidAPI job fetcher

import os
import requests
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv('SERPAPI_KEY')
JSEARCH_API_KEY = os.getenv('JSEARCH_API_KEY', '3bd3c70d78msh468db7b1dc08149p1dc5dcjsna8f00ee7c4c2')

# Fetch jobs from SerpAPI (Google Jobs)
def fetch_jobs_from_serpapi(search_query, location, max_results=10):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_jobs",
        "q": search_query,
        "location": location,
        "api_key": SERPAPI_KEY
    }
    response = requests.get(url, params=params)
    jobs = []
    if response.status_code == 200:
        data = response.json()
        results = data.get("jobs_results", [])
        for job in results[:max_results]:
            jobs.append({
                "title": job.get("title"),
                "company": job.get("company_name"),
                "description": job.get("description"),
                "url": job.get("via") or job.get("job_id")
            })
    return jobs

# Fetch jobs from JSearch API (RapidAPI)
def fetch_jobs_from_jsearch(search_query, location, max_results=10):
    url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "X-RapidAPI-Key": JSEARCH_API_KEY,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }
    params = {
        "query": f"{search_query} in {location}",
        "page": 1,
        "num_pages": 1
    }
    response = requests.get(url, headers=headers, params=params)
    jobs = []
    if response.status_code == 200:
        data = response.json()
        results = data.get("data", [])
        for job in results[:max_results]:
            jobs.append({
                "title": job.get("job_title"),
                "company": job.get("employer_name"),
                "description": job.get("job_description"),
                "url": job.get("job_apply_link") or job.get("job_google_link")
            })
    return jobs

def fetch_jobs_from_api(search_query, location, max_results=10, source='serpapi'):
    """
    Fetch jobs from an API (SerpAPI or RapidAPI JSearch).
    Args:
        search_query (str): Job title or keywords to search for.
        location (str): Location to search in.
        max_results (int): Maximum number of jobs to return.
        source (str): 'serpapi' or 'jsearch'.
    Returns:
        List[dict]: List of job dicts with 'title', 'company', 'description', 'url'.
    """
    if source == 'serpapi':
        return fetch_jobs_from_serpapi(search_query, location, max_results)
    elif source == 'jsearch':
        return fetch_jobs_from_jsearch(search_query, location, max_results)
    else:
        return [] 