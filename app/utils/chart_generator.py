"""
Chart Generator for Resume Analysis Visualizations
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import os
import json
from datetime import datetime

class ChartGenerator:
    def __init__(self):
        self.chart_dir = 'static/charts'
        os.makedirs(self.chart_dir, exist_ok=True)
    
    def generate_analysis_charts(self, analysis):
        """Generate charts for individual analysis"""
        charts = {}
        
        # Score breakdown pie chart
        charts['score_breakdown'] = self._create_score_breakdown_chart(analysis)
        
        # Keywords match chart
        charts['keywords_match'] = self._create_keywords_chart(analysis)
        
        # Skills radar chart
        charts['skills_radar'] = self._create_skills_radar_chart(analysis)
        
        return charts
    
    def _create_score_breakdown_chart(self, analysis):
        """Create score breakdown pie chart"""
        try:
            labels = ['Keyword Match', 'ATS Score', 'AI Quality']
            values = [analysis.keyword_score, analysis.ats_score, 
                     min(analysis.overall_score * 0.3 / 0.3, 100)]
            colors = ['#3B82F6', '#10B981', '#F59E0B']
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                marker_colors=colors,
                textinfo='label+percent',
                textposition='outside'
            )])
            
            fig.update_layout(
                title=f"Score Breakdown - Overall: {analysis.overall_score:.1f}%",
                font=dict(size=14),
                showlegend=True,
                height=400,
                margin=dict(t=50, b=50, l=50, r=50)
            )
            
            chart_path = f"{self.chart_dir}/score_breakdown_{analysis.id}.html"
            fig.write_html(chart_path)
            return chart_path.replace('static/', '')
            
        except Exception as e:
            print(f"Error creating score breakdown chart: {str(e)}")
            return None
    
    def _create_keywords_chart(self, analysis):
        """Create keywords match vs missing chart"""
        try:
            matched = analysis.get_matched_keywords()
            missing = analysis.get_missing_keywords()
            
            fig = go.Figure()
            
            # Matched keywords
            fig.add_trace(go.Bar(
                name='Matched Keywords',
                x=['Keywords'],
                y=[len(matched)],
                marker_color='#10B981',
                text=f'{len(matched)} matched',
                textposition='auto'
            ))
            
            # Missing keywords
            fig.add_trace(go.Bar(
                name='Missing Keywords',
                x=['Keywords'],
                y=[len(missing)],
                marker_color='#EF4444',
                text=f'{len(missing)} missing',
                textposition='auto'
            ))
            
            fig.update_layout(
                title='Keyword Analysis',
                xaxis_title='',
                yaxis_title='Number of Keywords',
                barmode='stack',
                height=300,
                margin=dict(t=50, b=50, l=50, r=50)
            )
            
            chart_path = f"{self.chart_dir}/keywords_{analysis.id}.html"
            fig.write_html(chart_path)
            return chart_path.replace('static/', '')
            
        except Exception as e:
            print(f"Error creating keywords chart: {str(e)}")
            return None
    
    def _create_skills_radar_chart(self, analysis):
        """Create skills radar chart"""
        try:
            categories = ['Technical Skills', 'Experience', 'Education', 'Certifications', 'Soft Skills']
            
            # Simple scoring based on text analysis
            text = analysis.resume_text.lower()
            scores = []
            
            # Technical skills
            tech_keywords = ['python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes']
            tech_score = sum(1 for keyword in tech_keywords if keyword in text) * 20
            scores.append(min(tech_score, 100))
            
            # Experience (based on years mentioned)
            exp_score = len([word for word in text.split() if 'year' in word]) * 25
            scores.append(min(exp_score, 100))
            
            # Education
            edu_keywords = ['degree', 'university', 'college', 'bachelor', 'master', 'phd']
            edu_score = sum(1 for keyword in edu_keywords if keyword in text) * 30
            scores.append(min(edu_score, 100))
            
            # Certifications
            cert_keywords = ['certified', 'certification', 'license']
            cert_score = sum(1 for keyword in cert_keywords if keyword in text) * 40
            scores.append(min(cert_score, 100))
            
            # Soft skills
            soft_keywords = ['leadership', 'communication', 'teamwork', 'problem solving']
            soft_score = sum(1 for keyword in soft_keywords if keyword in text) * 25
            scores.append(min(soft_score, 100))
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=scores,
                theta=categories,
                fill='toself',
                name='Skills Profile',
                line_color='#3B82F6'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                title="Skills Profile Analysis",
                height=400,
                margin=dict(t=50, b=50, l=50, r=50)
            )
            
            chart_path = f"{self.chart_dir}/skills_radar_{analysis.id}.html"
            fig.write_html(chart_path)
            return chart_path.replace('static/', '')
            
        except Exception as e:
            print(f"Error creating skills radar chart: {str(e)}")
            return None
    
    def generate_dashboard_charts(self, analyses):
        """Generate dashboard charts"""
        if not analyses:
            return {}
        
        charts = {}
        
        # Score trend over time
        charts['score_trend'] = self._create_score_trend_chart(analyses)
        
        # Job role distribution
        charts['role_distribution'] = self._create_role_distribution_chart(analyses)
        
        return charts
    
    def _create_score_trend_chart(self, analyses):
        """Create score trend chart"""
        try:
            df = pd.DataFrame([{
                'date': analysis.created_at,
                'overall_score': analysis.overall_score,
                'keyword_score': analysis.keyword_score,
                'ats_score': analysis.ats_score
            } for analysis in analyses])
            
            df = df.sort_values('date')
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['overall_score'],
                mode='lines+markers',
                name='Overall Score',
                line=dict(color='#3B82F6', width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['keyword_score'],
                mode='lines+markers',
                name='Keyword Score',
                line=dict(color='#10B981', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['ats_score'],
                mode='lines+markers',
                name='ATS Score',
                line=dict(color='#F59E0B', width=2)
            ))
            
            fig.update_layout(
                title='Score Trends Over Time',
                xaxis_title='Date',
                yaxis_title='Score (%)',
                height=400,
                margin=dict(t=50, b=50, l=50, r=50)
            )
            
            chart_path = f"{self.chart_dir}/score_trend.html"
            fig.write_html(chart_path)
            return chart_path.replace('static/', '')
            
        except Exception as e:
            print(f"Error creating score trend chart: {str(e)}")
            return None
    
    def _create_role_distribution_chart(self, analyses):
        """Create job role distribution chart"""
        try:
            role_counts = {}
            for analysis in analyses:
                role = analysis.job_role
                role_counts[role] = role_counts.get(role, 0) + 1
            
            fig = go.Figure(data=[go.Bar(
                x=list(role_counts.keys()),
                y=list(role_counts.values()),
                marker_color='#3B82F6'
            )])
            
            fig.update_layout(
                title='Analysis by Job Role',
                xaxis_title='Job Role',
                yaxis_title='Number of Analyses',
                height=300,
                margin=dict(t=50, b=50, l=50, r=50)
            )
            
            chart_path = f"{self.chart_dir}/role_distribution.html"
            fig.write_html(chart_path)
            return chart_path.replace('static/', '')
            
        except Exception as e:
            print(f"Error creating role distribution chart: {str(e)}")
            return None
    
    def generate_comparison_charts(self, analyses):
        """Generate comparison charts"""
        charts = {}
        
        if len(analyses) >= 2:
            charts['comparison'] = self._create_comparison_chart(analyses[:5])  # Compare top 5
        
        return charts
    
    def _create_comparison_chart(self, analyses):
        """Create comparison chart for multiple analyses"""
        try:
            fig = go.Figure()
            
            categories = ['Overall Score', 'Keyword Score', 'ATS Score']
            
            for i, analysis in enumerate(analyses):
                values = [analysis.overall_score, analysis.keyword_score, analysis.ats_score]
                
                fig.add_trace(go.Bar(
                    name=f"Analysis {analysis.id} ({analysis.job_role})",
                    x=categories,
                    y=values
                ))
            
            fig.update_layout(
                title='Resume Analysis Comparison',
                xaxis_title='Score Type',
                yaxis_title='Score (%)',
                barmode='group',
                height=400,
                margin=dict(t=50, b=50, l=50, r=50)
            )
            
            chart_path = f"{self.chart_dir}/comparison.html"
            fig.write_html(chart_path)
            return chart_path.replace('static/', '')
            
        except Exception as e:
            print(f"Error creating comparison chart: {str(e)}")
            return None
