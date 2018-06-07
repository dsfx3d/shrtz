from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('', include('frontend.urls')),
    path('admin/v1/', admin.site.urls),
    re_path('api/', include('api.urls'))
]
