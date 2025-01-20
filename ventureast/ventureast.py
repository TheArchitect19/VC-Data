from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time



# Set up WebDriver
service = Service('/usr/local/bin/chromedriver/chromedriver')  # Update the ChromeDriver path
driver = webdriver.Chrome(service=service)

# Open the portfolio page
url = "https://www.ventureast.net/portfolio"
driver.get(url)

# Allow the page to load
time.sleep(5)

# Find all company blocks
company_blocks = driver.find_elements(By.CSS_SELECTOR, "div[role='listitem'].item")

# Prepare data collection
data = []

# Extract company name and website from each block
for block in company_blocks:
    try:
        # Extract company name
        company_name = block.find_element(By.CSS_SELECTOR, ".title-link").text

        # Extract company website
        company_website = block.find_element(By.CSS_SELECTOR, ".title-link").get_attribute("href")

        # Append the data
        data.append({
            "Company Name": company_name,
            "Website": company_website
        })
    except Exception as e:
        print(f"Error processing block: {e}")

# Save data to Excel
df = pd.DataFrame(data)
df.to_excel('ventureast_portfolio.xlsx', index=False)

# Print completion message
print("Data saved to ventureast_portfolio.xlsx")

# Close the browser
driver.quit()
