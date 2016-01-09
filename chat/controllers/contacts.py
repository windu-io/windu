#! /usr/bin/env python
# -*- coding: utf-8 -*-


from .agent_factory import create_agent
from bulk_update.helper import bulk_update

from ..models import Contact as ModelContact


class Contacts:

    def __init__(self, account):
        self.__account = account

    def list_contacts(self):
        return ModelContact.objects.filter(account=self.__account).values('contact_id', 'first_name', 'last_name', 'exists')

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
            return {'code': '500', 'error': 'Fail to sync contacts - existence of contacts unknown (1)'}

        existing = inner_result.get('existing')
        non_existing = inner_result.get('nonExisting')

        if existing is None or non_existing is None:
            return {'code': '500', 'error': 'Fail to sync contacts - existence of contacts unknown (2)'}

        ret['existing'] = existing.values()
        ret['non_existing'] = non_existing
        return ret

    def sync_contacts(self, update_existing=True):

        numbers = []
        contacts = ModelContact.objects.filter(account=self.__account)

        for c in contacts:
            numbers.append(c.contact_id)

        result = self.__sync_contacts(numbers)
        result = self.__adjust_sync_result(result)
        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result
        if update_existing is False:
            return result

        # call bulk_update only if some records has changed
        update_existing = False
        for c in contacts:
            exists = c.contact_id not in result['non_existing']
            if exists != c.exists:
                c.exists = exists
                update_existing = True

        if update_existing:
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

    def remove_contacts(self, contacts):

        total = len(contacts)
        if contacts is None or total < 0:
            return {'error': 'Invalid contacts', 'code': '400'}
        if total == 1:
            return self.remove_contact(contacts[0])

        total_deleted = ModelContact.objects.filter(account=self.__account, contact_id__in=contacts).delete()[0]

        if total_deleted == 0:
            return {'message': 'No contact was deleted', 'code': '200'}
        result = self.sync_contacts(update_existing=False)
        result_code = result.get('code')
        if result_code is None or result_code [0] != '2':
            return result
        return {'code': '200', 'total_deleted': total_deleted}

    def remove_contact(self, contact_id):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        if not ModelContact.objects.filter(account=self.__account, contact_id=contact_id).exists():
            return {'error': 'Contact doesn\'t exists', 'code': '404'}

        c = ModelContact.objects.filter(account=self.__account, contact_id=contact_id).first()
        c.delete()

        result = self.sync_contacts(update_existing=False)
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
            return {'error': 'Contact doesn\'t exists', 'code': '404'}

        c = ModelContact.objects.filter(account=self.__account, contact_id=contact_id).first()
        c.first_name = first_name
        c.last_name = last_name
        c.save()
        return {'code':'200', 'updated_contact': contact_id}

    def __delete_contacts_id_import(self, contacts_id_to_delete):

        if contacts_id_to_delete is None or len(contacts_id_to_delete) == 0:
            return 0

        return ModelContact.objects.filter(account=self.__account, contact_id__in=contacts_id_to_delete).delete()[0]

    def __update_contact_import(self, contacts_to_update):

        total_updated = len(contacts_to_update)
        if contacts_to_update is None or total_updated == 0:
            return 0

        contacts_to_update = sorted(contacts_to_update, key=lambda contact: contact['contact_id'])

        contacts_id = [contact['contact_id'] for contact in contacts_to_update]
        contacts = ModelContact.objects.filter(account=self.__account, contact_id__in=contacts_id).order_by('contact_id')
        update_contacts = False
        for old_contact,new_contact in zip(contacts, contacts_to_update):

            first_name = new_contact.get('first_name')
            last_name = new_contact.get('last_name')

            if old_contact.first_name != first_name:
                old_contact.first_name = first_name
                update_contacts = True

            if old_contact.last_name != last_name:
                old_contact.last_name = last_name
                update_contacts = True

        if not update_contacts:
            return 0

        bulk_update(contacts, update_fields=['first_name', 'last_name'])
        return total_updated

    def __add_contacts_import(self, contacts_to_add):

        total_added = len(contacts_to_add)
        if contacts_to_add is None or total_added == 0:
            return 0

        contacts = []
        for c in contacts_to_add:
            contacts.append(ModelContact(contact_id=c.get('contact_id'),
                                         first_name=c.get('first_name'),
                                         last_name=c.get('last_name'), exists=False,account=self.__account))

        ModelContact.objects.bulk_create(contacts)
        return total_added

    def import_contacts(self, contacts):
        total = len(contacts)
        if contacts is None or total < 0:
            return {'error': 'Invalid contacts', 'code': '400'}

        current = ModelContact.objects.filter(account=self.__account).values_list('contact_id', flat=True)
        contacts_ids = [contact['contact_id'] for contact in contacts]

        new_contacts = set(contacts_ids)
        current_contacts = set(current)

        # Remove non-existent contacts from imported list
        contacts_id_to_delete = list(current_contacts.difference(new_contacts))
        total_deleted = self.__delete_contacts_id_import(contacts_id_to_delete)

        common_set = current_contacts.intersection(new_contacts)
        contacts_to_update = [contact for contact in contacts if contact['contact_id'] in common_set]
        total_updated = self.__update_contact_import(contacts_to_update)

        contacts_to_add_set = new_contacts.difference(common_set)
        contacts_to_add = [contact for contact in contacts if contact['contact_id'] in contacts_to_add_set]
        total_added = self.__add_contacts_import(contacts_to_add)

        # Nothing was changed
        if total_added == 0 and total_deleted == 0 and total_updated == 0:
            return {'code': '200', 'message': 'No contact modified'}

        # Nothing was added/removed
        if total_added == 0 and total_deleted == 0:
            return {'code': '200', 'contacts_updated': total_updated}

        update_existing = total_added > 0

        result = self.sync_contacts(update_existing=update_existing)
        result_code = result.get('code')
        if result_code is None or result_code [0] != '2':
            return result
        existing_count = len(result['existing'])
        non_existing_count = len(result['non_existing'])
        synced = existing_count + non_existing_count

        return {'code': '200', 'added': total_added,
                             'removed': total_deleted,
                             'updated': total_updated,
                              'synced': synced,
                            'existing': existing_count,
                        'non_existing': non_existing_count}

    def list_contact(self, contact_id):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}

        contact = ModelContact.objects.filter(account=self.__account, contact_id=contact_id).first()
        if contact is None:
            return {'error': 'Contact doesn\'t exists', 'code': '404'}

        return {'code': '200',
                'contact_id': contact.contact_id,
                'first_name': contact.first_name,
                'last_name': contact.last_name,
                'exists': contact.exists, }

