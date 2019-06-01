from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError


class RegistrationViewTest(TestCase):
    def setUp(self):
        self.c = Client()
        self.register = reverse('register')

    def test_registration_pass(self):
        credentials = {
            'username': 'user@test.com',
            'password1': 'Secret1!',
            'password2': 'Secret1!',
        }
        response = self.c.post(self.register, credentials)
        self.assertIsNotNone(User.objects.get(username='user@test.com'))
        try:
            user = User.objects.get(username='user@test.pl')
        except User.DoesNotExist:
            user = None
        self.assertIsNone(user, None)

    def test_registration_fail_length(self):
        credentials = {
            'username': 'User',
            'password1': 'short',
            'password2': 'short',
        }
        response = self.c.post(self.register, credentials)
        try:
            user = User.objects.get(username='User')
        except User.DoesNotExist:
            user = None
        self.assertIsNone(user, None)

        credentials = {
            'username': 'User',
            'password1': 'muchlonger',
            'password2': 'muchlonger',
        }
        response = self.c.post(self.register, credentials)
        try:
            user = User.objects.get(username='User')
        except User.DoesNotExist:
            user = None
        self.assertIsNotNone(user, None)

    def test_registration_fail_not_same(self):
        credentials = {
            'username': 'User',
            'password1': 'Vhgshd12d',
            'password2': 'khsddehhe45',
        }
        response = self.c.post(self.register, credentials)
        try:
            user = User.objects.get(username='User')
        except User.DoesNotExist:
            user = None
        self.assertIsNone(user, None)

    def test_registration_fail_password2_missing(self):
        credentials = {
            'username': 'User',
            'password1': 'Vhgshd12d'
        }
        response = self.c.post(self.register, credentials)
        try:
            user = User.objects.get(username='User')
        except User.DoesNotExist:
            user = None
        self.assertIsNone(user, None)

    def test_registration_fail_only_numeric(self):
        credentials = {
            'username': 'User',
            'password1': '59265423',
            'password2': '59265423',
        }
        response = self.c.post(self.register, credentials)
        try:
            user = User.objects.get(username='User')
        except User.DoesNotExist:
            user = None

        self.assertIsNone(user, None)
        credentials = {
            'username': 'User',
            'password1': 'as59265423',
            'password2': 'as59265423',
        }
        response = self.c.post(self.register, credentials)
        try:
            user = User.objects.get(username='User')
        except User.DoesNotExist:
            user = None
        self.assertIsNotNone(user, None)

    def test_registration_fail_same_same(self):
        credentials = {
            'username': 'VeryBadGuy',
            'password1': 'VeryBadGuy',
            'password2': 'VeryBadGuy'
        }
        response = self.c.post(self.register, credentials)
        try:
            user = User.objects.get(username='VeryBadGuy')
        except User.DoesNotExist:
            user = None
        self.assertIsNone(user, None)

        credentials = {
            'username': 'VeryBadGuy',
            'password1': '1goodGuy',
            'password2': '1goodGuy'
        }
        response = self.c.post(self.register, credentials)
        try:
            user = User.objects.get(username='VeryBadGuy')
        except User.DoesNotExist:
            user = None
        self.assertIsNotNone(user, None)

        def test_registration_fail_common(self):
            credentials = {
                'username': 'User',
                'password1': 'admin123',
                'password2': 'admin123'
            }
            response = self.c.post(self.register, credentials)
            try:
                user = User.objects.get(username='User')
            except User.DoesNotExist:
                user = None
            self.assertIsNone(user, None)

            credentials = {
                'username': 'User',
                'password1': '321nimda',
                'password2': '321nimda'
            }
            response = self.c.post(self.register, credentials)
            try:
                user = User.objects.get(username='User')
            except User.DoesNotExist:
                user = None
            self.assertIsNotNone(user, None)

        def test_registration_fail_already_in_db(self):
            credentials = {
                'username': 'User',
                'password1': 'Gtybx43k8a',
                'password2': 'Gtybx43k8a'
            }
            response = self.c.post(self.register, credentials)
            try:
                user = User.objects.get(username='User')
            except User.DoesNotExist:
                user = None
            self.assertIsNone(user, None)

            credentials = {
                'username': 'User',
                'password1': '321nimda',
                'password2': '321nimda'
            }
            response = self.c.post(self.register, credentials)
            self.assertTemplateNotUsed(response, 'login/login.html')


class LoginViewTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'user123',
            'password': 'Gtdhenys!'}
        User.objects.create_user(**self.credentials)
        self.c = Client()

    def test_login_success(self):
        response = self.c.post(reverse('login'),
                                    self.credentials,
                                    follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_login_wrong_password(self):
        credentials = {
            'username': 'user123',
            'password': 'Gtdhenys'}
        response = self.c.post(reverse('login'),
                                    credentials,
                                    follow=True)
        self.assertFalse(response.context['user'].is_active)

    def test_login_wrong_login(self):
        credentials = {
            'username': 'user0123',
            'password': 'Gtdhenys!'}
        response = self.c.post(reverse('login'),
                                    credentials,
                                    follow=True)
        self.assertFalse(response.context['user'].is_active)

    def test_login_fail_login_cap_sensitive(self):
        credentials = {
            'username': 'User123',
            'password': 'Gtdhenys!'}
        response = self.c.post(reverse('login'),
                                    credentials,
                                    follow=True)
        self.assertFalse(response.context['user'].is_active)
