from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from pages.login_page import LoginPage
from pages.new_order_page import NewOrderPage
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

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


if __name__ == '__main__':
		new_order_test()