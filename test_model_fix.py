#!/usr/bin/env python3
"""
Test the fixed ML model
"""

import sys
import os
sys.path.append("Phishing detection")
from inference import classify_email

# Test emails
test_emails = [
    {
        "name": "Obvious Phishing",
        "content": """Subject: URGENT: Verify Your Account Immediately

Your account has been suspended due to suspicious activity.
Click here to verify your account: http://fake-bank-verification.com/urgent
Please provide your password and social security number.
Act now or your account will be permanently closed!"""
    },
    {
        "name": "Nigerian Prince Scam", 
        "content": """Subject: Urgent Business Proposal

Dear Friend, I am Prince Johnson from Nigeria. I have $10 million to transfer.
Click here immediately: http://bit.ly/nigerian-prince
Provide your bank account details urgently."""
    },
    {
        "name": "Legitimate Email",
        "content": """Subject: Weekly Team Meeting Tomorrow

Hi Team,
Just a reminder about our weekly team meeting tomorrow at 2 PM in the conference room.
Please bring your status updates.
Best, Manager"""
    },
    {
        "name": "Company Newsletter",
        "content": """Subject: Company Newsletter - March 2024

Dear Employees,
Here's our monthly newsletter with company updates and achievements.
Thank you for your continued hard work.
HR Team"""
    }
]

print("="*60)
print("TESTING FIXED ML MODEL")
print("="*60)

for i, email in enumerate(test_emails, 1):
    print(f"\n{i}. Testing: {email['name']}")
    print("-" * 40)
    
    try:
        result = classify_email(email['content'])
        print(f"\nRESULT:\n{result}")
        
        # Check if result makes sense
        is_phishing_expected = "phishing" in email['name'].lower() or "scam" in email['name'].lower()
        is_phishing_detected = "PHISHING" in result.upper()
        
        if is_phishing_expected == is_phishing_detected:
            print("[SUCCESS] CORRECT PREDICTION!")
        else:
            print("[ERROR] WRONG PREDICTION!")
            
    except Exception as e:
        print(f"[ERROR] {e}")
    
    print("=" * 60)

print("\n[COMPLETE] Model testing complete!")