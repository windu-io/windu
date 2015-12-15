from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^chats/$', views.chats, name='chats'),
    url(r'^messages/(?P<entity_id>[0-9]+)/$', views.messages, name='messages'),
]