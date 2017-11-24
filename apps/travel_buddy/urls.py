from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^login$', views.login),
    url(r'^add$', views.add),
    url(r'logout$', views.logout),
    url(r'create$', views.create),
    url(r'travels$', views.destination_list),
    url(r'join/(?P<destination_id>\d+)$', views.join),
    url(r'destination/(?P<destination_id>\d+)$', views.destination), 
] 