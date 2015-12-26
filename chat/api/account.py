from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse

from ..models import Account
from ..controllers import account

# Create your views here.


def status_message(request):

    ac = Account.objects.first()

    controller = account.Account (ac.id, ac)
    if request.method == 'GET':
        result = controller.status_message ()
    elif request.method == 'POST':
        status_message = request.POST ['status_message']
        result = controller.update_status_message (status_message)
    status_code = result.pop ("code")
    response =  JsonResponse (result)
    response.status_code = status_code
    return response