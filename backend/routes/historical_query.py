from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
# Updated LlamaIndex imports
try:
    from llama_index.core import VectorStoreIndex, Document, Settings
    from llama_index.llms.ollama import Ollama
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.core.node_parser import SimpleNodeParser
    from llama_index.core.storage.storage_context import StorageContext
    from llama_index.vector_stores.simple import SimpleVectorStore
    LLAMA_INDEX_AVAILABLE = True
except ImportError as e:
    print(f"LlamaIndex import error: {e}")
    LLAMA_INDEX_AVAILABLE = False

import pandas as pd
import os
from datetime import datetime, timedelta
import json
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class QueryRequest(BaseModel):
    question: str
    time_filter: Optional[str] = None  # "24h", "7d", "30d", or None for all time
    include_context: Optional[bool] = True

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]
    query_metadata: Dict[str, Any]
    timestamp: str

class HistoricalDataIndexer:
    """Class to manage LlamaIndex for historical phishing data"""
    
    def __init__(self):
        if not LLAMA_INDEX_AVAILABLE:
            logger.warning("LlamaIndex not available, using fallback mode")
            self.llm = None
            self.embed_model = None
            self.index = None
            self.last_update = None
            return
            
        try:
            # Initialize Ollama LLM for LlamaIndex
            self.llm = Ollama(model="mistral:7b", base_url="http://localhost:11434")
            
            # Use a lightweight embedding model
            self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
            
            # Configure settings
            Settings.llm = self.llm
            Settings.embed_model = self.embed_model
            Settings.chunk_size = 512
            Settings.chunk_overlap = 50
            
            # Initialize storage
            self.vector_store = SimpleVectorStore()
            self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
            
            self.index = None
            self.last_update = None
            
        except Exception as e:
            logger.error(f"Failed to initialize LlamaIndex components: {e}")
            self.llm = None
            self.embed_model = None
            self.index = None
            self.last_update = None
    
    def load_and_process_data(self, time_filter: Optional[str] = None) -> List:
        """Load click data and convert to documents"""
        data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        log_file = os.path.join(data_dir, "click_logs.csv")
        
        if not os.path.exists(log_file):
            # Create directory and empty file if they don't exist
            os.makedirs(data_dir, exist_ok=True)
            with open(log_file, 'w', newline='') as f:
                import csv
                writer = csv.writer(f)
                writer.writerow(["timestamp", "user_email", "action_id", "ip_address"])
            return []
        
        try:
            df = pd.read_csv(log_file)
            if df.empty:
                return []
                
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Apply time filter if specified
            if time_filter:
                now = datetime.utcnow()
                if time_filter == "24h":
                    df = df[df['timestamp'] > (now - timedelta(hours=24))]
                elif time_filter == "7d":
                    df = df[df['timestamp'] > (now - timedelta(days=7))]
                elif time_filter == "30d":
                    df = df[df['timestamp'] > (now - timedelta(days=30))]
            
            if not LLAMA_INDEX_AVAILABLE:
                # Return simple dict format for fallback
                return df.to_dict('records')
            
            documents = []
            
            # Create documents from individual click records
            for _, row in df.iterrows():
                doc_text = f"""
                Phishing Click Event:
                Timestamp: {row['timestamp']}
                User Email: {row['user_email']}
                Action ID: {row['action_id']}
                IP Address: {row['ip_address']}
                Date: {row['timestamp'].strftime('%Y-%m-%d')}
                Time: {row['timestamp'].strftime('%H:%M:%S')}
                Day of Week: {row['timestamp'].strftime('%A')}
                Hour: {row['timestamp'].hour}
                """
                
                metadata = {
                    "timestamp": row['timestamp'].isoformat(),
                    "user_email": row['user_email'],
                    "action_id": row['action_id'],
                    "ip_address": row['ip_address'],
                    "date": row['timestamp'].strftime('%Y-%m-%d'),
                    "hour": row['timestamp'].hour,
                    "day_of_week": row['timestamp'].strftime('%A')
                }
                
                documents.append(Document(text=doc_text, metadata=metadata))
            
            # Create aggregate documents for better analysis
            if not df.empty:
                # Daily summary
                daily_summary = df.groupby(df['timestamp'].dt.date).agg({
                    'user_email': 'count'
                }).rename(columns={'user_email': 'total_clicks'})
                
                for date, data in daily_summary.iterrows():
                    day_data = df[df['timestamp'].dt.date == date]
                    summary_text = f"""
                    Daily Phishing Training Summary for {date}:
                    Total Clicks: {data['total_clicks']}
                    Unique Users: {day_data['user_email'].nunique()}
                    Most Active Hour: {day_data.groupby(day_data['timestamp'].dt.hour).size().idxmax() if not day_data.empty else 'N/A'}
                    """
                    
                    documents.append(Document(
                        text=summary_text,
                        metadata={"type": "daily_summary", "date": str(date)}
                    ))
                
                # User behavior patterns
                user_patterns = df.groupby('user_email').agg({
                    'timestamp': ['count', 'min', 'max'],
                    'action_id': 'nunique'
                })
                
                for user in user_patterns.index:
                    user_data = user_patterns.loc[user]
                    total_clicks = user_data[('timestamp', 'count')]
                    pattern_text = f"""
                    User Behavior Pattern for {user}:
                    Total Clicks: {total_clicks}
                    First Click: {user_data[('timestamp', 'min')]}
                    Last Click: {user_data[('timestamp', 'max')]}
                    Unique Actions: {user_data[('action_id', 'nunique')]}
                    Risk Level: {'HIGH' if total_clicks > 3 else 'MEDIUM' if total_clicks > 1 else 'LOW'}
                    """
                    
                    documents.append(Document(
                        text=pattern_text,
                        metadata={"type": "user_pattern", "user_email": user}
                    ))
            
            return documents
            
        except Exception as e:
            logger.error(f"Error processing data: {e}")
            return []
    
    def build_index(self, time_filter: Optional[str] = None):
        """Build or rebuild the vector index"""
        if not LLAMA_INDEX_AVAILABLE or self.llm is None:
            logger.warning("LlamaIndex not available, skipping index build")
            return
            
        try:
            documents = self.load_and_process_data(time_filter)
            
            if not documents:
                logger.warning("No documents to index")
                return
            
            # Create new index
            self.index = VectorStoreIndex.from_documents(
                documents,
                storage_context=self.storage_context
            )
            
            self.last_update = datetime.utcnow()
            logger.info(f"Index built with {len(documents)} documents")
            
        except Exception as e:
            logger.error(f"Error building index: {e}")
            raise
    
    def fallback_query(self, question: str, time_filter: Optional[str] = None) -> Dict[str, Any]:
        """Fallback query method when LlamaIndex is not available"""
        try:
            data = self.load_and_process_data(time_filter)
            
            if not data:
                return {
                    "answer": "No data available to analyze",
                    "sources": [],
                    "metadata": {"method": "fallback", "error": "No data"}
                }
            
            # Simple pattern matching for common questions
            question_lower = question.lower()
            
            if "user" in question_lower and "click" in question_lower:
                df = pd.DataFrame(data)
                user_clicks = df['user_email'].value_counts()
                answer = f"Users with most clicks: {user_clicks.head().to_dict()}"
            elif "hour" in question_lower or "time" in question_lower:
                df = pd.DataFrame(data)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                hourly = df.groupby(df['timestamp'].dt.hour).size()
                peak_hour = hourly.idxmax()
                answer = f"Peak activity hour: {peak_hour}:00 with {hourly[peak_hour]} clicks"
            elif "day" in question_lower:
                df = pd.DataFrame(data)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                daily = df.groupby(df['timestamp'].dt.day_name()).size()
                peak_day = daily.idxmax()
                answer = f"Peak activity day: {peak_day} with {daily[peak_day]} clicks"
            else:
                df = pd.DataFrame(data)
                total_clicks = len(df)
                unique_users = df['user_email'].nunique()
                answer = f"Total clicks: {total_clicks}, Unique users: {unique_users}"
            
            return {
                "answer": f"Fallback Analysis: {answer}",
                "sources": ["CSV data analysis"],
                "metadata": {"method": "fallback", "records_analyzed": len(data)}
            }
            
        except Exception as e:
            return {
                "answer": f"Error in fallback analysis: {str(e)}",
                "sources": [],
                "metadata": {"method": "fallback", "error": str(e)}
            }
    
    def query(self, question: str, time_filter: Optional[str] = None) -> Dict[str, Any]:
        """Query the index with a question"""
        if not LLAMA_INDEX_AVAILABLE or self.llm is None or self.index is None:
            return self.fallback_query(question, time_filter)
            
        try:
            # Rebuild index if needed or if time filter changed
            if self.index is None or time_filter:
                self.build_index(time_filter)
            
            if self.index is None:
                return self.fallback_query(question, time_filter)
            
            # Create query engine
            query_engine = self.index.as_query_engine(
                response_mode="tree_summarize",
                similarity_top_k=5
            )
            
            # Enhance the question with context
            enhanced_question = f"""
            Based on the phishing training click data, please answer this question: {question}
            
            Consider patterns in:
            - User behavior and click frequencies
            - Time-based trends (daily, hourly patterns)
            - Risk assessments and security implications
            - Training effectiveness indicators
            
            Provide specific data points and actionable insights where possible.
            """
            
            # Execute query
            response = query_engine.query(enhanced_question)
            
            # Extract sources
            sources = []
            if hasattr(response, 'source_nodes'):
                for node in response.source_nodes:
                    if hasattr(node, 'metadata'):
                        sources.append(str(node.metadata))
            
            return {
                "answer": str(response),
                "sources": sources[:5],  # Limit to top 5 sources
                "metadata": {
                    "query_time": datetime.utcnow().isoformat(),
                    "time_filter": time_filter,
                    "index_last_updated": self.last_update.isoformat() if self.last_update else None,
                    "method": "llamaindex"
                }
            }
            
        except Exception as e:
            logger.error(f"Error querying index: {e}")
            # Fallback to simple analysis
            return self.fallback_query(question, time_filter)

