from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
			self.mulch = options['mulch']
			self.tax_exempt = 'tax1' if options['tax_exempt'] else 'tax2'
			self.down_payment = options['down_payment'] if 'down_payment' in options else 0
	
	def fill_payment(self):
		self.click_on(self.payment_method)
		self.click_on(self.tax_exempt)
		self.set_down_payment()
		self.select_payment()

	def set_down_payment(self):
		raise NotImplementedError("Sublcass reponsability")

	def select_payment(self):
		element = self.wait().until(EC.element_to_be_clickable((By.ID, 'selmethodp')))
		select = Select(element)
		select.select_by_value('1')

	def rent_to_own_total(self):
		return self.driver.find_element(By.ID, 'renToOwn').text
	
	def rent_to_own_tax(self):
		return self.driver.find_element(By.ID, 'taxRen').text
	
	def rent_to_own_total_with_tax(self):
		return self.driver.find_element(By.ID, 'totRen').text
	
	def cash_tax(self):
		return self.driver.find_element(By.ID, 'tax').text
	
	def is_tax_exempt(self):
		return \
		(self.cash_tax() == '$0.00' or self.cash_tax() == '$0') or \
		(self.rent_to_own_tax() == '$0.00' or self.rent_to_own_tax() == '$0')
		
	def get_awp_global_variables(self):
		return self.driver.execute_script("""
			return {
				awp_playset_price: parseFloat(awp_playset_price),
				awp_total_cash: parseFloat(awp_total_cash),
				awp_ren_to_own: parseFloat(awp_ren_to_own),
				awp_total_ren: parseFloat(awp_total_ren),
				awp_tax_men: parseFloat(awp_tax_men),
				awp_totalMulchPrice: parseFloat(awp_totalMulchPrice)
				};
		""")

class CashPaymentSection(PaymentSection):

	def __init__(self, driver, url, options):
		super().__init__(driver, url, options)
		self.payment_method = 'payment1'

	def set_down_payment(self):
		pass

class RTOPaymentSection(PaymentSection):
	def __init__(self, driver, url, options):
		super().__init__(driver, url, options)
		self.payment_method = 'payment2'

	def set_down_payment(self):
		down_payment_input = self.wait().until(EC.element_to_be_clickable((By.ID, 'costreduc')))
		self.driver.execute_script("arguments[0].value = '%s';" % self.down_payment, down_payment_input)
		self.driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", down_payment_input)