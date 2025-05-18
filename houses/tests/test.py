from django.test import SimpleTestCase
from django.urls import path, reverse, resolve
from houses.views import *
import json

class TestUrls(SimpleTestCase):
    def test_list_url_is_resolved(self):
        reverse_from_method = reverse('follow')
        actual_url  = resolve(reverse_from_method)
        print(actual_url)  # shows the URL that will get called
        self.assertEquals(actual_url.func, follow ) # test if that method gets called based on the URL

    def test_list_url_is_resolved1(self):
        reverse_from_method = reverse('login_attempt')
        actual_url  = resolve(reverse_from_method)
        self.assertEquals(actual_url.func, login_attempt ) # test if that method gets called based on the URL

    def test_list_url_is_resolved2(self):
        reverse_from_method = reverse('view_page')
        actual_url  = resolve(reverse_from_method)
        print(actual_url)  # shows the URL that will get called
        self.assertEquals(actual_url.func, load_data ) # test if that method gets called based on the URL

    def test_list_url_is_resolved3(self):
        reverse_from_method = reverse('default_page')
        actual_url  = resolve(reverse_from_method)
        print(actual_url)  # shows the URL that will get called
        self.assertEquals(actual_url.func, index ) # test if that method gets called based on the URL

    def test_ajax_call_with_null_payload(self):
        reverse_from_method = reverse('follow')
        actual_url  = resolve(reverse_from_method)
        payload = None
        response = self.client.post(reverse_from_method, json.dumps(payload), content_type='application/json')
        print(actual_url)  # shows the URL that will get called
        self.assertEqual(response.status_code, 200)
        print(response.json())



