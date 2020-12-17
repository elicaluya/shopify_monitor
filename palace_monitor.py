import requests
import json
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def availabilityCheck():
	r = requests.get('https://shop-usa.palaceskateboards.com/products.json?limit=150')
	products = json.loads((r.text))['products']

	for product in products:
		product_name = product['title']
		if product_name == "P-FLAMES HOOD GREY MARL":
			product_url = "https://shop-usa.palaceskateboards.com/products/" + product['handle']
			return product_url
	return False



def buyProduct(url):
	options = Options()
	options.add_experimental_option("detach", True)
	driver = webdriver.Chrome(chrome_options=options, executable_path = r'C:\Users\elica\eclipse-workspace\SeleniumFramework\ChromeDriver\chromedriver.exe')
	

	driver.get(url)

	# selecting item on product page
	driver.find_element_by_xpath("//select/option[@value='32653913096285']").click()
	driver.find_element_by_xpath("//input[@class='add cart-btn clearfix']").click()
	driver.implicitly_wait(10)
	driver.find_element_by_xpath("//a[@class='cart-heading']").click()

	# On cart page
	checkbox = driver.find_element_by_xpath("//input[@class='checkbox-input']")
	driver.execute_script("arguments[0].click();", checkbox)
	driver.find_element_by_xpath("//input[@class='shopping-btn']").click()

	# On checkout page
	driver.find_element_by_xpath("//input[@placeholder='Email']").send_keys("example@gmail.com")
	driver.find_element_by_xpath("//input[@placeholder='First name']").send_keys("Joe")
	driver.find_element_by_xpath("//input[@placeholder='Last name']").send_keys("Mama")
	driver.find_element_by_xpath("//input[@placeholder='Address']").send_keys("123 First st.")
	driver.find_element_by_xpath("//input[@placeholder='Apartment, suite, etc. (optional)']").send_keys("Apt. A")
	driver.find_element_by_xpath("//input[@placeholder='City']").send_keys("Dublin")
	driver.find_element_by_xpath("//select[@id='checkout_shipping_address_country']/option[text()='United States']").click()
	driver.find_element_by_xpath("//select[@id='checkout_shipping_address_province']/option[text()='California']").click()
	driver.find_element_by_xpath("//input[@placeholder='ZIP code']").send_keys("94568")
	driver.find_element_by_xpath("//input[@placeholder='Phone']").send_keys("1234567891")

	# Switch to Captcha iframe
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']"))).click()
	wait = WebDriverWait(driver,120)

	# Wait until captcha is solved before moving forward
	try:
		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[aria-checked="true"]')))
	except TimeoutException:
		print("Failed to solve captcha in time")
	else:
		print("Successfully completed captcha")
		driver.switch_to.default_content()

	
	wait.until(EC.presence_of_element_located((By.XPATH, "//button[@name='button']"))).click()

	wait.until(EC.presence_of_element_located((By.XPATH, "//button[@name='button']"))).click()

	# Switch to individual iframes for each section and fill out info
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id^='card-fields-number-']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='number']"))).send_keys("1234")
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='number']"))).send_keys("1234")
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='number']"))).send_keys("1234")
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='number']"))).send_keys("1234")

	driver.switch_to.default_content()
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id^='card-fields-name-']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='name']"))).send_keys("Joe Mama")

	driver.switch_to.default_content()
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id^='card-fields-expiry-']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='expiry']"))).send_keys("12")
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='expiry']"))).send_keys("34")

	driver.switch_to.default_content()
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id^='card-fields-verification_value-']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='verification_value']"))).send_keys("123")

	# Submit order
	driver.switch_to.default_content()
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@name='button']"))).click()



myUrl = availabilityCheck()
if myUrl != False:
	print("Attempting to purchase product")
	buyProduct(myUrl)
else:
	print("Product Not Available")