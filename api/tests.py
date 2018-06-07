from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework.views import status

import json

from res.strings import APIResponseErrorMessages as Error, APIKeys, APIMethods, APIEndpointPaths
from res.numbers import APILimits
from .models import URLDictionary



class BaseViewTestCase(APITestCase):

    client = APIClient()

    @staticmethod
    def get_or_create_shrtzy(url):
        """
        get or create shrtzy by url
        :param url:
        :return shrtzyObj:
        """
        shrtzyObj = URLDictionary.get_shrtzy(url)
        return shrtzyObj

    def make_a_request(self, method, **kwargs):
        """
        """
        if method==APIMethods.POST:
            return self.client.post(
                reverse(
                    APIEndpointPaths.SHRTNR,
                ),
                data = json.dumps(kwargs['data']),
                content_type= 'application/json'
            )
        elif method==APIMethods.GET:
            return self.client.get(
                reverse(
                    APIEndpointPaths.SHRTNR
                )
            )
        else:
            return None

    @staticmethod
    def shrtzy_data(shrtzy):
        return {APIKeys.SHRTZY: shrtzy}

    @staticmethod
    def url_data(url):
        return {APIKeys.URL: url}

    def setUp(self):
        self.valid_url                  = 'https://www.google.com/'
        self.invalid_url                = 'not url'
        self.too_large_url              = 'https://www.google.com?q='+'a'*APILimits.MAX_URL_LEN
        self.valid_shrtzy               = 'not set yet'   # placeholder
        self.invalid_shrtzy             = 'doesnotexist'
        self.too_long_shrtzy            = 'a'+'b'*APILimits.MAX_SHRTZY_LEN
        self.special_shrtzy             = 'as#fv%@'

        self.valid_url_data             = {APIKeys.URL: self.valid_url}
        self.invalid_url_data           = {APIKeys.URL: self.invalid_url}
        self.shrtzy_and_url_data        = {APIKeys.URL: self.valid_url, APIKeys.SHRTZY: self.valid_shrtzy}
        self.no_data                    = {}

        self.invalid_url_response_msg   = 'requesting with invalid `url`. please request using a valid `url`'
        self.shrtzy_doesnt_exist_msg    = 'requested `shrtzy` does not exist. create a shrtzy by POSTing a `url` on this endpoint'

class ShrtnrEndpointAcceptanceTest(BaseViewTestCase):

    def verify_shrtnr_response(self, response, key, expected_key_value, expected_status_code):
        self.assertEqual(expected_status_code, response.status_code)
        self.assertIsNotNone(response.data)
        self.assertEqual(expected_key_value, response.data[key])


    # ACCEPTANCE CRITERIA - 1.1
    def test_post_shrtnr_always_return_shrtzy_for_valid_url(self):
        response = self.make_a_request(
            method=APIMethods.POST,
            data=self.valid_url_data
        )
        self.verify_shrtnr_response(
            response,
            APIKeys.URL, self.valid_url,
            status.HTTP_200_OK
        )
        

    # ACCEPTANCE CRITERIA - 1.2
    def test_post_shrtnr_always_return_bad_request_for_invalid_url(self):
        response = self.make_a_request(
            method=APIMethods.POST,
            data=self.invalid_url_data
        )
        self.verify_shrtnr_response(
            response,
            APIKeys.MSG, Error.INVALID_URL_REQUEST,
            status.HTTP_406_NOT_ACCEPTABLE
        )

    
    # ACCEPTANCE CRITERIA - 1.3
    def test_post_shrtnr_always_return_request_uri_too_long_for_suspeciously_long_url(self):
        response = self.make_a_request(
            method=APIMethods.POST,
            data=self.url_data(self.too_large_url)
        )
        self.verify_shrtnr_response(
            response,
            APIKeys.MSG, Error.URL_TOO_LARGE,
            status.HTTP_414_REQUEST_URI_TOO_LONG
        )

    
    # ACCEPTANCE CRITERIA - 2.1
    def test_post_shrtnr_always_return_url_if_requested_shrtzy_exists(self):
        self.valid_shrtzy = self.get_or_create_shrtzy(self.valid_url).shrtzy
        
        response = self.make_a_request(
            method=APIMethods.POST,
            data=self.shrtzy_data(self.valid_shrtzy)
        )
        self.verify_shrtnr_response(
            response,
            APIKeys.URL, self.valid_url,
            status.HTTP_200_OK
        )

    
    # ACCEPTANCE CRITERIA - 2.2
    def test_post_shrtnr_always_return_no_content_if_resquested_shrtzy_doesnt_exist(self):
        response = self.make_a_request(
            method=APIMethods.POST,
            data=self.shrtzy_data(self.invalid_shrtzy),
        )
        self.verify_shrtnr_response(
            response,
            APIKeys.MSG, Error.SHRTZY_DOESNT_EXIST,
            status.HTTP_204_NO_CONTENT
        )


    # ACCEPTANCE CRITERIA - 2.3
    def test_post_shrtnr_always_return_request_uri_too_long_for_suspeciously_long_shrtzy(self):
        response = self.make_a_request(
            method=APIMethods.POST,
            data=self.shrtzy_data(self.too_long_shrtzy)
        )
        self.verify_shrtnr_response(
            response,
            APIKeys.MSG, Error.SHRTZY_TOO_LARGE,
            status.HTTP_414_REQUEST_URI_TOO_LONG
        )


    # ACCEPTANCE CRITERIA - 2.4
    def test_post_shrtnr_always_return_not_acceptable_if_special_chars_in_shrtzy(self):
        response = self.make_a_request(
            method=APIMethods.POST,
            data=self.shrtzy_data(self.special_shrtzy)
        )
        self.verify_shrtnr_response(
            response,
            APIKeys.MSG, Error.SHRTZY_CONTAIN_SPECIAL_CHARS,
            status.HTTP_406_NOT_ACCEPTABLE
        )

    # ACCEPTANCE CRITERIA - 3
    def test_post_shrtnr_always_return_not_acceptable_if_requested_with_both_shrtzy_and_url(self):
        response = self.make_a_request(
            method=APIMethods.POST,
            data=self.shrtzy_and_url_data
        )
        self.verify_shrtnr_response(
            response,
            APIKeys.MSG, Error.CANT_REQUEST_WITH_BOTH_SHRTZY_AND_URL,
            status.HTTP_406_NOT_ACCEPTABLE
        )


    # ACCEPTANCE CRITERIA - 4
    def test_post_shrtnr_always_return_bad_request_if_requested_without_shrtzy_or_url(self):
        response = self.make_a_request(
            method=APIMethods.POST,
            data=self.no_data
        )
        self.verify_shrtnr_response(
            response,
            APIKeys.MSG, Error.NO_DATA_POSTED,
            status.HTTP_400_BAD_REQUEST
        )


    # ACCEPTANCE CRITERIA - 5
    def test_get_shrtnr_always_return_method_not_allowed(self):
        response = self.make_a_request(
            method=APIMethods.GET,
        )
        self.verify_shrtnr_response(
            response,
            APIKeys.MSG, Error.METHOD_NOT_ALLOWED,
            status.HTTP_405_METHOD_NOT_ALLOWED
        )