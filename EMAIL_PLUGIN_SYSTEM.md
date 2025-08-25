# Phishy AI Email Flagging Plugin System

🚩 **Comprehensive email security plugin system optimized for ngrok tunneling and easy deployment**

## Quick Start Guide

### 1. Prerequisites

**Required Software:**
- Python 3.8+ with pip
- ngrok account and CLI tool
- Chrome browser (for Gmail extension)

**Install Dependencies:**
```bash
pip install qrcode[pil] psutil requests fastapi uvicorn websockets
```

**Install ngrok:**
- Download from https://ngrok.com/download
- Sign up for free account at https://dashboard.ngrok.com
- Get your auth token from the dashboard

### 2. Quick Deployment

**Option A: Automated Deployment**
```bash
# Clone/navigate to Phishy directory
cd phishy

# Start with auto-configuration (recommended)
python start_with_plugins.py --auto-restart --auth-token YOUR_NGROK_TOKEN

# Or create quick start scripts
python start_with_plugins.py --create-scripts
```

**Option B: Manual Setup**
```bash
# Terminal 1: Start Phishy backend
python backend/app.py

# Terminal 2: Start ngrok tunnel
ngrok http 8080

# Terminal 3: Update configuration
python backend/ngrok_manager.py start --auth-token YOUR_TOKEN
```

### 3. Plugin Installation

**Gmail Chrome Extension:**
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select `plugins/gmail-chrome-extension/` folder
5. Configure with your ngrok URL

**Quick Configuration:**
1. Copy the ngrok URL from your terminal
2. Click the Phishy extension icon in Chrome
3. Paste URL and your email address
4. Click "Save Configuration"

## System Architecture

### Core Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Email Client  │───▶│  Ngrok Tunnel    │───▶│  Phishy Backend │
│   (Gmail, etc.) │    │  (Public HTTPS)  │    │  (FastAPI)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                        │                       │
        ▼                        ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Browser Plugin  │    │  Auto URL Sync   │    │  WebSocket Hub  │
│ (Chrome Ext)    │    │  (Dynamic Config)│    │  (Real-time)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Key Features

🔧 **Ngrok-Optimized:**
- Automatic tunnel URL detection and updates
- SSL certificate bypass for development
- WebSocket reconnection on tunnel restart
- Support for both free and paid ngrok accounts

🔒 **Security-First:**
- Real-time threat analysis with AI
- Minimal data collection and storage
- Encrypted communication channels
- User consent and privacy controls

📱 **Easy Setup:**
- QR code configuration for mobile
- One-click plugin installation
- Automatic server discovery
- Visual setup wizards

## API Endpoints

### Email Flagging Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/email-flagging/health` | GET | System health check |
| `/email-flagging/flag` | POST | Flag suspicious email |
| `/email-flagging/flags` | GET | Retrieve flagged emails |
| `/email-flagging/stats` | GET | Get flagging statistics |
| `/email-flagging/plugins/register` | POST | Register new plugin |
| `/email-flagging/plugins/setup/{id}` | GET | Get setup info + QR code |
| `/email-flagging/tunnel/status` | GET | Get tunnel status |
| `/email-flagging/tunnel/update` | POST | Update tunnel URL |
| `/email-flagging/ws/{client_id}` | WS | WebSocket connection |

### Example API Usage

**Flag an Email:**
```bash
curl -X POST "https://your-tunnel.ngrok.io/email-flagging/flag" \
  -H "Content-Type: application/json" \
  -d '{
    "email_id": "email123",
    "sender_email": "suspicious@example.com",
    "subject": "Urgent: Verify your account",
    "flag_category": "phishing",
    "confidence_level": 0.8,
    "user_email": "user@company.com",
    "client_info": {"plugin_type": "gmail"}
  }'
```

**Get Statistics:**
```bash
curl "https://your-tunnel.ngrok.io/email-flagging/stats"
```

**Test Health:**
```bash
curl "https://your-tunnel.ngrok.io/email-flagging/health"
```

## Email Client Plugins

### Gmail Chrome Extension

**Features:**
- 🚩 One-click email flagging
- 🤖 Real-time AI threat analysis  
- ⚠️ Visual suspicious email warnings
- 🔄 Auto-reconnect on server restart
- ⚙️ Easy configuration interface

**Installation:**
1. Load unpacked extension in Chrome
2. Configure ngrok URL in popup
3. Grant Gmail permissions
4. Start flagging suspicious emails

**Files:**
```
gmail-chrome-extension/
├── manifest.json       # Extension manifest
├── phishy-gmail.js     # Main content script
├── phishy-styles.css   # UI styling
├── popup.html          # Settings interface
├── popup.js           # Settings logic
├── background.js      # Service worker
└── README.md          # Documentation
```

### Outlook Plugin (Coming Soon)

**Planned Features:**
- Native Outlook add-in
- Office 365 integration
- Exchange server support
- Group policy deployment

### Thunderbird Extension (Coming Soon)

**Planned Features:**
- Cross-platform support
- IMAP/POP3 compatibility
- Local storage options
- Privacy-focused design

## Admin Dashboard

Access the admin dashboard at your ngrok URL to:

### Email Flagging Management
- View flagging statistics and trends
- Monitor connected plugins
- Export flagged email data
- Configure system settings

### Tunnel Monitoring
- Real-time tunnel status
- Connected plugin count
- URL update notifications
- Health monitoring

