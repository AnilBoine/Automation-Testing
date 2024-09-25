from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def initialize_driver(browser_name):
    if browser_name.lower() == 'chrome':
        options = webdriver.ChromeOptions()
        return webdriver.Chrome(options=options)
    elif browser_name.lower() == 'firefox':
        options = webdriver.FirefoxOptions()
        return webdriver.Firefox(options=options)
    elif browser_name.lower() == 'edge':
        options = webdriver.EdgeOptions()
        return webdriver.Edge(options=options)
    else:
        raise ValueError("Unsupported browser! Please choose 'chrome' or 'firefox' or 'edge'.")

# Specify the browser you want to use
browser_name = 'chrome'  # Change to 'firefox' or 'chrome' or 'edge'
driver = initialize_driver(browser_name)

# Maximize the browser window
driver.maximize_window()

# Clear cookies
driver.delete_all_cookies()

try:
    # Navigate to Amazon
    driver.get("https://www.amazon.in")
    time.sleep(4)  

    # Search for a product
    search_box = driver.find_element(By.ID, "twotabsearchtextbox")
    search_box.send_keys("watches")
    search_box.send_keys(Keys.RETURN)

    # Apply filters 
    time.sleep(4)  # Wait for results to load
    display_filter = driver.find_element(By.XPATH, "//span[text()='Analogue']")
    display_filter.click()
    time.sleep(4) # Wait for the filter to apply
    print("filter 1")
    discount_filter = driver.find_element(By.XPATH, "//span[text()='10% Off or more']")
    discount_filter.click()
    time.sleep(4) # Wait for the filter to apply
    print("filter 2")
    material_filter = driver.find_element(By.XPATH, "//span[text()='Leather']")
    material_filter.click()
    
    time.sleep(4)  # Wait for the filter to apply
    print("filter 3")
    
   # Select the product from the filtered results
    first_product = driver.find_element(By.XPATH, "//*[@id='search']/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/div/div/span/div/div/div[2]/div[1]/h2/a/span")
    
    # Wait for the anchor tag to be present
    anchor = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='search']/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/div/div/span/div/div/div[2]/div[1]/h2/a")) 
    )

    # Extract the href attribute
    href_value = anchor.get_attribute("href")
    first_product.click()
 
    time.sleep(4)  # Wait for the product page to load
    print("product selected")
    driver.switch_to.window(driver.window_handles[1])

    # navigate to URL
    driver.get(href_value)
    time.sleep(4) 
    # Add the product 
    add_to_cart_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[5]/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/div[4]/div/div[1]/div/div/div/form/div/div/div/div/div[4]/div/div[38]/div[1]/span/span/span/input")
    add_to_cart_button.click()

    print("add cart")
    
    
    try:
        skip = driver.find_element(By.XPATH, "/html/body/div[8]/div[3]/div[1]/div/div/div[2]/div[2]/div/div/div[3]/div/span[2]/span/input")
        skip.click()
    except NoSuchElementException:
        pass

    time.sleep(6)

    # Navigate to the cart
    cart_link = driver.find_element(By.XPATH, "//*[@id='nav-cart-count']")
    cart_link.click()
    print("view cart")

    time.sleep(6)  # Wait for the cart page to load

    product_title = driver.find_element(By.XPATH, "//span[contains(@class, 'a-truncate-cut')]").text

    print("Product added to cart successfully:", product_title)


except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the driver
    print("Testing Close")
    driver.quit()
