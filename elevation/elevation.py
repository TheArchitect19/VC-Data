from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


# Set up WebDriver
service = Service('/usr/local/bin/chromedriver/chromedriver')  # Update the ChromeDriver path
driver = webdriver.Chrome(service=service)

# Open the portfolio page
url = "https://elevationcapital.com/portfolio"
driver.get(url)

# Wait for the page to load and portfolio items to become visible
wait = WebDriverWait(driver, 10)
portfolio_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.relative a[href]")))

# Collect the links for all portfolio items
links = [item.get_attribute("href") for item in portfolio_items]

# Prepare data collection
data = []

# Iterate over each link
for link in links:
    try:
        # Navigate to the detail page
        driver.get(link)
        time.sleep(2)  # Allow the detail page to load

        # Extract company name
        try:
            company_name = driver.find_element(By.CSS_SELECTOR, "div.h6, div.h4").text
        except Exception:
            company_name = "N/A"

        # Extract founder name
        try:
            founder_element = driver.find_element(
                By.XPATH,
                "//div[contains(@class, 'border-b')]//span[contains(text(), 'Company Founders')]/following-sibling::span",
            )
            founder_name = founder_element.text.strip()
        except Exception:
            founder_name = "N/A"

        # Append the data
        data.append({
            "Company Name": company_name,
            "Founder Name": founder_name,
            "Detail Page Link": link
        })

        print(f"Processed: {company_name}")
    except Exception as e:
        print(f"Error processing link {link}: {e}")

# Save data to Excel
df = pd.DataFrame(data)
df.to_excel('elevationcapital_portfolio.xlsx', index=False)

# Print completion message
print("Data saved to elevationcapital_portfolio.xlsx")

# Close the browser
driver.quit()
