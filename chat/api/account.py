from django.http import HttpResponse
from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Account, User
from ..controllers import account

# Create your views here.

def status_message(request):

    user = User.objects.get(id=2)
    ac = Account.objects.filter(user=user).first()

    controller = account.Account (ac.id, ac)
    if request.method == 'GET':
        result = controller.status_message ()
    elif request.method == 'POST':
        status_message = request.POST ['status_message']
        result = controller.update_status_message (status_message)

    status_code = int (result.pop ("code"))
    if status_code == 200 and request.method == 'GET':
        result = {'status_message' : result ['statuses'][0]['data']}
    response =  JsonResponse (result)
    response.status_code = status_code
    return response