"""
Email Sender for Resume Analysis Reports
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

class EmailSender:
    def __init__(self):
        self.smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', 587))
        self.email = os.environ.get('SMTP_EMAIL')
        self.password = os.environ.get('SMTP_PASSWORD')
    
    def send_report(self, recipient_email, analysis, pdf_path):
        """Send resume analysis report via email"""
        if not self.email or not self.password:
            raise Exception("Email configuration not found. Please set SMTP_EMAIL and SMTP_PASSWORD environment variables.")
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = recipient_email
            msg['Subject'] = f"Resume Analysis Report - {analysis.job_role}"
            
            # Email body
            body = self._create_email_body(analysis)
            msg.attach(MIMEText(body, 'html'))
            
            # Attach PDF report
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= resume_analysis_report_{analysis.id}.pdf'
                )
                msg.attach(part)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            text = msg.as_string()
            server.sendmail(self.email, recipient_email, text)
            server.quit()
            
            print(f"Email sent successfully to {recipient_email}")
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            raise Exception(f"Failed to send email: {str(e)}")
    
    def _create_email_body(self, analysis):
        """Create HTML email body"""
        matched_keywords = analysis.get_matched_keywords()
        missing_keywords = analysis.get_missing_keywords()
        
        body = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background-color: #3B82F6; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; }}
                .score-box {{ background-color: #F3F4F6; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .score {{ font-size: 24px; font-weight: bold; color: #3B82F6; }}
                .keywords {{ margin: 10px 0; }}
                .matched {{ color: #10B981; }}
                .missing {{ color: #EF4444; }}
                .suggestions {{ background-color: #FEF3C7; padding: 15px; border-left: 4px solid #F59E0B; }}
                .footer {{ text-align: center; color: #6B7280; font-size: 12px; margin-top: 30px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Resume Analysis Report</h1>
                <p>AI-Powered Resume Analysis Results</p>
            </div>
            
            <div class="content">
                <h2>Analysis Summary</h2>
                <div class="score-box">
                    <p><strong>Resume:</strong> {analysis.filename}</p>
                    <p><strong>Job Role:</strong> {analysis.job_role}</p>
                    <p><strong>Analysis Date:</strong> {analysis.created_at.strftime('%B %d, %Y')}</p>
                    <p><strong>Overall Score:</strong> <span class="score">{analysis.overall_score:.1f}%</span></p>
                </div>
                
                <h3>Score Breakdown</h3>
                <ul>
                    <li><strong>Keyword Match:</strong> {analysis.keyword_score:.1f}%</li>
                    <li><strong>ATS Compatibility:</strong> {analysis.ats_score:.1f}%</li>
                    <li><strong>Overall Quality:</strong> {analysis.overall_score:.1f}%</li>
                </ul>
                
                <h3>Keyword Analysis</h3>
                <div class="keywords">
                    <p><strong class="matched">Matched Keywords ({len(matched_keywords)}):</strong></p>
                    <p>{', '.join(matched_keywords) if matched_keywords else 'None found'}</p>
                    
                    <p><strong class="missing">Missing Keywords ({len(missing_keywords)}):</strong></p>
                    <p>{', '.join(missing_keywords) if missing_keywords else 'All keywords found!'}</p>
                </div>
        """
        
        if analysis.ai_suggestions:
            body += f"""
                <h3>AI Recommendations</h3>
                <div class="suggestions">
                    {analysis.ai_suggestions.replace(chr(10), '<br>')}
                </div>
            """
        
        body += f"""
                <h3>Next Steps</h3>
                <ul>
                    <li>Review and incorporate the missing keywords identified above</li>
                    <li>Ensure your resume follows ATS-friendly formatting guidelines</li>
                    <li>Quantify your achievements with specific numbers and metrics</li>
                    <li>Tailor your resume content to match the specific job requirements</li>
                </ul>
                
                <p>Please find the detailed PDF report attached to this email.</p>
            </div>
            
            <div class="footer">
                <p>Generated by AI Resume Analyzer on {datetime.now().strftime('%B %d, %Y')}</p>
                <p>This is an automated email. Please do not reply.</p>
            </div>
        </body>
        </html>
        """
        
        return body
