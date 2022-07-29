from selenium.webdriver.common.by import By
from .common import Page

class LoginPage(Page):
	def __init__(self, driver, url, username, password) -> None:
		super().__init__(driver, url)
		self.driver = driver
		self.url = url
		self.username = username
		self.password = password
	
	@classmethod
	def for_seller(cls, driver, url):
		return LoginPage(driver, url, 'robertoseller', '9123')
	
	def open(self):
		self.driver.get(self.url)
	
	def quit(self):
		self.driver.quit()
	
	def login(self):
		self.driver.find_element(By.ID, 'username').send_keys(self.username)
		self.driver.find_element(By.ID, 'password').send_keys(self.password)
		self.click_on('sesion')

	def logout(self):
		self.driver.get(self.url + '/logout')

	def is_logged_in(self):
		return self.wait().until(
			lambda d: d.find_element(By.CLASS_NAME, 'perfil').is_displayed()
		)
	
	def is_logged_out(self):
		return self.wait().until(
			lambda d: d.find_element(By.ID, 'sesion').is_displayed()
		)