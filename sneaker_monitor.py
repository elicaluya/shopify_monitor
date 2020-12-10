import requests
import json
import time

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def availabilityCheck():
	r = requests.get('https://shop-usa.palaceskateboards.com/products.json')
	products = json.loads((r.text))['products']

	for product in products:
		product_name = product['title']

		if product_name == "P-FLAMES HOOD GREY MARL":
			print("Found Item: " + product_name)
			product_url = "https://shop-usa.palaceskateboards.com/products/" + product['handle']
			return product_url
	return False



def buyProduct(url):
	options = Options()
	options.add_experimental_option("detach", True)
	driver = webdriver.Chrome(chrome_options=options, executable_path = r'C:\Users\elica\eclipse-workspace\SeleniumFramework\ChromeDriver\chromedriver.exe')
	

	driver.get(url)

	# selecting item on product page
	driver.find_element_by_xpath("//select/option[@value='32653913129053']").click()
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



myUrl = availabilityCheck()
if myUrl != False:
	buyProduct(myUrl)
else:
	print("Not Available")