import requests

END_POINT = 'http://localhost:8000/auth/register/'
# END_POINT = 'http://localhost:8000/auth/'

r = requests.post(
    END_POINT,
    # data={'username': 'admin', 'password': 'qwerty'},
    data={
        'first_name': 'Api',
        'last_name': 'Tester2',
        'email': 'api2@tester.com',
        'username': 'api_tester2',
        'password': 'qwerty',
        'password2': 'qwerty'
    },
    headers={
        'Authorization': 'JWT ' + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjMwMjI0NzU1LCJlbWFpbCI6IiIsIm9yaWdfaWF0IjoxNjMwMjI0NDU1fQ.Q6Jd7rNqNeqtZNd0O2twW51lIWcTLe-XtJb5uwPXfSE'
    }
)
print(r.text)
