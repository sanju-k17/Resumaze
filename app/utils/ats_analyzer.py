"""
ATS (Applicant Tracking System) Analyzer
Analyzes resume for ATS compatibility
"""

import os
import re
import fitz  # PyMuPDF
from docx import Document

class ATSAnalyzer:
    def __init__(self):
        self.ats_factors = {
            'file_format': 20,      # PDF/DOCX compatibility
            'text_extraction': 25,   # Text extractability
            'formatting': 20,        # Clean formatting
            'structure': 20,         # Logical structure
            'keywords': 15           # Keyword density
        }
    
    def analyze_file(self, file_path):
        """Analyze file for ATS compatibility"""
        try:
            score = 0
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # File format score
            if file_ext in ['.pdf', '.docx']:
                score += self.ats_factors['file_format']
            
            # Extract text and analyze
            if file_ext == '.pdf':
                text = self._extract_pdf_text(file_path)
            elif file_ext == '.docx':
                text = self._extract_docx_text(file_path)
            else:
                return 0
            
            if text:
                score += self.ats_factors['text_extraction']
                
                # Analyze text structure
                score += self._analyze_structure(text)
                score += self._analyze_formatting(text)
                score += self._analyze_keywords(text)
            
            return min(score, 100)
            
        except Exception as e:
            print(f"ATS Analysis error: {str(e)}")
            return 50  # Default score if analysis fails
    
    def _extract_pdf_text(self, file_path):
        """Extract text from PDF"""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except:
            return ""
    
    def _extract_docx_text(self, file_path):
        """Extract text from DOCX"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except:
            return ""
    
    def _analyze_structure(self, text):
        """Analyze document structure"""
        score = 0
        text_lower = text.lower()
        
        # Check for common sections
        sections = ['experience', 'education', 'skills', 'summary', 'objective']
        found_sections = sum(1 for section in sections if section in text_lower)
        
        if found_sections >= 3:
            score = self.ats_factors['structure']
        elif found_sections >= 2:
            score = self.ats_factors['structure'] * 0.7
        else:
            score = self.ats_factors['structure'] * 0.3
        
        return score
    
    def _analyze_formatting(self, text):
        """Analyze formatting quality"""
        score = self.ats_factors['formatting']
        
        # Check for excessive special characters
        special_chars = len(re.findall(r'[^\w\s\.\,\-\@$$$$]', text))
        if special_chars > len(text) * 0.05:  # More than 5% special chars
            score *= 0.7
        
        # Check for reasonable line length
        lines = text.split('\n')
        avg_line_length = sum(len(line) for line in lines) / len(lines) if lines else 0
        if avg_line_length > 100:  # Very long lines might indicate formatting issues
            score *= 0.8
        
        return score
    
    def _analyze_keywords(self, text):
        """Analyze keyword density"""
        words = text.split()
        if len(words) < 100:
            return self.ats_factors['keywords'] * 0.5
        elif len(words) > 800:
            return self.ats_factors['keywords'] * 0.8
        else:
            return self.ats_factors['keywords']
