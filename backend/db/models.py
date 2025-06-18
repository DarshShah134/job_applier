from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class JobListing(Base):
    __tablename__ = 'job_listings'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    company = Column(String)
    description = Column(Text)
    url = Column(String)
    location = Column(String)
    date_posted = Column(DateTime)
    # Add more fields as needed 