#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser

from oauth2_provider.decorators import protected_resource

from ..controllers import groups as groups_controller
from ..decorators import active_account_required_400

from normalize_id import normalize_list
from normalize_id import normalize


def __get_contact(request):

    contact_id = request.POST.get('contact')
    if not contact_id:
        return {'code': 400, 'error': 'No contact provided (contact=XXXXXX)'}
    contact_id = normalize(contact_id)
    if contact_id is None:
        return {'code': 400, 'error': 'Invalid contact value [contact=XXXXXX]'}
    return {'contact': contact_id, 'code': 200}

# Create/List/Handle groups


# /api/groups/create-group/
@api_view(['POST'])
@protected_resource()
@parser_classes((JSONParser,))
@active_account_required_400()
def create_group(request):
    data = request.data
    if not data:
        return Response({'error': 'No data provided (json:{participants:[XXXXXX, YYYYY], subject:"Subject"}'}, 400)
    participants = data.get('participants')
    subject = data.get('subject')
    if participants is None or len(participants) == 0 or not subject:
        return Response({'error': 'No data provided (json:{participants:[XXXXXX, YYYYY], subject:"Subject"}'}, 400)
    participants = normalize_list(participants, 'contact_id')
    if len(participants) == 0:
        return Response({'error': 'No data provided (json:{participants:[XXXXXX, YYYYY], subject:"Subject"}'}, 400)

    controller = groups_controller.Groups(request.account)

    result = controller.create_group(participants, subject)

    status_code = int(result.pop('code'))

    if status_code == 200:  # Return 'Created' if success
        status_code = 201

    return Response(result, status_code)


# /api/groups/info-all/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def get_info_all(request):

    controller = groups_controller.Groups(request.account)

    result = controller.group_info_all()
    status_code = int(result.pop('code'))
    return Response(result, status_code)


# /api/groups/<group-id>/info/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def get_group_info(request, group_id):

    controller = groups_controller.Groups(request.account)

    result = controller.get_group_info(group_id)
    status_code = int(result.pop('code'))

    return Response(result, status_code)


def __groups_subject (request, group_id):

    controller = groups_controller.Groups(request.account)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        if not subject:
            return Response({'error': 'subject missing'}, 400)
        return controller.update_subject(subject)
    return controller.get_subject(group_id)


# /api/groups/<group-id>/subject/
@api_view(['GET','POST'])
@protected_resource()
@active_account_required_400()
def group_subject(request, group_id):

    result = __groups_subject(request, group_id)
    status_code = int(result.pop('code'))

    return Response(result, status_code)


# #### Group Photo

# /api/groups/<group-id>/preview-photo/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def preview_photo(request, group_id):

    if not group_id:
        return Response({'error': 'No group_id provided (group_id=XXX-XXX)'}, 400)

    controller = groups_controller.Groups(request.account)

    result = controller.photo(group_id, preview=True)

    status_code = int(result.pop('code'))

    if status_code != 200:
        return Response (result, status_code)

    picture_data = result['picture_data']
    mime_type = result['mime_type']
    return HttpResponse (picture_data, mime_type)


# /api/groups/<group-id>/preview-photo-url/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def preview_photo_url(request, group_id):

    if not group_id:
        return Response({'error': 'No group_id provided (group_id=XXX-XXX)'}, 400)

    controller = groups_controller.Groups(request.account)

    result = controller.photo(group_id, preview=True)

    status_code = result.pop('code')
    if status_code is None or status_code[0] == '5':
        return Response(result, int(status_code))

    response = {'photo_url': result['photo_url'],
                'photo_status': status_code }

    return Response(response)


def __get_profile_photo(request, group_id):
    controller = groups_controller.Groups(request.account)

    result = controller.photo(group_id, preview=False)

    status_code = int(result.pop('code'))

    if status_code != 200:
        return Response(result, status_code)

    picture_data = result['picture_data']
    mime_type = result['mime_type']
    return HttpResponse(picture_data, mime_type)


def __update_group_photo(request, group_id):

    photo_file = request.FILES.get ('photo')

    if photo_file is None:
        picture = request.POST.get('url')
    else:
        picture = photo_file.temporary_file_path()

    if picture is None:
        return Response({'error': 'No photo file provided multi-part (photo)'}, 400)

    controller = groups_controller.Groups(request.account)
    result = controller.update_group_photo(group_id, picture)
    status_code = int(result.pop('code'))
    if status_code != 200:
        return Response(result, status_code)

    return Response({}, status_code)


