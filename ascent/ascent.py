from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set up WebDriver
service = Service('/usr/local/bin/chromedriver/chromedriver')  # Update with your ChromeDriver path
driver = webdriver.Chrome(service=service)

# Open the Ascent Capital portfolio page
url = "https://ascentcapital.in/portfolio"
driver.get(url)

# Wait for portfolio items to load
wait = WebDriverWait(driver, 10)
portfolio_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.each-col")))

# Prepare data collection
data = []

# Process each portfolio item
for item in portfolio_items:
    try:
        # Click on the portfolio item to open the popup
        item.click()

        # Wait for the popup to load
        time.sleep(3)  # Adding a longer wait to ensure the popup has time to load

        # Extract company name
        try:
            company_name = driver.find_element(By.CSS_SELECTOR, "h2").text
        except Exception:
            company_name = "N/A"

        # Extract founder name
        try:
            # Explicitly waiting for the founder field to be visible
            founder_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'founder')]/following-sibling::div//p"))
            )
            founder = founder_element.text
        except Exception:
            founder = "N/A"

        # Extract website URL
        try:
            # Explicitly waiting for the website field to be visible
            website_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(),'website')]/following-sibling::div//p/a"))
            )
            website = website_element.get_attribute("href")
        except Exception:
            website = "N/A"

        # Append the data
        data.append({
            "Company Name": company_name,
            "Founder": founder,
            "Website": website
        })

        # Close the popup by clicking the close button
        try:
            close_button = driver.find_element(By.CSS_SELECTOR, "div.close")
            close_button.click()
            time.sleep(1)  # Allow the popup to close before moving on
        except Exception:
            print("Close button not found")

        print(f"Processed: {company_name}")
    except Exception as e:
        print(f"Error processing item: {e}")

# Save data to Excel
df = pd.DataFrame(data)
df.to_excel('ascentcapital_portfolio.xlsx', index=False)

# Print completion message
print("Data saved to ascentcapital_portfolio.xlsx")

# Close the browser
driver.quit()
