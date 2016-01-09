#! /usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.decorators import api_view
from rest_framework.response import Response
from oauth2_provider.decorators import protected_resource

from ..controllers import account
from ..decorators import active_account_required_400
from ..decorators import pending_account_required_400
from ..decorators import account_to_remove_required_400

from normalize_id import normalize

from django.http import HttpResponse

import mimetypes
import os


# /api/account/status-message
@api_view(['GET','POST'])
@protected_resource()
@active_account_required_400()
def status_message(request):

    controller = account.Account(request.account)

    if request.method == 'GET':
        result = controller.status_message ()
    elif request.method == 'POST':
        status = request.POST.get('status_message')
        if not status:
            return Response({'error':'status_message missing'}, 400)
        result = controller.update_status_message (status)

    status_code = int (result.pop('code'))

    if status_code == 200 and request.method == 'GET':
        result = {'status_message' : result ['statuses'][0]['data']}

    response = Response(result, status_code)
    response.status_code = status_code
    return response


# /api/account/profile-photo
@api_view(['GET','POST','DELETE'])
@protected_resource()
@active_account_required_400()
def profile_photo(request):
    if request.method == 'POST':
        return __update_profile_photo (request)
    if request.method == 'DELETE':
        return __delete_profile_photo (request)
    return __get_profile_photo (request)


def __get_profile_photo(request):

    controller = account.Account(request.account)
    result = controller.profile_photo()
    status_code = int(result.pop('code'))
    if status_code != 200:
        result.pop ('type')
        result.pop ('from')
        result.pop ('id')
        return Response (result, status_code)

    picture = result.get ('filename')
    if not picture or not os.path.isfile(picture):
        return Response({'error':'Profile photo not found'}, 404)
    picture_data = open(picture, "rb").read()
    mime_type = mimetypes.guess_type(picture)
    return HttpResponse (picture_data, mime_type)


def __update_profile_photo(request):
    photo_file = request.FILES.get ('photo')
    if photo_file is None:
        return Response({'error':'No photo file provided multi-part (photo)'}, 400)

    picture = photo_file.temporary_file_path()
    controller = account.Account(request.account)
    result = controller.update_profile_photo(picture)
    status_code = int(result.pop('code'))
    return Response(result, status_code)


def __delete_profile_photo(request):
    controller = account.Account(request.account)
    result = controller.remove_profile_photo()
    status_code = int(result.pop('code'))
    return Response(result, status_code)


# /api/account/connected-status
@api_view(['POST', 'GET'])
@protected_resource()
@active_account_required_400()
def connected_status(request):
    if request.method == 'POST':
        return __update_connected_status (request)
    return __get_connected_status (request)


def __update_connected_status(request):

    status = request.POST.get('status')
    if not status:
        return Response ({'error':'status missing (status=[online|offline])'}, 400)
    if status != 'online' and status != 'offline':
        return Response ({'error':'status wrong value (status=[online|offline])'}, 400)

    controller = account.Account(request.account)
    result = controller.update_connected_status(status)
    status_code = int (result.pop('code'))
    return Response (result, status_code)


def __get_connected_status(request):
    controller = account.Account(request.account)
    result = controller.connected_status()
    status_code = int (result.pop('code'))
    return Response (result, status_code)


# /api/account/nickname
@api_view(['POST','GET'])
@protected_resource()
@active_account_required_400()
def nickname(request):
    if request.method == 'POST':
        return __update_nickname(request)
    return __get_nickname(request)


def __update_nickname(request):

    nick = request.POST.get('nickname')
    if nick is None:
        return Response ({'error':'nickname missing (nickname)'}, 400)

    controller = account.Account(request.account)
    result = controller.update_nickname(nick)
    status_code = int (result.pop('code'))
    return Response (result, status_code)


def __get_nickname(request):
    controller = account.Account(request.account)
    result = controller.nickname()
    status_code = int (result.pop('code'))
    return Response (result, status_code)


# /api/account/privacy-settings
@api_view(['POST','GET'])
@protected_resource()
@active_account_required_400()
def privacy_settings(request):
    if request.method == 'POST':
        return __update_privacy_settings(request)
    return __get_privacy_settings(request)


def __is_privacy_setting_valid(setting):
    return setting == 'contacts' or setting == 'all' or setting == 'none'


def __update_privacy_settings(request):

    status_message = request.POST.get('status_message')
    photo = request.POST.get('photo')
    last_seen = request.POST.get('last_seen')
    if not status_message and not photo and not last_seen:
        return Response ({'error':'No privacy setting provided (status_message, photo, last_seen)'}, 400)

    if status_message is not None and not __is_privacy_setting_valid(status_message):
        return Response ({'error':'Invalid status_message value [all|contacts|none]'}, 400)
    if photo is not None and not __is_privacy_setting_valid(photo):
        return Response ({'error':'Invalid photo value [all|contacts|none]'}, 400)
    if last_seen is not None and not __is_privacy_setting_valid(last_seen):
        return Response ({'error':'Invalid last_seen value [all|contacts|none]'}, 400)

    settings = {}

    if status_message is not None:
        settings ['status_message'] = status_message
    if photo is not None:
        settings ['photo'] = photo
    if last_seen is not None:
        settings ['last_seen'] = last_seen

    controller = account.Account(request.account)
    result = controller.update_privacy_settings(settings)
    status_code = int(result.pop('code'))
    return Response(result, status_code)


def __get_privacy_settings(request):
    controller = account.Account(request.account)
    result = controller.privacy_settings()
    status_code = int(result.pop('code'))
    return Response(result, status_code)


# /api/account/create-account
@api_view(['POST'])
@protected_resource()
def create_account(request):
    number = str(request.POST.get('account'))
    if not number:
        return Response({'error':'No account number provided [account=<account number>]'}, 400)

    number = normalize(number)
    if not number or not number.isdigit():
        return Response ({'error':'Invalid account number [number=<account number>]'}, 400)

    nickname = request.POST.get('nickname')
    user = request.resource_owner
    result = account.Account.create_account(number, nickname, user)
    status_code = int(result.pop('code'))
    if status_code == 200:                # Return 'Created' if success
        status_code = 201
    return Response(result, status_code)


# /api/account/request-sms-code
@api_view(['POST'])
@protected_resource()
@pending_account_required_400()
def request_sms_code(request):
    controller = account.Account(request.account)
    result = controller.request_sms_code()
    status_code = int(result.pop('code'))
    return Response(result, status_code)


# /api/account/request-voice-code
@api_view(['POST'])
@protected_resource()
@pending_account_required_400()
def request_voice_code(request):
    controller = account.Account(request.account)
    result = controller.request_voice_code()
    status_code = int(result.pop('code'))
    return Response(result, status_code)


# /api/account/register-code
@api_view(['POST'])
@protected_resource()
@pending_account_required_400()
def register_code(request):
    code = str(request.POST.get('code'))
    if not code:
        return Response({'error': 'No code provided [code=<code received from SMS>]'}, 400)

    code = normalize(code)
    if not code or not code.isdigit():
        return Response ({'error':'Invalid account number [code=<code received from SMS>]'}, 400)

    controller = account.Account(request.account)
    result = controller.register_code(code)
    status_code = int(result.pop('code'))
    return Response(result, status_code)


# /api/account/remove-account
@api_view(['POST'])
@protected_resource()
@account_to_remove_required_400()
def remove_account(request):
    feedback = request.POST.get('feedback')
    controller = account.Account(request.account)
    result = controller.remove_account(feedback)
    status_code = int (result.pop('code'))
    return Response(result, status_code)



