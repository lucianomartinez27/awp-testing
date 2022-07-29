from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from pages.login_page import LoginPage
from pages.new_order_page import NewOrderPage
from pages.payment_section import PaymentSection

service = ChromeService(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

def login_test():
	login_page = LoginPage.for_seller(driver, 'http://localhost:5001')
	login_page.open()
	login_page.login()
	assert login_page.is_logged_in()
	login_page.logout()
	assert login_page.is_logged_out()
	login_page.quit()

def new_order_test():
	new_order_page = NewOrderPage(driver, 'http://localhost:5001')
	new_order_page.open()
	new_order_page.select_adventure_gym_category()
	new_order_page.select_a3_model()
	new_order_page.go_to_payment(mulch=False)

def payment_test():
	payment_options = {'payment_method': 'RTO', 'mulch': False, 'tax_exempt': False, 'down_payment': 100}
	payment_section = PaymentSection(driver, 'http://localhost:5001', payment_options)
	payment_section.open()
	payment_section.fill_payment()


if __name__ == '__main__':
	try:	
		payment_test()
	except Exception as e:
		print(e)
		driver.quit()
		raise e