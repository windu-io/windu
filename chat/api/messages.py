#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.parser import parse

from os.path import isfile

from rest_framework.decorators import api_view
from rest_framework.response import Response

from oauth2_provider.decorators import protected_resource

from ..controllers import messages as messages_controller
from ..decorators import active_account_required_400

from normalize_id import normalize


def __get_contact(request):

    contact_id = request.POST.get('contact')
    if not contact_id:
        return {'code': 400, 'error': 'No contact provided (contact=XXXXXX)'}
    contact_id = normalize(contact_id)
    if contact_id is None:
        return {'code': 400, 'error': 'Invalid contact value [contact=XXXXXX]'}
    return {'contact': contact_id, 'code': 200}


def __get_group(request):

    group_id = request.POST.get('group_id')
    if not group_id:
        return {'code': 400, 'error': 'No group id provided (group_id=XXXXXX)'}
    return {'group_id': group_id, 'code': 200}


def __get_target(request):

    contact = __get_contact(request)
    if contact.get('code') == 200:
        return {'target': contact['contact'], 'code': 200, 'is_group': False}

    group = __get_group(request)
    if group.get('code') == 200:
        return {'target': group['group_id'], 'code': 200, 'is_group': True}
    return contact


def __get_message(request):

    message = request.POST.get('message')
    if not message or len(message) == 0:
        return {'code': 400, 'error': 'No message provided (message=XXXXXX)'}
    return {'message': message, 'code': 200}


def __get_date_limit(request):

    date_limit = request.POST.get('date_limit')
    if not date_limit:
        return datetime.utcnow()
    if date_limit.isdigit():
        return datetime.utcfromtimestamp(int(date_limit))
    return parse(date_limit)


def __get_latitude(request):

    latitude = request.POST.get('latitude')
    if not latitude or len(latitude) == 0:
        return {'code': 400, 'error': 'No latitude provided (latitude=XXXXXX)'}
    return {'latitude': latitude, 'code': 200}


def __get_longitude(request):

    longitude = request.POST.get('longitude')
    if not longitude or len(longitude) == 0:
        return {'code': 400, 'error': 'No longitude provided (longitude=XXXXXX)'}
    return {'longitude': longitude, 'code': 200}


# /api/message/send-message/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def send_message(request):

    result_target = __get_target(request)
    if result_target['code'] != 200:
        return Response(result_target['error'], result_target['code'])
    target = result_target['target']
    is_group = result_target['is_group']

    result_message = __get_message(request)
    if result_message['code'] != 200:
        return Response(result_message['error'], result_message['code'])
    message = result_message['message']

    controller = messages_controller.Messages(request.account)

    result = controller.send_message(target, message, is_group)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


def __get_uploaded_filename(request):
    temp_filename = request.FILES.get ('filename')
    if temp_filename is None:
        return None
    return temp_filename.temporary_file_path()


def __get_url(request):
    return request.POST.get ('url')


def __get_vcard(request):
    return request.POST.get ('vcard')

def __get_name(request):
    return request.POST.get ('name')


def __get_caption(request):
    return request.POST.get ('caption')


# /api/message/send-image/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def send_image(request):

    result_target = __get_target(request)
    if result_target['code'] != 200:
        return Response(result_target['error'], result_target['code'])

    target = result_target['target']
    is_group = result_target['is_group']

    url = None
    filename = __get_uploaded_filename(request)
    if filename is None:
        url = __get_url(request)

    if filename is None and url is None:
        return Response('No image provided, you must pass a file (filename) or a url as parameter', 400)

    caption = __get_caption(request)

    controller = messages_controller.Messages(request.account)

    result = controller.send_image(target, filename, url, caption, is_group)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/message/send-location/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def send_location(request):

    result_target = __get_target(request)
    if result_target['code'] != 200:
        return Response(result_target['error'], result_target['code'])

    target = result_target['target']
    is_group = result_target['is_group']

    result_latitude = __get_latitude(request)
    if result_target['code'] != 200:
        return Response(result_latitude['error'], result_latitude['code'])
    latitude = result_latitude['latitude']

    result_longitude = __get_longitude(request)
    if result_longitude['code'] != 200:
        return Response(result_longitude['error'], result_longitude['code'])
    longitude = result_longitude['longitude']

    caption = __get_caption(request)

    controller = messages_controller.Messages(request.account)

    result = controller.send_location(target, latitude, longitude, caption, is_group)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/message/send-audio/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def send_audio(request):
    return __send_voice(request, voice=False)


# /api/message/send-voice/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def send_voice(request):
    return __send_voice(request, voice=True)


