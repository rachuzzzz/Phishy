#!/usr/bin/env python3
"""
SMTP Connection Troubleshooter for Phishy AI Platform
Diagnoses and fixes common SMTP connection issues
"""

import smtplib
import ssl
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json
from datetime import datetime

class SMTPDiagnostics:
    """Comprehensive SMTP diagnostics and testing"""
    
    def __init__(self):
        self.smtp_configs = {
            'gmail.com': {
                'server': 'smtp.gmail.com',
                'port': 587,
                'tls': True,
                'auth_note': 'Requires App Password (not regular password)'
            },
            'outlook.com': {
                'server': 'smtp.office365.com',
                'port': 587,
                'tls': True,
                'auth_note': 'Use regular email and password'
            },
            'hotmail.com': {
                'server': 'smtp.office365.com',
                'port': 587,
                'tls': True,
                'auth_note': 'Use regular email and password'
            },
            'yahoo.com': {
                'server': 'smtp.mail.yahoo.com',
                'port': 587,
                'tls': True,
                'auth_note': 'Requires App Password'
            }
        }
    
    def diagnose_smtp_connection(self, email: str, password: str = None):
        """Run comprehensive SMTP diagnostics"""
        print("🔍 SMTP Connection Diagnostics")
        print("=" * 50)
        print(f"📧 Email: {email}")
        print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        domain = email.split('@')[-1].lower()
        config = self.smtp_configs.get(domain)
        
        if not config:
            print(f"❌ Unsupported email domain: {domain}")
            print("📋 Supported domains:", list(self.smtp_configs.keys()))
            return False
        
        server = config['server']
        port = config['port']
        
        print(f"🌐 SMTP Server: {server}:{port}")
        print(f"🔒 TLS Required: {config['tls']}")
        print(f"📝 Auth Note: {config['auth_note']}")
        print()
        
        # Test 1: Network connectivity
        print("🧪 Test 1: Network Connectivity")
        try:
            socket.create_connection((server, port), timeout=10)
            print("   ✅ Can connect to SMTP server")
        except socket.timeout:
            print("   ❌ Connection timeout - check firewall/network")
            return False
        except socket.gaierror:
            print("   ❌ DNS resolution failed - check internet connection")
            return False
        except Exception as e:
            print(f"   ❌ Connection failed: {e}")
            return False
        
        # Test 2: SMTP handshake
        print("\\n🧪 Test 2: SMTP Handshake")
        try:
            smtp = smtplib.SMTP(server, port)
            response = smtp.ehlo()
            print(f"   ✅ SMTP handshake successful: {response[1].decode()[:50]}...")
            
            # Test STARTTLS
            if config['tls']:
                print("\\n🧪 Test 3: TLS Encryption")
                try:
                    smtp.starttls()
                    print("   ✅ TLS encryption enabled")
                except Exception as e:
                    print(f"   ❌ TLS failed: {e}")
                    smtp.quit()
                    return False
            
            smtp.quit()
        except Exception as e:
            print(f"   ❌ SMTP handshake failed: {e}")
            return False
        
        # Test 3: Authentication (if password provided)
        if password:
            print("\\n🧪 Test 4: Authentication")
            try:
                smtp = smtplib.SMTP(server, port)
                smtp.starttls()
                smtp.login(email, password)
                print("   ✅ Authentication successful")
                smtp.quit()
                return True
            except smtplib.SMTPAuthenticationError as e:
                print(f"   ❌ Authentication failed: {e}")
                self.suggest_auth_fixes(domain)
                return False
            except Exception as e:
                print(f"   ❌ Authentication error: {e}")
                return False
        else:
            print("\\n⚠️  Skipping authentication test (no password provided)")
            print("   ℹ️  Connection tests passed - authentication likely to work with correct credentials")
            return True
    
    def suggest_auth_fixes(self, domain):
        """Suggest fixes for authentication issues"""
        print("\\n🔧 Authentication Fix Suggestions:")
        
        if domain == 'gmail.com':
            print("   📱 Gmail requires App Passwords:")
            print("   1. Go to Google Account settings")
            print("   2. Enable 2-factor authentication")
            print("   3. Generate an App Password")
            print("   4. Use the 16-character app password (not your regular password)")
            print("   🔗 https://support.google.com/accounts/answer/185833")
        
        elif domain in ['outlook.com', 'hotmail.com']:
            print("   🏢 Outlook.com/Hotmail:")
            print("   1. Use your regular email and password")
            print("   2. If 2FA is enabled, you may need an app password")
            print("   3. Check if 'less secure apps' is enabled (if using old Outlook)")
        
        elif domain == 'yahoo.com':
            print("   🌐 Yahoo requires App Passwords:")
            print("   1. Go to Yahoo Account Security")
            print("   2. Generate an App Password")
            print("   3. Use the app password instead of your regular password")
            print("   🔗 https://help.yahoo.com/kb/generate-third-party-passwords-sln15241.html")
        
        print("\\n   💡 General tips:")
        print("   - Ensure 2-factor authentication is properly configured")
        print("   - Try generating a new app password")
        print("   - Check for typos in email/password")
        print("   - Verify account isn't locked or suspended")
    
    def test_phishy_smtp_endpoint(self, base_url="http://localhost:8080"):
        """Test the Phishy SMTP endpoint"""
        print("\\n🚀 Testing Phishy SMTP Endpoint")
        print("=" * 50)
        
        # Test health endpoint
        try:
            health_url = f"{base_url}/smtp/health"
            response = requests.get(health_url, timeout=5)
            if response.status_code == 200:
                print("   ✅ SMTP service is healthy")
            else:
                print(f"   ❌ SMTP service unhealthy: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("   ❌ Cannot connect to Phishy backend")
            print("   🔧 Fix: Start the backend with 'python backend/app.py'")
        except Exception as e:
            print(f"   ❌ Health check failed: {e}")
        
        # Test SMTP providers endpoint
        try:
            providers_url = f"{base_url}/smtp/smtp-providers"
            response = requests.get(providers_url, timeout=5)
            if response.status_code == 200:
                providers = response.json()
                print("   ✅ SMTP providers endpoint working")
                print(f"   📋 Available providers: {len(providers.get('providers', []))}")
            else:
                print(f"   ❌ Providers endpoint failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Providers test failed: {e}")
    
    def generate_test_email(self, sender_email: str, recipient_email: str):
        """Generate a test email for SMTP testing"""
        return {
            "username": sender_email,
            "password": "[YOUR_APP_PASSWORD]",
            "recipient": recipient_email,
            "subject": "🧪 Phishy AI SMTP Test Email",
            "body": f"""Hello!

This is a test email from the Phishy AI platform to verify SMTP connectivity.

Test Details:
- Sent from: {sender_email}
- Sent to: {recipient_email}
- Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Platform: Phishy AI Cybersecurity Training

If you received this email, your SMTP configuration is working correctly!

Best regards,
Phishy AI Team""",
            "is_html": False
        }
    
    def run_full_diagnostics(self, email: str, password: str = None, base_url: str = "http://localhost:8080"):
        """Run complete SMTP diagnostics"""
        print("🛡️  PHISHY AI SMTP DIAGNOSTICS")
        print("=" * 60)
        
        # Test 1: Direct SMTP connection
        smtp_success = self.diagnose_smtp_connection(email, password)
        
        # Test 2: Phishy endpoint
        self.test_phishy_smtp_endpoint(base_url)
        
        # Generate test email template
        print("\\n📧 Test Email Template")
        print("=" * 50)
        test_email = self.generate_test_email(email, email)
        print("   Copy this JSON to test email sending:")
        print("   ```json")
        print(json.dumps(test_email, indent=2))
        print("   ```")
        
        # Summary
        print("\\n📋 DIAGNOSTICS SUMMARY")
        print("=" * 50)
        if smtp_success:
            print("   ✅ SMTP connection tests passed")
            print("   ✅ Ready to send emails")
        else:
            print("   ❌ SMTP connection issues detected")
            print("   🔧 Follow the suggested fixes above")
        
        print("\\n🚀 Next Steps:")
        print("   1. Fix any connection issues identified above")
        print("   2. Add SMTP routes to your FastAPI app:")
        print("      load_route_module('smtp_sender', '/smtp', ['📧 SMTP Email'])")
        print("   3. Test sending with: POST /smtp/send-email")
        print("   4. Monitor logs in backend/logs/ for detailed error info")
        
        return smtp_success

def fix_app_routing():
    """Fix the missing SMTP route in app.py"""
    print("🔧 Fixing SMTP Route Registration")
    print("=" * 50)
    
    app_file = "C:\\Users\\thoma\\Desktop\\Phishy\\backend\\app.py"
    
    try:
        with open(app_file, 'r') as f:
            content = f.read()
        
        # Check if SMTP route is already added
        if 'smtp_sender' in content:
            print("   ✅ SMTP sender route already registered")
            return True
        
        # Find the line with email_flagging route and add SMTP after it
        lines = content.split('\\n')
        for i, line in enumerate(lines):
            if 'load_route_module("email_flagging"' in line:
                # Insert SMTP route after email_flagging
                smtp_line = 'load_route_module("smtp_sender", "/smtp", ["📧 SMTP Email Sender"])'
                lines.insert(i + 1, smtp_line)
                
                # Write back to file
                with open(app_file, 'w') as f:
                    f.write('\\n'.join(lines))
                
                print("   ✅ Added SMTP sender route to app.py")
                print("   📝 Added line: " + smtp_line)
                print("   🔄 Restart your backend to apply changes")
                return True
        
        print("   ❌ Could not find email_flagging route to insert after")
        return False
        
    except Exception as e:
        print(f"   ❌ Failed to fix routing: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python fix_smtp_issues.py <email> [password]")
        print("Example: python fix_smtp_issues.py your.email@gmail.com")
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Fix routing first
    fix_app_routing()
    print()
    
    # Run diagnostics
    diagnostics = SMTPDiagnostics()
    diagnostics.run_full_diagnostics(email, password)