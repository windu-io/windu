#! /usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.decorators import api_view
from rest_framework.response import Response
from oauth2_provider.decorators import protected_resource

from ..controllers import account
from ..decorators import active_account_required_400
from django.http import HttpResponseBadRequest


# Create your views here.
@api_view(['GET','POST'])
@protected_resource()
@active_account_required_400()
def status_message(request):

    a = request.account
    controller = account.Account(a)

    if request.method == 'GET':
        result = controller.status_message ()
    elif request.method == 'POST':
        status = request.POST.get('status_message')
        if not status:
            return Response ('status_message missing', 400)
        result = controller.update_status_message (status)

    status_code = int (result.pop ("code"))

    if status_code == 200 and request.method == 'GET':
        result = {'status_message' : result ['statuses'][0]['data']}

    response = Response(result, status_code)
    response.status_code = status_code
    return response
