#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

from datetime import datetime
from django.utils import timezone

from ..models import Account as ModelAccount
from ..models import Message
from ..models import MessageGroupRead

from ..util.image_uploader import ImageUploader
from ..util.audio_uploader import AudioUploader
from ..util.file_process import process_file

from ..models import FileUpload


class MessagesStore:

    def __init__(self):
        pass

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
    def get_image_data_from_file(path):

        filename, file_extension = os.path.splitext(path)

        allowed_extensions = ['.jpg', '.jpeg', '.gif', '.png']

        file_extension = file_extension.lower()

        if file_extension not in allowed_extensions:
            return {'error': 'Invalid image extension (jpg, jpeg, gif, png)'}

        file_info = process_file(path)
        if file_info is None:
            return {'error': 'Fail to get image data from ' + path}

        cached_url = MessagesStore.__ensure_image_uploaded(file_info)

        return {'filename': path,
                'length': file_info['length'],
                'hash': file_info['hash'],
                'url': cached_url}

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
    def get_audio_data_from_file(path):

        filename, file_extension = os.path.splitext(path)

        allowed_extensions = ['.3gp', '.caf', '.wav', '.mp3', '.wma', '.ogg', '.aif', '.aac', '.m4a'];

        file_extension = file_extension.lower()

        if file_extension not in allowed_extensions:
            return {'error': 'Invalid audio extension (3gp, caf, wav, mp3, wma, ogg, aif, aac, m4a)'}

        file_info = process_file(path)
        if file_info is None:
            return {'error': 'Fail to get audio data from ' + path}

        cached_url = MessagesStore.__ensure_audio_uploaded(file_info)

        return {'filename': path,
                'length': file_info['length'],
                'hash': file_info['hash'],
                'url': cached_url}

    @staticmethod
    def get_audio_data_from_url(url):
        cached_url = AudioUploader.upload_audio_from_url(url)

        return {'filename': url,
                'length': 0,
                'hash': '',
                'url': cached_url}

    @staticmethod
    def get_image_data_from_url(url):
        uploader = ImageUploader()
        cached_url = uploader.upload_photo_from_url(url)

        return {'filename': url,
                'length': 0,
                'hash': '',
                'url': cached_url}

    @staticmethod
    def create_message_model(account, message_data):

        t = message_data.get('time')
        if t is None:
            message_data['time'] = timezone.now()
        else:
            message_data['time'] = datetime.utcfromtimestamp(int(t))

        model = Message.objects.filter(account=account,
                                       message_id=message_data.get('message_id')).first()
        if model is None:
            Message.objects.create(account=account,
                               message_id=message_data.get('message_id'),
                               entity_id=message_data.get('entity_id'),
                               send_type=message_data.get('send_type'),
                               message_type=message_data.get('message_type'),
                               time=message_data.get('time'),
                               data=message_data.get('data'),
                               url=message_data.get('url'),
                               longitude=message_data.get('longitude'),
                               latitude=message_data.get('latitude'),
                               mimetype=message_data.get('mime_type'),
                               file_hash=message_data.get('file_hash'),
                               caption=message_data.get('caption'),
                               participant=message_data.get('participant'),
                               )
        else:
            model.time = message_data.get('time')
            model.data = message_data.get('data')
            model.url = message_data.get('url')
            model.longitude = message_data.get('longitude')
            model.latitude = message_data.get('latitude')
            model.mimetype = message_data.get('mime_type')
            model.file_hash = message_data.get('file_hash')
            model.caption = message_data.get('caption')
            model.participant = message_data.get('participant')
            model.save ()

    @staticmethod
    def __model_to_message_result(message):
        info = {
            'id': message.message_id,
            'type': message.message_type,
            'received': message.send_type == 'r'
        }

        if message.message_type == 't':
            info['text'] = message.data
        elif message.message_type == 'i' or message.message_type == 'a':
            info['url'] = message.url
            info['hash'] = message.file_hash
        elif message.message_type == 'l':
            info['latitude'] = message.latitude
            info['longitude'] = message.longitude
            if message.url is not None:
                info['url'] = message.url
            if not message.data.isspace():
                info['data'] = message.data
        elif message.message_type == 'c':
            info['vcard'] = message.data

        return info

    @staticmethod
    def get_messages(account, contact_id, after, limit, offset, received_only):

        if received_only:
            query_messages = Message.objects.filter(account=account,
                                                    entity_id=contact_id,
                                                    time__gt=after, send_type='r')[offset:limit]
        else:
            query_messages = Message.objects.filter(account=account,
                                                    entity_id=contact_id,
                                                    time__gt=after)[offset:limit]

        messages = []

        for message in query_messages:
            info = MessagesStore.__model_to_message_result(message)
            messages.append(info)

        return messages
