#! /usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser


from oauth2_provider.decorators import protected_resource

from ..controllers import contacts
from ..decorators import active_account_required_400

from normalize_id import normalize


# /api/contacts/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def list_contacts(request):

    controller = contacts.Contacts(request.account)

    c = controller.list_contacts()

    return Response(c)


# /api/contacts/add-contact/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def add_contact(request):
    contact_id = str(request.POST.get('contact_id'))
    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if not contact_id or not contact_id.isdigit():
        return Response({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')

    controller = contacts.Contacts(request.account)

    result = controller.add_contact(contact_id, first_name, last_name)

    status_code = int(result.pop('code'))

    if status_code == 200:                # Return 'Created' if success
        status_code = 201
    return Response(result, status_code)


# /api/contacts/<contact-id>/remove/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def remove_contact(request, contact_id):

    contact_id = str(request.POST.get('contact_id'))
    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    contact_id = normalize(contact_id)
    if not contact_id or not contact_id.isdigit():
        return Response ({'error': 'Invalid contact_id value [contact_id=XXXXXX]'}, 400)

    controller = contacts.Contacts(request.account)

    result = controller.remove_contact(contact_id)

    status_code = int(result.pop('code'))

    return Response(result, status_code)


# /api/contacts/<contact-id>/update/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def update_contact(request, contact_id):
    contact_id = str(request.POST.get('contact_id'))
    if not contact_id:
        return Response({'error': 'No contact_id provided (contact_id=XXXXXX)'}, 400)
    return Response()


# /api/contacts/remove-contacts/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def remove_contacts(request):
    return Response()


# /api/contacts/import-contacts/
@api_view(['POST'])
@protected_resource()
@parser_classes((JSONParser,))
@active_account_required_400()
def import_contacts(request):
    return Response()



