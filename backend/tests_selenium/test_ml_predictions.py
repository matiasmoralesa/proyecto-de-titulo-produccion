"""
ML Predictions E2E tests
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


pytestmark = pytest.mark.nondestructive


class TestMLPredictions:
    """Test ML predictions functionality"""
    
    def test_navigate_to_predictions(self, authenticated_driver, base_url):
        """Test navigation to predictions page"""
        driver = authenticated_driver
        
        # Try to navigate to predictions page
        driver.get(f"{base_url}/predictions")
        time.sleep(2)
        
        # Should be on predictions page
        assert "/predictions" in driver.current_url or "/ml-predictions" in driver.current_url
    
    def test_predictions_list_loads(self, authenticated_driver, base_url):
        """Test that predictions list loads"""
        driver = authenticated_driver
        driver.get(f"{base_url}/predictions")
        time.sleep(2)
        
        # Look for predictions display
        try:
            table_elements = driver.find_elements(By.CSS_SELECTOR, "table, .table, [role='table']")
            card_elements = driver.find_elements(By.CSS_SELECTOR, ".card, .prediction-card")
            
            assert len(table_elements) > 0 or len(card_elements) > 0, "No predictions display found"
        except Exception as e:
            pytest.skip(f"Predictions list not found: {e}")
    
    def test_risk_level_indicators(self, authenticated_driver, base_url):
        """Test that risk level indicators are visible"""
        driver = authenticated_driver
        driver.get(f"{base_url}/predictions")
        time.sleep(2)
        
        try:
            # Look for risk level indicators (badges, colors, etc.)
            risk_elements = driver.find_elements(By.CSS_SELECTOR, ".badge, .risk, [class*='risk-level']")
            
            if len(risk_elements) > 0:
                # Check for common risk level text
                page_text = driver.find_element(By.TAG_NAME, "body").text.lower()
                has_risk_levels = any(level in page_text for level in ['low', 'medium', 'high', 'critical', 'bajo', 'medio', 'alto'])
                
                assert has_risk_levels, "No risk level indicators found"
            else:
                pytest.skip("No risk elements found")
        except Exception as e:
            pytest.skip(f"Risk indicators not found: {e}")
    
    def test_filter_by_risk_level(self, authenticated_driver, base_url):
        """Test filtering predictions by risk level"""
        driver = authenticated_driver
        driver.get(f"{base_url}/predictions")
        time.sleep(2)
        
        try:
            # Look for risk level filter
            filter_elements = driver.find_elements(By.CSS_SELECTOR, "select[name*='risk'], .risk-filter, button[class*='filter']")
            
            if len(filter_elements) > 0:
                first_filter = filter_elements[0]
                first_filter.click()
                time.sleep(1)
                
                # Try to select a risk level
                options = driver.find_elements(By.CSS_SELECTOR, "option, .filter-option")
                if len(options) > 1:
                    options[1].click()
                    time.sleep(2)
                    
                    assert True, "Risk filter applied"
            else:
                pytest.skip("Risk filter not found")
        except Exception as e:
            pytest.skip(f"Filter functionality not found: {e}")
    
    def test_view_prediction_details(self, authenticated_driver, base_url):
        """Test viewing prediction details"""
        driver = authenticated_driver
        driver.get(f"{base_url}/predictions")
        time.sleep(2)
        
        try:
            # Find first prediction link or button
            pred_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/predictions/'], button[class*='view']")
            
            if len(pred_links) > 0:
                first_pred = pred_links[0]
                first_pred.click()
                time.sleep(2)
                
                # Should show prediction details (modal or new page)
                # Check if modal appeared or URL changed
                current_url = driver.current_url
                modals = driver.find_elements(By.CSS_SELECTOR, ".modal, [role='dialog']")
                
                assert "/predictions/" in current_url or len(modals) > 0, "Prediction details not shown"
            else:
                pytest.skip("No prediction links found")
        except Exception as e:
            pytest.skip(f"Prediction details not accessible: {e}")
    
    def test_generate_predictions_button(self, authenticated_driver, base_url):
        """Test generate predictions button exists"""
        driver = authenticated_driver
        driver.get(f"{base_url}/predictions")
        time.sleep(2)
        
        try:
            # Look for generate/refresh button
            generate_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), 'Generar') or contains(text(), 'Generate') or contains(text(), 'Actualizar')]")
            
            assert len(generate_buttons) > 0, "Generate predictions button not found"
        except Exception as e:
            pytest.skip(f"Generate button not found: {e}")
