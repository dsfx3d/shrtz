from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import status

from res.strings import APIKeys, APIResponseErrorMessages as Error, Misc
from .models import URLDictionary
from .serializers import URLDictionarySerializer
from .decorators import validate_requested_url, either_url_or_shrtzy, validate_requested_shrtzy



class GetOrCreateShrtzyView(generics.GenericAPIView):

    queryset = URLDictionary.objects.all()
    serializer_class = URLDictionarySerializer

    @either_url_or_shrtzy
    @validate_requested_url
    @validate_requested_shrtzy
    def post(self, request, *args, **kwargs):
        url = request.data.get(APIKeys.URL, Misc.EMPTY)
        shrtzy = request.data.get(APIKeys.SHRTZY, Misc.EMPTY)

        value = url or shrtzy
        try:
            shrtzyObj = URLDictionary.get_shrtzy(value)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_204_NO_CONTENT,
                data={APIKeys.MSG: Error.SHRTZY_DOESNT_EXIST}
            )

        return Response(
            data = URLDictionarySerializer(shrtzyObj).data,
            status = status.HTTP_200_OK
        )


    def get(self, request, *args, **kwargs):
        return Response(
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            data = {APIKeys.MSG: Error.METHOD_NOT_ALLOWED}
        )


    def head(self, request, *args, **kwargs):
        return Response(
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            data = {APIKeys.MSG: Error.METHOD_NOT_ALLOWED}
        )


    def put(self, request, *args, **kwargs):
        return Response(
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            data = {APIKeys.MSG: Error.METHOD_NOT_ALLOWED}
        )


    def patch(self, request, *args, **kwargs):
        return Response(
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            data = {APIKeys.MSG: Error.METHOD_NOT_ALLOWED}
        )
    

    def delete(self, request, *args, **kwargs):
        return Response(
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            data = {APIKeys.MSG: Error.METHOD_NOT_ALLOWED}
        )


    def copy(self, request, *args, **kwargs):
        return Response(
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            data = {APIKeys.MSG: Error.METHOD_NOT_ALLOWED}
        )


    def options(self, request, *args, **kwargs):
        return Response(
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            data = {APIKeys.MSG: Error.METHOD_NOT_ALLOWED}
        )


    def link(self, request, *args, **kwargs):
        return Response(
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            data = {APIKeys.MSG: Error.METHOD_NOT_ALLOWED}
        )



    def unlink(self, request, *args, **kwargs):
        return Response(
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            data = {APIKeys.MSG: Error.METHOD_NOT_ALLOWED}
        )


    def purge(self, request, *args, **kwargs):
        return Response(
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            data = {APIKeys.MSG: Error.METHOD_NOT_ALLOWED}
        )


    def lock(self, request, *args, **kwargs):
        return Response(
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            data = {APIKeys.MSG: Error.METHOD_NOT_ALLOWED}
        )


    def unlock(self, request, *args, **kwargs):
        return Response(
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            data = {APIKeys.MSG: Error.METHOD_NOT_ALLOWED}
        )


    def propfind(self, request, *args, **kwargs):
        return Response(
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            data = {APIKeys.MSG: Error.METHOD_NOT_ALLOWED}
        )


    def view(self, request, *args, **kwargs):
        return Response(
            status = status.HTTP_405_METHOD_NOT_ALLOWED,
            data = {APIKeys.MSG: Error.METHOD_NOT_ALLOWED}
        )