from flask import Flask, request, jsonify
from scraping.playwright_scraper import scrape_jobs_with_playwright
from scraping.api_fetcher import fetch_jobs_from_api
from nlp.extractor import filter_target_internship_jobs, is_target_internship_role

app = Flask(__name__)

# Improved flexible filter for internship roles
def is_flexible_internship_role(title):
    if not title:
        return False
    title_lower = title.lower()
    if "intern" not in title_lower:
        return False
    target_keywords = [
        "software", "development", "data", "ai", "ml", "quantitative", "cybersecurity"
    ]
    return any(keyword in title_lower for keyword in target_keywords)

def filter_flexible_internship_jobs(jobs):
    return [job for job in jobs if is_flexible_internship_role(job.get('title'))]

@app.route('/jobs/scrape_and_rank', methods=['POST'])
def scrape_and_rank():
    data = request.get_json()
    search_query = data.get('search_query', 'intern')
    location = data.get('location', '')
    source = data.get('source', 'jsearch')  # 'indeed', 'linkedin', 'glassdoor', 'serpapi', 'jsearch'
    max_results = int(data.get('max_results', 20))
    # Choose fetcher based on source
    if source in ['indeed', 'linkedin', 'glassdoor']:
        jobs = scrape_jobs_with_playwright(search_query, location, max_results, source=source)
    elif source in ['serpapi', 'jsearch']:
        jobs = fetch_jobs_from_api(search_query, location, max_results, source=source)
    else:
        return jsonify({'error': 'Invalid source'}), 400
    # Print all job titles for debugging
    print("Raw job titles:")
    for job in jobs:
        print(job.get('title'))
    # Use the improved flexible filter
    filtered_jobs = filter_flexible_internship_jobs(jobs)
    return jsonify({'jobs': filtered_jobs})

if __name__ == '__main__':
    app.run(debug=True) 