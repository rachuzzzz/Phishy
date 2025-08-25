#!/usr/bin/env python3
"""
Simple test to verify LLM is working
"""
import sys
import os
sys.path.append('backend')

# Test Ollama LLM directly
from langchain_ollama import OllamaLLM

def test_ollama():
    try:
        print("Testing Ollama connection...")
        llm = OllamaLLM(
            model="phi3:mini", 
            base_url="http://localhost:11434",
            timeout=15,
            temperature=0.3,
            num_predict=200
        )
        
        print("Testing LLM response...")
        response = llm.invoke("Hello, what is the current security status? Please provide a brief professional response.")
        print(f"LLM Response: {response}")
        print("✅ LLM is working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ LLM test failed: {e}")
        return False

def test_mock_llm():
    """Test the mock LLM fallback"""
    print("\nTesting Mock LLM...")
    sys.path.append('backend/routes')
    from admin_assistant import FastMockLLM
    
    mock_llm = FastMockLLM()
    response = mock_llm.invoke({"user_query": "What is the security status?", "analysis_data": "No data"})
    print(f"Mock LLM Response: {response}")
    print("✅ Mock LLM is working!")
    return True

if __name__ == "__main__":
    print("=== LLM Testing ===")
    
    # Test Ollama first
    ollama_works = test_ollama()
    
    # Test Mock LLM
    mock_works = test_mock_llm()
    
    if ollama_works:
        print("\n🎉 Ollama LLM is ready for use!")
    elif mock_works:
        print("\n⚠️  Using Mock LLM fallback (Ollama not available)")
    else:
        print("\n❌ Both LLM and Mock failed!")