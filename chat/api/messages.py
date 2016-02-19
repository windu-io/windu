#! /usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

from django.http import HttpResponse

from oauth2_provider.decorators import protected_resource

from ..controllers import messages as messages_controller
from ..decorators import active_account_required_400

from normalize_id import normalize


def __get_contact (request):

    contact_id = request.POST.get('contact')
    if not contact_id:
        return {'code': 400, 'error': 'No contact provided (contact=XXXXXX)'}
    contact_id = normalize(contact_id)
    if contact_id is None:
        return {'code': 400, 'error': 'Invalid contact value [contact=XXXXXX]'}
    return {'contact': contact_id, 'code': 200}


def __get_message(request):

    message = request.POST.get('message')
    if not message or len(message) == 0:
        return {'code': 400, 'error': 'No message provided (message=XXXXXX)'}
    return {'message': message, 'code': 200}


# /api/message/send-message/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def send_message(request):

    result_contact = __get_contact(request)
    if result_contact['code'] != 200:
        return Response(result_contact['error'], result_contact['code'])
    contact = result_contact['contact']

    result_message = __get_message(request)
    if result_message['code'] != 200:
        return Response(result_message['error'], result_message['code'])
    message = result_message['message']

    controller = messages_controller.Messages(request.account)

    result = controller.send_message (contact, message)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


def __get_uploaded_filename(request):
    temp_filename =  request.FILES.get ('filename')
    if temp_filename is None:
        return None
    return temp_filename.temporary_file_path()


def __get_url(request):
    return request.POST.get ('url')


def __get_caption(request):
    return request.POST.get ('caption')


# /api/message/send-image/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def send_image(request):

    result_contact = __get_contact(request)
    if result_contact['code'] != 200:
        return Response(result_contact['error'], result_contact['code'])
    contact = result_contact['contact']

    url = None
    filename = __get_uploaded_filename(request)
    if filename is None:
        url = __get_url(request)

    if filename is None and url is None:
        return Response('No image provided, you must pass a file (filename) or a url as parameter', 400)

    caption = __get_caption(request)

    controller = messages_controller.Messages(request.account)

    result = controller.send_image (contact, filename, url, caption)

    status_code = int(result.pop('code'))

    return Response(result, status_code)