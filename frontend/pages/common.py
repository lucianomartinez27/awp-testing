from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Page:
	def __init__(self, driver, url):
		self.driver = driver
		self.url = url
	
	def click_on(self, elementID):
		# we have to scroll to the element, otherwise it will not be clickable
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		element = self.driver.find_element(By.ID, elementID)
		self.driver.execute_script("arguments[0].click();", element)


	def wait(self):
		return WebDriverWait(self.driver, 5)