from django.conf.urls import url
from SLCapp import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout')
    url(r'^signup/$', views.signup, name='signup')
]
