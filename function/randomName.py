import requests

def get_random_name():
    response = requests.get("https://randomuser.me/api/?nat=us")
    if response.status_code == 200:
        data = response.json()
        first_name = data['results'][0]['name']['first']
        last_name = data['results'][0]['name']['last']
        return first_name, last_name
    else:
        return "DefaultFirstName", "DefaultLastName"