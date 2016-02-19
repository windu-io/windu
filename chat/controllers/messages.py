#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils import timezone
from .agent import get_agent_and_check_events

from .contacts import Contacts
from ..models import Account as ModelAccount
from ..models import Message
from ..models import MessageGroupRead
from ..models import ImageUpload

from ..util.image_uploader import ImageUploader
from ..util.file_process import process_file

import os

class Messages:

    def __init__(self, account):
        self.__account = account

    def __agent(self):
        return get_agent_and_check_events(self.__account)

    def __check_contact(self, contact_id):
        return Contacts.contact_valid(self.__account, contact_id)

    def __update_message_store(self, result):
        pass

    def __send_message(self, contact_id, message):
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

    def __send_image(self, contact_id, filename, caption, file_size = 0, file_hash = ''):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendMessageImage(contact_id, filename, caption, fsize=file_size, fhash=file_hash)
        except Exception as e:
            result['error'] = 'Error getting statuses: ' + str(e)
            result['code'] = '500'
        return result

    def __send_image_from_data (self, contact_id, caption, image_data):
        return self.__send_image(contact_id,
                                 image_data['filename'],
                                 caption,
                                 image_data['length'],
                                 image_data['hash'])


    @staticmethod
    def __ensure_image_uploaded(file_info):

        uploader = ImageUploader()
        hash_image = file_info.get('hash')
        image_upload = ImageUpload.objects.filter(hash=hash_image).first()

        if image_upload is not None:
            return image_upload.photo_url

        path = file_info.get('path')
        image_url = uploader.upload_photo(path)
        image_upload = ImageUpload.objects.create(hash=hash_image, photo_url=image_url)

        return image_upload.photo_url

    @staticmethod
    def __get_image_data_from_file(path):

        filename, file_extension = os.path.splitext(path)

        allowed_extensions = ['.jpg', '.jpeg', '.gif', '.png']

        if file_extension not in allowed_extensions:
            return {'error': 'Invalid image extension (jpg, jpeg, gif, png)'}

        file_info = process_file(path)
        if file_info is None:
            return {'error': 'Fail to get image data from ' + path}

        cached_url = Messages.__ensure_image_uploaded(file_info)

        return {'filename' : path,
                'length': file_info['length'],
                'hash': file_info['hash'],
                'url': cached_url }

    @staticmethod
    def __get_image_data_from_url(url):
        uploader = ImageUploader()
        cached_url = uploader.upload_photo(url)

        return {'filename' : url,
                'length': 0,
                'hash': '',
                'url': cached_url }

    @staticmethod
    def __get_image_data(filename, url):
        if filename is not None:
            return Messages.__get_image_data_from_file(filename)
        return Messages.__get_image_data_from_url(url)

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

        result['image_data'] = image_data

        self.__update_message_store(result)

        return result
