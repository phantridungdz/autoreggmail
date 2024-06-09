import time
import uuid
import gspread
import nopecha
import requests
import re
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from oauth2client.service_account import ServiceAccountCredentials
import cloudinary.uploader
from function.daisySms import get_ACCESS_NUMBER
from function.daisySms import getCode
from function.randomstring import randomString
from createProfile import create_profile
from gologin import GoLogin
from function.dongvanfb import readMailDongVan

nopecha.api_key = 'sub_1OztfXCRwBwvt6ptMtRcQc4w'


def upload_cloudinary_image(image):
    unique_public_id = "captcha_" + str(uuid.uuid4())
    cloudinary.config(
        cloud_name="",
        api_key="",
        api_secret=""
    )

    return cloudinary.uploader.upload(image, public_id=unique_public_id)
def sold_image_captcha(captcha_class, driver):
    sleep(3)
    captcha_image_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, captcha_class))
    )
    captcha_image_url = captcha_image_element.get_attribute('src')
    print("URL của hình ảnh captcha:", captcha_image_url)
    response = requests.get(captcha_image_url)
    try:
        if response.status_code == 200:
            captcha_image_path = "captcha_image" + str(uuid.uuid4()) + ".png"
            with open(captcha_image_path, 'wb') as f:
                f.write(response.content)

            public_url = upload_cloudinary_image(captcha_image_path).get('url')

            text = nopecha.Recognition.solve(
                type='textcaptcha',
                image_urls=[public_url],
            )

            print('Capt sold:', text[0])

            captcha_input_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "ca"))
            )
            captcha_input_element.send_keys(text[0])
        else:
            print("Can't load captcha image.")
        next_button_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "identifierNext"))
        )
        next_button_element.click()
    except Exception as e:
        print("Loi load captcha image")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[4]/div[2]/div/div[2]/div[2]/div/span'))
        )
        print("loi, thu lai")
        sold_image_captcha(captcha_class, driver)
    except:
        print('Khong loi')
        return True
def check_captcha_solved(driver):
    start_time = time.time()
    timeout = 5 * 60

    print('check_iframe_disappear')
    try:
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, '//iframe[starts-with(@title, "reCAPTCHA")]'))
        )
    except Exception as e:
        print(f"Error finding iframe: {e}")
        return False

    driver.switch_to.frame(iframe)

    while True:
        current_time = time.time()
        if current_time - start_time > timeout:
            print("Timeout reached. Captcha not solved.")
            driver.switch_to.default_content()
            return False

        try:
            checkedIcons = WebDriverWait(driver, 2).until(
                EC.presence_of_all_elements_located((
                    By.CLASS_NAME, 'recaptcha-checkbox-checked'))
            )
            print("checkedIcons " + str(len(checkedIcons)))
            driver.switch_to.default_content()
            return True
        except Exception as e:
            time.sleep(5)


scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds2.json", scope)

client = gspread.authorize(creds)

googleSheetName = client.open('Data')
sheet = googleSheetName.worksheet('data yahoo')

column = len(sheet.row_values(1))

row = len(sheet.col_values(5))

print('Numer of emails: ' + str(row))

fromNumber = input("Type number start:")

