# 🧠 AI Resume Analyzer

A comprehensive, AI-powered resume analysis web application built entirely with Python. This application provides intelligent resume analysis, ATS compatibility scoring, keyword optimization, and detailed PDF reports.

![AI Resume Analyzer](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Features

### ✨ Core Features
1. **📄 Resume Upload & Analysis** - Support for PDF and DOCX files
2. **🎯 Job Role Targeting** - Analyze resumes against specific job roles
3. **🔍 Keyword Matching** - Intelligent keyword detection and scoring
4. **🤖 AI-Powered Suggestions** - GPT-powered improvement recommendations
5. **📊 ATS Compatibility** - Applicant Tracking System readiness score
6. **📈 Interactive Visualizations** - Beautiful charts and graphs
7. **📋 PDF Report Generation** - Comprehensive downloadable reports
8. **📧 Email Integration** - Send reports directly to users
9. **📱 Mobile-Friendly Design** - Responsive UI for all devices
10. **🌙 Dark/Light Mode** - Theme switching capability

### 🔧 Advanced Features
11. **📊 Historical Dashboard** - Track analysis history and trends
12. **⚙️ Admin Panel** - Manage job roles and keywords
13. **🔄 Comparison Tool** - Compare multiple resume analyses
14. **🎨 Interactive Charts** - Plotly-powered visualizations
15. **🗄️ Data Persistence** - SQLite database for storing analyses



## 🛠️ Installation Guide for Windows 11

### Prerequisites
- Python 3.11 or higher
- Git (optional)
- OpenAI API key

### Step 1: Install Python
1. Download Python from [python.org](https://www.python.org/downloads/)
2. **Important**: Check "Add Python to PATH" during installation
3. Verify installation:
   \`\`\`cmd
   python --version
   pip --version
   \`\`\`

### Step 2: Create Project Directory
\`\`\`cmd
# Open Command Prompt as Administrator
cd C:\
mkdir ai-resume-analyzer
cd ai-resume-analyzer
\`\`\`

### Step 3: Set Up Virtual Environment
\`\`\`cmd
python -m venv venv
venv\Scripts\activate
\`\`\`

### Step 4: Create Project Files
Create all the files shown in the code project above, maintaining the directory structure.

### Step 5: Configure Environment Variables
Create a `.env` file in the root directory:
\`\`\`env
SECRET_KEY=your-super-secret-key-change-this-in-production
OPENAI_API_KEY=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
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
DATABASE_URL=sqlite:///resume_analyzer.db
FLASK_ENV=development
\`\`\`

### Step 6: Install Dependencies
\`\`\`cmd
pip install -r requirements.txt
\`\`\`

### Step 7: Run the Application
\`\`\`cmd
python main.py
\`\`\`

### Step 8: Access the Application
Open your browser and go to: `http://localhost:5000`

## 🔑 Configuration

### OpenAI API Key Setup
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Create an account and get your API key
3. Add it to your `.env` file as shown above

### Email Configuration (Optional)
For Gmail:
1. Enable 2-Factor Authentication
2. Generate an App Password:
   - Google Account → Security → 2-Step Verification → App passwords
3. Use the 16-character app password in your `.env` file

## 🧪 Testing

Run the test suite:
\`\`\`cmd
pytest tests/ -v
\`\`\`

## 🐳 Docker Deployment

Build and run with Docker:
\`\`\`cmd
docker build -t ai-resume-analyzer .
docker run -p 5000:5000 --env-file .env ai-resume-analyzer
\`\`\`

## 📊 Usage

1. **Upload Resume**: Drag and drop or click to upload PDF/DOCX files
2. **Select Job Role**: Choose from predefined roles or add custom ones
3. **Add Job Description**: Optional for more accurate analysis
4. **Get Results**: View comprehensive analysis with scores and suggestions
5. **Download Report**: Get detailed PDF report
6. **Email Report**: Send results directly to your email

## 🎯 API Endpoints

- `GET /` - Home page with upload form
- `POST /upload` - Handle resume upload and analysis
- `GET /results/<id>` - Display analysis results
- `GET /dashboard` - Historical dashboard
- `GET /admin` - Admin panel for managing job roles
- `GET /download-report/<id>` - Download PDF report
- `POST /email-report/<id>` - Email report to user

## 🔧 Troubleshooting

### Common Issues

**1. Python not found**
\`\`\`cmd
# Add Python to PATH manually
set PATH=%PATH%;C:\Users\YourUsername\AppData\Local\Programs\Python\Python311
\`\`\`

**2. OpenAI API errors**
- Verify your API key is correct
- Check your OpenAI account has credits
- The app will use fallback analysis if OpenAI fails

**3. File upload issues**
- Ensure the `uploads` folder exists and has write permissions
- Check Windows Defender isn't blocking file operations

**4. Email not working**
- Configure SMTP settings in `.env`
- Use app passwords for Gmail (not regular password)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for GPT API integration
- **Flask** for the web framework
- **Plotly** for interactive visualizations
- **PyMuPDF** for PDF processing
- **ReportLab** for PDF report generation
- **Tailwind CSS** for modern styling

## 📞 Support

- 📧 Email: support@resumeanalyzer.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/ai-resume-analyzer/issues)
- 📖 Documentation: [Wiki](https://github.com/yourusername/ai-resume-analyzer/wiki)

---

**Made with ❤️ and Python** | **Star ⭐ this repo if you found it helpful!**
