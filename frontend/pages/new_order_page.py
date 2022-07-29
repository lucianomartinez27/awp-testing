from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from .login_page import LoginPage
from selenium.webdriver.support.select import Select

from selenium.webdriver.support import expected_conditions as EC


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

	def select_colors(self, category, color):
		element = self.driver.find_element(By.ID, category)
		select = Select(element)
		select.select_by_visible_text(color)
	
	def click_on(self, elementID):
		# we have to scroll to the element, otherwise it will not be clickable
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		element = WebDriverWait(self.driver, 10).until(
    EC.element_to_be_clickable((By.ID, elementID)))
		element.click()

	def go_to_payment(self, mulch=False):
		self.select_all_colors()
		self.click_on('ctrlTree') # next button
		self.click_on('ctrlFour') # next button

		if not mulch:
			self.click_on('mulch2')
		else:
			self.select_mulch()
		self.click_on('ctrlFive') # next button

	def select_all_colors(self):
			self.select_colors('frame', 'WHITE')
			self.select_colors('brackets', 'RED')
			self.select_colors('swingColor', 'BLUE')
			self.select_colors('slideColor', 'BLUE')
	
	def select_mulch(self):
		raise NotImplementedError("Purchases with mulch are not implemented yet")