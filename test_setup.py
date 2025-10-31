#!/usr/bin/env python3
"""
Test script voor HotelProfessionals Chatbot
Run dit script om te controleren of alles correct is geconfigureerd.
"""

import os
import sys
import requests
import time

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def test_environment():
    """Test of environment variables correct zijn ingesteld"""
    print_header("Testing Environment Variables")
    
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if api_key:
        print_success(f"PERPLEXITY_API_KEY is set (length: {len(api_key)})")
        if len(api_key) < 20:
            print_error("API key lijkt te kort. Controleer of deze correct is.")
            return False
        return True
    else:
        print_error("PERPLEXITY_API_KEY is not set!")
        print_info("Maak een .env bestand aan met: PERPLEXITY_API_KEY=your_key_here")
        return False

def test_dependencies():
    """Test of alle dependencies geïnstalleerd zijn"""
    print_header("Testing Dependencies")
    
    required_packages = ["fastapi", "uvicorn", "requests"]
    all_installed = True
    
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package} is installed")
        except ImportError:
            print_error(f"{package} is NOT installed")
            all_installed = False
    
    if not all_installed:
        print_info("Run: pip install -r requirements.txt")
    
    return all_installed

def test_server():
    """Test of de server draait en reageert"""
    print_header("Testing Server")
    
    base_url = "http://127.0.0.1:8000"
    
    print_info("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_success(f"Server is running! Response: {data}")
        else:
            print_error(f"Server responded with status {response.status_code}")
            return False
    except requests.ConnectionError:
        print_error("Cannot connect to server!")
        print_info("Zorg dat de server draait: python main.py")
        return False
    except Exception as e:
        print_error(f"Error connecting to server: {e}")
        return False
    
    print_info("Testing session creation...")
    try:
        response = requests.post(f"{base_url}/new_session", timeout=5)
        if response.status_code == 200:
            data = response.json()
            session_id = data.get("session_id")
            print_success(f"Session created: {session_id}")
            
            # Test met een vraag
            print_info("Testing chat endpoint...")
            test_question = "Welke vacatures zijn er?"
            response = requests.get(
                f"{base_url}/ask",
                params={"question": test_question, "session_id": session_id},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "")
                print_success("Chat endpoint works!")
                print_info(f"Question: {test_question}")
                print_info(f"Answer preview: {answer[:100]}...")
                
                # Test session deletion
                print_info("Testing session deletion...")
                response = requests.delete(f"{base_url}/session/{session_id}", timeout=5)
                if response.status_code == 200:
                    print_success("Session deletion works!")
                else:
                    print_error(f"Session deletion failed with status {response.status_code}")
                
                return True
            else:
                print_error(f"Chat endpoint failed with status {response.status_code}")
                print_info(f"Response: {response.text}")
                return False
        else:
            print_error(f"Session creation failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error during testing: {e}")
        return False

def main():
    print_header("HotelProfessionals Chatbot - Setup Test")
    print("Dit script test of alles correct is geconfigureerd\n")
    
    # Test 1: Environment variables
    env_ok = test_environment()
    
    # Test 2: Dependencies
    deps_ok = test_dependencies()
    
    # Only test server if environment and deps are OK
    if env_ok and deps_ok:
        print_info("\nStart de server in een apart terminal venster als deze nog niet draait:")
        print_info("  python main.py")
        print_info("\nDruk op Enter om door te gaan met server testing...")
        input()
        
        server_ok = test_server()
    else:
        print_error("\nLos eerst de environment en dependency problemen op!")
        server_ok = False
    
    # Final summary
    print_header("Test Summary")
    
    if env_ok and deps_ok and server_ok:
        print_success("Alle tests geslaagd! Je bent klaar om te deployen. 🚀")
        print_info("\nVolgende stappen:")
        print_info("1. Push naar GitHub: git push origin main")
        print_info("2. Deploy naar Railway")
        print_info("3. Voeg PERPLEXITY_API_KEY toe in Railway environment variables")
        print_info("4. Update API_BASE_URL in index.html met je Railway URL")
        return 0
    else:
        print_error("Sommige tests zijn mislukt. Los de problemen op en probeer opnieuw.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
