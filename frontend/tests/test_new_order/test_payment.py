from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from pages.payment_section import CashPaymentSection, RTOPaymentSection
import unittest


class TestPayment(unittest.TestCase):

	def setUp(self):
		service = ChromeService(executable_path=ChromeDriverManager().install())
		options = webdriver.ChromeOptions()
		options.add_argument("--start-maximized")
		self.driver = webdriver.Chrome(service=service, options=options)
		self.driver.implicitly_wait(30)
	
	def tearDown(self):
		self.driver.quit()
	
	def test_cash_with_mulch_and_tax(self):
		payment_options = {'mulch': True, 'tax_exempt': False}
		payment_section = CashPaymentSection(self.driver, 'http://localhost:5001', payment_options)
		payment_section.open()
		payment_section.fill_payment()
		global_variables = payment_section.get_awp_global_variables()
		self.assertAlmostEqual(global_variables['awp_totalMulchPrice'], 1511, delta=1)
		self.assertAlmostEqual(global_variables['awp_playset_price'], 1287, delta=1)
		total_cash = 2972 #  total_mulch + playset_price + tax
		self.assertAlmostEqual(global_variables['awp_total_cash'], total_cash , delta=1)

	def test_payment_CASH_without_mulch_and_with_tax(self):
		payment_options = {'mulch': False, 'tax_exempt': False}
		payment_section = CashPaymentSection(self.driver, 'http://localhost:5001', payment_options)
		payment_section.open()
		payment_section.fill_payment()
		self.assertEqual(payment_section.cash_tax(), '$80.44')
	
	def test_payment_CASH_without_mulch_tax_exempt(self):
		payment_options = {'mulch': False, 'tax_exempt': True}
		payment_section = CashPaymentSection(self.driver, 'http://localhost:5001', payment_options)
		payment_section.open()
		payment_section.fill_payment()
		self.assertTrue(payment_section.is_tax_exempt())
		
	def test_payment_RTO_without_mulch_with_downpayment(self):
		payment_options = {'mulch': False, 'tax_exempt': True, 'down_payment': 100}
		payment_section = RTOPaymentSection(self.driver, 'http://localhost:5001', payment_options)
		payment_section.open()
		payment_section.fill_payment()
		global_variables = payment_section.get_awp_global_variables()
		self.assertAlmostEqual(global_variables['awp_tax_men'], 0, delta=0.1)
		self.assertAlmostEqual(global_variables['awp_ren_to_own'], 60, delta=1)
		self.assertAlmostEqual(global_variables['awp_total_ren'], 60, delta=1)
		self.assertTrue(payment_section.is_tax_exempt())

	
	def test_payment_RTO_withour_mulch_without_downpayment(self):
		payment_options = {'mulch': False, 'tax_exempt': False, 'down_payment': 0}
		payment_section = RTOPaymentSection(self.driver, 'http://localhost:5001', payment_options)
		payment_section.open()
		payment_section.fill_payment()
		global_variables = payment_section.get_awp_global_variables()
		self.assertAlmostEqual(global_variables['awp_total_cash'], global_variables['awp_totalMulchPrice'])
		self.assertAlmostEqual(global_variables['awp_ren_to_own'], 65, delta=0.1)
		self.assertAlmostEqual(global_variables['awp_tax_men'], 4, delta=0.1)
		self.assertAlmostEqual(global_variables['awp_total_ren'], 70, delta=1)
		self.assertAlmostEqual(global_variables['awp_totalMulchPrice'], 0, delta=0.1)
	
	def test_payment_RTO_with_mulch(self):
		payment_options = {'mulch': True, 'tax_exempt': False}
		payment_section = RTOPaymentSection(self.driver, 'http://localhost:5001', payment_options)
		payment_section.open()
		payment_section.fill_payment()
		global_variables = payment_section.get_awp_global_variables()
		self.assertAlmostEqual(global_variables['awp_totalMulchPrice'], 1511, delta=1)
		self.assertAlmostEqual(global_variables['awp_ren_to_own'], 65, delta=0.1)
		self.assertAlmostEqual(global_variables['awp_tax_men'], 4, delta=0.1)
		self.assertAlmostEqual(global_variables['awp_total_ren'], 70, delta=1)
		
	def test_payment_RTO_with_mulch_with_downpayment(self):
		base_down_payment = 1605
		payment_options = {'mulch': True, 'tax_exempt': False, 'down_payment': base_down_payment + 100}
		payment_section = RTOPaymentSection(self.driver, 'http://localhost:5001', payment_options)
		payment_section.open()
		payment_section.fill_payment()
		global_variables = payment_section.get_awp_global_variables()
		self.assertAlmostEqual(global_variables['awp_totalMulchPrice'], 1511, delta=1)
		self.assertAlmostEqual(global_variables['awp_ren_to_own'], 60, delta=1)
		self.assertAlmostEqual(global_variables['awp_tax_men'], 4, delta=1)
		self.assertAlmostEqual(global_variables['awp_total_ren'], 64, delta=1)
	