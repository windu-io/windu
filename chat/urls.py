from django.conf.urls import url

from . import views
from api import account

urlpatterns = [
    url(r'^chats/$', views.chats, name='chats'),
    url(r'^messages/(?P<entity_id>[0-9]+)/$', views.messages, name='messages'),
    url(r'^account/status-message/$', account.status_message, name='status-message'),
    url(r'^account/profile-photo/$', account.profile_photo, name='profile-photo'),
    url(r'^account/connected-status/$', account.connected_status, name='connected-status'),
]