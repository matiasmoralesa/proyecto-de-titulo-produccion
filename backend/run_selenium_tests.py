"""
Script to run Selenium E2E tests
"""
import subprocess
import sys
import time
import requests
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)


def print_header(text):
    """Print colored header"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{text:^60}")
    print(f"{Fore.CYAN}{'='*60}\n")


def print_success(text):
    """Print success message"""
    print(f"{Fore.GREEN}✓ {text}")


def print_error(text):
    """Print error message"""
    print(f"{Fore.RED}✗ {text}")


def print_warning(text):
    """Print warning message"""
    print(f"{Fore.YELLOW}⚠ {text}")


def print_info(text):
    """Print info message"""
    print(f"{Fore.BLUE}ℹ {text}")


def check_service(url, name):
    """Check if a service is running"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code < 500:
            print_success(f"{name} is running at {url}")
            return True
    except requests.exceptions.RequestException:
        pass
    
    print_error(f"{name} is not running at {url}")
    return False


def check_dependencies():
    """Check if required dependencies are installed"""
    print_header("Checking Dependencies")
    
    try:
        import selenium
        print_success(f"Selenium {selenium.__version__} installed")
    except ImportError:
        print_error("Selenium not installed")
        print_info("Run: pip install -r requirements-test.txt")
        return False
    
    try:
        import webdriver_manager
        print_success("webdriver-manager installed")
    except ImportError:
        print_error("webdriver-manager not installed")
        print_info("Run: pip install -r requirements-test.txt")
        return False
    
    try:
        import pytest
        print_success(f"pytest installed")
    except ImportError:
        print_error("pytest not installed")
        print_info("Run: pip install pytest")
        return False
    
    return True


def check_services():
    """Check if backend and frontend are running"""
    print_header("Checking Services")
    
    backend_running = check_service("http://localhost:8000/api/v1/", "Backend")
    frontend_running = check_service("http://localhost:5173/", "Frontend")
    
    if not backend_running:
        print_warning("Backend is not running. Start it with:")
        print_info("  cd backend && python manage.py runserver")
    
    if not frontend_running:
        print_warning("Frontend is not running. Start it with:")
        print_info("  cd frontend && npm run dev")
    
    return backend_running and frontend_running


def run_tests(test_path=None, verbose=True, headless=True):
    """Run Selenium tests"""
    print_header("Running Selenium Tests")
    
    cmd = ["pytest", "tests_selenium/"]
    
    if test_path:
        cmd = ["pytest", test_path]
    
    if verbose:
        cmd.append("-v")
    
    cmd.extend(["--tb=short", "--color=yes"])
    
    print_info(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, cwd=".", check=False)
        return result.returncode == 0
    except KeyboardInterrupt:
        print_warning("\nTests interrupted by user")
        return False
    except Exception as e:
        print_error(f"Error running tests: {e}")
        return False


def main():
    """Main function"""
    print_header("CMMS Selenium E2E Test Runner")
    
    # Check dependencies
    if not check_dependencies():
        print_error("Missing dependencies. Please install them first.")
        sys.exit(1)
    
    # Check services
    services_ok = check_services()
    
    if not services_ok:
        print_warning("\nServices are not running. Tests may fail.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print_info("Exiting. Please start the services and try again.")
            sys.exit(1)
    
    # Parse command line arguments
    test_path = None
    if len(sys.argv) > 1:
        test_path = sys.argv[1]
        print_info(f"Running specific test: {test_path}")
    
    # Run tests
    success = run_tests(test_path)
    
    # Print summary
    print_header("Test Summary")
    
    if success:
        print_success("All tests passed!")
        sys.exit(0)
    else:
        print_error("Some tests failed. Check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_warning("\n\nTest runner interrupted by user")
        sys.exit(1)
