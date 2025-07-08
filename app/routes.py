"""
Flask Routes for Resume Analyzer
"""

from flask import Blueprint, render_template, request, jsonify, send_file, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime

from app import db
from app.models import Analysis, JobRole, User
from app.utils.resume_parser import ResumeParser
from app.utils.ai_analyzer import AIAnalyzer
from app.utils.ats_analyzer import ATSAnalyzer
from app.utils.chart_generator import ChartGenerator
from app.utils.report_generator import ReportGenerator
from app.utils.email_sender import EmailSender

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    """Home page with upload form"""
    job_roles = JobRole.query.all()
    recent_analyses = Analysis.query.order_by(Analysis.created_at.desc()).limit(5).all()
    
    # Get statistics
    total_analyses = Analysis.query.count()
    avg_score = db.session.query(db.func.avg(Analysis.overall_score)).scalar() or 0
    
    return render_template('index.html', 
                         job_roles=job_roles, 
                         recent_analyses=recent_analyses,
                         total_analyses=total_analyses,
                         avg_score=round(avg_score, 1))

@main.route('/upload', methods=['POST'])
def upload_resume():
    """Handle resume upload and analysis"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['resume']
        job_role = request.form.get('job_role')
        job_description = request.form.get('job_description', '')
        email = request.form.get('email', '')
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF or DOCX files.'}), 400
        
        if not job_role:
            return jsonify({'error': 'Please select a job role'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join('uploads', unique_filename)
        file.save(filepath)
        
        # Parse resume
        parser = ResumeParser()
        resume_text = parser.extract_text(filepath)
        
        if not resume_text.strip():
            os.remove(filepath)
            return jsonify({'error': 'Could not extract text from resume'}), 400
        
        # Get job role keywords
        role = JobRole.query.filter_by(name=job_role).first()
        if not role:
            os.remove(filepath)
            return jsonify({'error': 'Invalid job role selected'}), 400
        
        # Analyze resume
        analyzer = AIAnalyzer()
        ai_analysis = analyzer.analyze_resume(resume_text, job_role, job_description)
        
        # Calculate keyword matching
        keywords = role.get_keywords()
        matched_keywords, missing_keywords, keyword_score = analyzer.calculate_keyword_score(resume_text, keywords)
        
        # ATS Analysis
        ats_analyzer = ATSAnalyzer()
        ats_score = ats_analyzer.analyze_file(filepath)
        
        # Calculate overall score
        overall_score = (keyword_score * 0.4 + ats_score * 0.3 + min(ai_analysis.get('quality_score', 70), 100) * 0.3)
        
        # Save analysis to database
        analysis = Analysis(
            filename=filename,
            job_role=job_role,
            keyword_score=keyword_score,
            ats_score=ats_score,
            overall_score=overall_score,
            ai_suggestions=ai_analysis.get('suggestions', ''),
            resume_text=resume_text[:5000],  # Truncate for storage
            email=email
        )
        analysis.set_matched_keywords(matched_keywords)
        analysis.set_missing_keywords(missing_keywords)
        
        db.session.add(analysis)
        db.session.commit()
        
        # Generate charts
        chart_gen = ChartGenerator()
        chart_paths = chart_gen.generate_analysis_charts(analysis)
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'analysis_id': analysis.id,
            'redirect_url': url_for('main.results', analysis_id=analysis.id)
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@main.route('/results/<int:analysis_id>')
def results(analysis_id):
    """Display analysis results"""
    analysis = Analysis.query.get_or_404(analysis_id)
    
    # Generate fresh charts for this analysis
    chart_gen = ChartGenerator()
    chart_paths = chart_gen.generate_analysis_charts(analysis)
    
    return render_template('results.html', 
                         analysis=analysis, 
                         chart_paths=chart_paths)

@main.route('/dashboard')
def dashboard():
    """Historical dashboard of all analyses"""
    analyses = Analysis.query.order_by(Analysis.created_at.desc()).all()
    
    # Generate dashboard charts
    chart_gen = ChartGenerator()
    dashboard_charts = chart_gen.generate_dashboard_charts(analyses)
    
    # Calculate statistics
    stats = {
        'total_analyses': len(analyses),
        'avg_score': sum(a.overall_score for a in analyses) / len(analyses) if analyses else 0,
        'top_role': max(set(a.job_role for a in analyses), key=lambda x: sum(1 for a in analyses if a.job_role == x)) if analyses else 'N/A',
        'recent_trend': 'improving' if len(analyses) >= 2 and analyses[0].overall_score > analyses[1].overall_score else 'stable'
    }
    
    return render_template('dashboard.html', 
                         analyses=analyses, 
                         stats=stats,
                         dashboard_charts=dashboard_charts)

@main.route('/admin')
def admin():
    """Admin panel for managing job roles and keywords"""
    job_roles = JobRole.query.all()
    return render_template('admin.html', job_roles=job_roles)

@main.route('/admin/role', methods=['POST'])
def add_role():
    """Add or update job role"""
    try:
        name = request.form.get('name')
        keywords = request.form.get('keywords')
        description = request.form.get('description', '')
        
        if not name or not keywords:
            flash('Name and keywords are required', 'error')
            return redirect(url_for('main.admin'))
        
        # Parse keywords (comma-separated)
        keyword_list = [k.strip().lower() for k in keywords.split(',') if k.strip()]
        
        # Check if role exists
        role = JobRole.query.filter_by(name=name).first()
        if role:
            role.set_keywords(keyword_list)
            role.description = description
            flash(f'Updated role: {name}', 'success')
        else:
            role = JobRole(name=name, description=description)
            role.set_keywords(keyword_list)
            db.session.add(role)
            flash(f'Added new role: {name}', 'success')
        
        db.session.commit()
        
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('main.admin'))

@main.route('/admin/role/<int:role_id>/delete', methods=['POST'])
def delete_role(role_id):
    """Delete job role"""
    try:
        role = JobRole.query.get_or_404(role_id)
        db.session.delete(role)
        db.session.commit()
        flash(f'Deleted role: {role.name}', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('main.admin'))

@main.route('/download-report/<int:analysis_id>')
def download_report(analysis_id):
    """Generate and download PDF report"""
    analysis = Analysis.query.get_or_404(analysis_id)
    
    try:
        report_gen = ReportGenerator()
        pdf_path = report_gen.generate_pdf_report(analysis)
        
        return send_file(pdf_path, 
                        as_attachment=True, 
                        download_name=f'resume_analysis_{analysis.id}.pdf',
                        mimetype='application/pdf')
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'error')
        return redirect(url_for('main.results', analysis_id=analysis_id))

@main.route('/email-report/<int:analysis_id>', methods=['POST'])
def email_report(analysis_id):
    """Email PDF report to user"""
    analysis = Analysis.query.get_or_404(analysis_id)
    email = request.form.get('email') or analysis.email
    
    if not email:
        return jsonify({'error': 'Email address required'}), 400
    
    try:
        # Generate report
        report_gen = ReportGenerator()
        pdf_path = report_gen.generate_pdf_report(analysis)
        
        # Send email
        email_sender = EmailSender()
        email_sender.send_report(email, analysis, pdf_path)
        
        return jsonify({'success': True, 'message': 'Report sent successfully!'})
    except Exception as e:
        return jsonify({'error': f'Failed to send email: {str(e)}'}), 500

@main.route('/api/theme', methods=['POST'])
def toggle_theme():
    """Toggle dark/light theme"""
    theme = request.json.get('theme', 'light')
    session['theme'] = theme
    return jsonify({'success': True, 'theme': theme})

@main.route('/compare')
def compare():
    """Compare multiple analyses"""
    analyses = Analysis.query.order_by(Analysis.created_at.desc()).limit(10).all()
    
    if len(analyses) < 2:
        flash('Need at least 2 analyses to compare', 'info')
        return redirect(url_for('main.dashboard'))
    
    # Generate comparison charts
    chart_gen = ChartGenerator()
    comparison_charts = chart_gen.generate_comparison_charts(analyses)
    
    return render_template('compare.html', 
                         analyses=analyses,
                         comparison_charts=comparison_charts)
