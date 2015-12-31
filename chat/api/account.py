#! /usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.decorators import api_view
from rest_framework.response import Response
from oauth2_provider.decorators import protected_resource

from ..controllers import account
from ..decorators import active_account_required_400

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
            return Response ({'error':'status_message missing'}, 400)
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
    status_code = int (result.pop('code'))
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
    status_code = int (result.pop('code'))
    return Response (result, status_code)


def __delete_profile_photo(request):
    controller = account.Account(request.account)
    result = controller.remove_profile_photo()
    status_code = int (result.pop('code'))
    return Response (result, status_code)
