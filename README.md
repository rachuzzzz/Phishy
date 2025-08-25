# 🎣 Phishy AI - Advanced Cybersecurity Training Platform

A comprehensive AI-powered phishing simulation and security awareness training platform.

## ✨ Features

- **🤖 AI Email Generation**: Create realistic phishing emails using Phi-3 Mini
- **📝 Email Editor**: Edit generated emails before sending
- **📧 SMTP Integration**: Send emails via Gmail SMTP
- **📊 Analytics Dashboard**: Track clicks and user behavior
- **🎯 Click Tracking**: Monitor phishing simulation engagement
- **🛡️ Security Training**: Redirect users to awareness content

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Gmail account with App Password enabled

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Backend
```bash
# Option 1: Use the startup script (Windows)
start_phishy.bat

# Option 2: Manual start
cd backend
python app.py
```

The backend will be available at: http://localhost:8080

### 3. Open the Frontend
```bash
# Option 1: Open directly in browser
Open `frontend/index.html` in your browser

# Option 2: Serve with Python (recommended)
cd frontend
python -m http.server 3001
# Then visit: http://localhost:3001
```

### 4. Test the System
```bash
python test_email_system.py
```

## 📧 Email Setup Guide

### Setting up Gmail for SMTP

1. **Enable 2-Factor Authentication**
   - Go to your Google Account settings
   - Security > 2-Step Verification > Turn on

2. **Generate App Password**
   - Google Account > Security > App passwords
   - Generate password for "Mail"
   - Save the 16-character password (this is NOT your regular Gmail password)

3. **Use in Phishy**
   - Gmail Address: your.email@gmail.com
   - App Password: the 16-character password from step 2

## 🎯 How to Use

### Generate Phishing Emails
1. Navigate to "AI Email Generator" in the sidebar
2. Enter target email address
3. Describe the type of phishing email you want
4. Click "Generate Phishing Email"
5. **Edit the generated content** in the text editor
6. Configure SMTP settings
7. Test connection and send

### Example Prompts
- "Create a urgent security alert about account suspension"
- "Generate a fake IT support request for password reset"
- "Make a convincing fake reward notification email"
- "Create a fake COVID-19 vaccination appointment email"

### Analytics Dashboard
- View click statistics
- Monitor user behavior
- Track training effectiveness
- Generate reports

## 🔧 API Endpoints

### Core Endpoints
- `GET /health` - System health check
- `GET /docs` - API documentation

### Email Generation
- `POST /llm/generate-email` - Generate phishing email
- `POST /llm/chat` - General AI chat
- `GET /llm/scenarios` - Available scenarios

### SMTP
- `POST /smtp/test-smtp` - Test SMTP connection
- `POST /smtp/send-email` - Send email

### Tracking
- `GET /track/click` - Track email clicks
- `GET /track/stats` - Click statistics
- `GET /track/logs` - Detailed logs

## 🛠️ Configuration

### Environment Variables
Create a `.env` file in the backend directory:
```env
BACKEND_PORT=8080
FRONTEND_PORT=3001
DEBUG=True
```

### LLM Integration (Optional)
For advanced AI features, install Ollama:
1. Download Ollama from https://ollama.ai
2. Install Phi-3 Mini: `ollama pull phi3:mini`
3. The system will automatically use it if available

## 📊 Project Structure

```
Phishy/
├── backend/                 # FastAPI backend
│   ├── app.py              # Main application
│   ├── routes/             # API route modules
│   │   ├── llm_generator.py
│   │   ├── smtp_sender.py
│   │   ├── click_tracker.py
│   │   └── analytics.py
│   ├── data/               # Data storage
│   ├── logs/               # Application logs
│   └── requirements.txt
├── frontend/               # Web interface
│   └── index.html         # Main interface
├── test_email_system.py   # Test suite
├── start_phishy.bat      # Windows startup script
└── README.md
```

## 🔒 Security Notes

⚠️ **IMPORTANT**: This tool is designed for cybersecurity training and awareness purposes only.

- All generated emails include educational disclaimers
- Tracking URLs redirect to training materials
- Use only in authorized training environments
- Obtain proper approvals before conducting simulations
- Follow your organization's policies and applicable laws

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Install dependencies
cd backend
pip install -r requirements.txt

# Check for port conflicts
netstat -an | findstr :8080
```

### Email sending fails
- Verify Gmail App Password (not regular password)
- Ensure 2-factor authentication is enabled
- Check SMTP test endpoint: `/smtp/test-smtp`
- Review backend logs in `backend/logs/`

### Frontend not loading
- Try serving with Python: `python -m http.server 3001`
- Check browser console for errors
- Verify backend is running at http://localhost:8080

### AI features not working
- Install Ollama: https://ollama.ai
- Pull model: `ollama pull phi3:mini`
- Check LLM health: http://localhost:8080/llm/health
- System works with fallback templates if Ollama unavailable

## 📚 Documentation

- **API Docs**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health
- **Training Page**: http://localhost:8080/training/phishing-awareness.html

## 🤝 Support

Run the test suite to diagnose issues:
```bash
python test_email_system.py
```

This will test all major components and provide specific guidance on any problems found.

## 📜 License

This project is for educational and training purposes only. Use responsibly and in accordance with applicable laws and organizational policies.