#! /usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.decorators import api_view
from rest_framework.response import Response
from oauth2_provider.decorators import protected_resource

from ..controllers import user
from ..decorators import active_account_required_400
from ..decorators import pending_account_required_400
from ..decorators import account_to_remove_required_400

from normalize_id import normalize

from django.http import HttpResponse

import mimetypes
import os


# /api/user/create-user
@api_view(['POST'])
def create_user(request):
    username = request.POST.get('username')
    if not username:
        return Response({'error': 'No username provided [username=<username>]'}, 400)
    email = request.POST.get('email')
    if not email:
            return Response({'error': 'No email provided [email=<your-email@some.com>]'}, 400)

    password = request.POST.get('password')
    if not password:
        return Response({'error': 'No password provided [password=<password>]'}, 400)

    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')

    result = user.User.create_user(username, password, email, first_name, last_name)
    status_code = int(result.pop('code'))
    if status_code == 200:  # Return 'Created' if success
        status_code = 201
    return Response(result, status_code)


# /api/user/update-user
@api_view(['POST'])
@protected_resource()
def update_user(request):
    pass


# /api/user/confirm-email
@api_view(['GET'])
@protected_resource()
def confirm_email(request):
    pass


# /api/user/confirm-email
@api_view(['GET'])
@protected_resource()
def remove_user(request):
    pass


# /api/user/confirm-email
@api_view(['POST'])
def reset_password(request):
    pass


# /api/user/update-reset-password
@api_view(['POST'])
def update_reset_password(request):
    pass


