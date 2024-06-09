import requests
from bs4 import BeautifulSoup

def readMailDongVan(hotmail, passwd):
    url = 'https://tools.dongvanfb.net/api/get_messages'

    headers = {
        'authority': 'tools.dongvanfb.net',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://dongvanfb.net',
        'referer': 'https://dongvanfb.net/',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
    }

    params = {
        'mail': hotmail,
        'pass': passwd
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        response_final  = response.json()
        message_html = response_final['messages'][0]['message']

        soup = BeautifulSoup(message_html, 'html.parser')

        text = soup.get_text()

        print(text)

        return text

    else:
        print("Failed to retrieve data: ", response.status_code)

        return ("Failed to retrieve data: ", response.status_code)