def __delete_group_photo(request, group_id):

    controller = groups_controller.Groups(request.account)
    result = controller.delete_group_photo(group_id)
    status_code = int(result.pop('code'))

    if status_code != 200:
        return Response(result, status_code)

    return Response({}, status_code)


# /api/groups/<group-id>/photo/
@api_view(['GET', 'POST', 'DELETE'])
@protected_resource()
@active_account_required_400()
def photo(request, group_id):

    if not group_id:
        return Response({'error': 'No group_id provided (group_id=XXX-XXX)'}, 400)

    if request.method == 'POST':
        return __update_group_photo(request, group_id)
    if request.method == 'DELETE':
        return __delete_group_photo(request, group_id)
    return __get_profile_photo(request, group_id)


# /api/groups/<group-id>/photo-url/
@api_view(['GET'])
@protected_resource()
@active_account_required_400()
def photo_url(request, group_id):

    if not group_id:
        return Response({'error': 'No group_id provided (group_id=XXX-XXX)'}, 400)

    controller = groups_controller.Groups(request.account)

    result = controller.photo(group_id, preview=False)

    status_code = result.pop('code')
    if status_code is None or status_code[0] == '5':
        return Response(result, int(status_code))

    response = {'photo_url': result['photo_url'],
                'photo_status': status_code }

    return Response(response)


# /api/groups/<group-id>/add-participant/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def add_participant(request, group_id):

    if not group_id:
        return Response({'error': 'No group_id provided (group_id=XXX-XXX)'}, 400)

    result_contact = __get_contact(request)
    if result_contact['code'] != 200:
        return Response(result_contact['error'], result_contact['code'])

    contact = result_contact['contact']

    controller = groups_controller.Groups(request.account)

    result = controller.add_participant(group_id, contact)

    status_code = int(result.pop('code'))

    if status_code != 200:
        return Response(result, status_code)

    return Response({}, status_code)


# /api/groups/<group-id>/remove-participant/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def remove_participant(request, group_id):

    if not group_id:
        return Response({'error': 'No group_id provided (group_id=XXX-XXX)'}, 400)

    result_contact = __get_contact(request)
    if result_contact['code'] != 200:
        return Response(result_contact['error'], result_contact['code'])

    contact = result_contact['contact']

    controller = groups_controller.Groups(request.account)

    result = controller.remove_participant(group_id, contact)

    status_code = int(result.pop('code'))

    if status_code != 200:
        return Response(result, status_code)

    return Response({}, status_code)


# /api/groups/<group-id>/promote-participant/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def promote_participant(request, group_id):

    if not group_id:
        return Response({'error': 'No group_id provided (group_id=XXX-XXX)'}, 400)

    result_contact = __get_contact(request)
    if result_contact['code'] != 200:
        return Response(result_contact['error'], result_contact['code'])

    contact = result_contact['contact']

    controller = groups_controller.Groups(request.account)

    result = controller.promote_participant(group_id, contact)

    status_code = int(result.pop('code'))

    if status_code != 200:
        return Response(result, status_code)

    return Response({}, status_code)


# /api/groups/<group-id>/demote-participant/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def demote_participant(request, group_id):

    if not group_id:
        return Response({'error': 'No group_id provided (group_id=XXX-XXX)'}, 400)

    result_contact = __get_contact(request)
    if result_contact['code'] != 200:
        return Response(result_contact['error'], result_contact['code'])

    contact = result_contact['contact']

    controller = groups_controller.Groups(request.account)

    result = controller.demote_participant(group_id, contact)

    status_code = int(result.pop('code'))

    if status_code != 200:
        return Response(result, status_code)

    return Response({}, status_code)


# /api/groups/<group-id>/leave/
@api_view(['POST'])
@protected_resource()
@active_account_required_400()
def leave_group(request, group_id):

    if not group_id:
        return Response({'error': 'No group_id provided (group_id=XXX-XXX)'}, 400)

    controller = groups_controller.Groups(request.account)

    result = controller.leave_group(group_id)

    status_code = int(result.pop('code'))

    if status_code != 200:
        return Response(result, status_code)

    return Response({}, status_code)
