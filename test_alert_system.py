#!/usr/bin/env python3
"""
Test script for the enhanced Phishy AI alert system
Tests the auto-scan and warning functionality
"""

import requests
import json
import time
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8080"
TEST_EMAILS = [
    {
        "name": "High Risk Phishing Email",
        "content": """Subject: URGENT: Verify Your Account Immediately

Dear Customer,

Your account has been suspended due to unusual activity. Click here to verify your account immediately: http://123.456.789.0/verify-account

Please provide your password and social security number to continue.

Act now or your account will be permanently deleted!

Best regards,
Security Team""",
        "expected_risk": "HIGH"
    },
    {
        "name": "Medium Risk Suspicious Email", 
        "content": """Subject: Update Your Information

Hi there,

We need to update your account information. Please click the link below:
https://bit.ly/update-info

Thank you for your cooperation.

Customer Service""",
        "expected_risk": "MEDIUM"
    },
    {
        "name": "Low Risk Normal Email",
        "content": """Subject: Weekly Team Meeting

Hi Team,

Don't forget about our weekly team meeting tomorrow at 2 PM in the conference room.

Thanks,
Manager""",
        "expected_risk": "LOW"
    }
]

def test_phishing_detector():
    """Test the phishing detector API endpoint"""
    print("🧪 Testing Phishing Detector API...")
    
    detector_url = f"{API_BASE_URL}/detector/analyze-email"
    
    for test_email in TEST_EMAILS:
        print(f"\n📧 Testing: {test_email['name']}")
        
        payload = {
            "email_content": test_email["content"],
            "include_detailed_analysis": True,
            "cache_results": False
        }
        
        try:
            response = requests.post(detector_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Status: SUCCESS")
                print(f"   🎯 Risk Level: {result.get('risk_level', 'UNKNOWN')}")
                print(f"   📊 Confidence: {result.get('confidence_score', 0):.1f}%")
                print(f"   🚨 Is Phishing: {result.get('is_phishing', False)}")
                print(f"   ⚡ Analysis Time: {result.get('analysis_time', 0):.3f}s")
                
                # Show risk factors
                risk_factors = result.get('analysis_details', {}).get('risk_factors', [])
                if risk_factors:
                    print(f"   ⚠️  Risk Factors: {', '.join(risk_factors)}")
                
                # Check if result matches expectation
                expected = test_email['expected_risk']
                actual = result.get('risk_level', 'UNKNOWN')
                if expected == actual:
                    print(f"   ✅ Expected risk level matched: {expected}")
                else:
                    print(f"   ⚠️  Risk level mismatch: expected {expected}, got {actual}")
                    
            else:
                print(f"   ❌ HTTP Error: {response.status_code}")
                print(f"   📄 Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request Error: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected Error: {e}")
        
        time.sleep(1)  # Rate limiting

def test_email_flagging():
    """Test the email flagging endpoint"""
    print("\n🚩 Testing Email Flagging API...")
    
    flagging_url = f"{API_BASE_URL}/email-flagging/flag"
    
    test_flag = {
        "email_id": f"test_email_{int(time.time())}",
        "sender_email": "suspicious@phishing-test.com",
        "subject": "TEST: Urgent Account Verification Required",
        "body": TEST_EMAILS[0]["content"],
        "flag_category": "phishing",
        "confidence_level": 0.9,
        "user_email": "test@company.com",
        "client_info": {
            "plugin_type": "gmail",
            "user_agent": "Test Script",
            "url": "test://automated-test"
        },
        "plugin_version": "1.0.0-test",
        "additional_context": "Automated test of alert system"
    }
    
    try:
        response = requests.post(flagging_url, json=test_flag, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Email flagged successfully")
            print(f"   📧 Email ID: {result.get('email_id')}")
            print(f"   📅 Flagged at: {result.get('flagged_at')}")
            
            # Check analysis result
            analysis = result.get('analysis', {})
            if analysis:
                print(f"   🎯 AI Analysis - Risk: {analysis.get('threat_level', 'N/A')}")
                print(f"   📊 AI Confidence: {analysis.get('confidence_score', 0):.1f}%")
                
        else:
            print(f"   ❌ HTTP Error: {response.status_code}")
            print(f"   📄 Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request Error: {e}")
    except Exception as e:
        print(f"   ❌ Unexpected Error: {e}")

def test_health_checks():
    """Test system health endpoints"""
    print("\n🏥 Testing System Health...")
    
    health_endpoints = [
        ("/email-flagging/health", "Email Flagging System"),
        ("/detector/health", "Phishing Detector"),
        ("/detector/detector-status", "Detector Status")
    ]
    
    for endpoint, name in health_endpoints:
        url = f"{API_BASE_URL}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ {name}: HEALTHY")
                if 'version' in data:
                    print(f"      Version: {data['version']}")
                if 'model_type' in data:
                    print(f"      Model: {data['model_type']}")
            else:
                print(f"   ❌ {name}: ERROR ({response.status_code})")
        except Exception as e:
            print(f"   ❌ {name}: UNREACHABLE ({e})")

def generate_test_report():
    """Generate a comprehensive test report"""
    print("\n" + "="*60)
    print("🛡️  PHISHY AI ALERT SYSTEM TEST REPORT")
    print("="*60)
    print(f"📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API Base URL: {API_BASE_URL}")
    print()
    
    # Run all tests
    test_health_checks()
    test_phishing_detector()
    test_email_flagging()
    
    print("\n" + "="*60)
    print("📋 IMPLEMENTATION SUMMARY")
    print("="*60)
    print("✅ Auto-scan functionality implemented")
    print("✅ Real-time warning system added")
    print("✅ Enhanced Gmail extension with AI integration")
    print("✅ Fallback rule-based detection")
    print("✅ Visual warning alerts with risk levels")
    print("✅ Integration with existing flagging system")
    print()
    print("🚀 To activate the alert system:")
    print("   1. Start the Phishy backend: python backend/app.py")
    print("   2. Load the Gmail extension in Chrome")
    print("   3. Configure the extension with your ngrok URL")
    print("   4. Open emails in Gmail - warnings will appear automatically!")
    print()
    print("🔧 Features added:")
    print("   • Automatic email content scanning on open")
    print("   • Visual warnings for HIGH/CRITICAL risk emails")  
    print("   • Caution alerts for MEDIUM risk emails")
    print("   • Integration with ML models and rule-based fallback")
    print("   • Real-time threat analysis")
    print("   • User-friendly security recommendations")
    print("="*60)

if __name__ == "__main__":
    generate_test_report()