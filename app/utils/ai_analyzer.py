"""
AI-powered Resume Analyzer using OpenAI API
"""

import openai
import os
import re
from typing import List, Dict, Tuple
import json

class AIAnalyzer:
    def __init__(self):
        # Set OpenAI API key from environment variable
        openai.api_key = os.environ.get('OPENAI_API_KEY')
        self.model = "gpt-3.5-turbo"
    
    def analyze_resume(self, resume_text: str, job_role: str, job_description: str = "") -> Dict:
        """Comprehensive AI analysis of resume"""
        try:
            # Prepare the prompt
            prompt = self._create_analysis_prompt(resume_text, job_role, job_description)
            
            # Make API call to OpenAI
            if openai.api_key:
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert HR professional and resume analyst."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=1000,
                    temperature=0.7
                )
                
                ai_response = response.choices[0].message.content
                return self._parse_ai_response(ai_response)
            else:
                # Fallback analysis without OpenAI
                return self._fallback_analysis(resume_text, job_role)
                
        except Exception as e:
            print(f"AI Analysis error: {str(e)}")
            return self._fallback_analysis(resume_text, job_role)
    
    def _create_analysis_prompt(self, resume_text: str, job_role: str, job_description: str) -> str:
        """Create detailed prompt for AI analysis"""
        prompt = f"""
        Analyze this resume for a {job_role} position and provide detailed feedback.
        
        Resume Text:
        {resume_text[:3000]}  # Limit text to avoid token limits
        
        Job Role: {job_role}
        """
        
        if job_description:
            prompt += f"\nJob Description: {job_description[:1000]}"
        
        prompt += """
        
        Please provide analysis in the following format:
        
        STRENGTHS:
        - List 3-5 key strengths
        
        IMPROVEMENTS:
        - List 3-5 specific improvement suggestions
        
        MISSING_ELEMENTS:
        - List elements that should be added
        
        QUALITY_SCORE: [0-100]
        
        RECOMMENDATIONS:
        - Provide 3-5 actionable recommendations
        """
        
        return prompt
    
    def _parse_ai_response(self, response: str) -> Dict:
        """Parse AI response into structured data"""
        analysis = {
            'strengths': [],
            'improvements': [],
            'missing_elements': [],
            'quality_score': 75,
            'suggestions': '',
            'recommendations': []
        }
        
        try:
            # Extract sections using regex
            sections = {
                'strengths': r'STRENGTHS:(.*?)(?=IMPROVEMENTS:|MISSING_ELEMENTS:|QUALITY_SCORE:|RECOMMENDATIONS:|$)',
                'improvements': r'IMPROVEMENTS:(.*?)(?=STRENGTHS:|MISSING_ELEMENTS:|QUALITY_SCORE:|RECOMMENDATIONS:|$)',
                'missing_elements': r'MISSING_ELEMENTS:(.*?)(?=STRENGTHS:|IMPROVEMENTS:|QUALITY_SCORE:|RECOMMENDATIONS:|$)',
                'recommendations': r'RECOMMENDATIONS:(.*?)(?=STRENGTHS:|IMPROVEMENTS:|MISSING_ELEMENTS:|QUALITY_SCORE:|$)'
            }
            
            for key, pattern in sections.items():
                match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
                if match:
                    content = match.group(1).strip()
                    # Split by bullet points or newlines
                    items = [item.strip('- ').strip() for item in content.split('\n') if item.strip() and item.strip() != '-']
                    analysis[key] = [item for item in items if len(item) > 10]  # Filter out short items
            
            # Extract quality score
            score_match = re.search(r'QUALITY_SCORE:\s*(\d+)', response, re.IGNORECASE)
            if score_match:
                analysis['quality_score'] = int(score_match.group(1))
            
            # Create suggestions text
            suggestions = []
            if analysis['improvements']:
                suggestions.extend(analysis['improvements'])
            if analysis['recommendations']:
                suggestions.extend(analysis['recommendations'])
            
            analysis['suggestions'] = '\n'.join(f"• {suggestion}" for suggestion in suggestions[:8])
            
        except Exception as e:
            print(f"Error parsing AI response: {str(e)}")
            analysis['suggestions'] = "AI analysis completed. Consider improving keyword density and formatting."
        
        return analysis
    
    def _fallback_analysis(self, resume_text: str, job_role: str) -> Dict:
        """Fallback analysis when AI is not available"""
        word_count = len(resume_text.split())
        
        # Basic heuristic analysis
        quality_score = 60
        
        # Adjust score based on length
        if word_count > 200:
            quality_score += 10
        if word_count > 400:
            quality_score += 10
        
        # Check for common sections
        sections = ['experience', 'education', 'skills', 'contact']
        found_sections = sum(1 for section in sections if section in resume_text.lower())
        quality_score += found_sections * 5
        
        suggestions = [
            "Ensure your resume includes all relevant keywords for the position",
            "Use action verbs to describe your accomplishments",
            "Quantify your achievements with specific numbers and metrics",
            "Keep your resume format clean and ATS-friendly",
            "Tailor your resume content to match the job requirements"
        ]
        
        return {
            'quality_score': min(quality_score, 95),
            'suggestions': '\n'.join(f"• {suggestion}" for suggestion in suggestions),
            'strengths': ["Professional formatting", "Relevant experience"],
            'improvements': ["Add more quantified achievements", "Include relevant keywords"],
            'missing_elements': ["Skills section optimization"],
            'recommendations': suggestions[:3]
        }
    
    def calculate_keyword_score(self, resume_text: str, keywords: List[str]) -> Tuple[List[str], List[str], float]:
        """Calculate keyword matching score"""
        resume_lower = resume_text.lower()
        
        matched_keywords = []
        missing_keywords = []
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Check for exact match or partial match
            if keyword_lower in resume_lower or any(word in resume_lower for word in keyword_lower.split()):
                matched_keywords.append(keyword)
            else:
                missing_keywords.append(keyword)
        
        # Calculate score
        if not keywords:
            return matched_keywords, missing_keywords, 0.0
        
        score = (len(matched_keywords) / len(keywords)) * 100
        return matched_keywords, missing_keywords, round(score, 1)
    
    def analyze_job_description_similarity(self, resume_text: str, job_description: str) -> Dict:
        """Analyze similarity between resume and job description"""
        if not job_description:
            return {'similarity_score': 0, 'common_terms': [], 'suggestions': []}
        
        # Simple keyword overlap analysis
        resume_words = set(word.lower() for word in re.findall(r'\b\w+\b', resume_text) if len(word) > 3)
        jd_words = set(word.lower() for word in re.findall(r'\b\w+\b', job_description) if len(word) > 3)
        
        common_words = resume_words.intersection(jd_words)
        similarity_score = len(common_words) / len(jd_words) * 100 if jd_words else 0
        
        return {
            'similarity_score': round(similarity_score, 1),
            'common_terms': list(common_words)[:20],  # Top 20 common terms
            'suggestions': [
                "Include more keywords from the job description",
                "Align your experience descriptions with job requirements",
                "Use similar terminology as mentioned in the job posting"
            ]
        }
