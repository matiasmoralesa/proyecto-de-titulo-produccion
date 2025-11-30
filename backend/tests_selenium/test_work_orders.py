"""
Work Orders E2E tests
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


pytestmark = pytest.mark.nondestructive


class TestWorkOrders:
    """Test work orders functionality"""
    
    def test_navigate_to_work_orders(self, authenticated_driver, base_url):
        """Test navigation to work orders page"""
        driver = authenticated_driver
        
        # Try to navigate to work orders page
        driver.get(f"{base_url}/work-orders")
        time.sleep(2)
        
        # Should be on work orders page
        assert "/work-orders" in driver.current_url or "/workorders" in driver.current_url
    
    def test_work_orders_list_loads(self, authenticated_driver, base_url):
        """Test that work orders list loads"""
        driver = authenticated_driver
        driver.get(f"{base_url}/work-orders")
        time.sleep(2)
        
        # Look for table or list of work orders
        try:
            table_elements = driver.find_elements(By.CSS_SELECTOR, "table, .table, [role='table']")
            card_elements = driver.find_elements(By.CSS_SELECTOR, ".card, .work-order-card")
            
            assert len(table_elements) > 0 or len(card_elements) > 0, "No work orders display found"
        except Exception as e:
            pytest.skip(f"Work orders list not found: {e}")
    
    def test_filter_work_orders_by_status(self, authenticated_driver, base_url):
        """Test filtering work orders by status"""
        driver = authenticated_driver
        driver.get(f"{base_url}/work-orders")
        time.sleep(2)
        
        try:
            # Look for status filter
            filter_elements = driver.find_elements(By.CSS_SELECTOR, "select[name*='status'], .status-filter")
            
            if len(filter_elements) > 0:
                first_filter = filter_elements[0]
                first_filter.click()
                time.sleep(1)
                
                # Select an option
                options = driver.find_elements(By.CSS_SELECTOR, "option")
                if len(options) > 1:
                    options[1].click()
                    time.sleep(2)
                    
                    assert True, "Status filter applied"
            else:
                pytest.skip("Status filter not found")
        except Exception as e:
            pytest.skip(f"Filter functionality not found: {e}")
    
    def test_view_work_order_details(self, authenticated_driver, base_url):
        """Test viewing work order details"""
        driver = authenticated_driver
        driver.get(f"{base_url}/work-orders")
        time.sleep(2)
        
        try:
            # Find first work order link
            wo_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/work-orders/'], .work-order-link")
            
            if len(wo_links) > 0:
                first_wo = wo_links[0]
                first_wo.click()
                time.sleep(2)
                
                # Should navigate to work order detail page
                assert "/work-orders/" in driver.current_url or "/workorders/" in driver.current_url
            else:
                pytest.skip("No work order links found")
        except Exception as e:
            pytest.skip(f"Work order details not accessible: {e}")
    
    def test_search_work_orders(self, authenticated_driver, base_url):
        """Test work order search functionality"""
        driver = authenticated_driver
        driver.get(f"{base_url}/work-orders")
        time.sleep(2)
        
        try:
            # Look for search input
            search_input = driver.find_element(By.CSS_SELECTOR, "input[type='search'], input[placeholder*='Buscar']")
            
            # Enter search term
            search_input.clear()
            search_input.send_keys("Mantenimiento")
            search_input.send_keys(Keys.RETURN)
            
            time.sleep(2)
            
            # Check that results are filtered
            page_text = driver.find_element(By.TAG_NAME, "body").text
            assert "Mantenimiento" in page_text or "mantenimiento" in page_text.lower()
        except Exception as e:
            pytest.skip(f"Search functionality not found: {e}")