def __send_voice(request, voice):

    result_target = __get_target(request)
    if result_target['code'] != 200:
        return Response(result_target['error'], result_target['code'])

    target = result_target['target']
    is_group = result_target['is_group']

    url = None
    filename = __get_uploaded_filename(request)
    if filename is None:
        url = __get_url(request)

    if filename is None and url is None:
        return Response('No audio provided, you must pass a file (filename) or a url as parameter', 400)

    controller = messages_controller.Messages(request.account)

    result = controller.send_audio(target, filename, url, voice, is_group)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/message/send-video/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def send_video(request):
    result_target = __get_target(request)
    if result_target['code'] != 200:
        return Response(result_target['error'], result_target['code'])

    target = result_target['target']
    is_group = result_target['is_group']

    url = None
    filename = __get_uploaded_filename(request)
    if filename is None:
        url = __get_url(request)

    if filename is None and url is None:
        return Response('No video provided, you must pass a file (filename) or a url as parameter', 400)

    caption = __get_caption(request)

    controller = messages_controller.Messages(request.account)

    result = controller.send_video(target, filename, url, caption, is_group)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


def __get_vcard_content(filename, vcard):
    if not filename or not isfile(filename):
        return vcard
    with open(filename, 'r') as vcard_file:
        vcard = vcard_file.read().decode('utf-8')
    return vcard


# /api/message/send-vcard/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def send_vcard(request):

    result_target = __get_target(request)
    if result_target['code'] != 200:
        return Response(result_target['error'], result_target['code'])

    target = result_target['target']
    is_group = result_target['is_group']

    vcard = None
    filename = __get_uploaded_filename(request)
    if filename is None:
        vcard = __get_vcard(request)

    vcard = __get_vcard_content(filename, vcard)

    if vcard is None:
        return Response('No vCard provided, you must pass a vCard file (filename) or a vcard as parameter (vcard)', 400)

    name = __get_name(request)

    controller = messages_controller.Messages(request.account)

    result = controller.send_vcard(target, vcard, name, is_group)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


def __set_typing(request, typing):
    result_target = __get_target(request)
    if result_target['code'] != 200:
        return Response(result_target['error'], result_target['code'])

    target = result_target['target']
    is_group = result_target['is_group']

    controller = messages_controller.Messages(request.account)

    result = controller.set_typing(target, typing, is_group)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/message/set-paused/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def set_paused(request):
    return __set_typing(request, typing=False)


# /api/message/set-typing/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def set_typing(request):
    return __set_typing(request, typing=True)


def __get_messages_after(request):
    after = request.GET.get('after')
    if not after:
        return datetime.utcfromtimestamp(0)
    if after.isdigit():
        return datetime.utcfromtimestamp(int(after))
    return parse(after)


def __get_messages_offset(request):
    offset = request.GET.get('offset')
    if offset is None or not offset.isdigit():
        return 0
    return int(offset)


def __get_messages_limit(request):
    limit = request.GET.get('limit')
    if limit is None or not limit.isdigit():
        return 20
    return int(limit)


def __get_messages_received_only(request):
    received_only = request.GET.get('received_only')
    if received_only is None or received_only != '1':
        return False
    return True


# /api/message/chats/<contact-id>/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def get_messages(request, target_id):

    after = __get_messages_after(request)
    offset = __get_messages_offset(request)
    limit = __get_messages_limit(request)
    received_only = __get_messages_received_only(request)

    controller = messages_controller.Messages(request.account)

    result = controller.get_messages(target_id, after, limit, offset, received_only)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/message/update-last-read/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def update_last_read(request):

    result_contact = __get_contact(request)
    if result_contact['code'] != 200:
        return Response(result_contact['error'], result_contact['code'])
    contact = result_contact['contact']

    date_limit = __get_date_limit(request)

    controller = messages_controller.Messages(request.account)

    result = controller.update_last_read (contact, date_limit)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/message/delivered/<contact-id>/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def get_delivered_messages(request, contact_id):

    after = __get_messages_after(request)
    offset = __get_messages_offset(request)
    limit = __get_messages_limit(request)

    controller = messages_controller.Messages(request.account)

    result = controller.get_delivered_messages(contact_id, after, limit, offset)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/message/read/<contact-id>/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def get_read_messages(request, contact_id):

    after = __get_messages_after(request)
    offset = __get_messages_offset(request)
    limit = __get_messages_limit(request)

    controller = messages_controller.Messages(request.account)

    result = controller.get_read_messages(contact_id, after, limit, offset)

    status_code = int(result.pop('code'))

    return Response(result, status_code)



