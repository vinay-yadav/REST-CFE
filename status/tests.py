from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from .models import Status

User = get_user_model()


class StatusTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='vinay', email='vinay@rr.com')
        user.set_password('qwerty')
        user.save()

    def test_creating_status(self):
        user = User.objects.get(username='vinay')
        obj = Status.object.create(content='test content', user=user)
        self.assertEqual(obj.id, 1)
        qs = Status.object.all()
        self.assertEqual(qs.count(), 1)

# class StatusAPITestCase(APITestCase):
#     def setUp(self):
#         user = User.objects.create(username='vinay', email='vinay@rr.com')
#         user.set_password('qwerty')
#         user.save()
#
#     def test_creating_status(self):
#         user = User.objects.get(username='vinay')
#         obj = Status.object.create(content='test content', user=user)
#         self.assertEqual(obj.id, 1)
#         qs = Status.object.all()
#         self.assertEqual(qs.count(), 1)
