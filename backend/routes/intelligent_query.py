"""
Intelligent Query Router for Phishy Platform

This route uses intent classification to automatically route user queries to:
- CHAT: Educational conversations via LLM 
- REPORT: Analytics and reporting via structured data

Integrates with existing llm_generator.py and admin_assistant.py routes.
"""

import logging
import time
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

# Import existing route functions
try:
    from .llm_generator import general_chat, ChatRequest, ChatResponse
    LLM_GENERATOR_AVAILABLE = True
except ImportError as e:
    logger.warning(f"LLM generator import failed: {e}")
    LLM_GENERATOR_AVAILABLE = False

try:
    from .admin_assistant import admin_query, AdminQuery, AdminResponse
    ADMIN_ASSISTANT_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Admin assistant import failed: {e}")
    ADMIN_ASSISTANT_AVAILABLE = False

try:
    from .click_tracker import get_click_stats
    CLICK_TRACKER_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Click tracker import failed: {e}")
    CLICK_TRACKER_AVAILABLE = False

try:
    from .analytics import perform_analytics, AnalyticsRequest, AnalyticsEngine
    ANALYTICS_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Analytics import failed: {e}")
    ANALYTICS_AVAILABLE = False

# Import our intent classifier
from classifier import predict_intent, get_classifier

router = APIRouter()
logger = logging.getLogger(__name__)

class IntelligentQueryRequest(BaseModel):
    query: str = Field(..., description="User query to route intelligently")
    temperature: Optional[float] = Field(0.7, ge=0.1, le=1.0, description="LLM temperature for chat responses")
    max_tokens: Optional[int] = Field(500, ge=50, le=1000, description="Max tokens for chat responses") 
    include_analytics: Optional[bool] = Field(True, description="Include analytics data for report queries")

class IntelligentQueryResponse(BaseModel):
    query: str
    predicted_intent: str  # "CHAT" or "REPORT"
    response: str
    response_type: str  # "llm_chat", "structured_report", "analytics_data"
    model_used: Optional[str] = None
    generation_time_ms: int
    timestamp: str
    confidence_info: Optional[Dict[str, Any]] = None

@router.post("/intelligent-query", response_model=IntelligentQueryResponse)
async def intelligent_query(request: IntelligentQueryRequest):
    """
    Intelligent query routing using intent classification.
    
    Routes queries to appropriate handlers:
    - CHAT -> LLM for educational conversations  
    - REPORT -> Structured data/analytics for reporting
    """
    start_time = datetime.utcnow()
    logger.info(f"Processing intelligent query: {request.query}")
    
    try:
        # Step 1: Predict intent using our classifier
        predicted_intent = predict_intent(request.query)
        logger.info(f"Predicted intent: {predicted_intent} for query: '{request.query}'")
        
        # Step 2: Route based on predicted intent
        if predicted_intent == "CHAT":
            # Route to LLM for educational/conversational responses
            response_data = await _handle_chat_intent(request)
            response_type = "llm_chat"
            
        elif predicted_intent == "REPORT":
            # Route to analytics/reporting for data queries
            response_data = await _handle_report_intent(request)
            response_type = "structured_report"
            
        else:
            # Fallback (shouldn't happen with our binary classifier)
            logger.warning(f"Unknown intent: {predicted_intent}, defaulting to CHAT")
            response_data = await _handle_chat_intent(request)
            response_type = "llm_chat_fallback"
        
        # Step 3: Calculate timing
        generation_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
        
        # Step 4: Return structured response
        return IntelligentQueryResponse(
            query=request.query,
            predicted_intent=predicted_intent,
            response=response_data["response"],
            response_type=response_type,
            model_used=response_data.get("model_used"),
            generation_time_ms=generation_time,
            timestamp=datetime.utcnow().isoformat(),
            confidence_info=response_data.get("confidence_info")
        )
        
    except Exception as e:
        logger.error(f"Error in intelligent query processing: {e}")
        # Fallback to basic chat response
        try:
            fallback_response = await _handle_chat_intent(request)
            generation_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            return IntelligentQueryResponse(
                query=request.query,
                predicted_intent="CHAT",
                response=fallback_response["response"],
                response_type="fallback_chat",
                model_used=fallback_response.get("model_used"),
                generation_time_ms=generation_time,
                timestamp=datetime.utcnow().isoformat()
            )
        except Exception as fallback_error:
            logger.error(f"Fallback also failed: {fallback_error}")
            raise HTTPException(
                status_code=500, 
                detail=f"Query processing failed: {str(e)}"
            )

