"""harf_synonym URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from synonym.views import get_synonym_view
from synonym.views_api import WordApiViewSet

router = DefaultRouter()

router.register('', WordApiViewSet)
# router.register('', qwerty)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', get_synonym_view, name='synonym'),
    path('api/v1/get-synonym/', include(router.urls))
]
