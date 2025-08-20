"""
Setup and run the comprehensive testing system
"""

import os
import sys
import subprocess
import asyncio

def check_environment():
    """Check if the environment is ready for testing"""
    print("🔍 Checking test environment...")
    
    issues = []
    
    # Check if server is running
    try:
        import requests
        response = requests.get("http://localhost:8008/health", timeout=5)
        if response.status_code == 200:
            print("✅ API server is running")
        else:
            issues.append("❌ API server returned non-200 status")
    except Exception as e:
        issues.append(f"❌ Cannot connect to API server: {e}")
    
    # Check OpenAI API key
    if os.getenv('OPENAI_API_KEY'):
        print("✅ OpenAI API key is set")
    else:
        print("⚠️ OpenAI API key not set - AI analysis will be skipped")
    
    # Check Python packages
    required_packages = ['requests', 'openai']
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} package available")
        except ImportError:
            issues.append(f"❌ Missing required package: {package}")
    
    return issues

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    packages = ['requests', 'openai']
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")

async def run_tests():
    """Run the comprehensive test suite"""
    print("🚀 Starting comprehensive test suite...")
    
    try:
        from run_comprehensive_test import ComprehensiveTestRunner
        
        runner = ComprehensiveTestRunner()
        report = await runner.run_full_test_suite()
        
        return report
        
    except Exception as e:
        print(f"❌ Test suite failed: {e}")
        return None

def main():
    """Main setup and execution function"""
    print("🧪 Tidal Streamline Comprehensive Testing System")
    print("=" * 50)
    
    # Check environment
    issues = check_environment()
    
    if issues:
        print("\\n🔧 Environment Issues Found:")
        for issue in issues:
            print(f"  {issue}")
        
        # Try to fix package issues
        if any("Missing required package" in issue for issue in issues):
            response = input("\\n🛠️ Install missing packages? (y/n): ")
            if response.lower() == 'y':
                install_requirements()
                # Re-check
                issues = check_environment()
        
        # Check if critical issues remain
        critical_issues = [i for i in issues if "API server" in i or "Missing required package" in i]
        if critical_issues:
            print("\\n❌ Critical issues prevent testing:")
            for issue in critical_issues:
                print(f"  {issue}")
            print("\\nPlease resolve these issues and try again.")
            return
    
    print("\\n✅ Environment ready for testing!")
    
    # Ask for confirmation
    response = input("\\n🚀 Run comprehensive test suite? This will test all 12 role categories (y/n): ")
    if response.lower() != 'y':
        print("Test cancelled.")
        return
    
    # Set OpenAI key if not set
    if not os.getenv('OPENAI_API_KEY'):
        key = input("\\n🔑 Enter OpenAI API key for AI analysis (or press Enter to skip): ")
        if key.strip():
            os.environ['OPENAI_API_KEY'] = key.strip()
    
    # Run the tests
    asyncio.run(run_tests())

if __name__ == "__main__":
    main()