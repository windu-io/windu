#! /usr/bin/env python
# -*- coding: utf-8 -*-

from message_store import MessagesStore

def __on_message_received_server(account, data):
    print ('__on_message_received_server')
    print (data)
    return


def __on_message_received_client(account, data):
    print ('__on_message_received_client')
    print (data)
    return


def __on_get_receipt(account, data):
    print ('__on_get_receipt')
    print (data)
    return


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


def __find_event_handler(account, name):
    handlers = {
        'onmessagereceivedserver': __on_message_received_server,
        'onmessagereceivedclient': __on_message_received_client,
        'ongetreceipt': __on_get_receipt,
        'ongetgroupimage': __on_get_group_message,
        'ongetmessage': __on_get_message,
    }
    return handlers.get(name)
