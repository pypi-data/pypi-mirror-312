from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from dataclasses import dataclass
import time
import re

@dataclass
class Prediction:
    chance: float
    message: str
    date: datetime.datetime

    @property
    def formatted_chance(self):
        return f"{self.chance}%"

def predict(zipcode: str) -> Prediction:
    """Get snow day prediction for a given ZIP code."""
    if not (isinstance(zipcode, str) and len(zipcode) == 5 and zipcode.isdigit()):
        raise ValueError("ZIP code must be a 5-digit string")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        url = f"https://snowdaypredictor.com/result/{zipcode}"
        driver.get(url)
        
        time.sleep(2)
        
        wait = WebDriverWait(driver, 10)
        percentage_div = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "percentage"))
        )
        
        try:
            odometer = percentage_div.find_element(By.CLASS_NAME, "odometer-value")
            chance = float(odometer.text)
        except:
            try:
                odometer_values = percentage_div.find_elements(By.CLASS_NAME, "odometer-value")
                visible_values = [v for v in odometer_values if v.is_displayed()]
                if visible_values:
                    chance = float(visible_values[-1].text)
                else:
                    raise ValueError("No visible odometer values found")
            except:
                raw_text = percentage_div.text
                numbers = re.findall(r'\d+', raw_text)
                if numbers:
                    chance = float(numbers[0])
                else:
                    raise ValueError("Could not find prediction value")
        
        try:
            below_text = percentage_div.find_element(By.CLASS_NAME, "below-text")
            message = below_text.text.strip()
        except:
            message = "Chance of a snow day"
        
        prediction_date = datetime.datetime.today() + datetime.timedelta(days=1)
        
        return Prediction(
            chance=chance,
            message=message,
            date=prediction_date
        )
    finally:
        driver.quit() 