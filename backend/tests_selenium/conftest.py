"""
Pytest configuration for Selenium tests
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application"""
    return "http://localhost:5173"


@pytest.fixture(scope="session")
def api_url():
    """API URL for the backend"""
    return "http://localhost:8000"


@pytest.fixture(scope="function")
def driver():
    """Create and configure Chrome WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Create driver - force win64 architecture
    import platform
    arch = "win64" if platform.machine().endswith('64') else "win32"
    service = Service(ChromeDriverManager(driver_version="latest", os_type=arch).install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    
    yield driver
    
    # Cleanup
    driver.quit()


@pytest.fixture(scope="function")
def authenticated_driver(driver, base_url):
    """Create an authenticated driver session"""
    # Navigate to login page
    driver.get(f"{base_url}/login")
    time.sleep(2)
    
    # Perform login
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    # Wait for login form
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    password_input = driver.find_element(By.NAME, "password")
    
    # Enter credentials
    username_input.send_keys("admin")
    password_input.send_keys("admin123")
    
    # Submit form
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    login_button.click()
    
    # Wait for redirect to dashboard
    WebDriverWait(driver, 10).until(
        EC.url_contains("/dashboard")
    )
    
    time.sleep(2)
    
    return driver


@pytest.fixture(scope="function")
def test_user_credentials():
    """Test user credentials"""
    return {
        "admin": {"username": "admin", "password": "admin123"},
        "supervisor": {"username": "supervisor", "password": "super123"},
        "operator": {"username": "operator1", "password": "oper123"}
    }
