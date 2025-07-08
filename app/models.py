"""
Database Models for Resume Analyzer
"""

from app import db
from datetime import datetime
import json

class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    job_role = db.Column(db.String(100), nullable=False)
    keyword_score = db.Column(db.Float, default=0.0)
    ats_score = db.Column(db.Float, default=0.0)
    overall_score = db.Column(db.Float, default=0.0)
    matched_keywords = db.Column(db.Text)  # JSON string
    missing_keywords = db.Column(db.Text)  # JSON string
    ai_suggestions = db.Column(db.Text)
    resume_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(255))
    
    def get_matched_keywords(self):
        return json.loads(self.matched_keywords) if self.matched_keywords else []
    
    def set_matched_keywords(self, keywords):
        self.matched_keywords = json.dumps(keywords)
    
    def get_missing_keywords(self):
        return json.loads(self.missing_keywords) if self.missing_keywords else []
    
    def set_missing_keywords(self, keywords):
        self.missing_keywords = json.dumps(keywords)

class JobRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    keywords = db.Column(db.Text, nullable=False)  # JSON string
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_keywords(self):
        return json.loads(self.keywords) if self.keywords else []
    
    def set_keywords(self, keywords):
        self.keywords = json.dumps(keywords)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
