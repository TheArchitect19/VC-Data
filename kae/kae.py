from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Configure Chrome options

# Set up WebDriver
service = Service('/usr/local/bin/chromedriver/chromedriver')  # Update ChromeDriver path
driver = webdriver.Chrome(service=service)

# Open the main page
main_url = "https://kae-capital.com/investments/"
driver.get(main_url)

# Wait for the page to load
wait = WebDriverWait(driver, 20)

# Find all company links
try:
    company_links = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/investments/')]"))
    )
except Exception as e:
    print(f"Error finding company links: {e}")
    driver.quit()
    exit()

# Extract unique company URLs
company_urls = list(set([link.get_attribute("href") for link in company_links]))

# Prepare data collection
data = []

# Visit each company page and extract details
for url in company_urls:
    driver.get(url)
    time.sleep(2)  # Allow the page to load completely

    try:
        # Extract company name
        company_name = driver.find_element(By.XPATH, "//h1").text

        # Extract founder names and their LinkedIn profiles
        founders = []
        founder_elements = driver.find_elements(By.XPATH, "//a[contains(@class, 'invest_founders')]")
        for founder in founder_elements:
            founder_name = founder.text.strip()
            founder_linkedin = founder.get_attribute("href")
            founders.append(f"{founder_name} ({founder_linkedin})")

        # Extract company website
        try:
            company_website = driver.find_element(By.XPATH, "//a[contains(@href, 'http') and text()='Website']").get_attribute("href")
        except:
            company_website = "N/A"

        # Append data
        data.append({
            "Company Name": company_name,
            "Founders": "; ".join(founders),
            "Company Website": company_website,
        })

    except Exception as e:
        print(f"Error processing URL {url}: {e}")

# Save data to Excel
df = pd.DataFrame(data)
df.to_excel('kae_capital_investments.xlsx', index=False)

print("Data saved to kae_capital_investments.xlsx")
driver.quit()
