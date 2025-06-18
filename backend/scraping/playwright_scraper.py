# Playwright job board scraper

from playwright.sync_api import sync_playwright
import time

def scrape_indeed_jobs(page, search_query, location, max_results=10):
    url = f"https://www.indeed.com/jobs?q={search_query.replace(' ', '+')}&l={location.replace(' ', '+')}"
    page.goto(url)
    page.wait_for_selector('div.job_seen_beacon', timeout=10000)
    job_cards = page.query_selector_all('div.job_seen_beacon')
    jobs = []
    for card in job_cards[:max_results]:
        title_el = card.query_selector('h2.jobTitle span')
        company_el = card.query_selector('span.companyName')
        desc_el = card.query_selector('div.job-snippet')
        link_el = card.query_selector('a')
        title = title_el.inner_text().strip() if title_el else None
        company = company_el.inner_text().strip() if company_el else None
        description = desc_el.inner_text().strip().replace('\n', ' ') if desc_el else None
        url = link_el.get_attribute('href') if link_el else None
        if url and not url.startswith('http'):
            url = 'https://www.indeed.com' + url
        jobs.append({
            'title': title,
            'company': company,
            'description': description,
            'url': url
        })
    return jobs

def scrape_linkedin_jobs(page, search_query, location, max_results=10):
    url = f"https://www.linkedin.com/jobs/search/?keywords={search_query.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
    page.goto(url)
    try:
        page.wait_for_selector('ul.jobs-search__results-list li', timeout=10000)
    except Exception:
        return []
    job_cards = page.query_selector_all('ul.jobs-search__results-list li')
    jobs = []
    for card in job_cards[:max_results]:
        title_el = card.query_selector('h3.base-search-card__title')
        company_el = card.query_selector('h4.base-search-card__subtitle')
        desc_el = card.query_selector('p.job-search-card__snippet')
        link_el = card.query_selector('a.base-card__full-link')
        title = title_el.inner_text().strip() if title_el else None
        company = company_el.inner_text().strip() if company_el else None
        description = desc_el.inner_text().strip().replace('\n', ' ') if desc_el else None
        url = link_el.get_attribute('href') if link_el else None
        jobs.append({
            'title': title,
            'company': company,
            'description': description,
            'url': url
        })
    return jobs

def scrape_glassdoor_jobs(page, search_query, location, max_results=10):
    url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={search_query.replace(' ', '%20')}&locT=C&locId=&locKeyword={location.replace(' ', '%20')}"
    page.goto(url)
    try:
        page.wait_for_selector('ul.jobs li.react-job-listing', timeout=10000)
    except Exception:
        return []
    job_cards = page.query_selector_all('ul.jobs li.react-job-listing')
    jobs = []
    for card in job_cards[:max_results]:
        title_el = card.query_selector('a.jobLink span')
        company_el = card.query_selector('div.jobHeader a')
        desc_el = card.query_selector('div.job-snippet')
        link_el = card.query_selector('a.jobLink')
        title = title_el.inner_text().strip() if title_el else None
        company = company_el.inner_text().strip() if company_el else None
        description = desc_el.inner_text().strip().replace('\n', ' ') if desc_el else None
        url = link_el.get_attribute('href') if link_el else None
        if url and not url.startswith('http'):
            url = 'https://www.glassdoor.com' + url
        jobs.append({
            'title': title,
            'company': company,
            'description': description,
            'url': url
        })
    return jobs

def scrape_jobs_with_playwright(search_query, location, max_results=10, source='indeed'):
    """
    Scrape job listings from a job board using Playwright.
    Args:
        search_query (str): Job title or keywords to search for.
        location (str): Location to search in.
        max_results (int): Maximum number of jobs to return.
        source (str): 'indeed', 'linkedin', or 'glassdoor'.
    Returns:
        List[dict]: List of job dicts with 'title', 'company', 'description', 'url'.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        if source == 'indeed':
            jobs = scrape_indeed_jobs(page, search_query, location, max_results)
        elif source == 'linkedin':
            jobs = scrape_linkedin_jobs(page, search_query, location, max_results)
        elif source == 'glassdoor':
            jobs = scrape_glassdoor_jobs(page, search_query, location, max_results)
        else:
            jobs = []
        browser.close()
    return jobs 