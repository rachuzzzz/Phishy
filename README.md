# 🎣 Phishy - AI-Powered Cybersecurity Training Platform

<div align="center">

**An advanced phishing simulation and security awareness training platform powered by AI**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-Educational-orange.svg)](#license)

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [API Documentation](#api-documentation) • [Architecture](#architecture)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Chrome Extension Setup](#chrome-extension-setup)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Security & Legal](#security--legal)
- [License](#license)

---

## 🎯 Overview

**Phishy** is a comprehensive cybersecurity training platform designed for organizations to conduct realistic phishing simulations and security awareness training. It combines advanced AI/ML technologies with user-friendly interfaces to help train employees to recognize and avoid phishing attacks.

### Key Capabilities

- **AI-Powered Email Generation**: Generate realistic phishing emails using Phi-3 Mini LLM
- **Real-Time Detection**: ML-based phishing detection with XGBoost classifier
- **Gmail Integration**: Chrome extension provides real-time warnings in Gmail
- **Comprehensive Analysis**: Multi-service email analysis (URLScan.io, AbuseIPDB, Google Safe Browsing)
- **Click Tracking & Analytics**: Monitor campaign effectiveness with detailed analytics
- **Forecasting**: Predict future attack patterns using time-series analysis

---

## ✨ Features

### 🤖 AI Email Generation
- **LLM Integration**: Uses Phi-3 Mini via Ollama for realistic email generation
- **6+ Predefined Scenarios**: Account security, payment requests, reward notifications, etc.
- **Custom Prompts**: Generate custom phishing scenarios
- **Fallback Templates**: Works without LLM using built-in templates

### 🛡️ ML-Based Detection
- **XGBoost Classifier**: Advanced machine learning model for phishing detection
- **Semantic Analysis**: Sentence embeddings (all-MiniLM-L6-v2)
- **Risk Scoring**: Confidence-based classification (LOW, MEDIUM, HIGH, CRITICAL)
- **Multi-Factor Analysis**: URL indicators, urgency patterns, suspicious language

### 📊 Analytics & Tracking
- **Click Tracking**: Monitor user interactions with phishing emails
- **Campaign Analytics**: View success rates, click patterns, and trends
- **Forecasting**: Prophet-based time-series prediction
- **Report Generation**: Export analytics as PDF reports

### 🔍 Comprehensive Email Analysis
- **ML Classification**: Instant phishing detection
- **URL Analysis**: URLScan.io integration for link safety
- **IP Intelligence**: AbuseIPDB reputation checking
- **File Analysis**: Attachment scanning
- **Header Analysis**: Email header inspection
- **Sender Reputation**: Sender scoring system

### 🌐 Chrome Extension
- **Gmail Integration**: Real-time phishing warnings in Gmail
- **Instant Analysis**: Automatic email scanning on open
- **Visual Alerts**: Color-coded warning banners
- **Configuration UI**: Easy setup through popup interface
- **Manifest V3**: Latest Chrome extension standard

### 📧 SMTP Integration
- **Auto-Detection**: Automatic SMTP server detection by domain
- **Multi-Provider**: Gmail, Outlook, Yahoo, AOL, ProtonMail, Zoho
- **App Password Support**: Secure authentication
- **HTML Emails**: Support for rich HTML content

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn 0.24.0 (ASGI)
- **ML/AI**:
  - scikit-learn 1.3.0+
  - XGBoost
  - sentence-transformers 2.2.0+
  - Phi-3 Mini (via Ollama)
- **Data Processing**: Pandas 2.1.4, NumPy 1.24.3
- **HTTP Client**: httpx 0.25.2
- **Validation**: Pydantic 2.5.0

### Frontend
- **Core**: HTML5, CSS3, Vanilla JavaScript
- **Visualization**: Chart.js 3.9.1
- **PDF Export**: jsPDF 2.5.1
- **Typography**: Google Fonts

### Chrome Extension
- **Standard**: Manifest V3
- **APIs**: Chrome Storage, Content Scripts, Service Workers

### External Services
- Ollama (Phi-3 Mini LLM)
- Google Safe Browsing API
- URLScan.io
- AbuseIPDB

---

## 📦 Installation

### Prerequisites
- **Python 3.8+**
- **Git** (optional)
- **Ollama** (optional, for AI features)
- **ngrok** (optional, for Chrome extension)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/phishy.git
cd phishy
```

### Step 2: Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Install Ollama (Optional)
For AI email generation:
1. Download from [https://ollama.ai](https://ollama.ai)
2. Install Phi-3 Mini:
   ```bash
   ollama pull phi3:mini
   ```

### Step 4: Install ngrok (Optional)
For Chrome extension to work:
1. Download from [https://ngrok.com/download](https://ngrok.com/download)
2. Extract and add to PATH

---

## 🚀 Quick Start

### Option 1: Unified Startup (Windows)
```cmd
start.bat
```
When prompted:
- Press **Y** for ngrok mode (required for Chrome extension)
- Press **N** for local-only mode

### Option 2: Manual Startup

#### Start Backend
```bash
cd backend
python app.py
```
Backend runs at: `http://localhost:8080`

#### Start Frontend
```bash
cd frontend
python -m http.server 3001
```
Frontend available at: `http://localhost:3001`

#### Start ngrok (for Chrome Extension)
```bash
ngrok http 8080
```
Copy the HTTPS URL (e.g., `https://abc123.ngrok-free.app`)

---

## ⚙️ Configuration

### Environment Variables
Create `.env` file in `backend/` directory:

```env
# Server Configuration
BACKEND_PORT=8080
FRONTEND_PORT=3001
HOST=0.0.0.0
DEBUG=True

# External API Keys (Optional)
GOOGLE_SAFE_BROWSING_API_KEY=your_key_here
URLSCAN_API_KEY=your_key_here
ABUSEIPDB_API_KEY=your_key_here
```

### Gmail SMTP Setup
For sending phishing simulation emails:

1. **Enable 2-Factor Authentication**
   - Google Account > Security > 2-Step Verification

2. **Generate App Password**
   - Google Account > Security > App passwords
   - Select "Mail" and generate
   - Save the 16-character password

3. **Use in Phishy**
   - Email: `your.email@gmail.com`
   - Password: Use the 16-character app password (NOT your regular password)

---

## 📖 Usage Guide

### Generate Phishing Emails

1. Open Phishy web interface: `http://localhost:3001`
2. Navigate to **AI Email Generator**
3. Enter target email address
4. Choose a scenario or enter custom prompt
5. Click **Generate Phishing Email**
6. Edit the generated content
7. Configure SMTP settings
8. Test connection and send

#### Example Prompts
```
"Create an urgent security alert about account suspension"
"Generate a fake IT support request for password reset"
"Make a convincing fake reward notification email"
"Create a fake shipping notification from Amazon"
```

### View Analytics

1. Navigate to **Analytics Dashboard**
2. View real-time statistics:
   - Total emails sent
   - Click-through rates
   - User vulnerability scores
   - Campaign effectiveness
3. Export reports as PDF

### Track Campaigns

- Monitor click logs in real-time
- View geographic distribution
- Analyze user agents
- Track time-based patterns

---

## 🔌 Chrome Extension Setup

### Installation

1. **Start Phishy with ngrok**
   ```cmd
   start.bat
   ```
   Press **Y** when prompted

2. **Get ngrok URL**
   - Look for `Forwarding https://xxxx.ngrok-free.app` in ngrok window
   - Copy the HTTPS URL

3. **Load Extension in Chrome**
   - Open `chrome://extensions/`
   - Enable **Developer mode** (top-right toggle)
   - Click **Load unpacked**
   - Select folder: `chrome-extension/`

4. **Configure Extension**
   - Click Phishy extension icon
   - Enter your Gmail address
   - Paste ngrok URL (HTTPS, no trailing slash)
   - Click **Save Settings**
   - Click **Test Connection**

5. **Test in Gmail**
   - Open [Gmail](https://mail.google.com)
   - Open any email
   - See Phishy analysis banner

### Extension Features

- **Instant Analysis**: ML classification on email open
- **Visual Warnings**: Color-coded risk banners
- **URL Scanning**: Automatic link safety checks
- **AI Explanations**: Explainable security analysis

---

## 📚 API Documentation

### System Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Platform information |
| GET | `/health` | Health check |
| GET | `/docs` | Swagger API documentation |
| GET | `/redoc` | ReDoc API documentation |

### Email Generation

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/llm/generate-email` | Generate phishing email with AI |
| POST | `/llm/chat` | General AI chat interface |
| GET | `/llm/scenarios` | List available phishing scenarios |

**Request Body** (`/llm/generate-email`):
```json
{
  "target_email": "user@example.com",
  "scenario": "account_security",
  "custom_prompt": "Optional custom instructions",
  "max_tokens": 500,
  "temperature": 0.7
}
```

### SMTP Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/smtp/send-email` | Send email via SMTP |
| POST | `/smtp/test-smtp` | Test SMTP connection |

**Request Body** (`/smtp/send-email`):
```json
{
  "username": "sender@gmail.com",
  "password": "app_password_here",
  "recipient": "target@example.com",
  "subject": "Email Subject",
  "body": "Email body",
  "html_body": "<html>HTML content</html>",
  "is_html": true
}
```

### Phishing Detection

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/detector/analyze` | ML-based phishing detection |
| POST | `/comprehensive/analyze` | Full multi-service analysis |

**Request Body** (`/detector/analyze`):
```json
{
  "email_content": "Email text to analyze",
  "sender": "sender@example.com",
  "subject": "Email subject",
  "urls": ["https://suspicious-link.com"]
}
```

### Analytics & Tracking

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/track/click` | Track email click |
| GET | `/track/stats` | Get click statistics |
| GET | `/analytics/analyze` | Detailed analytics |
| GET | `/forecast/predict` | Forecast future trends |

### Query Routing

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/smart/query` | Intelligent query routing |
| POST | `/ai/classifier/predict` | Intent classification |

**Request Body** (`/smart/query`):
```json
{
  "query": "Show me click statistics for last week"
}
```

---

## 📁 Project Structure

```
Phishy/
├── backend/                          # FastAPI Backend
│   ├── app.py                        # Main application entry point
│   ├── requirements.txt              # Python dependencies
│   ├── classifier.py                 # Intent classifier (ML)
│   ├── ngrok_manager.py              # ngrok integration
│   │
│   ├── routes/                       # API Route Modules
│   │   ├── llm_generator.py          # AI email generation (60KB)
│   │   ├── smtp_sender.py            # SMTP email sending (14KB)
│   │   ├── phishing_detector.py      # ML phishing detection (18KB)
│   │   ├── comprehensive_analysis.py # Multi-service analysis (43KB)
│   │   ├── click_tracker.py          # Click tracking (12KB)
│   │   ├── analytics.py              # Analytics dashboard (29KB)
│   │   ├── email_tracking.py         # Email status tracking (14KB)
│   │   ├── email_flagging.py         # Email flagging system (26KB)
│   │   ├── smart_query_handler.py    # Query routing (20KB)
│   │   ├── forecast.py               # Time-series forecasting (22KB)
│   │   ├── classifier_endpoint.py    # Classifier API (1KB)
│   │   ├── plugin_api.py             # Plugin system (11KB)
│   │   ├── file_analysis.py          # File attachment analysis (2KB)
│   │   ├── ip_intelligence.py        # IP reputation (4KB)
│   │   └── phishing.py               # Phishing simulation (11KB)
│   │
│   ├── data/                         # Data Storage
│   │   ├── click_logs.csv            # Click tracking logs
│   │   ├── intent_dataset.csv        # ML training data
│   │   └── intent_model/             # Trained models
│   │
│   ├── logs/                         # Application Logs
│   │   └── phishy_app.log
│   │
│   └── training/                     # Training Materials
│       └── phishing-awareness.html   # Auto-generated training page
│
├── frontend/                         # Web Interface
│   ├── index.html                    # Main UI (328KB, fully embedded)
│   ├── phishylogo.png                # Logo (1.4MB)
│   ├── phishytitlecard.png           # Title card (1.4MB)
│   ├── hook.png                      # Icon (7.5KB)
│   └── mail2.png                     # Icon (14.5KB)
│
├── chrome-extension/                 # Gmail Chrome Extension
│   ├── manifest.json                 # Extension manifest (V3)
│   ├── background.js                 # Background service worker (2KB)
│   ├── content.js                    # Gmail content script (81KB)
│   ├── popup.html                    # Settings UI (1.7KB)
│   ├── popup.js                      # Popup logic (5.7KB)
│   ├── popup.css                     # Popup styles (3.7KB)
│   └── styles.css                    # Content styles (17KB)
│
├── .env.example                      # Example environment config
├── .gitignore                        # Git ignore rules
├── start.bat                         # Unified startup script (Windows)
└── README.md                         # This file

Total: 15 Active Route Modules | 79 API Endpoints | 500KB+ Backend Code
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      PHISHY PLATFORM                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  PRESENTATION LAYER                                     │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  • Web Dashboard (Port 3001)                           │   │
│  │  • Chrome Extension (Gmail Integration)                │   │
│  │  • Analytics & Reporting Interface                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↕ HTTP/HTTPS                         │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  NGROK TUNNEL (Optional)                                │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  • ngrok http 8080 → HTTPS URL                         │   │
│  │  • Required for Chrome Extension                       │   │
│  │  • Dashboard: http://127.0.0.1:4040                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↕ Tunnel                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  APPLICATION LAYER (FastAPI - Port 8080)               │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  Route Modules:                                         │   │
│  │  ├─ AI Generation (llm_generator.py)                   │   │
│  │  ├─ SMTP Sending (smtp_sender.py)                      │   │
│  │  ├─ ML Detection (phishing_detector.py)                │   │
│  │  ├─ Analysis (comprehensive_analysis.py)               │   │
│  │  ├─ Tracking (click_tracker.py)                        │   │
│  │  ├─ Analytics (analytics.py)                           │   │
│  │  ├─ Forecasting (forecast.py)                          │   │
│  │  ├─ Query Routing (smart_query_handler.py)             │   │
│  │  └─ ... (15 modules total)                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↕                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  AI/ML LAYER                                            │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  • Ollama (Phi-3 Mini LLM)                             │   │
│  │  • XGBoost Classifier                                   │   │
│  │  • Sentence Transformers (Embeddings)                   │   │
│  │  • Prophet (Time-Series Forecasting)                    │   │
│  │  • Intent Classifier (Logistic Regression)              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↕                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  DATA LAYER                                             │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  • CSV Logs (click_logs.csv)                           │   │
│  │  • Training Data (intent_dataset.csv)                   │   │
│  │  • ML Models (XGBoost, embeddings)                      │   │
│  │  • Application Logs (phishy_app.log)                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            ↕ API Calls                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  EXTERNAL SERVICES                                      │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │  • Google Safe Browsing API                            │   │
│  │  • URLScan.io                                          │   │
│  │  • AbuseIPDB                                           │   │
│  │  • SMTP Providers (Gmail, Outlook, Yahoo, etc.)        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Email Generation**: User request → LLM/Template → Generated email
2. **Email Sending**: Generated email → SMTP → Target recipient
3. **Click Tracking**: Recipient clicks link → Tracker → CSV log → Analytics
4. **Detection**: Email content → ML classifier → Risk score → User alert
5. **Analysis**: Email → Multi-service APIs → Comprehensive report

---

## 🔧 Troubleshooting

### Backend Won't Start

**Check Python Version**
```bash
python --version  # Should be 3.8+
```

**Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

**Check Port Conflicts**
```bash
# Windows
netstat -an | findstr :8080

# Linux/Mac
lsof -i :8080
```

### Email Sending Fails

- ✓ Verify using Gmail **App Password** (not regular password)
- ✓ Ensure 2-factor authentication is enabled
- ✓ Test SMTP: `POST http://localhost:8080/smtp/test-smtp`
- ✓ Check logs: `backend/logs/phishy_app.log`

### Frontend Not Loading

- ✓ Serve with Python: `python -m http.server 3001`
- ✓ Check browser console (F12)
- ✓ Verify backend running at `http://localhost:8080`
- ✓ Check CORS configuration in `backend/app.py`

### AI Features Not Working

- ✓ Install Ollama from [https://ollama.ai](https://ollama.ai)
- ✓ Pull model: `ollama pull phi3:mini`
- ✓ Check LLM health: `http://localhost:8080/llm/health`
- ✓ System works with fallback templates if Ollama unavailable

### Chrome Extension Issues

**"Configuration Needed"**
- Click extension icon
- Enter email and ngrok URL
- Save settings and reload Gmail

**"Cannot connect to backend"**
- Verify backend running
- Check ngrok is active
- Ensure URL is HTTPS with no trailing slash
- Test URL: `https://your-ngrok-url/health`

**Extension Not Scanning Emails**
- Reload Gmail tab (Ctrl+R)
- Check extension enabled in `chrome://extensions/`
- View console: Right-click extension → Inspect popup
- Check content script loaded: F12 in Gmail

**ngrok URL Keeps Changing**
- Free ngrok accounts get new URLs on restart
- Update extension settings with new URL each time
- Consider ngrok paid plan for static URL

### Viewing Logs

**Backend Logs**
```bash
tail -f backend/logs/phishy_app.log
```

**Extension Logs**
- Open Gmail
- Press F12 → Console tab
- Look for "Phishy" messages

**ngrok Dashboard**
- Access: `http://127.0.0.1:4040`
- View all HTTP requests/responses

---

## 🔒 Security & Legal

### ⚠️ Important Warnings

This tool is designed **EXCLUSIVELY** for cybersecurity training and awareness purposes.

### Legal Requirements

- ✓ Obtain **written authorization** before conducting simulations
- ✓ Use only in **authorized training environments**
- ✓ Follow **organizational policies** and **applicable laws**
- ✓ Comply with **anti-phishing regulations** in your jurisdiction
- ✓ Inform participants about **training nature** of simulations

### Ethical Guidelines

- All generated emails should include educational disclaimers
- Tracking URLs must redirect to training materials
- Never use for malicious purposes
- Respect privacy and data protection laws
- Obtain informed consent from participants

### Data Protection

- Click logs contain IP addresses and user agents
- Store data securely and comply with GDPR/CCPA
- Implement data retention policies
- Provide opt-out mechanisms
- Anonymize data where possible

---

## 📜 License

This project is for **educational and training purposes only**.

**Terms of Use:**
- Non-commercial use only
- Must obtain authorization before deployment
- No warranty provided
- Use at your own risk
- Must comply with local laws and regulations

**Disclaimer:**
The authors are not responsible for misuse of this software. Users are solely responsible for ensuring compliance with all applicable laws, regulations, and organizational policies.

---

## 📞 Support & Documentation

### Resources

- **API Documentation**: `http://localhost:8080/docs` (Swagger)
- **Alternative API Docs**: `http://localhost:8080/redoc`
- **Health Check**: `http://localhost:8080/health`
- **Training Page**: `http://localhost:8080/training/phishing-awareness.html`

### Testing

Test all components:
```bash
# Check backend health
curl http://localhost:8080/health

# Test LLM integration
curl http://localhost:8080/llm/scenarios

# View analytics
curl http://localhost:8080/track/stats
```

---

<div align="center">

**Made with ❤️ for Cybersecurity Education**

⚠️ Use Responsibly | 🎓 Train Ethically | 🛡️ Secure Properly

</div>
