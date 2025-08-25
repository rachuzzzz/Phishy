#!/usr/bin/env python3
"""
ML Model Diagnostic Tool for Phishy AI
Debug classification model issues
"""

import sys
import os
import json
import requests
import numpy as np
from datetime import datetime

class ModelDiagnostics:
    def __init__(self, base_url="http://localhost:8080"):
        self.base_url = base_url
        self.test_emails = {
            "obvious_phishing": [
                {
                    "name": "Urgent Account Verification",
                    "content": """Subject: URGENT: Verify Your Account Immediately
                    
Your account has been suspended due to suspicious activity.
Click here to verify your account: http://fake-bank-verification.com/urgent
Please provide your password and social security number.
Act now or your account will be permanently closed!""",
                    "expected": "phishing"
                },
                {
                    "name": "Phishy Training Email", 
                    "content": """Subject: Urgent Action Required for Annual Ice Cream Day Event
                    
Dear student, this is a phishing simulation training email from Phishy AI.
Action Required: https://8407feb1df43.ngrok-free.app/track/click?user_email=test@gmail.com
Click here to verify your participation.""",
                    "expected": "phishing"
                },
                {
                    "name": "Nigerian Prince Scam",
                    "content": """Subject: Urgent Business Proposal
                    
Dear Friend, I am Prince Johnson from Nigeria. I have $10 million to transfer.
Click here immediately: http://bit.ly/nigerian-prince
Provide your bank account details urgently.""",
                    "expected": "phishing"
                }
            ],
            "legitimate_emails": [
                {
                    "name": "Meeting Reminder",
                    "content": """Subject: Weekly Team Meeting Tomorrow
                    
Hi Team,
Just a reminder about our weekly team meeting tomorrow at 2 PM in the conference room.
Please bring your status updates.
Best, Manager""",
                    "expected": "safe"
                },
                {
                    "name": "Newsletter",
                    "content": """Subject: Company Newsletter - March 2024
                    
Dear Employees,
Here's our monthly newsletter with company updates and achievements.
Thank you for your continued hard work.
HR Team""",
                    "expected": "safe"
                }
            ]
        }
    
    def test_api_connection(self):
        """Test if the API is responding"""
        print("🌐 Testing API Connection...")
        try:
            response = requests.get(f"{self.base_url}/detector/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ API responding: {data}")
                return True
            else:
                print(f"   ❌ API error: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Connection failed: {e}")
            return False
    
    def test_model_status(self):
        """Check model loading status"""
        print("\n🤖 Testing Model Status...")
        try:
            response = requests.get(f"{self.base_url}/detector/detector-status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   📊 Model Status: {data}")
                
                if data.get('model_type') == 'ml_model':
                    print("   ✅ ML model loaded successfully")
                else:
                    print("   ⚠️ Using rule-based fallback (ML model not loaded)")
                    
                return data
            else:
                print(f"   ❌ Status check failed: {response.status_code}")
                return None
        except Exception as e:
            print(f"   ❌ Status check error: {e}")
            return None
    
    def test_single_email(self, email_data):
        """Test classification on a single email"""
        try:
            response = requests.post(
                f"{self.base_url}/detector/analyze-email",
                json={
                    "email_content": email_data["content"],
                    "include_detailed_analysis": True,
                    "cache_results": False
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"\n📧 Email: {email_data['name']}")
                print(f"   Expected: {email_data['expected']}")
                print(f"   Predicted: {'phishing' if result.get('is_phishing') else 'safe'}")
                print(f"   Risk Level: {result.get('risk_level', 'UNKNOWN')}")
                print(f"   Confidence: {result.get('confidence_score', 0):.1f}%")
                print(f"   Method: {result.get('analysis_details', {}).get('analysis_method', 'unknown')}")
                
                # Check if prediction matches expectation
                is_correct = (
                    (email_data['expected'] == 'phishing' and result.get('is_phishing')) or
                    (email_data['expected'] == 'safe' and not result.get('is_phishing'))
                )
                
                print(f"   Result: {'✅ CORRECT' if is_correct else '❌ WRONG'}")
                
                # Show risk factors if available
                risk_factors = result.get('analysis_details', {}).get('risk_factors', [])
                if risk_factors:
                    print(f"   Risk Factors: {risk_factors}")
                
                return {
                    'email': email_data['name'],
                    'expected': email_data['expected'],
                    'predicted': 'phishing' if result.get('is_phishing') else 'safe',
                    'correct': is_correct,
                    'confidence': result.get('confidence_score', 0),
                    'risk_level': result.get('risk_level'),
                    'full_result': result
                }
            else:
                print(f"   ❌ API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"   ❌ Test failed: {e}")
            return None
    
    def run_comprehensive_tests(self):
        """Run all diagnostic tests"""
        print("🔍 ML MODEL COMPREHENSIVE DIAGNOSTICS")
        print("=" * 60)
        print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 API URL: {self.base_url}")
        
        # Test 1: API Connection
        if not self.test_api_connection():
            print("\n❌ Cannot proceed - API not responding")
            return
        
        # Test 2: Model Status
        model_status = self.test_model_status()
        if not model_status:
            print("\n⚠️ Cannot get model status")
        
        # Test 3: Classification Tests
        print("\n🧪 CLASSIFICATION TESTS")
        print("-" * 40)
        
        all_results = []
        
        # Test obvious phishing emails
        print("\n🚨 Testing Obvious Phishing Emails:")
        for email in self.test_emails["obvious_phishing"]:
            result = self.test_single_email(email)
            if result:
                all_results.append(result)
        
        # Test legitimate emails
        print("\n✅ Testing Legitimate Emails:")
        for email in self.test_emails["legitimate_emails"]:
            result = self.test_single_email(email)
            if result:
                all_results.append(result)
        
        # Analysis
        print("\n" + "=" * 60)
        print("📊 DIAGNOSTIC SUMMARY")
        print("=" * 60)
        
        if not all_results:
            print("❌ No test results - API or model issues")
            return
        
        correct_predictions = sum(1 for r in all_results if r['correct'])
        total_tests = len(all_results)
        accuracy = (correct_predictions / total_tests) * 100 if total_tests > 0 else 0
        
        print(f"🎯 Overall Accuracy: {accuracy:.1f}% ({correct_predictions}/{total_tests})")
        
        # Detailed analysis
        phishing_tests = [r for r in all_results if r['expected'] == 'phishing']
        safe_tests = [r for r in all_results if r['expected'] == 'safe']
        
        phishing_correct = sum(1 for r in phishing_tests if r['correct'])
        safe_correct = sum(1 for r in safe_tests if r['correct'])
        
        print(f"🚨 Phishing Detection: {phishing_correct}/{len(phishing_tests)} correct")
        print(f"✅ Safe Email Detection: {safe_correct}/{len(safe_tests)} correct")
        
        # Show problematic cases
        wrong_predictions = [r for r in all_results if not r['correct']]
        if wrong_predictions:
            print(f"\n❌ MISCLASSIFIED EMAILS:")
            for r in wrong_predictions:
                print(f"   • {r['email']}: Expected {r['expected']}, got {r['predicted']} ({r['confidence']:.1f}%)")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        if accuracy < 50:
            print("   🚨 CRITICAL: Model is performing worse than random!")
            print("   • Check if model file exists and loads properly")
            print("   • Verify training data quality")
            print("   • Consider retraining from scratch")
        elif accuracy < 70:
            print("   ⚠️ POOR: Model needs significant improvement")
            print("   • Add more training data")
            print("   • Check feature engineering")
            print("   • Tune hyperparameters")
        elif accuracy < 90:
            print("   📈 GOOD: Model is working but could be better")
            print("   • Fine-tune with more diverse examples")
            print("   • Adjust confidence thresholds")
        else:
            print("   ✅ EXCELLENT: Model is performing well!")
        
        # Check if using fallback
        using_fallback = any(r['full_result'].get('analysis_details', {}).get('analysis_method') == 'rule_based' 
                           for r in all_results)
        if using_fallback:
            print("   ⚠️ WARNING: Some tests used rule-based fallback instead of ML model")
            print("   • Check model loading in inference.py")
            print("   • Verify XGBoost and SentenceTransformers installation")
        
        print("=" * 60)
        
        return all_results
    
    def check_model_files(self):
        """Check if model files exist"""
        print("\n📁 Checking Model Files...")
        
        model_path = "Phishing detection/model/xgb_model.json"
        if os.path.exists(model_path):
            print(f"   ✅ XGBoost model found: {model_path}")
            print(f"      Size: {os.path.getsize(model_path)} bytes")
        else:
            print(f"   ❌ XGBoost model NOT FOUND: {model_path}")
            print("   💡 Train your model first with the training script")
        
        inference_path = "Phishing detection/inference.py"
        if os.path.exists(inference_path):
            print(f"   ✅ Inference script found: {inference_path}")
        else:
            print(f"   ❌ Inference script NOT FOUND: {inference_path}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Debug Phishy AI ML Model")
    parser.add_argument("--url", default="http://localhost:8080", help="API base URL")
    args = parser.parse_args()
    
    diagnostics = ModelDiagnostics(args.url)
    
    # Check model files first
    diagnostics.check_model_files()
    
    # Run comprehensive tests
    results = diagnostics.run_comprehensive_tests()
    
    print(f"\n🏁 Diagnostics complete! Check the results above.")
    print(f"💡 If model is performing poorly, check training data and retrain.")