### Plugin Setup Wizard
- Generate QR codes for easy setup
- Step-by-step installation guides
- Test connectivity
- Troubleshooting tools

## Configuration

### Environment Variables

```bash
# .env file
BASE_URL=https://your-tunnel.ngrok.io
NGROK_AUTH_TOKEN=your_ngrok_token
DEBUG=true
```

### Plugin Configuration

**Gmail Extension Settings:**
```json
{
  "phishyApiUrl": "https://your-tunnel.ngrok.io",
  "phishyUserEmail": "user@company.com",
  "phishyEnabled": true,
  "phishyPluginId": "gmail_123456789"
}
```

### Ngrok Configuration

**Basic Setup:**
```yaml
# ngrok.yml
version: "2"
authtoken: your_token_here
tunnels:
  phishy:
    proto: http
    addr: 8080
    bind_tls: true
```

**Advanced Setup (Paid Account):**
```yaml
version: "2"
authtoken: your_token_here
tunnels:
  phishy:
    proto: http
    addr: 8080
    subdomain: mycompany-phishy
    bind_tls: true
    inspect: false
```

## Deployment Options

### Development Environment

```bash
# Quick development setup
python start_with_plugins.py --auto-restart

# Manual control
python backend/app.py &
ngrok http 8080 &
python backend/ngrok_manager.py start
```

### Production Environment

```bash
# With custom subdomain (paid ngrok)
python start_with_plugins.py \
  --subdomain mycompany-phishy \
  --auth-token $NGROK_TOKEN \
  --auto-restart

# With Docker (future enhancement)
docker-compose up -d
```

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Deploy Phishy with ngrok
  run: |
    pip install -r requirements.txt
    python start_with_plugins.py --auth-token ${{ secrets.NGROK_TOKEN }}
```

## Security Considerations

### Data Protection
- 🔒 All communication encrypted via HTTPS/WSS
- 🛡️ Minimal email content storage
- 🗑️ Automatic data expiration
- 👤 User consent for all data processing

### Network Security
- 🌐 ngrok provides secure tunneling
- 🔐 Optional authentication tokens
- 🚫 No open ports on local machine
- 📡 WebSocket origin validation

### Privacy Controls
- 📧 Email body analysis is optional
- 🔕 Users can disable specific features
- 📊 Anonymous usage analytics only
- 🗂️ Local data storage when possible

## Troubleshooting

### Common Issues

**Connection Failed:**
```bash
# Check ngrok status
curl http://127.0.0.1:4040/api/tunnels

# Test backend health
curl http://localhost:8080/health

# Verify tunnel accessibility
curl https://your-tunnel.ngrok.io/health
```

**Plugin Not Loading:**
```bash
# Check Chrome extension console
# Open DevTools > Console in Gmail
# Look for Phishy messages

# Verify permissions
# Check chrome://extensions/
```

**WebSocket Issues:**
```bash
# Test WebSocket connection
# Browser DevTools > Network > WS tab
# Look for successful WebSocket handshake
```

### Debug Mode

Enable verbose logging:
```bash
# Backend debug mode
DEBUG=true python backend/app.py

# Extension debug mode
# Open Chrome DevTools in Gmail
# Check Console and Network tabs
```

### Reset Configuration

```bash
# Clear all stored data
python -c "
import json
from pathlib import Path
for f in Path('data').glob('*.json'):
    f.unlink()
print('Configuration reset')
"
```

## Advanced Features

### Custom AI Models

Integrate your own threat detection models:
```python
# In email_flagging.py
async def analyze_email_with_ai(flag_request):
    # Your custom AI logic here
    return EmailAnalysisResult(...)
```

### Webhook Integration

Set up webhooks for external systems:
```python
# Send alerts to Slack, Teams, etc.
await send_webhook_alert(threat_data)
```

### Multi-Tenant Support

Configure for multiple organizations:
```python
# Organization-specific configuration
organization_configs = {
    "company1": {"api_key": "...", "settings": {...}},
    "company2": {"api_key": "...", "settings": {...}}
}
```

## Support and Community

### Getting Help

1. **Documentation**: Check this guide and plugin READMEs
2. **Logs**: Review backend logs and browser console
3. **Health Checks**: Use built-in diagnostic endpoints
4. **GitHub Issues**: Report bugs and request features

### Contributing

1. **Plugin Development**: Create plugins for new email clients
2. **AI Models**: Contribute threat detection algorithms
3. **Documentation**: Improve guides and tutorials
4. **Testing**: Help test across different environments

### License

This email flagging plugin system is part of the Phishy AI security platform. See the main project license for details.

---

## Quick Reference

### Essential Commands
```bash
# Start everything
python start_with_plugins.py --auto-restart

# Test API
curl https://your-tunnel.ngrok.io/email-flagging/health

# View logs
tail -f backend/logs/phishy_app.log

# Reset config
rm -rf data/*.json
```

### Important URLs
- **Admin Dashboard**: `https://your-tunnel.ngrok.io`
- **Plugin Setup**: `https://your-tunnel.ngrok.io/email-flagging/plugins/setup/gmail`
- **API Docs**: `https://your-tunnel.ngrok.io/docs`
- **Health Check**: `https://your-tunnel.ngrok.io/email-flagging/health`

**🛡️ Happy phishing simulation and security training!**