for numberOfRow in range(int(fromNumber), row + 1):

    profileId, first_name, last_name = create_profile(numberOfRow, GoLogin)

    print('Full name: ' + first_name + ' ' + last_name)

    email = sheet.cell(numberOfRow, 5).value
    print('email: ', sheet.cell(numberOfRow, 5).value)
    password = sheet.cell(numberOfRow, 6).value
    print('pass: ', password)
    hotmail = sheet.cell(numberOfRow, 7).value
    hotmail_mail = hotmail.split('|')[0]
    print('hotmail mail: ', hotmail_mail)
    hotmail_pass = hotmail.split('|')[1]
    print('hotmail pass: ', hotmail_pass)
    print('------------------------------Start-------------------------------------')
    gl = GoLogin({
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NjA5MWE2NGZiNmYxZGU5YzhlYzRhMDMiLCJ0eXBlIjoiZGV2Iiwiand0aWQiOiI2NjBkMjkzYTg2OTRkZDU5ODJmNDBlNDAifQ._YA1_ozzYgajQytX3zsb0wYXkJLKwlQn0HPVsWvqU00",
        "profile_id": profileId,
    })
    debugger_address = gl.start()
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", debugger_address)
    service = Service(executable_path='./chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get("http://mail.google.com")

        sleep(3)
        try:
            sigInButton = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//a[starts-with(@data-action, "sign in")]'))
            )
            sigInButton.click()
        except:

            print('Not see sign in button')

        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "identifier"))
        )

        email_input.send_keys(email)
        sleep(1)
        next_button = driver.find_element(By.ID, "identifierNext")

        next_button.click()

        sleep(6)

        try:
            titleBot = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[1]/div/div/div'))
            )
            if titleBot.text == 'Confirm you’re not a robot':
                print('Confirm you’re not a robot')
                sleep(5)

                if check_captcha_solved(driver):
                    next_button = driver.find_element(By.XPATH,
                                                      "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button")
                    next_button.click()
                else:
                    print('Time out 5 ')
            else:
                print('Need captcha image')
                sold_image_captcha("captchaimg", driver)

                next_button = driver.find_element(By.XPATH,
                                                  "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button")
                next_button.click()
                sleep(6)


        except:
            print('nno check bot')
        sleep(10)
        forgotPassword_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "forgotPassword"))
        )

        forgotPassword_element.click()
        sleep(7)
        titleBot = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[1]/div/div/div'))
        )
        if titleBot.text == 'Confirm you’re not a robot':
            print('Confirm you’re not a robot')
            sleep(5)

            if check_captcha_solved(driver):
                next_button = driver.find_element(By.XPATH,
                                                  "/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[3]/div/div[1]/div/div/button")
                next_button.click()



        # forgotPassword_element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.ID, "forgotPassword"))
        # )
        #
        # forgotPassword_element.click()

        sleep(7)
        try:
            currentPass = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//input[starts-with(@aria-label, "Enter last password")]'))
            )
            currentPass.send_keys(password)
        except:
            print('Browser not allow')

        sleep(2)

        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "passwordNext"))
        )

        next_button.click()

        driver.execute_script('''window.open("https://login.yahoo.com/?done=https://mail.yahoo.com%2F&add=1","_blank");''')

        handles = driver.window_handles

        driver.switch_to.window(handles[1])

        sleep(3)

        mail_element =  driver.find_element(By.ID, "login-username")
        mail_element.send_keys(email)

        sleep(1)
        input_id = "browser-fp-data"
        driver.execute_script(f"document.getElementById('{input_id}').value = '';")
        next_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "login-signin"))
        )
        next_button.click()
        sleep(5)

        try:

            login_passwd_element = driver.find_element(By.ID, "login-passwd")

            login_passwd_element.send_keys(password)
        except:
            driver.switch_to.default_content()
            sleep(5)
            try:
                iframe = driver.find_element(By.ID, "recaptcha-iframe")
                driver.switch_to.frame(iframe)
            except Exception as e:
                print(f"Error finding iframe")

            if check_captcha_solved(driver):
                driver.switch_to.default_content()
                iframe = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((
                        By.ID, "recaptcha-iframe")
                    ))
                driver.switch_to.frame(iframe)
                next_button = driver.find_element(By.ID,
                                                  "recaptcha-submit")
                next_button.click()
                driver.switch_to.default_content()
                sleep(5)
                login_passwd_element = WebDriverWait(driver, 8).until(
                    EC.presence_of_element_located((By.ID, "login-passwd"))
                )

                login_passwd_element.send_keys(password)

            else:
                print('Time out 5 ')

        driver.switch_to.default_content()
        sleep(7)
        next_button = driver.find_element(By.ID, "login-signin")

        next_button.click()
        sleep(3)
        try:
            next_button = driver.find_element(By.ID, "login-signin")
            print(next_button.text)
            next_button.click()
        except:
            driver.get('https://mail.yahoo.com')
            print('error click 1')

        sleep(5)
        # cookies = driver.get_cookies()
        # cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        # print(cookie_string)

        try:
            laterbutton = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div[1]/section/div/div[1]/div[2]/button[2]")
            laterbutton.click()
            sleep(3)
        except:
            print('Note see later button')
        mailBox_element = driver.find_element(By.XPATH, '//a[starts-with(@data-test-id, "message-list-item")]')

        print('mailBox_element after login:', mailBox_element.text)

        match = re.search(r'\bverification code is: (\d{6})\b', mailBox_element.text)
        verification_code = ""
        if match:
            verification_code = match.group(1)
            print("Google Verification Code:", verification_code)
        else:
            print("No verification code found.")
        sleep(1)

        driver.switch_to.window(handles[0])
        try:
            titleRecovery = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[3]/div/div/section/header/div/h2/span'))
            )
            print('titleRecovery.text', titleRecovery.text)
            if 'Get a verification code' in titleRecovery.text:
                print('need verify phone')
                sheet.update_cell(numberOfRow, 9, "verify phone")
        except:
            print('need verify phone except')

        codeInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idvPinId"))
        )
        codeInput.send_keys(verification_code)
        sleep(1)
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idvpreregisteredemailNext"))
        )
        next_button.click()
        sleep(6)

        numberPhone = get_ACCESS_NUMBER()
        print("numberPhone: ", numberPhone)

        phoneInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "phoneNumberId"))
        )
        phoneInput.send_keys(numberPhone.split(':')[2])

        sleep(1)

        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idvanyphonecollectNext"))
        )
        next_button.click()

        code = getCode(numberPhone.split(':')[1])

        try:
            codeInput = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "idvAnyPhonePin"))
            )
            codeInput.send_keys(code)

            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "idvanyphoneverifyNext"))
            )
            next_button.click()
            sleep(5)
        except:
            print('Error verify phone')

        sleep(7)
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "next"))
            )
            next_button.click()
        except:
            print('Error click Send')

        titleCodeYahoo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/form/span/section/div/div'))
        )
        print('titleCodeYahoo.text', titleCodeYahoo.text)

        if 'Google will send a verification code to' in titleCodeYahoo.text:
            try:
                driver.switch_to.window(handles[1])
                sleep(3)
                driver.get('https://mail.yahoo.com')
                sleep(5)
                driver.switch_to.default_content()

                mailBox_element = driver.find_element(By.XPATH, '//a[starts-with(@data-test-id, "message-list-item")]')
                print('mailBox_element.text 1234', mailBox_element.text)

                match = re.search(r'\bemail belongs to you. (\d{6})\b', mailBox_element.text)
                verification_code = ""
                if match:
                    verification_code = match.group(1)
                    print("Yahoo Verification Code:", verification_code)
                else:
                    print("No verification code found.")
                driver.switch_to.window(handles[0])
                codeInput = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "verifyAccountPin"))
                )
                codeInput.send_keys(verification_code)

                next_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "next"))
                )
                next_button.click()
                sleep(7)
            except:
                driver.switch_to.window(handles[0])
        try:
            titleChangePass = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '/html/body/div[1]/div[1]/div[2]/div/div/div[1]/div[2]/h1/span'))
            )

            print('titleChangePass', titleChangePass.text)

            if titleChangePass.text != 'Welcome' and titleChangePass.text != 'Change Password':
                try:
                    continueButton = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "/html/body/div[1]/div[1]/div[2]/div/div/div[3]/div/div[1]/div/div/div/a"))
                    )
                    continueButton.click()
                except:

                    print('error click continue')

                try:
                    nextButton = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID,
                                                        "next"))
                    )
                    nextButton.click()
                except:
                    print('error send button')
            else:
                print('No need check')
        except:
            print('No need check')

        sleep(10)
        print('Password typing')
        createPassInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div/div[1]/input"))
        )

        createPassInput.send_keys(password)
        sleep(1)
        confirmPassInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "/html/body/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input"))
        )

        confirmPassInput.send_keys(password)
        sleep(1)
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "changepasswordNext"))
        )
        next_button.click()

        sleep(6)
        driver.get('https://mail.google.com/')

        firstNameInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "FirstName"))
        )
        firstNameInput.clear()
        firstNameInput.send_keys(first_name)

        LastnameInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "LastName"))
        )
        LastnameInput.clear()
        LastnameInput.send_keys(last_name)

        hotmailInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "GmailAddress"))
        )
        new_mail = hotmail_mail.split('@')[0] + randomString()
        print("New mail:", new_mail)
        sheet.update_cell(numberOfRow, 11, new_mail + "@gmail.com")
        hotmailInput.send_keys(new_mail)

        recoveryMailInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "RecoveryEmailAddress"))
        )
        recoveryMailInput.clear()
        recoveryMailInput.send_keys(hotmail_mail)

        sleep(1)

        submitButton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "submitbutton"))
        )
        submitButton.click()

        sleep(5)

        phoneInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "signupidvinput"))
        )
        phoneInput.send_keys(numberPhone.split(':')[2])

        continueButton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "next-button"))
        )
        continueButton.click()
        sleep(4)
        sheet.update_cell(numberOfRow, 10, numberPhone.split(':')[2])
        code = getCode(numberPhone.split(':')[1])

        codeInput = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "verify-phone-input"))
        )
        codeInput.send_keys(code)

        continueButton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "VerifyPhone"))
        )
        continueButton.click()

        sleep(5)
        try:
            titleAllowSmart = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '/html/body/div[23]/div[2]/div/div[1]/div[2]'))
            )

            print('Allow smart', titleAllowSmart.text)

            if 'Allow smart features in Gmail' in titleAllowSmart.text:
                turnOffRatio = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                                                    "/html/body/div[23]/div[2]/div/div[2]/div[3]/label/span"))
                )

                turnOffRatio.click()

                nextBtn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME,
                                                    "data_consent_dialog_next"))
                )

                nextBtn.click()
                sleep(1)

                turnOffBtn = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME,
                                                    "turn_off_in_product"))
                )

                turnOffBtn.click()

                sleep(4)

                driver.refresh()

                sleep(5)


        except:
            print('no need Allow smart')

        driver.get(
            'https://myaccount.google.com/recovery/email?continue=https%3A%2F%2Fmyaccount.google.com%2Femail%3Fhl%3Den&hl=en')
        try:
            titleToContinue = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div/form/span/section[1]/div/div/div'))
            )

            print('To continue', titleToContinue.text)

            if 'To continue, first verify ' in titleToContinue.text:
                confirmPassInput = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.NAME,
                                                    "Passwd"))
                )

                confirmPassInput.send_keys(password)

                next_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "passwordNext"))
                )

                next_button.click()
        except:
            print('errooo21')

        sleep(4)
        nextBtn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '/html/body/c-wiz/div/div[2]/div[2]/c-wiz/div[1]/div[4]/div/form/div/div[2]/div[2]/div/button'))
        )
        nextBtn.click()
        sleep(5)
        try:
            message = readMailDongVan(hotmail_mail, hotmail_pass)

            print('Message:', message)

            match = re.search(r'\bthis recovery email:(\d{6})\b', message)
            verification_code = ""
            if match:
                verification_code = match.group(1)
                print("Yahoo Verification Code:", verification_code)
                codeInput = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        '/html/body/div[13]/div[2]/div/div[1]/div/div[1]/div[2]/div/div/label/input'))
                )
                nextBtn.send_keys(verification_code)
            else:
                print("No verification code found.")
        except:
            print('errodajksd')
        sleep(2)

        driver.get("https://policies.google.com/terms?hl=en-US")
        sleep(4)
        version_country = driver.find_element(By.XPATH, '//a[starts-with(@data-name, "country-version")]')
        sheet.update_cell(numberOfRow, 9, version_country.text)

    except:
        print('error unknow')
        sheet.update_cell(numberOfRow, 9, "Error Unknow")
        gl.stop()
        driver.quit()

