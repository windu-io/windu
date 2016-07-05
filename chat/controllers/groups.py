#! /usr/bin/env python
# -*- coding: utf-8 -*-


from .agent_factory import create_agent

from ..controllers.contacts import Contacts
from ..util.file_process import process_file

import os


class Groups:

    def __init__(self, account):
        self.__account = account

    def __agent(self):
        return create_agent(self.__account)

    def __check_contact(self, contact_id):
        return Contacts.contact_valid(self.__account, contact_id)

    def __create_group (self, participants, subject):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendGroupsChatCreate(subject, participants)
        except Exception as e:
            result['error'] = 'Error creating group: ' + str(e)
            result['code'] = '500'
        return result

    def create_group(self, participants, subject):
        participants = Contacts.existing_contacts_from_ids(self.__account, participants)
        return self.__create_group(participants, subject)

    def __group_info_all (self):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendGetGroups()
        except Exception as e:
            result['error'] = 'Error getting groups info: ' + str(e)
            result['code'] = '500'
        return result

    def group_info_all(self):
        return self.__group_info_all()

    def __get_group_info (self, group_id):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendGetGroupInfo(group_id)
        except Exception as e:
            result['error'] = 'Error getting group info: ' + str(e)
            result['code'] = '500'
        return result

    def get_group_info(self, group_id):
        return self.__get_group_info(group_id)

    def get_subject (self, group_id):
        result = self.__get_group_info(group_id)
        code = result.get('code')
        if code != '200':
            return result
        return {'code': '200', 'subject': result.get('subject')}

    def __update_subject(self, group_id, subject):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendSetGroupSubject(group_id, subject)
        except Exception as e:
            result['error'] = 'Error updating groups subject: ' + str(e)
            result['code'] = '500'
        return result

    def update_subject (self, group_id, subject):
        return self.__update_subject(group_id, subject)

    def __update_group_photo(self, group_id, picture):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendSetGroupPicture(group_id, picture)
        except Exception as e:
            result['error'] = 'Error updating group photo: ' + str(e)
            result['code'] = '500'
        return result

    def update_group_photo(self, group_id, picture):
        return self.__update_group_photo(group_id, picture)

    def __delete_group_photo(self, group_id):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendRemoveGroupPicture(group_id)
        except Exception as e:
            result['error'] = 'Error removing group photo: ' + str(e)
            result['code'] = '500'
        return result

    def delete_group_photo (self, group_id):
        return self.__delete_group_photo(group_id)

    def __get_photo_from_server(self, contact_id, preview):
        result = {}
        agent = self.__agent()
        try:
            if preview:
                result = agent.sendGetProfilePicturePreview(contact_id)
            else:
                result = agent.sendGetProfilePicture(contact_id)
        except Exception as e:
            result['error'] = 'Error getting group photo preview: ' + str(e)
            result['code'] = '500'
        return result

    def __get_photo(self, contact_id, preview):

        server_result = self.__get_photo_from_server(contact_id, preview)

        status_code = server_result.get('code')
        if status_code is None or status_code[0] != '2':
            return server_result
        path = server_result.get('filename')
        if not path or not os.path.isfile(path):
            return {'error': 'Group photo not found', 'code': '404'}

        return process_file(path)

    def photo(self, group_id, preview):

        if group_id is None:
            return {'error': 'Invalid group_id', 'code': '400'}

        photo = self.__get_photo(group_id, preview=preview)

        photo_data = {group_id: photo}

        Contacts.ensure_images_are_uploaded(photo_data)

        return photo

    def __add_participant(self, group_id, contact_id):

        result = {}
        agent = self.__agent()
        try:
            result = agent.sendGroupsParticipantAdd(group_id, contact_id)
        except Exception as e:
            result['error'] = 'Error adding participant to the group: ' + str(e)
            result['code'] = '500'
        return result

    def add_participant(self, group_id, contact_id):

        if group_id is None:
            return {'error': 'Invalid group_id', 'code': '400'}
        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}

        contact = self.__check_contact(contact_id)
        if contact.get('code') != '200':
            return contact

        return self.__add_participant(group_id, contact_id)

    def __remove_participant(self, group_id, contact_id):

        result = {}
        agent = self.__agent()
        try:
            result = agent.sendGroupsParticipantRemove(group_id, contact_id)
        except Exception as e:
            result['error'] = 'Error removing participant to the group: ' + str(e)
            result['code'] = '500'
        return result

    def remove_participant(self, group_id, contact_id):

        if group_id is None:
            return {'error': 'Invalid group_id', 'code': '400'}
        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}

        return self.__remove_participant(group_id, contact_id)

    def __promote_participant(self, group_id, contact_id):

        result = {}
        agent = self.__agent()
        try:
            result = agent.sendPromoteParticipant(group_id, contact_id)
        except Exception as e:
            result['error'] = 'Error promoting participant to the group: ' + str(e)
            result['code'] = '500'
        return result

    def promote_participant(self, group_id, contact_id):

        if group_id is None:
            return {'error': 'Invalid group_id', 'code': '400'}
        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}

        return self.__promote_participant(group_id, contact_id)

    def __demote_participant(self, group_id, contact_id):

        result = {}
        agent = self.__agent()
        try:
            result = agent.sendDemoteParticipant(group_id, contact_id)
        except Exception as e:
            result['error'] = 'Error demoting participant to the group: ' + str(e)
            result['code'] = '500'
        return result

    def demote_participant(self, group_id, contact_id):

        if group_id is None:
            return {'error': 'Invalid group_id', 'code': '400'}
        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}

        return self.__demote_participant(group_id, contact_id)

    def __leave_group(self, group_id):

        result = {}
        agent = self.__agent()
        try:
            result = agent.sendGroupsLeave(group_id)
        except Exception as e:
            result['error'] = 'Error leaving group: ' + str(e)
            result['code'] = '500'
        return result

    def leave_group(self, group_id):

        if group_id is None:
            return {'error': 'Invalid group_id', 'code': '400'}

        return self.__leave_group(group_id)






