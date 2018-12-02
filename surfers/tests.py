import logging

from django.test import TestCase
from django.contrib.auth import get_user_model


class TestViews(TestCase):

    def setUp(self):
        get_user_model().objects.create_user(username='user', password='test')

    def test_map_denies_anonymous(self):
        response = self.client.get('/map/')
        self.assertRedirects(response, '/login/?next=/map/')

    def test_map_loads(self):
        self.client.login(username='user', password='test')  # defined in fixture or with factory in setUp()
        response = self.client.get('/map/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sunmap.html')
