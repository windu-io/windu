
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import Account, User
from ..controllers import account

# Create your views here.
@api_view(['GET', 'POST'])
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
    response = Response (result, status_code)
    response.status_code = status_code
    return response