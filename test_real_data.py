#!/usr/bin/env python3
"""
Test the real data loader
"""
import sys
import os
sys.path.append('backend')

from routes.admin_assistant import load_comprehensive_real_data, prepare_comprehensive_data_summary

def test_data_loader():
    print("Testing real data loader...")
    
    # Test comprehensive data loading
    real_data = load_comprehensive_real_data()
    print("\nReal data loaded:")
    for key, value in real_data.items():
        if key == 'user_details':
            print(f"  {key}: {len(value)} users")
            for email, details in list(value.items())[:2]:  # Show first 2 users
                print(f"    {email}: {details['clicks']} clicks, last seen {details['last_seen'][:10]}")
        elif key == 'flagged_email_details':
            print(f"  {key}: {len(value)} flagged emails")
            for email in value[:2]:  # Show first 2
                print(f"    From: {email['sender']}, Subject: {email['subject'][:30]}...")
        else:
            print(f"  {key}: {value}")
    
    # Test data summary
    print("\n" + "="*60)
    print("Testing comprehensive data summary:")
    print("="*60)
    summary = prepare_comprehensive_data_summary("What is the security status?")
    print(summary)

if __name__ == "__main__":
    test_data_loader()