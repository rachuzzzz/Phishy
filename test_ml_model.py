#!/usr/bin/env python3

import sys
import os
import asyncio
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

async def test_ml_model():
    """Test the ML model loading and prediction"""
    
    try:
        from backend.routes.phishing_detector import EnhancedPhishingDetector
        
        detector = EnhancedPhishingDetector()
        
        print("Testing ML model initialization...")
        
        # Test model initialization
        result = await detector.initialize_models()
        print(f"Model initialization result: {result}")
        
        # Check cache status
        from backend.routes.phishing_detector import model_cache
        print(f"Model cache initialized: {model_cache['initialized']}")
        print(f"Classifier loaded: {model_cache['classifier'] is not None}")
        print(f"Embedder loaded: {model_cache['embedder'] is not None}")
        
        # Test prediction with a sample phishing email
        test_email = """
        URGENT: Your account will be suspended!
        
        Dear customer,
        
        We detected suspicious activity on your account. Click here immediately to verify your account:
        http://fake-bank-login.com/verify
        
        You have 24 hours to respond or your account will be permanently closed.
        
        Security Team
        """
        
        print("Testing prediction with sample email...")
        
        # Extract features
        features = detector.extract_advanced_features(test_email)
        print(f"Extracted features: {list(features.keys())}")
        
        # Test ML analysis
        analysis_result = await detector.analyze_with_ml(test_email, features)
        print(f"Analysis result: {analysis_result}")
        
        return analysis_result
        
    except Exception as e:
        print(f"Error testing ML model: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = asyncio.run(test_ml_model())
    if result:
        print("ML model test completed successfully!")
        print(f"Prediction: {'PHISHING' if result.get('is_phishing') else 'SAFE'}")
        print(f"Confidence: {result.get('confidence', 0):.2f}%")
        print(f"Method: {result.get('method', 'unknown')}")
    else:
        print("ML model test failed!")