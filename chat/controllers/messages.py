#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

from datetime import datetime
from django.utils import timezone

from bulk_update.helper import bulk_update

from .agent import get_agent_and_check_events

from .contacts import Contacts

from .events import check_events_now

from .message_store import MessagesStore


class Messages:

    def __init__(self, account):
        self.__account = account

    def __agent(self):
        return get_agent_and_check_events(self.__account)

    def __check_contact(self, contact_id):
        return Contacts.contact_valid(self.__account, contact_id)

    def create_message_model(self, message_data):
        return MessagesStore.create_message_model(self.__account, message_data)

    def __send_message(self, contact_id, message):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendMessage(contact_id, message)
        except Exception as e:
            result['error'] = 'Error sending message: ' + str(e)
            result['code'] = '500'
        return result

    def __send_location(self, contact_id, latitude, longitude, caption):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendMessageLocation(contact_id, latitude, longitude, caption)
        except Exception as e:
            result['error'] = 'Error sending location: ' + str(e)
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

        message_data = {
            'message_id': result.get('id'),
            'entity_id': contact_id,
            'data': message,
            'message_type': 't',
            'send_type': 's',
            'time' : result.get('t')
        }

        self.create_message_model(message_data)

        return {'message_id': result.get('id'), 'code': status_code}

    def __send_image(self, contact_id, filename, caption, file_size = 0, file_hash = ''):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendMessageImage(contact_id, filename, caption, fsize=file_size, fhash=file_hash)
        except Exception as e:
            result['error'] = 'Error sending image: ' + str(e)
            result['code'] = '500'
        return result

    def __send_video(self, contact_id, filename, caption):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendMessageVideo(contact_id, filename, caption)
        except Exception as e:
            result['error'] = 'Error sending video: ' + str(e)
            result['code'] = '500'
        return result

    def __send_audio(self, contact_id, filename, file_size = 0, file_hash='', voice=False):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendMessageAudio(contact_id, filename, voice=voice, file_size=file_size, file_hash=file_hash)
        except Exception as e:
            result['error'] = 'Error sending audio: ' + str(e)
            result['code'] = '500'
        return result

    def __send_image_from_data (self, contact_id, caption, image_data):
        return self.__send_image(contact_id,
                                 image_data['filename'],
                                 caption,
                                 image_data['length'],
                                 image_data['hash'])

    def __send_audio_from_data (self, contact_id, audio_data, voice):
        return self.__send_audio(contact_id,
                                 audio_data['filename'],
                                 audio_data['length'],
                                 audio_data['hash'],
                                 voice)

    @staticmethod
    def __get_image_data(filename, url):
        if filename is not None:
            return MessagesStore.get_image_data_from_file(filename)
        return MessagesStore.get_image_data_from_url(url)

    @staticmethod
    def __get_audio_data(filename, url):
        if filename is not None:
            return MessagesStore.get_audio_data_from_file(filename)
        return MessagesStore.get_audio_data_from_url(url)

    def send_image(self, contact_id, filename, url, caption):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        contact = self.__check_contact(contact_id)
        if contact.get('code') != '200':
            return contact

        image_data = Messages.__get_image_data(filename, url)

        error = image_data.get('error')
        if error is not None:
            return {'error': error, 'code': '400'}

        if caption is None:
            caption = ''

        result = self.__send_image_from_data(contact_id, caption, image_data)

        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        message_data = {
            'message_id': result.get('id'),
            'entity_id': contact_id,
            'data': '',
            'caption': caption,
            'message_type': 'i',
            'send_type': 's',
            'time': result.get('t'),
            'url': image_data.get('url'),
            'file_hash': image_data.get('hash'),
        }

        self.create_message_model(message_data)

        return {'id': result.get('id'), 'code': status_code, 'url': image_data.get('url'), 'hash': image_data.get('hash')}

    def send_location(self, contact_id, latitude, longitude, caption):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        contact = self.__check_contact(contact_id)
        if contact.get('code') != '200':
            return contact

        result = self.__send_location(contact_id, latitude, longitude, caption)

        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        message_data = {
            'message_id': result.get('id'),
            'entity_id': contact_id,
            'data': '',
            'caption': caption,
            'message_type': 'l',
            'send_type': 's',
            'time': result.get('t'),
            'latitude': latitude,
            'longitude': longitude,
        }

        self.create_message_model(message_data)

        return {'id': result.get('id'), 'code':  status_code}

    def send_audio(self, contact_id, filename, url, voice):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        contact = self.__check_contact(contact_id)
        if contact.get('code') != '200':
            return contact

        audio_data = Messages.__get_audio_data(filename, url)

        error = audio_data.get('error')
        if error is not None:
            return {'error': error, 'code': '400'}

        result = self.__send_audio_from_data(contact_id, audio_data, voice)

        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        if voice:
            message_type = 's'
        else:
            message_type = 'a'

        message_data = {
            'message_id': result.get('id'),
            'entity_id': contact_id,
            'data': '',
            'message_type': message_type,
            'send_type': 's',
            'time': result.get('t'),
            'url': audio_data.get('url'),
            'file_hash': audio_data.get('hash'),
        }

        self.create_message_model(message_data)

        return {'id': result.get('id'), 'code': status_code, 'url': audio_data.get('url'), 'hash': audio_data.get('hash')}

    @staticmethod
    def __get_video_path(path, url):
        if path is not None:
                filename, file_extension = os.path.splitext(path)
                allowed_extensions = ['.3gp', '.mp4', '.mov', '.avi']
                file_extension = file_extension.lower()
                if file_extension not in allowed_extensions:
                    return {'error': 'Invalid video extension (3gp, mp4, mov, avi)'}
                return {'path' : path}
        return {'path': url}

    def send_video(self, contact_id, filename, url, caption):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        contact = self.__check_contact(contact_id)
        if contact.get('code') != '200':
            return contact

        path_data = Messages.__get_video_path(filename,url)
        error = path_data.get('error')
        if error is not None:
            return {'error': error, 'code': '400'}

        if caption is None:
            caption = ''

        path = path_data['path']

        result = self.__send_video(contact_id, path, caption)

        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        message_data = {
            'message_id': result.get('id'),
            'entity_id': contact_id,
            'data': '',
            'message_type': 'v',
            'send_type': 's',
            'caption': caption,
            'time': result.get('t'),
        }

        self.create_message_model(message_data)

        return {'id': result.get('id'), 'code':  status_code}

    def __send_vcard(self, contact_id, vcard, name):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendVcard(contact_id, vcard, name)
        except Exception as e:
            result['error'] = 'Error sending vCard: ' + str(e)
            result['code'] = '500'
        return result

    def send_vcard(self, contact_id, vcard, name):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        contact = self.__check_contact(contact_id)
        if contact.get('code') != '200':
            return contact

        if name is None:
            name = ''

        result = self.__send_vcard(contact_id, vcard, name)

        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        message_data = {
            'message_id': result.get('id'),
            'entity_id': contact_id,
            'data': vcard,
            'message_type': 'c',
            'send_type': 's',
            'caption': name,
            'time': result.get('t'),
        }

        self.create_message_model(message_data)

        return {'id': result.get('id'), 'code':  status_code}

    def __set_typing(self, contact_id, typing):
        result = {}
        agent = self.__agent()
        try:
            if typing:
                result = agent.sendMessageComposing(contact_id)
            else:
                result = agent.sendMessagePaused(contact_id)

        except Exception as e:
            result['error'] = 'Error sending typing/paused: ' + str(e)
            result['code'] = '500'
        return result

    def set_typing(self, contact_id, typing):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        contact = self.__check_contact(contact_id)
        if contact.get('code') != '200':
            return contact

        result = self.__set_typing(contact_id, typing)

        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        return result

    def get_messages(self, contact_id, after, limit, offset, received_only):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}

        result = check_events_now(self.__account)

        if result is not None:

            status_code = result.get('code')

            if status_code is None or status_code[0] != '2':
                return result

        messages = MessagesStore.get_messages(self.__account, contact_id, after, limit, offset, received_only)

        return {'code': '200', 'messages': messages}

    def get_delivered_messages(self, contact_id, after, limit, offset):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}

        result = check_events_now(self.__account)

        if result is not None:

            status_code = result.get('code')

            if status_code is None or status_code[0] != '2':
                return result

        messages = MessagesStore.get_delivered_messages(self.__account, contact_id, after, limit, offset)

        return {'code': '200', 'messages': messages}

    def get_read_messages(self, contact_id, after, limit, offset):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}

        result = check_events_now(self.__account)

        if result is not None:

            status_code = result.get('code')

            if status_code is None or status_code[0] != '2':
                return result

        messages = MessagesStore.get_read_messages(self.__account, contact_id, after, limit, offset)

        return {'code': '200', 'messages': messages}

    def __send_message_read(self, contact_id, message_ids):

        result = {}
        agent = self.__agent()
        try:
                result = agent.sendMessageReadBatch(contact_id, message_ids)
        except Exception as e:
            result['error'] = 'Error sending message read: ' + str(e)
            result['code'] = '500'
        return result

    def update_last_read (self, contact_id, date_limit):

        if contact_id is None:
            return {'error': 'Invalid contact_id', 'code': '400'}
        if date_limit is None:
            return {'error': 'Invalid date_limit', 'code': '400'}

        message_ids = []
        messages = MessagesStore.get_unread_received_messages (self.__account, contact_id, date_limit)
        if messages is None:
            return {'code': '200', 'message': 'No message found to mark as read'}

        for message in messages:
            message_ids.append(message.message_id)
            message.read = datetime.utcnow()

        if len(messages) == 0:
            return {'code': '200', 'message': 'No message found to mark as read'}

        result = self.__send_message_read (contact_id, message_ids)

        status_code = result.get('code')

        if status_code is None or status_code[0] != '2':
            return result

        bulk_update(messages, update_fields=['read'])

        return result




