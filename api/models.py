from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db import models

from api.utils import generate_hash



DEF_SHRTZY_LEN = 6

def generate_shrtzy():
    return generate_hash(DEF_SHRTZY_LEN)

class URLDictionary(models.Model):
    '''
    Model to hold URLs with corresponding Shortzies (shortened URLs)

    Fields:
        1. url::URLField
        2. shrtzy::CharField
        3. createdAt::DateTimeField
    '''
    url = models.URLField(null=False, unique=True, validators=[URLValidator])
    shrtzy = models.CharField(max_length=DEF_SHRTZY_LEN, unique=True, null=False, default=generate_shrtzy)
    createdAt = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        url = str(self.url)
        if len(self.url) > 30: url = url[:27] + '...'
        return f'{self.shrtzy} - {url}'

    @staticmethod
    def get_shrtzy(value):
        url_val = URLValidator()

        try:
            url_val(value)
        except ValidationError:
            return URLDictionary.objects.get(shrtzy=value)

        shrtzy, _ = URLDictionary.objects.get_or_create(url=value)
        return shrtzy