import re

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework.views import status

from res.strings import APIKeys, APIResponseErrorMessages, Misc
from res.numbers import APILimits



def validate_requested_url(fn):
    """
    ensure POSTed url is valid
    """
    def decorated(*args, **kwargs):
        urlValidator = URLValidator()

        view = args[0]
        url = view.request.data.get(APIKeys.URL, Misc.EMPTY)

        if len(url) > APILimits.MAX_URL_LEN:
            error_msg = {APIKeys.MSG: APIResponseErrorMessages.URL_TOO_LARGE}
            return Response(
                status=status.HTTP_414_REQUEST_URI_TOO_LONG,
                data=error_msg
            )

        try: # URL Validation
            if url and url!=Misc.EMPTY:
                urlValidator(url)
        except ValidationError:
            error_msg = {APIKeys.MSG: APIResponseErrorMessages.INVALID_URL_REQUEST}
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data=error_msg
            )

        return fn(*args, **kwargs)
    return decorated


def validate_requested_shrtzy(fn):
    """
    """
    def decorated(*args, **kwargs):
        view = args[0]
        shrtzy = view.request.data.get(APIKeys.SHRTZY, Misc.EMPTY)

        if len(shrtzy)>APILimits.MAX_SHRTZY_LEN:
            error_msg = {APIKeys.MSG: APIResponseErrorMessages.SHRTZY_TOO_LARGE}
            return Response(
                status=status.HTTP_414_REQUEST_URI_TOO_LONG,
                data=error_msg
            )

        if re.findall(r'\W', shrtzy):
            error_msg = {APIKeys.MSG: APIResponseErrorMessages.SHRTZY_CONTAIN_SPECIAL_CHARS}
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data=error_msg
            )

        return fn(*args, **kwargs)
    return decorated


def either_url_or_shrtzy(fn):
    """
    """
    def decorated(*args, **kwargs):
        view = args[0]
        url = view.request.data.get(APIKeys.URL, Misc.NONE)
        shrtzy = view.request.data.get(APIKeys.SHRTZY, Misc.NONE)
        
        if url and shrtzy:
            error_msg = {APIKeys.MSG: APIResponseErrorMessages.CANT_REQUEST_WITH_BOTH_SHRTZY_AND_URL}
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data=error_msg
            )
        
        if not url and not shrtzy:
            error_msg = {APIKeys.MSG: APIResponseErrorMessages.NO_DATA_POSTED}
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=error_msg
            )

        return fn(*args, **kwargs)
    
    return decorated