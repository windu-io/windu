#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from .agent_factory import create_agent
from bulk_update.helper import bulk_update

from .account import Account
from ..models import Contact as ModelContact
from ..models import ContactsFromMessage
from ..models import StatusMessage
from ..models import ProfilePhoto
from ..models import ImageUpload

from ..util.image_uploader import ImageUploader

import hashlib
import mimetypes
import os


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

    @staticmethod
    def __adjust_sync_result(result):

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
        result = Contacts.__adjust_sync_result(result)
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
        for old_contact, new_contact in zip(contacts, contacts_to_update):

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

    @staticmethod
    def contact_valid (account, contact_id):
        controller = Contacts(account)
        return controller.check_contact(contact_id)

    @staticmethod
    def current_contacts(account):
        controller = Contacts(account)
        return controller.__current_contacts()

    def __current_contacts(self):
        return ModelContact.objects.filter(account=self.__account, exists=True).values_list('contact_id', flat=True)

    def __contacts_from_contacts_ids(self, contacts_ids):
        return ModelContact.objects.filter(account=self.__account, contact_id__in=contacts_ids)

    # Check if the contact is valid (was previously synced or sent a message)
    def check_contact(self, contact_id):
        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        if not ModelContact.objects.filter(account=self.__account, contact_id=contact_id, exists=True).exists():
            if not ContactsFromMessage.objects.filter(account=self.__account, contact_id=contact_id).exists():
                return {'error': 'Contact does not exists, you must sync your first or receive a message from him/her', 'code': '400'}

        return {'code': '200'}

    def __update_status_message_history(self, statuses_messages):

        contacts_ids = [status['contact_id'] for status in statuses_messages if status['status_message'] is not None]

        new_statuses_messages = {}

        for s in statuses_messages:
            if s['status_message'] is None:
                continue
            new_statuses_messages[s['contact_id']] = s['status_message']

        contacts = self.__contacts_from_contacts_ids(contacts_ids)

        status_messages = []

        for contact in contacts:
            # Just in case, some contact was deleted
            contact_id = contact.contact_id
            if contact_id not in contacts_ids:
                continue

            current_status_message = contact.status_message
            new_status_message = new_statuses_messages [contact_id]

            if not current_status_message or new_status_message != current_status_message:
                status_messages.append(StatusMessage(contact_id=contact_id,
                                                     status_message=new_status_message,
                                                     account=self.__account))
                contact.status_message = new_status_message

        update_existing = len(status_messages) > 0

        if not update_existing:
            return

        StatusMessage.objects.bulk_create(status_messages)
        bulk_update(contacts, update_fields=['status_message'])

    def status_message_history(self, contact_id):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        result = self.check_contact(contact_id)
        if result.get('code') != '200':
            return result

        values = StatusMessage.objects.filter(account=self.__account, contact_id=contact_id).\
                                       order_by('-updated').\
                                       values('contact_id', 'status_message', 'updated')

        return {'code': '200', 'values': values}

    def __get_statuses_messages(self, contacts):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendGetStatuses(contacts)
        except Exception as e:
            result['error'] = 'Error getting statuses: ' + str(e)
            result['code'] = '500'
        return result

    def status_message(self, contact_id):
        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        result = self.check_contact(contact_id)
        if result.get('code') != '200':
            return result

        contacts = [contact_id]

        result = self.__get_statuses_messages(contacts)
        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        self.__update_status_message_history(result.get('statuses_messages'))

        return result

    def statuses_messages(self):

        contacts = self.__current_contacts()

        result = self.__get_statuses_messages(contacts)
        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        self.__update_status_message_history(result.get('statuses_messages'))

        return result

    def __get_connected_statuses(self, contacts):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendGetPresences(contacts)
        except Exception as e:
            result['error'] = 'Error getting connected status: ' + str(e)
            result['code'] = '500'
        return result

    def __last_connected_status(self, contacts_ids):
        connected_statuses = self.__contacts_from_contacts_ids(contacts_ids)\
            .values('contact_id', 'last_seen', 'connected_status')
        return {'code': '200', 'connected_statuses': connected_statuses}

    def __update_connected_status(self, new_connected_statuses):

        connected_statuses = []
        contacts_ids = new_connected_statuses.keys()

        contacts = self.__contacts_from_contacts_ids(contacts_ids)

        update_existing = False

        for contact in contacts:
            contact_id = contact.contact_id
            current_connected_status = contact.connected_status
            last_seen_str = new_connected_statuses[contact_id]

            if last_seen_str == 'online':
                new_connected_status = 'online'
                last_seen = datetime.datetime.now()
            elif last_seen_str == 'deny':
                new_connected_status = 'deny'
                last_seen = None
            elif last_seen_str.isdigit():
                new_connected_status = 'offline'
                last_seen = datetime.datetime.fromtimestamp(int(last_seen_str))
            else:
                continue

            connected_statuses.append({'contact_id': contact_id,
                                       'last_seen': last_seen,
                                       'connected_status': new_connected_status})

            if not current_connected_status or new_connected_status != current_connected_status:
                contact.connected_status = new_connected_status
                update_existing = True

            if contact.last_seen != last_seen:
                contact.last_seen = last_seen
                update_existing = True

        if not update_existing:
            return

        bulk_update(contacts, update_fields=['last_seen', 'connected_status'])

        return {'code': '200', 'connected_statuses': connected_statuses}

    def connected_status(self, contact_id):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        result = self.check_contact(contact_id)
        if result.get('code') != '200':
            return result

        our_connected_status = Account.account_connected_status(self.__account)

        contacts = [contact_id]

        if our_connected_status != 'online':
            return self.__last_connected_status (contacts)

        result = self.__get_connected_statuses(contacts)
        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        return self.__update_connected_status(result.get('connected_status'))

    def connected_statuses(self):

        contacts = self.__current_contacts()

        our_connected_status = Account.account_connected_status(self.__account)

        if our_connected_status != 'online':
            return self.__last_connected_status (contacts)

        result = self.__get_connected_statuses(contacts)
        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        return self.__update_connected_status(result.get('connected_status'))

