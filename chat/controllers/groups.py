#! /usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import timedelta
from datetime import datetime

from django.utils import timezone
from django.db.models import Q

from .agent_factory import create_agent
from bulk_update.helper import bulk_update

from windu.settings import WINDU_PROFILE_PHOTO_CACHE_MINUTES

from ..controllers.contacts import Contacts
from .account import Account
from ..models import Contact as ModelContact
from ..models import ContactsFromMessage
from ..models import StatusMessage
from ..models import ProfilePhoto
from ..models import FileUpload

from ..util.image_uploader import ImageUploader
from ..util.file_process import process_file

import os


class Groups:

    def __init__(self, account):
        self.__account = account

    def __agent(self):
        return create_agent(self.__account)

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




