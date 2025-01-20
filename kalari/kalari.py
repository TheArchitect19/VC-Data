from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Set up the WebDriver
service = Service('/usr/local/bin/chromedriver/chromedriver')  # Update the path to your ChromeDriver
driver = webdriver.Chrome(service=service)

# Open the main page
main_url = "https://kalaari.com/portfolio/"
driver.get(main_url)

# Wait for the page to load completely
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/portfolio/')]"))
)

# Find all company URLs
company_url_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/portfolio/')]")
company_urls = [element.get_attribute("href") for element in company_url_elements]

# Prepare data collection
data = []

# Visit each company's page to retrieve details
for company_url in company_urls:
    driver.get(company_url)
    try:
        # Wait for the founders' LinkedIn links to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, 'linkedin.com')]"))
        )
        
        # Get the founders' LinkedIn links
        founder_elements = driver.find_elements(By.XPATH, "//a[contains(@href, 'linkedin.com')]")
        founders = [founder.get_attribute("href") for founder in founder_elements]
    except Exception as e:
        # Handle missing data
        founders = []

    # Extract company name from the URL (last part of the URL)
    company_name = company_url.rstrip('/').split('/')[-1].replace('-', ' ').title()

    # Append to the data
    data.append({
        "Company Name": company_name,
        "Company URL": company_url,
        "Founders": ", ".join(founders)
    })

# Save the data to a DataFrame and Excel
df = pd.DataFrame(data)
df.to_excel('./kalaari_portfolio_startups.xlsx', index=False)

# Print completion message
print("Data saved to kalaari_portfolio_startups.xlsx")

# Close the browser
driver.quit()
