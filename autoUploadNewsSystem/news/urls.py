from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^result/$', views.result, name='result'),
]
