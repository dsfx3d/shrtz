from django.core.validators import URLValidator
from django.db import models
from api.utils import generate_hash
from shrtzy.settings import HOST

DEF_SHRTZY_LEN = 5

def generate_shrtzy():
    return generate_hash(DEF_SHRTZY_LEN)

class IndexQuerySet(models.QuerySet):
    def atShrtzy(self, shrtzy):
        return self.get(shrtzy=shrtzy)

    def atUrl(self, url):
        return self.get(url=url)

    def insert(self, url):
        return self.create(url=url)

    def deleteShrtzy(self, shrtzy):
        return self.atShrtzy(shrtzy).delete()

    def deleteUrl(self, url):
        return self.atUrl(url).delete()


class IndexManager(models.Manager):
    def get_queryset(self):
        return IndexQuerySet(self.model, using=self._db)

    def atShrtzy(self, shrtzy):
        return self.get_queryset().atShrtzy(shrtzy)

    def atUrl(self, url):
        return self.get_queryset().atUrl(url)

    def addToDictionary(self, url):
        return self.get_queryset().insert(url)

    def deleteShrtzy(self, shrtzy):
        return self.get_queryset().deleteShrtzy(shrtzy)
    
    def deleteUrl(self, url):
        return self.get_queryset().deleteUrl(url)


class URLDictionary(models.Model):
    url = models.URLField(null=False, unique=True, validators=[URLValidator])
    shrtzy = models.URLField(unique=True, null=False, validators=[URLValidator], default=generate_shrtzy)
    createdAt = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    index = IndexManager()

    def __str__(self):
        url = str(self.url)
        if len(self.url) > 10: url = url[:7] + '...'
        return f'{self.shrtzy} - {url}'