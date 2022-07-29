from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from .common import Page

from .new_order_page import NewOrderPage

class PaymentSection(Page):
	def __init__(self, driver, url, options=None):
		super().__init__(driver, url)
		self.driver = driver
		self.url = url
		self.new_order_page = NewOrderPage(driver, url)
		self.options = self.get_options(options)

	def open(self):
		self.new_order_page.open()
		self.new_order_page.select_adventure_gym_category()
		self.new_order_page.select_a3_model()
		self.new_order_page.go_to_payment(mulch=self.mulch)
	
	def quit(self):
		self.new_order_page.quit()

	def get_options(self, options):
		if options is None:
			return self.options
		else:
			self.payment_method = 'payment2' if 'RTO' ==  options['payment_method'] else 'payment1'
			self.mulch = True if 'mulch' == options['mulch'] else False
			self.tax_exempt = 'tax1' if 'tax_exempt' == options['tax_exempt'] else 'tax2'
			self.down_payment = options['down_payment'] if 'down_payment' in options else 0
	
	def fill_payment(self):
		self.new_order_page.click_on(self.payment_method)
		self.click_on(self.tax_exempt)
		self.set_down_payment()
		self.select_payment()

	def set_down_payment(self):
		down_payment_input = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'costreduc')))
		down_payment_input.clear()
		down_payment_input.send_keys(self.down_payment)

	def select_payment(self):
		element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'selmethodp')))
		select = Select(element)
		select.select_by_value('1')

	def rent_to_own_total(self):
		return self.driver.find_element(By.ID, 'renToOwn').text
	
	def rent_to_own_tax(self):
		return self.driver.find_element(By.ID, 'taxRen').text
	
	def rent_to_own_total_with_tax(self):
		return self.driver.find_element(By.ID, 'totRen').text
	
	def return_awp_playset_price(self):
		return self.driver.execute_script("return awp_playset_price;")