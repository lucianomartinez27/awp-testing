from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from .login_page import LoginPage


class NewOrderPage:
	def __init__(self, driver, url):
		self.driver = driver
		self.url = url
		self.login_page = LoginPage.for_seller(driver, url)

	def open(self):
		self.login_page.open()
		self.login_page.login()
		WebDriverWait(self.driver, 5).until(
			lambda d: d.find_element(By.CLASS_NAME, 'men-ope').is_displayed()
		)
		self.driver.get(self.url + '/neworder')

	def quit(self):
		self.driver.quit()
	
	def select_adventure_gym_category(self):
		adventure_gym_xpath = (By.XPATH, '//*[@id="one"]/div[2]/div/div[1]/div/div/a')
		self.driver.find_element(*adventure_gym_xpath).click()
	
	def select_a3_model(self):
		a3_model_xpath = (By.XPATH, '//*[@id="two"]/div/div/div[1]/div/div/a')
		self.driver.find_element(*a3_model_xpath).click()