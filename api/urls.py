from django.urls import path

from .views import GetOrCreateShrtzyView


urlpatterns = [
    path('shrtnr/', GetOrCreateShrtzyView.as_view(), name='shrtnr')
]