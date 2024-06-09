import time
from time import sleep
import requests

api_key = ''
url = f"https://daisysms.com/stubs/handler_api.php?api_key={api_key}&action=getNumber&service=go&max_price=0.5"

def get_ACCESS_NUMBER():
    response = requests.get(url)
    if response.status_code == 200:
        print("Yêu cầu thành công!")
        print(response.text)
        return response.text
    else:
        print(f"Lỗi: {response.status_code}")
        if response.status_code == 400:
            print("Thử lại")
            sleep(3)
            return get_ACCESS_NUMBER()
        else:
            return f"Lỗi: {response.status_code}"

# get_ACCESS_NUMBER()

def getCode(activation_id):
    url = f"https://daisysms.com/stubs/handler_api.php?api_key={api_key}&action=getStatus&id={activation_id}"

    while True:
        response = requests.get(url)
        if response.status_code == 200:
            response_text = response.text
            print(f"Phản hồi: {response_text}")

            if "STATUS_OK" in response_text:
                code = response_text.split(':')[1]
                print(f"Mã đã nhận: {code}")
                return code
            elif "NO_ACTIVATION" in response_text:
                print("ID không tồn tại.")
                return "ID không tồn tại."

            elif "STATUS_CANCEL" in response_text:
                print("Thuê bao đã được hủy.")
                return "Thuê bao đã được hủy."

            elif "STATUS_WAIT_CODE" in response_text:
                print("Đang chờ SMS...")
            else:
                print("Trạng thái không xác định.")
        else:
            print(f"Lỗi: {response.status_code}")

        time.sleep(3)

# getCode('14024460290')