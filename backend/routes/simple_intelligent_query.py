"""
Simple Intelligent Query Router for Phishy Platform

This is a simplified version that avoids problematic imports
and focuses on core intent classification functionality.
"""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import asyncio
import httpx

# Import our intent classifier (this should work)
from classifier import predict_intent, get_classifier

router = APIRouter()
logger = logging.getLogger(__name__)

class SimpleIntelligentQueryRequest(BaseModel):
    query: str = Field(..., description="User query to route intelligently")
    temperature: Optional[float] = Field(0.7, ge=0.1, le=1.0, description="LLM temperature")
    max_tokens: Optional[int] = Field(500, ge=50, le=1000, description="Max tokens")

class SimpleIntelligentQueryResponse(BaseModel):
    query: str
    predicted_intent: str  # "CHAT" or "REPORT"
    response: str
    response_type: str
    generation_time_ms: int
    timestamp: str

@router.post("/intelligent-query", response_model=SimpleIntelligentQueryResponse)
async def simple_intelligent_query(request: SimpleIntelligentQueryRequest):
    """
    Simple intelligent query routing using intent classification.
    Routes to existing endpoints based on predicted intent.
    """
    start_time = datetime.utcnow()
    logger.info(f"Processing query: {request.query}")
    
    try:
        # Step 1: Predict intent
        predicted_intent = predict_intent(request.query)
        logger.info(f"Predicted intent: {predicted_intent}")
        
        # Step 2: Route based on intent
        if predicted_intent == "CHAT":
            response_data = await _handle_chat_simple(request)
            response_type = "llm_chat"
        else:  # REPORT
            response_data = await _handle_report_simple(request)
            response_type = "structured_report"
        
        generation_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        
        return SimpleIntelligentQueryResponse(
            query=request.query,
            predicted_intent=predicted_intent,
            response=response_data,
            response_type=response_type,
            generation_time_ms=generation_time,
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in simple intelligent query: {e}")
        generation_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        
        return SimpleIntelligentQueryResponse(
            query=request.query,
            predicted_intent="CHAT",
            response=f"I'm here to help with cybersecurity questions. I encountered an issue: {str(e)}",
            response_type="error_fallback",
            generation_time_ms=generation_time,
            timestamp=datetime.utcnow().isoformat()
        )

async def _handle_chat_simple(request: SimpleIntelligentQueryRequest) -> str:
    """Handle CHAT intent by calling existing LLM endpoint"""
    try:
        # Call the existing /llm/chat endpoint
        async with httpx.AsyncClient(timeout=30.0) as client:
            chat_payload = {
                "message": request.query,
                "temperature": request.temperature,
                "max_tokens": request.max_tokens
            }
            
            response = await client.post(
                "http://localhost:8080/llm/chat",
                json=chat_payload
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "I'm here to help with cybersecurity!")
            else:
                logger.error(f"LLM endpoint error: {response.status_code}")
                return _fallback_chat_response(request.query)
                
    except Exception as e:
        logger.error(f"Error calling LLM endpoint: {e}")
        return _fallback_chat_response(request.query)

async def _handle_report_simple(request: SimpleIntelligentQueryRequest) -> str:
    """Handle REPORT intent by calling existing analytics endpoints"""
    try:
        query_lower = request.query.lower()
        
        # Determine what kind of report to generate
        if any(kw in query_lower for kw in ['click', 'user', 'activity']):
            return await _get_click_report()
        else:
            return await _get_general_report(request.query)
            
    except Exception as e:
        logger.error(f"Error handling report: {e}")
        return f"📊 **Report Generation Error**\n\nUnable to generate report: {str(e)}"

async def _get_click_report() -> str:
    """Get click tracking report from existing endpoint"""
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get("http://localhost:8080/track/stats")
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get("stats", {})
                
                return f"""📊 **Click Tracking Report**

**Current Metrics:**
• Total Click Events: {stats.get('total_clicks', 0)}
• Unique Users: {stats.get('unique_users', 0)}
• Recent Activity (24h): {stats.get('recent_activity', {}).get('last_24h', 0)}
• Recent Activity (7d): {stats.get('recent_activity', {}).get('last_7d', 0)}

**Top Users:**
{_format_top_users(stats.get('top_users', {}))}

💡 **Generated using intelligent query routing**"""
            else:
                return "📊 **Click Report**: Unable to retrieve click statistics."
                
    except Exception as e:
        return f"📊 **Click Report Error**: {str(e)}"

def _format_top_users(top_users: dict) -> str:
    """Format top users for display"""
    if not top_users:
        return "• No user activity data available"
    
    lines = []
    for email, clicks in list(top_users.items())[:5]:
        username = email.split('@')[0] if '@' in email else email
        lines.append(f"• {username}: {clicks} clicks")
    
    return '\n'.join(lines)

async def _get_general_report(query: str) -> str:
    """Generate a general report"""
    try:
        # Try to get some basic stats
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8080/track/stats")
            
            if response.status_code == 200:
                data = response.json()
                stats = data.get("stats", {})
                
                return f"""📈 **Security Analytics Report**

**System Status:** Operational
**Total Security Events:** {stats.get('total_clicks', 0)}
**Monitored Users:** {stats.get('unique_users', 0)}
**Recent Activity:** {stats.get('recent_activity', {}).get('last_24h', 0)} events (24h)

**Assessment:** {'Active monitoring detected' if stats.get('total_clicks', 0) > 0 else 'No recent activity'}

💡 **Report generated using AI-powered query routing**"""
            else:
                return "📈 **Security Report**: System operational, detailed metrics unavailable."
                
    except Exception as e:
        return f"📈 **Security Report**: Unable to generate detailed report: {str(e)}"

def _fallback_chat_response(query: str) -> str:
    """Fallback response for chat queries when LLM is unavailable"""
    query_lower = query.lower()
    
    if any(greeting in query_lower for greeting in ['hello', 'hi', 'hey', 'good morning']):
        return """Hello! I'm Phishy, your cybersecurity assistant. I'm here to help with:

• **Phishing education** - Learn about phishing attacks and prevention
• **Security awareness** - Best practices for staying safe online  
• **Threat analysis** - Understanding cybersecurity risks
• **Analytics & reporting** - Security metrics and user behavior insights

How can I assist you with cybersecurity today?"""
    
    elif any(word in query_lower for word in ['phishing', 'phish']):
        return """**What is Phishing?**

Phishing is a cybercrime where attackers impersonate legitimate organizations to trick people into revealing sensitive information like passwords, credit card numbers, or personal data.

**Common Signs of Phishing:**
• Urgent or threatening language
• Requests for sensitive information
• Suspicious sender addresses
• Generic greetings ("Dear Customer")
• Poor grammar/spelling
• Suspicious links or attachments

**Protection Tips:**
• Verify sender identity independently
• Don't click suspicious links
• Use multi-factor authentication
• Keep software updated
• Report suspicious emails

Stay vigilant and when in doubt, don't click!"""
    
    else:
        return """I'm here to help with cybersecurity questions and security analysis. Some topics I can assist with:

• **Phishing awareness** and prevention
• **Cybersecurity best practices**
• **Security metrics** and analytics
• **Threat assessment** and risk analysis

Feel free to ask me about any cybersecurity topic, or request security reports and analytics!"""

# Utility endpoints
@router.get("/classifier/info")
async def get_classifier_info():
    """Get classifier information"""
    try:
        classifier = get_classifier()
        return {
            "status": "operational",
            "model_info": classifier.get_model_info(),
            "available_intents": ["CHAT", "REPORT"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classifier error: {str(e)}")

@router.post("/classifier/predict")
async def predict_intent_endpoint(query: str):
    """Test intent prediction"""
    try:
        intent = predict_intent(query)
        return {
            "query": query,
            "predicted_intent": intent,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")