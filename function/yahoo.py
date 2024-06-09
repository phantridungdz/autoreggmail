import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium_stealth import stealth
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random

def loginYahoo():

    urlLinkedin = "https://www.google.com/"
    email = "monkeyface_18@yahoo.com"
    password = "Matkhau123!@#"

    def get_random_name():
        response = requests.get("https://randomuser.me/api/")
        if response.status_code == 200:
            data = response.json()
            first_name = data['results'][0]['name']['first']
            last_name = data['results'][0]['name']['last']
            return first_name, last_name
        else:
            return "DefaultFirstName", "DefaultLastName"

    def random_proxy_choice():
        proxies = [
            "hyperion.p.shifter.io:17010",
            "hyperion.p.shifter.io:17011",
            "hyperion.p.shifter.io:17012",
            "hyperion.p.shifter.io:17013",
            "hyperion.p.shifter.io:17014"
        ]
        return random.choice(proxies)

    def create_driver_with_profile(profile_path, proxy):
        options = ChromeOptions()
        # options.add_extension('ext.crx')
        options.add_extension('fingerprint.crx')
        options.add_extension('webRTC.crx')
        options.add_extension('captcha.crx')

        # options.add_argument("--headless")
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument(f"user-data-dir={profile_path}")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        print("Proxy use:", proxy)
        options.add_argument('--proxy-server=%s' % proxy)

        driver = webdriver.Chrome(options=options)
        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )
        driver.get(urlLinkedin)
        return driver

    proxy = random_proxy_choice()
    first_name, last_name = get_random_name()
    profile_path = fr"C:\Users\PC\AppData\Local\Google\Chrome\User Data\{first_name}-{last_name}"

    driver = create_driver_with_profile(profile_path, proxy)

    driver.get("http://mail.google.com")

    sleep(10)
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "identifier"))
    )

    email_input.send_keys(email)

    next_button = driver.find_element(By.ID, "identifierNext")

    next_button.click()
    sleep(2)

    sleep(100)




