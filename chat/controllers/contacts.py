#! /usr/bin/env python
# -*- coding: utf-8 -*-


from .agent_factory import create_agent
from bulk_update.helper import bulk_update

from ..models import Contact as ModelContact


class Contacts:

    def __init__(self, account):
        self.__account = account

    def list_contacts(self):
        return ModelContact.objects.filter(account=self.__account)

    def __agent(self):
        return create_agent(self.__account)

    def __sync_contacts(self, numbers):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendSync(numbers)
        except Exception as e:
            result['error'] = 'Error syncing contacts: ' + str(e)
            result['code'] = '500'
        return result

    def __adjust_sync_result(self,result):

        ret = {'code': result.get('code')}

        inner_result = result.get('result')
        if inner_result is None:
            return {'code': '500', 'error':'Fail to sync contacts - existence of contacts unknown (1)'}

        existing = inner_result.get('existing')
        non_existing = inner_result.get('nonExisting')

        if existing is None or non_existing is None:
            return {'code': '500', 'error':'Fail to sync contacts - existence of contacts unknown (2)'}

        ret['existing'] = existing.values()
        ret['non_existing'] = non_existing
        return ret

    def sync_contacts(self):

        numbers = []
        contacts = ModelContact.objects.filter(account=self.__account)

        for c in contacts:
            numbers.append(c.contact_id)

        result = self.__sync_contacts(numbers)
        result = self.__adjust_sync_result(result)
        status_code = result.get('code')
        if status_code is None or status_code[0] != '2':
            return result

        for c in contacts:
            c.exists = c.contact_id not in result['non_existing']

        bulk_update(contacts, update_fields=['exists'])
        return result

    def add_contact(self, contact_id, first_name, last_name):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        if ModelContact.objects.filter(account=self.__account, contact_id=contact_id).exists():
            return {'error': 'Contact already exists', 'code': '400'}

        c = ModelContact.objects.create(contact_id=contact_id, first_name=first_name, last_name=last_name, exists=False, account=self.__account)
        result = self.sync_contacts()
        result_code = result.get('code')
        if result_code is None or result_code [0] != '2':
            c.delete()
            return result
        id = c.id
        c = ModelContact.objects.get(id=id)
        ret = {'code': '201', 'contact_id': c.contact_id, 'exists': c.exists}
        return ret

    def remove_contact(self, contact_id):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        if not ModelContact.objects.filter(account=self.__account, contact_id=contact_id).exists():
            return {'error': 'Contact doesn\'t exists', 'code': '400'}

        c = ModelContact.objects.filter(account=self.__account, contact_id=contact_id).first()
        c.delete()

        result = self.sync_contacts()
        result_code = result.get('code')
        if result_code is None or result_code [0] != '2':
            return result
        fail_deleted = contact_id in result['existing'] or contact_id in result['non_existing']
        if fail_deleted:
            return {'code': '500', 'contact_id': contact_id, 'error': 'Contact still synced :-('}
        return {'code': '200', 'removed_contact': contact_id}

    def update_contact(self, contact_id, first_name, last_name):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        if not ModelContact.objects.filter(account=self.__account, contact_id=contact_id).exists():
            return {'error': 'Contact doesn\'t exists', 'code': '400'}

        c = ModelContact.objects.filter(account=self.__account, contact_id=contact_id).first()
        c.first_name = first_name
        c.last_name = last_name
        c.save()
        return {'code':'200', 'updated_contact': contact_id}



