from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configure Chrome options


# Set up WebDriver
service = Service('/usr/local/bin/chromedriver/chromedriver')  # Update ChromeDriver path
driver = webdriver.Chrome(service=service)

# Open the website
main_url = "https://www.chiratae.com/companies/"
driver.get(main_url)

# Wait for the page to load
wait = WebDriverWait(driver, 20)

# Find all company blocks
try:
    company_blocks = wait.until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "card-item"))
    )
except Exception as e:
    print(f"Error waiting for company blocks: {e}")
    driver.quit()
    exit()

# Prepare data collection
data = []

for block in company_blocks:
    try:
        # Extract company name
        company_name = block.find_element(By.CLASS_NAME, "card-title").text

        # Extract social media links
        social_media_elements = block.find_elements(By.CLASS_NAME, "social-media-icons-item")
        social_media_links = [social.get_attribute("href") for social in social_media_elements]

        # Append data
        data.append({
            "Company Name": company_name,
            "Social Media Profiles": ", ".join(social_media_links)
        })
    except Exception as e:
        print(f"Error processing block: {e}")

# Save data to Excel
df = pd.DataFrame(data)
df.to_excel('chiratae_companies_social_profiles.xlsx', index=False)

print("Data saved to chiratae_companies_social_profiles.xlsx")
driver.quit()
