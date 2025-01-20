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

# Open the Axilor portfolio page
url = "https://www.axilor.com/portfolio/"
driver.get(url)

# Wait for portfolio items to load
wait = WebDriverWait(driver, 10)
portfolio_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li a.box-link")))

# Collect all portfolio links
links = [item.get_attribute("href") for item in portfolio_items]

# Prepare data collection
data = []

# Append the links to the data
for link in links:
    data.append({"Company Link": link})

# Save data to Excel
df = pd.DataFrame(data)
df.to_excel('axilor_portfolio_links.xlsx', index=False)

# Print completion message
print("Data saved to axilor_portfolio_links.xlsx")

# Close the browser
driver.quit()
