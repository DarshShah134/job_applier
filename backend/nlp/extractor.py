# NLP extractor for job fields

import spacy
import re

# Load spaCy English model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None  # Model not loaded, handle in function

# Example list of common tech skills (expand as needed)
COMMON_SKILLS = [
    "Python", "Java", "JavaScript", "SQL", "AWS", "Docker", "Kubernetes", "React", "Node.js",
    "C++", "C#", "Git", "Linux", "TensorFlow", "PyTorch", "Machine Learning", "Data Analysis",
    "Communication", "Leadership", "Project Management", "Agile", "Scrum"
]

# List of target internship roles (lowercase for matching)
TARGET_INTERNSHIP_KEYWORDS = [
    "software engineer intern",
    "software development intern",
    "data engineering intern",
    "ai intern",
    "ml intern",
    "quantitative developer intern",
    "quantitative research intern",
    "cybersecurity intern"
]

def is_target_internship_role(title):
    if not title:
        return False
    title_lower = title.lower()
    return any(keyword in title_lower for keyword in TARGET_INTERNSHIP_KEYWORDS)

def filter_target_internship_jobs(jobs):
    """
    Filter jobs to only include those whose title matches the target internship roles.
    """
    return [job for job in jobs if is_target_internship_role(job.get('title'))]

def extract_job_fields(job_description):
    """
    Extract job title, responsibilities, and skills from a job description using spaCy and regex.
    Returns a dict with 'title', 'responsibilities', 'skills'.
    """
    if not job_description:
        return {'title': None, 'responsibilities': [], 'skills': []}
    # Load spaCy model if not loaded
    global nlp
    if nlp is None:
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            return {'title': None, 'responsibilities': [], 'skills': []}
    doc = nlp(job_description)
    # Title extraction: look for first noun chunk or use first line
    lines = job_description.split('\n')
    title = None
    for line in lines:
        if len(line.strip()) > 5 and len(line.split()) < 10:
            title = line.strip()
            break
    if not title and doc.noun_chunks:
        title = next(doc.noun_chunks).text
    # Responsibilities extraction: bullet points or imperative sentences
    bullets = re.findall(r'[-*•]\s*(.+)', job_description)
    if not bullets:
        # Fallback: sentences starting with a verb
        bullets = [sent.text.strip() for sent in doc.sents if sent.text.strip() and sent[0].pos_ == 'VERB']
    responsibilities = bullets
    # Skills extraction: match from COMMON_SKILLS
    skills_found = set()
    for skill in COMMON_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, job_description, re.IGNORECASE):
            skills_found.add(skill)
    skills = list(skills_found)
    return {
        'title': title,
        'responsibilities': responsibilities,
        'skills': skills
    } 