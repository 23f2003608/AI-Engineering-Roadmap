import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

HOMEPAGE = "http://books.toscrape.com"

def get_data(url, categories):
    # 1. Modern Options Setup
    browser_options = Options()
    browser_options.add_argument("--headless") # Updated headless syntax (without UI pop-up)
    # 2. Service Manager Active (No manual path needed)
    driver = webdriver.Chrome(options=browser_options) #Launch a Google Chrome browser that I can control programmatically
    
    driver.get(url)
    driver.implicitly_wait(10) # Global safety net
    
    data = []
    for category in categories:
        # 3. Updated Locating Method (Using By.XPATH)
        # Added quotes around the category variable for valid XPATH syntax
        category_link = driver.find_element(By.XPATH, f"//a[contains(text(), '{category}')]")
        category_link.click()

        try:
            # 4. Explicit Wait to ensure dynamic content is loaded
            books = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.product_pod'))
            )
            
        except Exception as e:
            print(f"Error loading category {category}: {e}")
            continue # Move to next category if one fails

        for book in books:
            # 5. Updated WebElement Actions
            title_el = book.find_element(By.CSS_SELECTOR, "h3 > a")
            price_el = book.find_element(By.CSS_SELECTOR, ".price_color")
            stock_el = book.find_element(By.CSS_SELECTOR, ".instock.availability")
            
            data.append({
                'title': title_el.get_attribute("title"), # Extracting attribute
                'price': price_el.text,                  # Extracting visible text
                'stock': stock_el.text.strip(),          # strip() cleans up whitespace
                'Category': category
            })

        # Return to homepage to pick the next category
        driver.get(url)

    driver.quit()
    return data

def export_csv(data):
    # Using pandas to save data as mentioned in the guide
    df = pd.DataFrame(data)
    df.to_csv("books_exported.csv", index=False)
    print(df)  # DEBUG

def main():
    # You can now easily add more categories here
    data = get_data(url=HOMEPAGE, categories=["Humor", "Art", "Music"])
    export_csv(data)
    print('DONE')

if __name__ == '__main__':
    main()