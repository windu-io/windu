#! /usr/bin/env python
# -*- coding: utf-8 -*-

from message_store import MessagesStore


def __on_message_received_client(account, data):

    message_id = data.get('id')
    entity_id = data.get('from')
    if message_id is None or entity_id is None:
        return

    message_data = {
        'entity_id': entity_id,
        'message_id': message_id,
        'time': data.get ('t'),
    }

    MessagesStore.update_delivered_date(account, message_data)


def __on_get_receipt(account, data):

    message_id = data.get('id')
    entity_id = data.get('from')
    if message_id is None or entity_id is None:
        return

    message_data = {
        'entity_id': entity_id,
        'message_id': message_id,
        'time': data.get('t'),
    }

    MessagesStore.update_read_date(account, message_data)


def __on_get_group_message(account, data):
    print ('__on_get_group_message')
    print (data)
    return


def __on_get_message(account, message_info):

    text = message_info.get('data')
    message_id = message_info.get('id')
    entity_id = message_info.get('from')

    if text is None or message_id is None or entity_id is None:
        return

    message_data = {
        'message_id': message_id,
        'entity_id': entity_id,
        'data': text,
        'message_type': 't',
        'send_type': 'r',
        'time': message_info.get('t'),
    }

    MessagesStore.create_message_model(account, message_data)


def __on_get_image(account, message_info):

    caption = message_info.get('caption')
    message_id = message_info.get('id')
    entity_id = message_info.get('from')
    file = message_info.get('file')

    if file is None or message_id is None or entity_id is None:
        return

    image_data = MessagesStore.get_image_data_from_file(file)
    if image_data is None or image_data.get('url') is None:
        return

    message_data = {
        'message_id': message_id,
        'entity_id': entity_id,
        'data': '',
        'caption': caption,
        'message_type': 'i',
        'send_type': 'r',
        'time': message_info.get('t'),
        'url': image_data.get('url'),
        'file_hash': image_data.get('hash'),
    }

    MessagesStore.create_message_model(account, message_data)


def __on_get_video(account, message_info):

    caption = message_info.get('caption')
    message_id = message_info.get('id')
    entity_id = message_info.get('from')
    url = message_info.get('url')

    if url is None or message_id is None or entity_id is None:
        return

    message_data = {
        'message_id': message_id,
        'entity_id': entity_id,
        'data': '',
        'message_type': 'v',
        'send_type': 'r',
        'caption': caption,
        'time': message_info.get('t'),
        'url': message_info.get('url'),
        'file_hash': message_info.get('filehash'),
        'mime_type': message_info.get('mimetype'),
    }

    MessagesStore.create_message_model(account, message_data)


def __on_get_audio(account, message_info):

        message_id = message_info.get('id')
        entity_id = message_info.get('from')
        url = message_info.get('url')

        if url is None or message_id is None or entity_id is None:
            return

        audio_data = MessagesStore.get_audio_data_from_url(url)

        message_data = {
            'message_id': message_id,
            'entity_id': entity_id,
            'data': '',
            'message_type': 'a',
            'send_type': 'r',
            'time': message_info.get('t'),
            'url': audio_data.get('url'),
            'file_hash': audio_data.get('hash'),
        }

        MessagesStore.create_message_model(account, message_data)


def __on_get_vcard(account, message_info):

        name = message_info.get('name')
        vcard = message_info.get('data')
        message_id = message_info.get('id')
        entity_id = message_info.get('from')

        if vcard is None or message_id is None or entity_id is None:
            return

        message_data = {
            'message_id': message_id,
            'entity_id': entity_id,
            'data': vcard,
            'caption': name,
            'message_type': 'c',
            'send_type': 'r',
            'time': message_info.get('t'),
        }

        MessagesStore.create_message_model(account, message_data)


def __on_get_location(account, message_info):

    name = message_info.get('name')
    url = message_info.get('url')
    message_id = message_info.get('id')
    entity_id = message_info.get('from')
    latitude = message_info.get('latitude')
    longitude = message_info.get('longitude')
    location_icon = message_info.get('data')
    image_url = None
    if location_icon is not None:
        image_data = MessagesStore.get_image_data_from_file(location_icon)
        image_url = image_data.get('url')

    if latitude is None or longitude is None or message_id is None or entity_id is None:
        return

    message_data = {
        'message_id': message_id,
        'entity_id': entity_id,
        'data': image_url,
        'caption': name,
        'latitude': latitude,
        'longitude': longitude,
        'url': url,
        'message_type': 'l',
        'send_type': 'r',
        'time': message_info.get('t'),
    }

    MessagesStore.create_message_model(account, message_data)


def __find_event_handler(account, name):
    handlers = {
        'onmessagereceivedclient': __on_message_received_client,
        'ongetreceipt': __on_get_receipt,
        'ongetgroupimage': __on_get_group_message,
        'ongetmessage': __on_get_message,
        'ongetimage': __on_get_image,
        'ongetvideo': __on_get_video,
        'ongetaudio': __on_get_audio,
        'ongetvcard': __on_get_vcard,
        'ongetlocation': __on_get_location,
    }
    return handlers.get(name)
