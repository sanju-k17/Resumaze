"""
PDF Report Generator using ReportLab
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.report_dir = 'static/reports'
        os.makedirs(self.report_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1F2937')
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#374151')
        )
        
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            alignment=TA_JUSTIFY
        )
    
    def generate_pdf_report(self, analysis):
        """Generate comprehensive PDF report"""
        try:
            filename = f"resume_analysis_report_{analysis.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(self.report_dir, filename)
            
            doc = SimpleDocTemplate(filepath, pagesize=A4, 
                                  rightMargin=72, leftMargin=72,
                                  topMargin=72, bottomMargin=18)
            
            story = []
            
            # Title
            story.append(Paragraph("Resume Analysis Report", self.title_style))
            story.append(Spacer(1, 20))
            
            # Analysis Summary
            story.append(Paragraph("Analysis Summary", self.heading_style))
            
            summary_data = [
                ['Resume File:', analysis.filename],
                ['Job Role:', analysis.job_role],
                ['Analysis Date:', analysis.created_at.strftime('%B %d, %Y at %I:%M %p')],
                ['Overall Score:', f"{analysis.overall_score:.1f}%"]
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 4*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB'))
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 20))
            
            # Score Breakdown
            story.append(Paragraph("Score Breakdown", self.heading_style))
            
            score_data = [
                ['Metric', 'Score', 'Description'],
                ['Keyword Match', f"{analysis.keyword_score:.1f}%", 'Relevance to job requirements'],
                ['ATS Compatibility', f"{analysis.ats_score:.1f}%", 'Applicant Tracking System readiness'],
                ['Overall Quality', f"{analysis.overall_score:.1f}%", 'Combined assessment score']
            ]
            
            score_table = Table(score_data, colWidths=[2*inch, 1.5*inch, 2.5*inch])
            score_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB'))
            ]))
            
            story.append(score_table)
            story.append(Spacer(1, 20))
            
            # Keyword Analysis
            story.append(Paragraph("Keyword Analysis", self.heading_style))
            
            matched_keywords = analysis.get_matched_keywords()
            missing_keywords = analysis.get_missing_keywords()
            
            if matched_keywords:
                story.append(Paragraph("<b>Matched Keywords:</b>", self.body_style))
                matched_text = ", ".join(matched_keywords)
                story.append(Paragraph(matched_text, self.body_style))
                story.append(Spacer(1, 10))
            
            if missing_keywords:
                story.append(Paragraph("<b>Missing Keywords:</b>", self.body_style))
                missing_text = ", ".join(missing_keywords)
                story.append(Paragraph(f'<font color="red">{missing_text}</font>', self.body_style))
                story.append(Spacer(1, 20))
            
            # AI Suggestions
            if analysis.ai_suggestions:
                story.append(Paragraph("AI-Powered Recommendations", self.heading_style))
                
                # Split suggestions by bullet points
                suggestions = analysis.ai_suggestions.split('\n')
                for suggestion in suggestions:
                    if suggestion.strip():
                        story.append(Paragraph(suggestion, self.body_style))
                
                story.append(Spacer(1, 20))
            
            # Resume Content Preview
            story.append(Paragraph("Resume Content Preview", self.heading_style))
            preview_text = analysis.resume_text[:1000] + "..." if len(analysis.resume_text) > 1000 else analysis.resume_text
            story.append(Paragraph(preview_text, self.body_style))
            story.append(Spacer(1, 20))
            
            # Recommendations
            story.append(Paragraph("Next Steps", self.heading_style))
            
            recommendations = [
                "• Review and incorporate the missing keywords identified above",
                "• Ensure your resume follows ATS-friendly formatting guidelines",
                "• Quantify your achievements with specific numbers and metrics",
                "• Tailor your resume content to match the specific job requirements",
                "• Consider having your resume reviewed by industry professionals"
            ]
            
            for rec in recommendations:
                story.append(Paragraph(rec, self.body_style))
            
            story.append(Spacer(1, 30))
            
            # Footer
            footer_text = f"Generated by AI Resume Analyzer on {datetime.now().strftime('%B %d, %Y')}"
            footer_style = ParagraphStyle(
                'Footer',
                parent=self.styles['Normal'],
                fontSize=9,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#6B7280')
            )
            story.append(Paragraph(footer_text, footer_style))
            
            # Build PDF
            doc.build(story)
            
            return filepath
            
        except Exception as e:
            print(f"Error generating PDF report: {str(e)}")
            raise Exception(f"Failed to generate PDF report: {str(e)}")
