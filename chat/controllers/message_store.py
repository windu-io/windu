#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from django.utils import timezone

from ..models import Account as ModelAccount
from ..models import Message
from ..models import MessageGroupRead


class MessagesStore:

    def __init__(self):
        pass

    @staticmethod
    def create_message_model(account, message_data):

        t = message_data.get('time')
        if t is None:
            message_data['time'] = timezone.now()
        else:
            message_data['time'] = datetime.utcfromtimestamp(int(t))

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
