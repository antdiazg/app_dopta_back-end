import requests

url = 'http://127.0.0.1:8000/login/'
data = {'username': 'Nicolongo', 'password': 'chevoce123'}
response = requests.post(url, data=data)

print(response.json())