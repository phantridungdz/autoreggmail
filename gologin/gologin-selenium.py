import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gologin import GoLogin
from selenium.webdriver.chrome.service import Service

gl = GoLogin({
	"token": "",
	"profile_id": "",
})

service = Service(executable_path='./chromedriver.exe')

debugger_address = gl.start()
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", debugger_address)
driver = webdriver.Chrome(service=service, options=chrome_options)

profile_info = gl.getProfile("660e8a8527a1a317499ed247")

print(profile_info)

driver.get("http://www.python.org")
assert "Python" in driver.title
time.sleep(3)
driver.quit()
time.sleep(3)
gl.stop()
