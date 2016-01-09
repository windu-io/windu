from django.conf.urls import url

from . import views
from api import account
from api import contacts

urlpatterns = [
    url(r'^chats/$', views.chats, name='chats'),
    url(r'^messages/(?P<entity_id>[0-9]+)/$', views.messages, name='messages'),
    url(r'^account/status-message/$', account.status_message, name='status-message'),
    url(r'^account/profile-photo/$', account.profile_photo, name='profile-photo'),
    url(r'^account/connected-status/$', account.connected_status, name='connected-status'),
    url(r'^account/nickname/$', account.nickname, name='nickname'),
    url(r'^account/privacy-settings/$', account.privacy_settings, name='privacy-settings'),
    url(r'^account/create-account/$', account.create_account, name='create-account'),
    url(r'^account/request-sms-code/$', account.request_sms_code, name='request-sms-code'),
    url(r'^account/request-voice-code/$', account.request_voice_code, name='request-voice-code'),
    url(r'^account/register-code/$', account.register_code, name='register-code'),
    url(r'^account/remove-account/$', account.remove_account, name='remove-account'),
    url(r'^contacts/$', contacts.list_contacts, name='contacts'),
    url(r'^contacts/add-contact/$', contacts.add_contact, name='add-contact'),
    url(r'^contacts/(?P<contact_id>[0-9]+)/$', contacts.handle_contact, name='handle-contact'),
    url(r'^contacts/remove-contacts/$', contacts.remove_contacts, name='remove-contacts'),
    url(r'^contacts/import-contacts/$', contacts.import_contacts, name='import-contact'),
]


