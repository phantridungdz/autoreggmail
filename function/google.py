import random
import uuid
from time import sleep
import nopecha
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from function.cloudinaryd import upload_cloudinary_image

def safe_find_element_by_id(driver, element_id):
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, element_id))
        )
        return element
    except:
        return None
def safe_find_element_by_class(driver, element_class):
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, element_class))
        )
        return element
    except:
        return None
def safe_find_element_by_xpath(driver, element_xpath):
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, element_xpath))
        )
        return element
    except:
        return None
def sold_image_captcha(captcha_class, driver):
    sleep(3)
    captcha_image_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, captcha_class))
    )
    captcha_image_url = captcha_image_element.get_attribute('src')
    print("URL image captcha:", captcha_image_url)
    response = requests.get(captcha_image_url)
    if response.status_code == 200:
        captcha_image_path = "captcha_image"+ str(uuid.uuid4()) +".png"
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
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, '/html/body/div[1]/div[1]/div[2]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div[4]/div[2]/div/div[2]/div[2]/div/span'))
        )
        print("Error")
        sold_image_captcha(captcha_class, driver)
    except:
        return True

def sold_captcha(captchaType, type, driver):
    print('type', type)
    sleep(5)
    captchaElements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, captchaType))
    )
    url_image = captchaElements[0].get_attribute('src')
    response = requests.get(url_image)
    if response.status_code == 200:
        captcha_image_path = "recaptcha"+ str(uuid.uuid4())+".png"
        with open(captcha_image_path, 'wb') as f:
            f.write(response.content)

        task = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "rc-imageselect-desc-no-canonical"))
        )

        task_final = task[0].get_attribute('innerText').replace('\n', ' ').replace(' If there are none, click skip', '.')

        print("task", task_final)

        public_url = upload_cloudinary_image(captcha_image_path).get('url')

        print('public_url', public_url)

        clicks = nopecha.Recognition.solve(
            type='recaptcha',
            task=task_final,
            image_urls=[public_url],
            grid=type
        )

        print('clicks', clicks)

        tiles = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.rc-imageselect-tile"))
        )

        for i, should_click in enumerate(clicks):
            if should_click:
                sleep(random.randint(1, 2))
                tiles[i].click()

        assert len(tiles) == len(clicks), "Số lượng tiles không khớp với mẫu click."

        # if (type == '4x4') and (
        #         clicks == [False, False, False, False, False, False, False, False, False, False, False, False, False,
        #                    False, False, False]):
        #     return True
        # elif (type == '3x3') and (clicks == [False, False, False, False, False, False, False, False, False]):
        #     return True
        # else:
        #     sold_captcha(captchaType, type)
        return True
def check_util_success(driver):
    isType44 = safe_find_element_by_class(driver, "rc-image-tile-44")
    typeCaptcha = ''
    if isType44:
        print('Type 4x4')
        typeCaptcha = '4x4'
    else:
        print('Type 3x3')
        typeCaptcha = '3x3'
    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, '//iframe[starts-with(@title, "recaptcha challenge expires in two minutes")]'))
    )

    driver.switch_to.frame(iframe)

    if typeCaptcha == '4x4':
        captchaType = "rc-image-tile-44"
    else:
        captchaType = "rc-image-tile-33"

    if (sold_captcha(captchaType, type, driver)):
        sleep(3)
        verify_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "recaptcha-verify-button"))
        )
        verify_element.click()

    captchaBox = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "rc-imageselect-desc-no-canonical"))
    )
    if(captchaBox):
        driver.switch_to.default_content()
        check_util_success(type, driver)
    else:
        return True
def forgotPass(email, driver):

    driver.get("http://mail.google.com")

    sleep(3)
    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "identifier"))
    )

    email_input.send_keys(email)

    next_button = driver.find_element(By.ID, "identifierNext")

    next_button.click()
    sleep(3)

    haveCaptchaImage = safe_find_element_by_id(driver, "captchaimg")

    print('haveCaptchaImage', haveCaptchaImage)

    if haveCaptchaImage:
        try:
            sold_image_captcha("captchaimg", driver)
        except Exception as e:
            print('Not find the image captcha:' + str(e))

    haveCaptcha = safe_find_element_by_xpath(driver, '//iframe[starts-with(@title, "recaptcha challenge expires in two minutes")]')

    if haveCaptcha:
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, '//iframe[starts-with(@title, "recaptcha challenge expires in two minutes")]'))
        )

        driver.switch_to.frame(iframe)

    forgotPassword_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "forgotPassword"))
    )

    forgotPassword_element.click()


    check_util_success(driver)
