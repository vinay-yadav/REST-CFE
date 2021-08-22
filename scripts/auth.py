import requests

END_POINT = 'http://localhost:8000/auth/'

r = requests.post(END_POINT, data={'username': 'admin', 'password': 'qwerty'})
print(r.text)