# Initialize the indexer
indexer = HistoricalDataIndexer()

@router.post("/query/historical", response_model=QueryResponse)
async def query_historical_data(request: QueryRequest):
    """Query historical phishing data using LlamaIndex or fallback"""
    try:
        result = indexer.query(request.question, request.time_filter)
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            query_metadata=result["metadata"],
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error in historical query: {e}")
        raise HTTPException(status_code=500, detail=f"Query error: {str(e)}")

@router.post("/query/rebuild-index")
async def rebuild_index(time_filter: Optional[str] = None):
    """Manually rebuild the vector index"""
    try:
        if LLAMA_INDEX_AVAILABLE:
            indexer.build_index(time_filter)
            return {
                "message": "Index rebuilt successfully",
                "last_update": indexer.last_update.isoformat() if indexer.last_update else None,
                "time_filter": time_filter
            }
        else:
            return {
                "message": "LlamaIndex not available, using fallback mode",
                "last_update": None,
                "time_filter": time_filter
            }
    except Exception as e:
        logger.error(f"Error rebuilding index: {e}")
        raise HTTPException(status_code=500, detail=f"Index rebuild error: {str(e)}")

@router.get("/query/index-status")
async def get_index_status():
    """Get the current status of the vector index"""
    return {
        "llamaindex_available": LLAMA_INDEX_AVAILABLE,
        "index_exists": indexer.index is not None if LLAMA_INDEX_AVAILABLE else False,
        "last_update": indexer.last_update.isoformat() if indexer.last_update else None,
        "service_context_info": {
            "llm_model": "mistral:7b" if LLAMA_INDEX_AVAILABLE else "unavailable",
            "embedding_model": "BAAI/bge-small-en-v1.5" if LLAMA_INDEX_AVAILABLE else "unavailable",
            "chunk_size": 512 if LLAMA_INDEX_AVAILABLE else "unavailable"
        }
    }

@router.get("/query/sample-questions")
async def get_sample_questions():
    """Get sample questions that work well with the historical data"""
    return {
        "sample_questions": [
            "Which users have clicked on phishing emails multiple times?",
            "What are the peak hours for phishing clicks?",
            "How has user behavior changed over the last 30 days?",
            "Which day of the week has the most phishing clicks?",
            "Who are the highest risk users based on click patterns?",
            "What is the average time between clicks for repeat offenders?",
            "Are there any IP addresses with suspicious activity?",
            "How effective has our training been in reducing clicks?",
            "What patterns do we see in user behavior?",
            "Which users need additional security training?"
        ],
        "time_filters": ["24h", "7d", "30d", None],
        "tips": [
            "Use specific time filters for focused analysis",
            "Ask about patterns and trends for better insights",
            "Include user email addresses for individual assessments",
            "Ask comparative questions about before/after training periods"
        ]
    }