import requests
import json

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def availabilityCheck():
	r = requests.get('https://shop-usa.palaceskateboards.com/products.json')
	products = json.loads((r.text))['products']

	for product in products:
		product_name = product['title']
		if product_name == "DOMINATOR PERFORMANCE JACKET JUNGLE DPM":
			product_url = "https://shop-usa.palaceskateboards.com/products/" + product['handle']
			return product_url

	return False


driver = webdriver.Chrome(executable_path = r'C:\Users\elica\eclipse-workspace\SeleniumFramework\ChromeDriver\chromedriver.exe')

driver.get('https://shop-usa.palaceskateboards.com/products/f0epjdj4n3lr')
driver.find_element_by_xpath("//select/option[@value='35703051014']").click()
driver.find_element_by_xpath("//input[@class='add cart-btn clearfix']").click()

driver.implicitly_wait(10)
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[@class='cart-heading']"))).click()

driver.find_element_by_xpath("//a[@class='cart-heading']").click()
driver.find_element_by_xpath("//input[@class='checkbox-input']").click()
driver.find_element_by_xpath("//input[@class='shopping-btn']").click()