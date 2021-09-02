from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse as api_reverse

User = get_user_model()


class UserTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='vinay', email='vinay@rr.com')
        user.set_password('qwerty')
        user.save()

    def test_created_user(self):
        qs = User.objects.filter(username='vinay')
        self.assertEqual(qs.count(), 1)


class UserAPITestCase(APITestCase):
    def setUp(self):
        user = User.objects.create(username='vinay', email='vinay@rr.com')
        user.set_password('qwerty')
        user.save()

    def test_created_user_std(self):
        qs = User.objects.filter(username='vinay')
        self.assertEqual(qs.count(), 1)

    # def test_register_user_api_fail(self):
    #     url = api_reverse('accounts:register')
    #
    #     data = {
    #         'username': 'test_user',
    #         'email': 'test@api.com',
    #         'password': 'qwertyzoo',
    #         'password2': 'qwertyzoo'
    #     }
    #
    #     response = self.client.post(url, data, format='json')
    #     print('response.status_code', response.data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user_api(self):
        url = api_reverse('accounts:login')

        data = {
            'username': 'vinay',
            'password': 'qwerty',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_token_api(self):
        url = api_reverse('accounts:login')
        data = {
            'username': 'vinay',
            'password': 'qwerty',
        }
        response = self.client.post(url, data, format='json')
        token = response.data.get('token', None)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        response2 = self.client.post(url, data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
