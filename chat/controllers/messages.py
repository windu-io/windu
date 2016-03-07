#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils import timezone
from .agent import get_agent_and_check_events

from .contacts import Contacts
from ..models import Account as ModelAccount
from ..models import Message
from ..models import MessageGroupRead
from ..models import FileUpload

from ..util.image_uploader import ImageUploader
from ..util.audio_uploader import AudioUploader
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

        self.__update_message_store (result)

        return result

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
    def __ensure_image_uploaded(file_info):

        uploader = ImageUploader()
        hash_image = file_info.get('hash')
        image_upload = FileUpload.objects.filter(hash=hash_image).first()

        if image_upload is not None:
            return image_upload.file_url

        path = file_info.get('path')
        image_url = uploader.upload_photo(path)
        image_upload = FileUpload.objects.create(hash=hash_image, file_url=image_url)

        return image_upload.file_url

    @staticmethod
    def __ensure_audio_uploaded(file_info):

        hash_audio = file_info.get('hash')
        mime_type = file_info.get('mime_type')
        if mime_type is None:
            mime_type = 'audio/mpeg'
        else:
            mime_type = mime_type[0]
        file_upload = FileUpload.objects.filter(hash=hash_audio).first()

        if file_upload is not None:
            return file_upload.file_url

        path = file_info.get('path')
        audio_url = AudioUploader.upload_audio(path, mime_type)
        image_upload = FileUpload.objects.create(hash=hash_audio, file_url=audio_url)

        return image_upload.file_url

    @staticmethod
    def __get_image_data_from_file(path):

        filename, file_extension = os.path.splitext(path)

        allowed_extensions = ['.jpg', '.jpeg', '.gif', '.png']

        file_extension = file_extension.lower()

        if file_extension not in allowed_extensions:
            return {'error': 'Invalid image extension (jpg, jpeg, gif, png)'}

        file_info = process_file(path)
        if file_info is None:
            return {'error': 'Fail to get image data from ' + path}

        cached_url = Messages.__ensure_image_uploaded(file_info)

        return {'filename': path,
                'length': file_info['length'],
                'hash': file_info['hash'],
                'url': cached_url}

    @staticmethod
    def __get_audio_data_from_file(path):

        filename, file_extension = os.path.splitext(path)

        allowed_extensions = ['.3gp', '.caf', '.wav', '.mp3', '.wma', '.ogg', '.aif', '.aac', '.m4a'];

        file_extension = file_extension.lower()

        if file_extension not in allowed_extensions:
            return {'error': 'Invalid audio extension (3gp, caf, wav, mp3, wma, ogg, aif, aac, m4a)'}

        file_info = process_file(path)
        if file_info is None:
            return {'error': 'Fail to get audio data from ' + path}

        cached_url = Messages.__ensure_audio_uploaded(file_info)

        return {'filename': path,
                'length': file_info['length'],
                'hash': file_info['hash'],
                'url': cached_url}

    @staticmethod
    def __get_image_data_from_url(url):
        uploader = ImageUploader()
        cached_url = uploader.upload_photo_from_url(url)

        return {'filename': url,
                'length': 0,
                'hash': '',
                'url': cached_url}

    @staticmethod
    def __get_audio_data_from_url(url):
        cached_url = AudioUploader.upload_audio_from_url(url)

        return {'filename': url,
                'length': 0,
                'hash': '',
                'url': cached_url}

    @staticmethod
    def __get_image_data(filename, url):
        if filename is not None:
            return Messages.__get_image_data_from_file(filename)
        return Messages.__get_image_data_from_url(url)

    @staticmethod
    def __get_audio_data(filename, url):
        if filename is not None:
            return Messages.__get_audio_data_from_file(filename)
        return Messages.__get_audio_data_from_url(url)

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

        self.__update_message_store (result)

        return result

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

        result['audio_data'] = audio_data

        self.__update_message_store(result)

        return result

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

        self.__update_message_store(result)

        return result

