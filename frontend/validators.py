import re

from django.http import Http404

from res.numbers import APILimits



def validate_shrtzy(shrtzy):

    if (len(shrtzy)>APILimits.MAX_SHRTZY_LEN) or (re.findall(r'\W', shrtzy)):
        raise Http404