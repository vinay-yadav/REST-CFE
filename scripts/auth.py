import requests

END_POINT = 'http://localhost:8000/auth/register/'
# END_POINT = 'http://localhost:8000/auth/'

r = requests.post(
    END_POINT,
    # data={'username': 'admin', 'password': 'qwerty'},
    data={
        'first_name': 'Api',
        'last_name': 'Tester3',
        'email': 'api3@tester.com',
        'username': 'api_tester3',
        'password': 'qwerty',
        'password2': 'qwerty'
    },
    # headers={
    #     'Authorization': 'JWT ' + 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyMCwidXNlcm5hbWUiOiJhcGlfdGVzdGVyMiIsImV4cCI6MTYzMDU4MDkwNywiZW1haWwiOiJhcGkyQHRlc3Rlci5jb20iLCJvcmlnX2lhdCI6MTYzMDU4MDYwN30.q-sk4p20zLehK_MFwEto6VfBNlVGXhtAlZ50op8VQso'
    # }
)
print(r.text)
