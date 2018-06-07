from django.test import TestCase
from django.urls import reverse

from rest_framework.views import status
from rest_framework.test import APIClient

from res.strings import APIEndpointPaths as Path, APIMethods, APIKeys, APIResponseErrorMessages
from res.numbers import APILimits
from api.tests import BaseViewTestCase as BTC



class BaseViewTestCase(TestCase):
    
    def setUp(self):
        self.non_existant_shrtzy = 'doesnotexist'
        self.invalid_shrtzy = 'a%ygb'
        self.invalid_shrtzy_2 = 'a'+'b'*APILimits.MAX_SHRTZY_LEN
        self.valid_url = 'https://www.google.com/'

        self.valid_shrtzy = BTC().make_a_request(
            method=APIMethods.POST,
            data=BTC.url_data(self.valid_url)
        ).data[APIKeys.SHRTZY]


class SHRTZYRedirectPageAcceptanceTest(BaseViewTestCase):

    def verify_response(self, response, key, expected_key_value, expected_status_code):
        self.assertEqual(expected_status_code, response.status_code)
        self.assertIsNotNone(response.data)
        self.assertEqual(expected_key_value, response.data[key])

    # ACCEPTANCE TEST - 1.1
    def test_if_shrtzy_exist_always_redirect(self):
        response = self.client.get(
            reverse(Path.SHRTZY_REDIRECT, kwargs={'shrtzy':self.valid_shrtzy})
        )

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)


    # ACCEPTANCE TEST - 1.2
    def test_if_shrtzy_is_invalid_always_return_404_not_found(self):
        response = self.client.get(
            reverse(Path.SHRTZY_REDIRECT, kwargs={'shrtzy':self.invalid_shrtzy})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(
            reverse(Path.SHRTZY_REDIRECT, kwargs={'shrtzy':self.invalid_shrtzy_2})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    # ACCEPTANCE TEST - 1.3
    def test_if_shrtzy_does_not_exist_always_return_404_not_found(self):
        response = self.client.get(
            reverse(Path.SHRTZY_REDIRECT, kwargs={'shrtzy':self.non_existant_shrtzy})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
