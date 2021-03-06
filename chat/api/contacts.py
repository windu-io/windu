#! /usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

from django.http import HttpResponse

from oauth2_provider.decorators import protected_resource

from ..controllers import contacts as contacts_controller
from ..decorators import active_account_required_400

from normalize_id import normalize
from normalize_id import normalize_list
from normalize_id import normalize_list_field

# Adding/Importing/Removing/Listing contacts


# /api/contacts/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def list_contacts(request):

    controller = contacts_controller.Contacts(request.account)

    contacts = controller.list_contacts()

    return Response(contacts)


# /api/contacts/add-contact/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def add_contact(request):

    contact_id = str(request.POST.get('contact_id'))
    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if contact_id is None:
        return Response({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')

    controller = contacts_controller.Contacts(request.account)

    result = controller.add_contact(contact_id, first_name, last_name)

    status_code = int(result.pop('code'))

    if status_code == 200:                # Return 'Created' if success
        status_code = 201
    return Response(result, status_code)


def __update_contact(request, contact_id):

    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')

    if first_name is None and last_name is None:
        return Response({'error': 'You must provide first_name or last_name'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.update_contact(contact_id, first_name, last_name)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


def __list_contact(request, contact_id):
    controller = contacts_controller.Contacts(request.account)

    result = controller.list_contact(contact_id)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


def __remove_contact(request, contact_id):
    controller = contacts_controller.Contacts(request.account)

    result = controller.remove_contact(contact_id)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/contacts/<contact-id>/ (PATCH, DELETE, GET)
@api_view(['PATCH','DELETE','GET'])
@protected_resource()
@active_account_required_400()
def handle_contact(request, contact_id):

    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if contact_id is None:
        return Response({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    if request.method == 'PATCH':
        return __update_contact(request, contact_id)
    if request.method == 'DELETE':
        return __remove_contact(request, contact_id)
    return __list_contact(request, contact_id)


# /api/contacts/remove-contacts/
@api_view(['POST'])
@protected_resource()
@parser_classes((JSONParser,))
@active_account_required_400()
def remove_contacts(request):
    data = request.data
    if not data:
        return Response({'error': 'No data provided (json:{contacts:[XXXXXX,YYYYYY,ZZZZZZZ]}'}, 400)
    contacts = data.get('contacts')
    if contacts is None or len(contacts) == 0:
        return Response({'error': 'No contacts provided (json:{contacts:[XXXXXX,YYYYYY,ZZZZZZZ]}'}, 400)
    contacts = normalize_list(contacts)
    if len(contacts) == 0:
        return Response({'error': 'Invalid contacts provided (json:{contacts:[XXXXXX,YYYYYY,ZZZZZZZ]}'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.remove_contacts(contacts)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/contacts/import-contacts/
@api_view(['POST'])
@protected_resource()
@parser_classes((JSONParser,))
@active_account_required_400()
def import_contacts(request):
    data = request.data
    if not data:
        return Response({'error': 'No data provided (json:{contacts:[{contact_id:XXXXXX,first_name:John},...]}'}, 400)
    contacts = data.get('contacts')
    if contacts is None or len(contacts) == 0:
        return Response({'error': 'No contacts provided (json:{contacts:[{contact_id:XXXXXX,first_name:John},...]}'}, 400)
    contacts = normalize_list_field(contacts, 'contact_id')
    if len(contacts) == 0:
        return Response({'error': 'Invalid contacts provided (json:{contacts:[{contact_id:XXXXXX,first_name:John},...]}'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.import_contacts(contacts)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/contacts/force-sync/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def force_sync(request):

    controller = contacts_controller.Contacts(request.account)

    result = controller.sync_contacts()

    status_code = int(result.pop('code'))

    return Response(result, status_code)

# Status


# /api/contacts/<contact-id>/status-message/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def status_message(request, contact_id):

    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if contact_id is None:
        return Response({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.status_message(contact_id)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/contacts/<contact-id>/status-message-history/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def status_message_history(request, contact_id):

    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if contact_id is None:
        return Response({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.status_message_history(contact_id)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/contacts/statuses-messages/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def statuses_messages(request):

    controller = contacts_controller.Contacts(request.account)

    result = controller.statuses_messages()

    status_code = int(result.pop('code'))

    return Response(result, status_code)

#  Connected Status & Last seen


# /api/contacts/<contact-id>/connected-status/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def connected_status(request, contact_id):

    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if contact_id is None:
        return Response({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.connected_status(contact_id)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/contacts/connected-statuses/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def connected_statuses(request):

    controller = contacts_controller.Contacts(request.account)

    result = controller.connected_statuses()

    status_code = int(result.pop('code'))

    return Response(result, status_code)

# Profile photo


# /api/contacts/<contact-id>/preview-photo/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def preview_photo(request, contact_id):

    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if contact_id is None:
        return Response({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.photo(contact_id, preview=True, url=False)

    status_code = int(result.pop('code'))

    if status_code != 200:
        return Response (result, status_code)

    picture_data = result['picture_data']
    mime_type = result['mime_type']
    return HttpResponse (picture_data, mime_type)


# /api/contacts/<contact-id>/preview-photo-url/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def preview_photo_url(request, contact_id):

    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if contact_id is None:
        return Response({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.photo(contact_id, preview=True, url=True)

    status_code = result.pop('code')
    if status_code is None or status_code[0] == '5':
        return Response(result, int(status_code))

    response = {'photo_url': result['photo_url'],
                'photo_status': status_code }

    return Response(response)


# /api/contacts/<contact-id>/preview-photo-history-urls/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def preview_photo_history_urls(request, contact_id):

    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if contact_id is None:
        return Response({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.photo_history_urls(contact_id, preview=True)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/contacts/preview-photos-urls/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def preview_photos_urls(request):

    controller = contacts_controller.Contacts(request.account)

    result = controller.photos_urls(preview=True)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/contacts/<contact-id>/photo/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def photo(request, contact_id):

    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if contact_id is None:
        return Response({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.photo(contact_id, preview=False, url=False)

    status_code = int(result.pop('code'))

    if status_code != 200:
        return Response(result, status_code)

    picture_data = result['picture_data']
    mime_type = result['mime_type']
    return HttpResponse (picture_data, mime_type)


# /api/contacts/<contact-id>/photo-url/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def photo_url(request, contact_id):

    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if contact_id is None:
        return Response({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.photo(contact_id, preview=False, url=True)

    status_code = result.pop('code')
    if status_code is None or status_code[0] == '5':
        return Response(result, int(status_code))

    response = {'photo_url': result['photo_url'],
                'photo_status': status_code }

    return Response(response)


# /api/contacts/<contact-id>/photo-history-urls/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def photo_history_urls(request, contact_id):

    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if contact_id is None:
        return Response({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.photo_history_urls(contact_id, preview=False)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/contacts/photos-urls/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def photos_urls(request):

    controller = contacts_controller.Contacts(request.account)

    result = controller.photos_urls(preview=False)

    status_code = int(result.pop('code'))

    return Response(result, status_code)

# Blocking/Unblocking


# /api/contacts/<contact-id>/block/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def block(request, contact_id):

    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if contact_id is None:
        return Response({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.block(contact_id)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/contacts/<contact-id>/unblock/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def unblock(request, contact_id):

    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if contact_id is None:
        return Response({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.unblock(contact_id)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


def __set_blocked_list (request):

    data = request.data
    if not data:
        return Response({'error': 'No data provided (json:{contacts:[XXXXXX,YYYYYY,ZZZZZZZ]}'}, 400)
    numbers = data.get('contacts')
    if numbers is None or len(numbers) == 0:
        return Response({'error': 'No number provided (json:{contacts:[XXXXXX,YYYYYY,ZZZZZZZ]}'}, 400)
    contacts = normalize_list(numbers)
    if len(numbers) == 0:
        return Response({'error': 'Invalid numbers provided (json:{contacts:[XXXXXX,YYYYYY,ZZZZZZZ]}'}, 400)

    controller = contacts_controller.Contacts(request.account)

    result = controller.set_blocked_list(numbers)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


def __get_blocked_list (request):

    controller = contacts_controller.Contacts(request.account)

    result = controller.get_blocked_list()

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/contacts/blocked-list/
@api_view(['GET', 'POST'])
@protected_resource()
@active_account_required_400()
@parser_classes((JSONParser,))
def blocked_list(request):

    if request.method == 'POST':
        return __set_blocked_list(request)
    return __get_blocked_list(request)