# Photo

    def __get_preview_photo_from_server(self, contact_id):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendGetProfilePicturePreview (contact_id)
        except Exception as e:
            result['error'] = 'Error getting profile photo preview: ' + str(e)
            result['code'] = '500'
        return result

    @staticmethod
    def __process_profile_photo (path):

        h = hashlib.sha1()

        file_picture = open(path, "rb")
        picture_data = file_picture.read()
        file_picture.close()
        mime_type = mimetypes.guess_type(path)

        h.update(picture_data)
        digest = h.hexdigest()

        return {
                'code': '200',
                'path': path,
                'picture_data': picture_data,
                'mime_type': mime_type,
                'hash': digest
                }

    def __get_preview_photo(self, contact_id):

        server_result = self.__get_preview_photo_from_server(contact_id)

        status_code = server_result.get('code')
        if status_code is None or status_code[0] != '2':
            return server_result
        path = server_result.get ('filename')
        if not path or not os.path.isfile(path):
            return {'error': 'Profile photo not found', 'code': '404'}

        return Contacts.__process_profile_photo(path)

    @staticmethod
    def __upload_photo(photo_info, uploader):

        photo_hash = photo_info['hash']
        photo = Contacts.__check_uploaded_photo(photo_hash)
        if photo is not None:
            return photo

        return uploader.upload_photo(photo_info['path'])

    @staticmethod
    def __code_to_photo_status (code):
        if code == '404':
            return 'i'
        if code == '401':
            return 'u'
        if code == '200':
            return 'k'
        return None

    @staticmethod
    def __ensure_images_are_uploaded (preview_photo_results):

        uploader = ImageUploader()
        new_images = []
        for contact_id in preview_photo_results:
            photo_info = preview_photo_results[contact_id]
            photo_status = Contacts.__code_to_photo_status(photo_info.get('code'))
            if photo_status != 'k':
                continue

            hash_photo = photo_info.get('hash')
            if ImageUpload.objects.filter(hash=hash_photo).exists():
                continue

            path = photo_info.get('path')
            photo_url = uploader.upload_photo(hash_photo, path)
            new_images.append(ImageUpload(hash=hash_photo, photo_url=photo_url))

        if len(new_images) == 0:
            return

        ImageUpload.objects.bulk_create(new_images)

    def __update_preview_photos_history(self, preview_photo_results):

        Contacts.__ensure_images_are_uploaded(preview_photo_results)

        contact_ids = preview_photo_results.keys()
        contacts = self.__contacts_from_contacts_ids(contact_ids)

        profile_photos = []

        for contact in contacts:

            contact_id = contact.contact_id

            current_photo_status = contact.preview_photo_status
            current_photo_hash = contact.preview_photo_hash
            photo_info = preview_photo_results[contact_id]

            new_photo_status = Contacts.__code_to_photo_status(photo_info.get('code'))
            if not new_photo_status:
                continue

            photo_hash = photo_info.get('hash')

            if current_photo_status != new_photo_status or photo_hash != current_photo_hash:

                contact.preview_photo_status = new_photo_status

                if new_photo_status == 'i' or new_photo_status == 'u':
                    contact.preview_photo = None
                    contact.preview_photo_hash = None
                else:
                    contact.preview_photo = ImageUpload.objects.get(hash=photo_hash)
                    contact.preview_photo_hash = photo_hash

                profile_photos.append(ProfilePhoto(account=self.__account,
                                                   contact_id=contact_id,
                                                   photo=contact.preview_photo,
                                                   photo_status=contact.preview_photo_status,
                                                   preview=True))

        update_existing = len(profile_photos) > 0

        if not update_existing:
            return

        ProfilePhoto.objects.bulk_create(profile_photos)
        bulk_update(contacts, update_fields=['preview_photo', 'preview_photo_hash', 'preview_photo_status'])

    def preview_photo(self, contact_id):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        result = self.check_contact(contact_id)
        if result.get('code') != '200':
            return result

        result = self.__get_preview_photo(contact_id)

        status_code = result.get('code')

        if status_code is None or status_code[0] == '5':
            return result

        photo_data = {contact_id: result}

        self.__update_preview_photos_history(photo_data)

        return result

    def preview_photo_url(self, contact_id):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        result = self.check_contact(contact_id)
        if result.get('code') != '200':
            return result

        contacts = [contact_id]

        result = self.__get_preview_photo_url(contacts)
        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        return self.__update_preview_photos_history(result)

    def preview_photo_history_urls(self, contact_id):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        result = self.check_contact(contact_id)
        if result.get('code') != '200':
            return result
        return None

    def preview_photos_urls(self):

        contacts = self.__current_contacts()

        result = self.__get_preview_photos(contacts)
        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        return self.__update_preview_photos_history(result)

    def __get_photos(self, contact_ids):
        return None

    def __update_photos_history(self, results):
        return None

    def photo(self, contact_id):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        result = self.check_contact(contact_id)
        if result.get('code') != '200':
            return result

        contacts = [contact_id]

        result = self.__get_photos(contacts)
        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        return self.__update_preview_photos_history(result)

    def photo_url(self, contact_id):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        result = self.check_contact(contact_id)
        if result.get('code') != '200':
            return result

        contacts = [contact_id]

        result = self.__get_photos(contacts)
        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        return self.__update_preview_photos_history(result)

    def photo_history_urls(self, contact_id):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        result = self.check_contact(contact_id)
        if result.get('code') != '200':
            return result
        return None

    def photos_urls(self):

        contacts = self.__current_contacts()

        result = self.__get_preview_photos(contacts)
        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        return self.__update_preview_photos_history(result)






