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
main_url = "https://blume.vc/startups"
driver.get(main_url)

# Wait for the page to load completely
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[@data-highlight-term]"))
)

# Scroll to load all data (if the page has infinite scroll)
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.implicitly_wait(scroll_pause_time)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Find all company names and construct their URLs
elements = driver.find_elements(By.XPATH, "//div[@data-highlight-term]")
company_names = [element.get_attribute("data-highlight-term") for element in elements]
company_urls = [f"https://blume.vc/{'-'.join(name.lower().split())}" for name in company_names]

# Prepare data collection
data = []
print(len(company_urls))
# Visit each company's page to retrieve details
for company_name, company_url in zip(company_names, company_urls):
    driver.get(company_url)
    try:
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@href and contains(@class, 'hover:no-underline')]"))
        )
        
        # Get the company website
        company_website_element = driver.find_element(By.XPATH, "//a[@href and contains(@class, 'hover:no-underline')]")
        company_website = company_website_element.get_attribute("href")
        
        # Get the founder LinkedIn ID
        founder_elements = driver.find_elements(By.XPATH, "//ul[contains(@class, 'font-title')]//a[@href and contains(@href, 'linkedin')]")
        founders = [founder.get_attribute("href") for founder in founder_elements]
    except Exception as e:
        # Handle missing data
        company_website = None
        founders = []

    # Append to the data
    data.append({
        "Company Name": company_name,
        "Company URL": company_url,
        "Company Website": company_website,
        "Founders": ", ".join(founders)
    })

# Save the data to a DataFrame and Excel
df = pd.DataFrame(data)
df.to_excel('blume_vc_startups.xlsx', index=False)

# Print completion message
print("Data saved to blume_vc_startups.xlsx")

# Close the browser
driver.quit()
