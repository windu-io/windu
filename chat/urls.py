from django.conf.urls import url

from . import views
from api import account
from api import contacts
from api import messages

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
    url(r'^contacts/force-sync/$', contacts.force_sync, name='force-sync'),

    url(r'^contacts/(?P<contact_id>[0-9]+)/status-message/$', contacts.status_message, name='contact-status-message'),
    url(r'^contacts/(?P<contact_id>[0-9]+)/status-message-history/$', contacts.status_message_history, name='status-message-history'),
    url(r'^contacts/statuses-messages/$', contacts.statuses_messages, name='statuses-messages'),

    url(r'^contacts/(?P<contact_id>[0-9]+)/connected-status/$', contacts.connected_status, name='contact-connected-status'),
    url(r'^contacts/connected-statuses/$', contacts.connected_statuses, name='contact-connected-statuses'),

    url(r'^contacts/(?P<contact_id>[0-9]+)/preview-photo/$', contacts.preview_photo, name='preview-photo'),
    url(r'^contacts/(?P<contact_id>[0-9]+)/preview-photo-url/$', contacts.preview_photo_url, name='preview-photo-url'),
    url(r'^contacts/(?P<contact_id>[0-9]+)/preview-photo-history-urls/$', contacts.preview_photo_history_urls, name='preview-photo-history-urls'),
    url(r'^contacts/preview-photos-urls/$', contacts.preview_photos_urls, name='preview-photos-urls'),
    url(r'^contacts/(?P<contact_id>[0-9]+)/photo/$', contacts.photo, name='photo'),
    url(r'^contacts/(?P<contact_id>[0-9]+)/photo-url/$', contacts.photo_url, name='photo-url'),
    url(r'^contacts/(?P<contact_id>[0-9]+)/photo-history-urls/$', contacts.photo_history_urls, name='photo-history-urls'),
    url(r'^contacts/preview-photos-urls/$', contacts.preview_photos_urls, name='preview-photos-urls'),

    url(r'^contacts/(?P<contact_id>[0-9]+)/block/$', contacts.block, name='block'),
    url(r'^contacts/(?P<contact_id>[0-9]+)/unblock/$', contacts.unblock, name='unblock'),
    url(r'^contacts/blocked-list/$', contacts.blocked_list, name='blocked-list'),
    # sending message
    url(r'^messages/send-message/$', messages.send_message, name='send-message'),
    url(r'^messages/send-image/$', messages.send_image, name='send-image'),
    url(r'^messages/send-location/$', messages.send_location, name='send-location'),
    url(r'^messages/send-audio/$', messages.send_audio, name='send-audio'),
    url(r'^messages/send-voice/$', messages.send_voice, name='send-voice'),
    url(r'^messages/send-video/$', messages.send_video, name='send-video'),
    url(r'^messages/send-vcard/$', messages.send_vcard, name='send-vcard'),
    # sending typing state
    url(r'^messages/set-typing/$', messages.set_typing, name='set-typing'),
    url(r'^messages/set-paused/$', messages.set_paused, name='set-paused'),

    # getting message
    url(r'^messages/chats/(?P<contact_id>[0-9]+)/$', messages.get_messages, name='get-messages'),
]


