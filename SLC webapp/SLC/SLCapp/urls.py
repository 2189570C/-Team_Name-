from django.conf.urls import url
from SLCapp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]
