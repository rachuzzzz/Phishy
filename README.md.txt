# Phishy - Advanced Cybersecurity Training Platform

A comprehensive phishing simulation and training platform powered by AI/LLM technology for security awareness training.

## Features

- 🎯 **AI-Generated Phishing Emails**: Uses Mistral 7B via Ollama for realistic phishing simulations
- 📊 **Advanced Analytics**: Dual-engine analytics with Pandas and Polars for performance comparison
- 🤖 **Admin Assistant**: LangChain-powered assistant for security insights and recommendations
- 📈 **Forecasting**: Prophet-based click trend forecasting and risk assessment
- 🔍 **Historical Queries**: LlamaIndex-powered natural language queries over historical data
- 📝 **Click Tracking**: Comprehensive click logging and user behavior analysis

## Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Ollama** (for AI features)

### Installation

1. **Clone and setup**:
```bash
git clone <repository>
cd phishy-platform
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Setup Ollama** (for AI features):
```bash
# Install Ollama from https://ollama.ai/
ollama serve
ollama pull mistral:7b
```

4. **Run startup diagnostics**:
```bash
python startup.py
```

5. **Start the server**:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Core Endpoints
- `GET /` - Platform information
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation

### Phishing Simulation
- `POST /llm/generate-email` - Generate AI-powered phishing emails
- `POST /phishing/generate` - Generate basic phishing emails
- `GET /track/click` - Track user clicks (redirects to training)

### Analytics
- `POST /analytics/analyze` - Advanced analytics with Pandas/Polars
- `GET /analytics/user-profile/{email}` - Individual user analysis
- `GET /analytics/risk-assessment` - Comprehensive risk assessment
- `GET /analytics/trends` - Time-based trend analysis

### Admin Assistant
- `POST /admin/query` - Natural language queries to admin assistant
- `POST /admin/generate-report` - Generate security reports
- `GET /admin/conversation-history` - View conversation history

### Forecasting
- `POST /forecast/generate` - Generate click trend forecasts
- `GET /forecast/visualization` - Get forecast visualization data
- `POST /forecast/retrain` - Retrain forecasting model

### Historical Queries
- `POST /query/historical` - Natural language queries over historical data
- `POST /query/rebuild-index` - Rebuild vector index
- `GET /query/sample-questions` - Get sample questions

## Configuration

### Environment Variables
Create a `.env` file:
```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b

# Application Settings
DEBUG=true
LOG_LEVEL=INFO
```

### Data Directory
The platform automatically creates a `data/` directory containing:
- `click_logs.csv` - Click tracking data
- `click_logs.txt` - Text-based logs

### Training Materials
Training materials are served from `training/` directory:
- `phishing-awareness.html` - Default training page

## Architecture

### Core Components

1. **FastAPI Application** (`app.py`)
   - Main application with module loading
   - CORS configuration
   - Static file serving
   - Global exception handling

2. **Route Modules**:
   - `click_tracker.py` - Click tracking and logging
   - `llm_generator.py` - AI-powered email generation
   - `phishing.py` - Basic phishing email templates
   - `analytics.py` - Advanced analytics engine
   - `admin_assistant.py` - LangChain admin assistant
   - `historical_query.py` - LlamaIndex historical queries
   - `forecast.py` - Prophet forecasting engine

3. **Data Processing**:
   - CSV-based data storage
   - Pandas/Polars dual-engine analytics
   - Vector indexing for semantic search

4. **AI Integration**:
   - Ollama for local LLM inference
   - LangChain for conversational AI
   - LlamaIndex for document queries
   - Prophet for time series forecasting

## Usage Examples

### Generate Phishing Email
```bash
curl -X POST "http://localhost:8000/llm/generate-email" \
  -H "Content-Type: application/json" \
  -d '{"user_email": "user@company.com", "scenario_type": "account_security"}'
```

### Query Analytics
```bash
curl -X POST "http://localhost:8000/analytics/analyze" \
  -H "Content-Type: application/json" \
  -d '{"engine": "polars", "time_range": "7d", "group_by": "day"}'
```

### Ask Admin Assistant
```bash
curl -X POST "http://localhost:8000/admin/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "Which users have the highest risk scores?"}'
```

### Generate Forecast
```bash
curl -X POST "http://localhost:8000/forecast/generate" \
  -H "Content-Type: application/json" \
  -d '{"forecast_days": 30, "confidence_interval": 0.8}'
```

## Development

### Running with Debug Mode
```bash
uvicorn app:app --reload --log-level debug
```

### Testing Components
```bash
# Test Ollama connection
curl http://localhost:11434/api/tags

# Test platform health
curl http://localhost:8000/health

# Test LLM health
curl http://localhost:8000/llm/health
```

### Adding New Features
1. Create new route module in `routes/`
2. Add import in `app.py`
3. Update documentation

## Troubleshooting

### Common Issues

1. **Ollama Connection Failed**:
   ```bash
   # Start Ollama service
   ollama serve
   
   # Verify model is available
   ollama list
   ```

2. **Import Errors**:
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

3. **Data Directory Issues**:
   ```bash
   # Create data directory
   mkdir -p data
   
   # Check permissions
   chmod 755 data
   ```

4. **Module Loading Failures**:
   - Check `app.py` logs for specific import errors
   - Verify all dependencies are installed
   - Run `python startup.py` for diagnostics

### Performance Optimization

1. **Analytics Performance**:
   - Use Polars engine for large datasets
   - Apply time filters to reduce data size
   - Cache frequently accessed data

2. **LLM Performance**:
   - Use smaller models for faster inference
   - Implement request queuing for high loads
   - Cache common responses

## Security Considerations

⚠️ **Important**: This platform is designed for internal security training only.

- All generated emails are for training purposes
- Click tracking is logged for analysis
- User data should be handled according to privacy policies
- Deploy behind proper authentication in production

## License

This project is for educational and internal security training purposes only.

## Support

For issues and questions:
1. Check the logs in `phishy_app.log`
2. Run diagnostics with `python startup.py`
3. Verify Ollama service is running
4. Check API documentation at `/docs`