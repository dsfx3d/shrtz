from django.urls import path

from .views import shrtzy_redirect


urlpatterns = [
    path('<str:shrtzy>/', shrtzy_redirect, name='shrtzy-redirect')
]