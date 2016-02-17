#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils import timezone
from .agent import get_agent_and_check_events

from .contacts import Contacts
from ..models import Account as ModelAccount
from ..models import Message
from ..models import MessageGroupRead


class Messages:

    def __init__(self, account):
        self.__account = account

    def __agent(self):
        return get_agent_and_check_events(self.__account)

    def __check_contact(self, contact_id):
        return Contacts.contact_valid(self.__account, contact_id)

    def __update_message_store(self, result):
        pass

    def __send_message (self, contact_id, message):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendMessage(contact_id, message)
        except Exception as e:
            result['error'] = 'Error getting statuses: ' + str(e)
            result['code'] = '500'
        return result

    def send_message(self, contact_id, message):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        contact = self.__check_contact(contact_id)
        if contact.get('code') != '200':
            return contact

        result = self.__send_message(contact_id, message)

        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        self.__update_message_store (result)

        return result
