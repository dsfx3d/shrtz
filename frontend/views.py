from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.http import Http404

from rest_framework.response import Response
from rest_framework.views import status

from api.models import URLDictionary
from res.strings import APIMethods, APIKeys, APIResponseErrorMessages as Error
from .validators import validate_shrtzy



def shrtzy_redirect(request, shrtzy):
    validate_shrtzy(shrtzy)
    if APIMethods.GET == request.method:
        try:
            shrtzyObj = URLDictionary.get_shrtzy(shrtzy)
        except ObjectDoesNotExist:
            raise Http404

        return redirect(shrtzyObj.url)
    else:
        error_message = {APIKeys.MSG: Error.ONLY_METHOD_GET_IS_ALLOWED}
        return Response(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            data=error_message
        )