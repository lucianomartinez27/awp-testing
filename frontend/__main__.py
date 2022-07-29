from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from pages.login_page import LoginPage
from pages.new_order_page import NewOrderPage
from pages.payment_section import PaymentSection
import unittest



def login_test(driver):
	login_page = LoginPage.for_seller(driver, 'http://localhost:5001')
	login_page.open()
	login_page.login()
	assert login_page.is_logged_in()
	login_page.logout()
	assert login_page.is_logged_out()
	login_page.quit()

def new_order_test(driver):
	new_order_page = NewOrderPage(driver, 'http://localhost:5001')
	new_order_page.open()
	new_order_page.select_adventure_gym_category()
	new_order_page.select_a3_model()
	new_order_page.go_to_payment(mulch=False)

def payment_test(driver, downpayment=0):
	payment_options = {'payment_method': 'RTO', 'mulch': False, 'tax_exempt': False, 'down_payment': downpayment}
	payment_section = PaymentSection(driver, 'http://localhost:5001', payment_options)
	payment_section.open()
	payment_section.fill_payment()

class TestPayment(unittest.TestCase):
	def setUp(self):
		service = ChromeService(executable_path=ChromeDriverManager().install())
		options = webdriver.ChromeOptions()
		options.add_argument("--start-maximized")
		self.driver = webdriver.Chrome(service=service, options=options)
		self.driver.implicitly_wait(30)
	
	def tearDown(self):
		self.driver.quit()
		
	def test_payment_RTO_with_downpayment(self):
		payment_options = {'payment_method': 'RTO', 'mulch': False, 'tax_exempt': False, 'down_payment': 100}
		payment_section = PaymentSection(self.driver, 'http://localhost:5001', payment_options)
		payment_section.open()
		payment_section.fill_payment()

		self.assertEqual(payment_section.rent_to_own_total(), '$60.25')
		self.assertEqual(payment_section.rent_to_own_tax(), '$3.77')
		self.assertEqual(payment_section.rent_to_own_total_with_tax(), '$64.02')
	
	def test_payment_RTO_without_downpayment(self):
		payment_options = {'payment_method': 'RTO', 'mulch': False, 'tax_exempt': False, 'down_payment': 0}
		payment_section = PaymentSection(self.driver, 'http://localhost:5001', payment_options)
		payment_section.open()
		payment_section.fill_payment()

		self.assertEqual(payment_section.rent_to_own_total(), '$65.00')
		self.assertEqual(payment_section.rent_to_own_tax(), '$4.06')
		self.assertEqual(payment_section.rent_to_own_total_with_tax(), '$69.06')
  
if __name__ == '__main__':
	unittest.main()