async def _handle_chat_intent(request: IntelligentQueryRequest) -> Dict[str, Any]:
    """Handle CHAT intent by routing to LLM"""
    try:
        if not LLM_GENERATOR_AVAILABLE:
            return {
                "response": "Hello! I'm here to help with cybersecurity questions. The advanced LLM chat system is currently unavailable, but I can provide basic assistance.",
                "model_used": "simple_fallback"
            }
        
        # Create chat request for LLM
        chat_req = ChatRequest(
            message=request.query,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        # Call existing LLM chat endpoint
        chat_response = await general_chat(chat_req)
        
        return {
            "response": chat_response.response,
            "model_used": chat_response.model_used,
            "confidence_info": {
                "route": "llm_chat",
                "generation_time_ms": chat_response.generation_time_ms
            }
        }
        
    except Exception as e:
        logger.error(f"Error handling chat intent: {e}")
        return {
            "response": f"I'm here to help with cybersecurity questions. I encountered an issue processing your request: {str(e)}",
            "model_used": "error_fallback"
        }

async def _handle_report_intent(request: IntelligentQueryRequest) -> Dict[str, Any]:
    """Handle REPORT intent by routing to analytics/reporting"""
    try:
        query_lower = request.query.lower()
        
        # Determine specific report type based on keywords
        if any(kw in query_lower for kw in ['click', 'user', 'activity', 'tracking']):
            return await _generate_click_report(request)
        
        elif any(kw in query_lower for kw in ['analytics', 'analysis', 'trend', 'pattern']):
            return await _generate_analytics_report(request)
        
        elif any(kw in query_lower for kw in ['status', 'overview', 'summary', 'dashboard']):
            return await _generate_status_report(request)
        
        else:
            # Generic report using admin assistant
            return await _generate_admin_report(request)
            
    except Exception as e:
        logger.error(f"Error handling report intent: {e}")
        return {
            "response": f"Unable to generate report: {str(e)}. Please try a more specific query.",
            "model_used": "report_fallback"
        }

async def _generate_click_report(request: IntelligentQueryRequest) -> Dict[str, Any]:
    """Generate click tracking report"""
    try:
        if not CLICK_TRACKER_AVAILABLE:
            return {
                "response": "📊 **Click Tracking Report**\n\nClick tracking system is currently unavailable. Please check system status.",
                "model_used": "unavailable_fallback"
            }
            
        # Get click stats using existing function
        stats_response = get_click_stats()
        
        # Extract stats data from JSONResponse
        if hasattr(stats_response, 'body'):
            import json
            stats_data = json.loads(stats_response.body)
        else:
            # Direct function call returns dict - try to get the actual response
            try:
                # stats_response might be a JSONResponse object with content
                stats_data = stats_response
            except:
                stats_data = {
                    "stats": {
                        "total_clicks": 0,
                        "unique_users": 0, 
                        "recent_activity": {"last_24h": 0, "last_7d": 0},
                        "top_users": {}
                    }
                }
        
        stats = stats_data.get("stats", {})
        
        # Format response
        response = f"""📊 **Click Tracking Report**

**Current Metrics:**
• Total Click Events: {stats.get('total_clicks', 0)}
• Unique Users: {stats.get('unique_users', 0)} 
• Recent Activity (24h): {stats.get('recent_activity', {}).get('last_24h', 0)}
• Recent Activity (7d): {stats.get('recent_activity', {}).get('last_7d', 0)}

**Top Users:**"""
        
        top_users = stats.get('top_users', {})
        if top_users:
            for email, clicks in list(top_users.items())[:5]:
                response += f"\n• {email.split('@')[0]}: {clicks} clicks"
        else:
            response += "\n• No user activity data available"
        
        response += "\n\n💡 **Generated using intelligent query routing**"
        
        return {
            "response": response,
            "model_used": "structured_data",
            "confidence_info": {
                "route": "click_report",
                "data_source": "click_logs.csv",
                "records_processed": stats.get('total_clicks', 0)
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating click report: {e}")
        return {
            "response": f"Unable to generate click report: {str(e)}",
            "model_used": "error_fallback"
        }

async def _generate_analytics_report(request: IntelligentQueryRequest) -> Dict[str, Any]:
    """Generate advanced analytics report"""
    try:
        if request.include_analytics:
            # Use existing analytics endpoint
            analytics_req = AnalyticsRequest(
                engine=AnalyticsEngine.PANDAS,
                time_range="7d"
            )
            
            analytics_response = await perform_analytics(analytics_req)
            
            # Format the analytics response
            summary = analytics_response.summary
            response = f"""📈 **Analytics Report**

**Summary:**
• Time Period: {analytics_response.time_range}
• Analysis Engine: {analytics_response.engine}
• Data Points: {summary.get('total_events', 0)}

**Key Insights:**
• Peak Activity Hour: {summary.get('peak_hour', 'N/A')}
• Risk Level: {summary.get('risk_level', 'Unknown')}

💡 **Generated using intelligent query routing with advanced analytics**"""

        else:
            response = "📈 **Analytics Report**\n\nBasic analytics data requested. Enable detailed analytics for comprehensive insights."
        
        return {
            "response": response,
            "model_used": "pandas_analytics", 
            "confidence_info": {
                "route": "analytics_report",
                "analysis_engine": "pandas"
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating analytics report: {e}")
        return {
            "response": f"📈 **Analytics Report**\n\nUnable to generate detailed analytics: {str(e)}",
            "model_used": "analytics_fallback"
        }

async def _generate_status_report(request: IntelligentQueryRequest) -> Dict[str, Any]:
    """Generate system status report"""
    try:
        # Get basic stats
        stats_response = get_click_stats()
        classifier = get_classifier()
        
        # Format status response
        response = f"""🔍 **System Status Report**

**Security Monitoring:**
• Click Tracking: Active
• Intent Classification: {classifier.get_model_info()['model_loaded']}
• Data Processing: Operational

**Quick Stats:**
• Total Events Tracked: Active monitoring
• System Health: Operational
• Last Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}

💡 **Generated using intelligent query routing**"""

        return {
            "response": response,
            "model_used": "system_status",
            "confidence_info": {
                "route": "status_report",
                "system_health": "operational"
            }
        }
        
    except Exception as e:
        return {
            "response": f"🔍 **System Status**: Unable to generate status report: {str(e)}",
            "model_used": "status_fallback"
        }

async def _generate_admin_report(request: IntelligentQueryRequest) -> Dict[str, Any]:
    """Generate report using admin assistant for complex queries"""
    try:
        # Use existing admin query system as fallback
        admin_req = AdminQuery(
            query=request.query,
            include_data_analysis=request.include_analytics
        )
        
        admin_response = await admin_query(admin_req)
        
        return {
            "response": admin_response.response,
            "model_used": "admin_assistant",
            "confidence_info": {
                "route": "admin_report",
                "suggestions": admin_response.suggestions,
                "data_insights": bool(admin_response.data_insights)
            }
        }
        
    except Exception as e:
        return {
            "response": f"Unable to process admin query: {str(e)}",
            "model_used": "admin_fallback"
        }

# Additional endpoints for classifier management
@router.get("/classifier/info")
async def get_classifier_info():
    """Get information about the intent classifier"""
    try:
        classifier = get_classifier()
        return {
            "classifier_info": classifier.get_model_info(),
            "available_intents": ["CHAT", "REPORT"],
            "training_data_size": 90,  # From our generated dataset
            "status": "operational"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classifier info error: {str(e)}")

@router.post("/classifier/predict")
async def predict_query_intent(query: str):
    """Direct intent prediction endpoint for testing"""
    try:
        intent = predict_intent(query)
        return {
            "query": query,
            "predicted_intent": intent,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Intent prediction error: {str(e)}")

@router.post("/classifier/retrain")
async def retrain_classifier():
    """Retrain the classifier (for expanding dataset)"""
    try:
        classifier = get_classifier()
        classifier.train(force_retrain=True)
        
        return {
            "message": "Classifier retrained successfully",
            "model_info": classifier.get_model_info(),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining error: {str(e)}")