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

# Open the portfolio page
url = "https://www.3one4capital.com/portfolio"
driver.get(url)

# Wait for portfolio items to load
wait = WebDriverWait(driver, 10)
portfolio_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='listitem'] a.pc-card")))

# Collect all portfolio links
links = [item.get_attribute("href") for item in portfolio_items]

# Prepare data collection
data = []

# Process each portfolio link
for link in links:
    try:
        # Navigate to the detail page
        driver.get(link)
        time.sleep(2)  # Allow the detail page to load

        # Extract company name
        try:
            company_name = driver.find_element(By.CSS_SELECTOR, "h1.h1").text
        except Exception:
            company_name = "N/A"

        # Extract founder or social profiles
        try:
            # Company website
            website = driver.find_element(
                By.XPATH, "//a[contains(@href, 'http') and contains(@class, 'pc-social-link')]"
            ).get_attribute("href")
        except Exception:
            website = "N/A"

        try:
            # LinkedIn profile
            linkedin = driver.find_element(
                By.XPATH, "//a[contains(@href, 'linkedin.com') and contains(@class, 'pc-social-link')]"
            ).get_attribute("href")
        except Exception:
            linkedin = "N/A"

        # Append the data
        data.append({
            "Company Name": company_name,
            "Website": website,
            "LinkedIn": linkedin,
            "Detail Page Link": link
        })

        print(f"Processed: {company_name}")
    except Exception as e:
        print(f"Error processing link {link}: {e}")

# Save data to Excel
df = pd.DataFrame(data)
df.to_excel('3one4capital_portfolio.xlsx', index=False)

# Print completion message
print("Data saved to 3one4capital_portfolio.xlsx")

# Close the browser
driver.quit()
