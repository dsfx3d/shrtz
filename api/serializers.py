from rest_framework import serializers

from .models import URLDictionary


class URLDictionarySerializer(serializers.ModelSerializer):
    class Meta:
        model = URLDictionary
        fields = ('url','shrtzy')