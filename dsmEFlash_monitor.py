import requests
import json
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys


def availabilityCheck(name):
	r = requests.get('https://eflash-us.doverstreetmarket.com/products.json?limit=150')
	products = json.loads((r.text))['products']

	for product in products:
		product_name = product['title']
		if name in product_name:
			product_url = "https://eflash-us.doverstreetmarket.com/products/" + product['handle']
			return product_url
	return False



def buyProduct(url, info, size):
	options = Options()
	options.add_experimental_option("detach", True)
	driver = webdriver.Chrome(chrome_options=options, executable_path = r'C:\Users\elica\eclipse-workspace\SeleniumFramework\ChromeDriver\chromedriver.exe')
	

	driver.get(url)

	# selecting item on product page
	sizeString = "//select/option[text()='" + size + "']"
	driver.find_element_by_xpath(sizeString).click()
	driver.find_element_by_xpath("//button[@class='btn product-form__cart-submit']").click()

	# On cart page
	driver.find_element_by_xpath("//input[@class='btn btn--small-wide']").click()

	# On checkout page
	driver.find_element_by_xpath("//input[@placeholder='Email']").send_keys(info['personal']['email'])
	driver.find_element_by_xpath("//input[@placeholder='First name (optional)']").send_keys(info['personal']['firstName'])
	driver.find_element_by_xpath("//input[@placeholder='Last name']").send_keys(info['personal']['lastName'])
	driver.find_element_by_xpath("//input[@placeholder='Address']").send_keys(info['address']['street'])
	driver.find_element_by_xpath("//input[@placeholder='Apartment, suite, etc. (optional)']").send_keys(info['address']['address2'])
	driver.find_element_by_xpath("//input[@placeholder='City']").send_keys(info['address']['city'])
	countryString = "//select[@id='checkout_shipping_address_country']/option[text()='" + info['address']['country'] + "']"
	driver.find_element_by_xpath(countryString).click()
	stateString = "//select[@id='checkout_shipping_address_province']/option[text()='" + info['address']['state'] + "']"
	driver.find_element_by_xpath(stateString).click()
	driver.find_element_by_xpath("//input[@placeholder='ZIP code']").send_keys(info['address']['zip'])
	driver.find_element_by_xpath("//input[@placeholder='Phone']").send_keys(info['personal']['phone'])

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

	# On shipping price page
	wait.until(EC.presence_of_element_located((By.XPATH, "//button[@name='button']"))).click()

	# Switch to individual iframes for each section and fill out info
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id^='card-fields-number-']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='number']"))).send_keys(info['payment']['card1'])
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='number']"))).send_keys(info['payment']['card2'])
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='number']"))).send_keys(info['payment']['card3'])
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='number']"))).send_keys(info['payment']['card4'])

	driver.switch_to.default_content()
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id^='card-fields-name-']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='name']"))).send_keys(info['payment']['name'])

	driver.switch_to.default_content()
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id^='card-fields-expiry-']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='expiry']"))).send_keys(info['payment']['exMonth'])
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='expiry']"))).send_keys(info['payment']['exYear'])

	driver.switch_to.default_content()
	WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[id^='card-fields-verification_value-']")))
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='verification_value']"))).send_keys(info['payment']['vCode'])

	# Submit order
	driver.switch_to.default_content()
	WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@id='continue_button']"))).click()



with open('info/product_info.json') as product_json:
	product_info = json.load(product_json)

with open('info/user_info.json') as user_json:
	user_info = json.load(user_json)

pName = product_info['product_name']
pSize = product_info['size']


myUrl = availabilityCheck(pName)
while True:
	if myUrl != False:
		print("Attempting to purchase product")
		buyProduct(myUrl, user_info, pSize)
		break
	else:
		print("Product Not Available")
		time.sleep(4)