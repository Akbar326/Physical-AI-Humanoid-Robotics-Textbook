# Test script to verify the RAG chatbot system
import os
import sys
import asyncio
import json
from pathlib import Path

def test_frontend_files():
    """Test that all frontend files exist and are properly structured"""
    print("Testing frontend files...")

    frontend_path = Path("frontend/src")

    # Check if frontend directory exists
    if not frontend_path.exists():
        print("[FAILED] Frontend directory does not exist")
        return False

    # Check for required files
    required_files = ["index.html", "script.js", "styles.css"]
    for file in required_files:
        file_path = frontend_path / file
        if not file_path.exists():
            print(f"[FAILED] {file} does not exist")
            return False
        print(f"[PASSED] {file} exists")

    # Check content of HTML file
    html_file = frontend_path / "index.html"
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    if "<div class=\"chat-container\">" not in html_content:
        print("[FAILED] Chat container not found in HTML")
        return False

    print("[PASSED] HTML structure is correct")
    return True

def test_backend_files():
    """Test that all backend files exist and are properly configured"""
    print("\nTesting backend files...")

    backend_path = Path("backend")

    # Check if backend directory exists
    if not backend_path.exists():
        print("[FAILED] Backend directory does not exist")
        return False

    # Check for main.py
    main_file = backend_path / "main.py"
    if not main_file.exists():
        print("[FAILED] backend/main.py does not exist")
        return False

    # Check content of main.py for StaticFiles import and frontend serving
    with open(main_file, 'r', encoding='utf-8') as f:
        main_content = f.read()

    if "from fastapi.staticfiles import StaticFiles" not in main_content:
        print("[FAILED] StaticFiles import not found in main.py")
        return False

    if "StaticFiles(directory=frontend_path, html=True)" not in main_content:
        print("[FAILED] Frontend serving code not found in main.py")
        return False

    print("[PASSED] Backend configuration is correct")
    return True

def test_environment_variables():
    """Test that required environment variables are documented"""
    print("\nTesting environment variables...")

    env_file = Path("backend/.env")
    if not env_file.exists():
        print("[INFO] .env file does not exist (this is okay for production)")
        return True

    with open(env_file, 'r', encoding='utf-8') as f:
        env_content = f.read()

    required_vars = ["OPENAI_API_KEY", "SITEMAP_URL", "PORT"]
    for var in required_vars:
        if var not in env_content:
            print(f"[INFO] {var} not found in .env file")

    print("[PASSED] Environment variables check completed")
    return True

def test_readme_files():
    """Test that README files are updated"""
    print("\nTesting README files...")

    # Check main README
    main_readme = Path("README.md")
    if not main_readme.exists():
        print("[FAILED] Main README.md does not exist")
        return False

    with open(main_readme, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    if "Frontend-Backend Integration" not in readme_content:
        print("[FAILED] Frontend-Backend Integration section not found in README")
        return False

    # Check frontend README
    frontend_readme = Path("frontend/README.md")
    if not frontend_readme.exists():
        print("[FAILED] Frontend README.md does not exist")
        return False

    print("[PASSED] README files are properly updated")
    return True

def run_all_tests():
    """Run all tests and return overall status"""
    print("Running RAG Chatbot System Tests...\n")

    tests = [
        test_frontend_files(),
        test_backend_files(),
        test_environment_variables(),
        test_readme_files()
    ]

    passed = sum(tests)
    total = len(tests)

    print(f"\nTest Results: {passed}/{total} test groups passed")

    if passed == total:
        print("[SUCCESS] All tests passed! The RAG chatbot system is properly configured.")
        return True
    else:
        print("[ERROR] Some tests failed. Please review the output above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)