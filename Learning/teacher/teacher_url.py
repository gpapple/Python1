from django.conf.urls import include, url
from django.contrib import admin
from . import views as f

urlpatterns = [
    url(r'student/',f.do_app)
]
