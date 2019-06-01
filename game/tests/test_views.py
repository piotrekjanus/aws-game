from django.test import TestCase, Client
from django.urls import reverse
from tabs.views import game_view, stats_view, home_view, get_match_result
from django.contrib.auth.models import User
from django.contrib.auth import SESSION_KEY


class ViewsTest_GET(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'User',
            'password': 'admin'}
        self.user = User.objects.create_user(**self.credentials)
        self.c = Client()
        self.login = reverse('login')
        self.logout = reverse('logout')
        self.register = reverse('register')
        self.game = reverse('game')
        self.stats = reverse('stats')
        self.home = reverse('homepage')
        self.results = reverse('results')

    def test_login_GET(self):
        response = self.c.get(self.login)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/login.html')
        self.assertTemplateNotUsed(response, 'index.html')

    def test_login_logged_user_GET(self):
        response = self.c.post(self.login, self.credentials)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))

    def test_logout_GET(self):
        response = self.c.get(self.logout, follow=True)

        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertTemplateNotUsed(response, 'login/logout.html')
        self.assertRedirects(response, reverse('login'))

    def test_register_GET(self):
        response = self.c.get(self.register)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/register.html')
        self.assertTemplateNotUsed(response, 'index.html')

    def test_game_GET(self):
        self.c.login(username='User', password='admin')
        response = self.c.get(self.game)
        self.c.logout()
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tabs/game.html')
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateNotUsed(response, 'login/register.html')

    def test_game_GET_fail(self):
        response = self.c.get(self.game)
        self.assertNotEqual(response.status_code, 200)

    def test_stats_GET(self):
        self.c.login(username='User', password='admin')
        response = self.c.get(self.stats)
        self.c.logout()
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'tabs/stats.html')
        self.assertTemplateUsed(response, 'index.html')

    def test_stats_GET_fail(self):
        response = self.c.get(self.stats)
        self.assertNotEqual(response.status_code, 200)

    def test_home_view_GET(self):
        self.c.login(username='User', password='admin')
        response = self.c.get(self.home)
        self.c.logout()
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_home_view_GET_fail(self):
        response = self.c.get(self.home)
        self.assertNotEqual(response.status_code, 200)

    def test_results_GET(self):
        response = self.c.get(self.results)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'base.html')
        self.assertTemplateNotUsed(response, 'index.html')
        self.assertTemplateNotUsed(response, 'tabs/stats.html')


class ViewsTest_POST(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'User',
            'password': 'admin'}
        self.user = User.objects.create_user(**self.credentials)
        self.c = Client()
        self.login = reverse('login')

    def test_login_POST(self):
        response = self.c.post(self.login, self.credentials)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))

    def test_login_POST_fail(self):
        credentials = {
            'username': 'User',
            'email': 'admin'}
        response = self.c.post(self.login, credentials)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)

    def test_register_POST(self):
        response = self.c.post(self.login, self.credentials)
        self.assertEquals(response.status_code, 302)
        self.assertRedirects(response, reverse('homepage'))

    def test_register_POST_fail(self):
        credentials = {
            'username': 'User',
            'email': 'admin'}
        response = self.c.post(self.login, credentials)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)


class LoginTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'User',
            'password': 'admin123'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        response = self.client.post(reverse('login'),
                                    self.credentials,
                                    follow=True)
        self.assertTrue(response.context['user'].is_active)

class RegisterTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'User',
            'password1': 'VrWvr!32',
            'password2': 'VrWvr!32'}

    def test_register(self):
        response = self.client.post(reverse('register'),
                                    self.credentials,
                                    follow=True)
        self.assertRedirects(response, reverse('login'))

    def test_register_fail(self):
        credentials = {
            'username': 'User',
            'password1': 'VrWvr!32',
            'password2': 'VrWvq!33'}
        response = self.client.post(reverse('register'),
                                    credentials,
                                    follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/register.html')
        self.assertTemplateNotUsed(response, 'login/login.html')
