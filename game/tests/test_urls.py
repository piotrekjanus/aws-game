from django.test import SimpleTestCase
from django.urls import reverse, resolve

from login.views import register_view, login_view, logout_view
from tabs.views import home_view, game_view, stats_view, get_match_result


class UrlTest(SimpleTestCase):

    def test_login_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login_view)

    def test_logout_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout_view)

    def test_register_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register_view)

    def test_homepage_resolves(self):
        url = reverse('homepage')
        self.assertEquals(resolve(url).func, home_view)

    def test_game_view_resolves(self):
        url = reverse('game')
        self.assertEquals(resolve(url).func, game_view)

    def test_stats_resolves(self):
        url = reverse('stats')
        self.assertEquals(resolve(url).func, stats_view)

    def test_register_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register_view)

    def test_match_result_resolves(self):
        url = reverse('results')
        self.assertEquals(resolve(url).func, get_match_result)
