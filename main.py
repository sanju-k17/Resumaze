from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

from app import create_app

if __name__ == '__main__':
    app = create_app()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("🚀 Starting AI Resume Analyzer...")
    print(f"📍 Running on http://localhost:{port}")
    print("📊 Features: AI Analysis, ATS Scoring, Keyword Matching, PDF Reports")
    
    app.run(host='0.0.0.0', port=port, debug=debug)