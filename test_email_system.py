#!/usr/bin/env python3
"""
Test script to verify Phishy email generation and sending functionality
"""

import requests
import json
import sys
from time import sleep

# Configuration
BASE_URL = "http://localhost:8080"
TEST_EMAIL = "test@company.com"

def test_backend_health():
    """Test if the backend is running"""
    print("🔍 Testing backend health...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy!")
            data = response.json()
            print(f"   📍 Backend Port: {data.get('port_configuration', {}).get('backend_port', '8080')}")
            print(f"   📍 Routes Loaded: {', '.join(data.get('routes_loaded', []))}")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   💡 Make sure to run 'python app.py' in the backend directory first")
        return False

def test_llm_health():
    """Test LLM service connectivity"""
    print("\n🤖 Testing LLM service...")
    try:
        response = requests.get(f"{BASE_URL}/llm/health", timeout=10)
        data = response.json()
        
        if data.get("status") == "healthy":
            print("✅ LLM service is healthy!")
            print(f"   🧠 Model: {data.get('ollama_service', {}).get('recommended_model', 'Unknown')}")
        elif data.get("status") == "degraded":
            print("⚠️ LLM service is degraded (fallback available)")
            print("   💡 Ollama may not be running - emails will use templates")
        else:
            print("❌ LLM service unavailable")
            
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ LLM health check failed: {e}")
        return False

def test_email_generation():
    """Test email generation"""
    print("\n📧 Testing email generation...")
    
    payload = {
        "user_email": TEST_EMAIL,
        "custom_topic": "Test security awareness email",
        "use_llm": True,
        "temperature": 0.7,
        "max_tokens": 300
    }
    
    try:
        print("   📤 Generating test email...")
        response = requests.post(f"{BASE_URL}/llm/generate-email", json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Email generation successful!")
            print(f"   📧 Target: {data.get('email')}")
            print(f"   🎯 Method: {data.get('generation_method')}")
            print(f"   🔗 Tracking URL: {data.get('track_url')}")
            print(f"   📝 Content Preview: {data.get('email_content', '')[:100]}...")
            return data
        else:
            print(f"❌ Email generation failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Email generation error: {e}")
        return None

def test_smtp_connection():
    """Test SMTP connection (optional - requires user input)"""
    print("\n📨 SMTP Connection Test")
    print("   To test email sending, you'll need:")
    print("   1. A Gmail address")
    print("   2. A Gmail App Password (not your regular password)")
    print("   3. To enable 2-factor authentication on Gmail")
    print("")
    
    test_smtp = input("   Do you want to test SMTP connection? (y/N): ").lower().strip()
    
    if test_smtp == 'y':
        gmail_address = input("   Enter Gmail address: ").strip()
        app_password = input("   Enter Gmail App Password: ").strip()
        
        if gmail_address and app_password:
            payload = {
                "smtp_email": gmail_address,
                "smtp_password": app_password
            }
            
            try:
                print("   🔗 Testing SMTP connection...")
                response = requests.post(f"{BASE_URL}/smtp/test-smtp", json=payload, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        print("✅ SMTP connection successful!")
                        return True
                    else:
                        print(f"❌ SMTP connection failed: {data.get('error')}")
                        return False
                else:
                    print(f"❌ SMTP test failed: {response.status_code}")
                    return False
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ SMTP test error: {e}")
                return False
        else:
            print("   ⏭️ Skipping SMTP test (credentials not provided)")
    else:
        print("   ⏭️ Skipping SMTP test")
    
    return None

def print_frontend_instructions():
    """Print instructions for using the frontend"""
    print("\n🎯 Frontend Usage Instructions:")
    print("="*50)
    print("1. Open 'frontend/index.html' in your web browser")
    print("2. Or serve it with a local server:")
    print("   cd frontend")
    print("   python -m http.server 3001")
    print("   Then visit: http://localhost:3001")
    print("")
    print("3. In the web interface:")
    print("   • Click 'AI Email Generator' in the sidebar")
    print("   • Enter a target email address")
    print("   • Describe the type of email you want")
    print("   • Click 'Generate Phishing Email'")
    print("   • Edit the generated content if needed")
    print("   • Configure SMTP settings to send")
    print("")
    print("📚 API Documentation: http://localhost:8080/docs")

def main():
    """Run all tests"""
    print("🎣 Phishy AI Platform Test Suite")
    print("="*40)
    
    # Test 1: Backend Health
    if not test_backend_health():
        print("\n❌ Cannot proceed - backend is not running")
        sys.exit(1)
    
    # Test 2: LLM Health  
    test_llm_health()
    
    # Test 3: Email Generation
    generated_email = test_email_generation()
    
    # Test 4: SMTP (optional)
    smtp_works = test_smtp_connection()
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    print("✅ Backend Health: OK")
    print("✅ Email Generation: OK" if generated_email else "❌ Email Generation: FAILED")
    
    if smtp_works is True:
        print("✅ SMTP Connection: OK")
    elif smtp_works is False:
        print("❌ SMTP Connection: FAILED")
    else:
        print("⏭️ SMTP Connection: SKIPPED")
    
    if generated_email:
        print("\n🎉 Core functionality is working!")
        print_frontend_instructions()
    else:
        print("\n⚠️ Some issues found - check the errors above")
    
    print("\n🚀 Backend is running at: http://localhost:8080")
    print("📚 API Documentation: http://localhost:8080/docs")

if __name__ == "__main__":
    main()