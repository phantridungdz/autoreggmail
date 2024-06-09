import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gologin import GoLogin
from selenium.webdriver.chrome.service import Service

gl = GoLogin({
	"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NjA5MWE2NGZiNmYxZGU5YzhlYzRhMDMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NjBkMjkzYTg2OTRkZDU5ODJmNDBlNDAifQ._YA1_ozzYgajQytX3zsb0wYXkJLKwlQn0HPVsWvqU00",
	"profile_id": "660e8a8527a1a317499ed247",
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
