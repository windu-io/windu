#! /usr/bin/env python
# -*- coding: utf-8 -*-


def __on_message_received_server(data):
    print ('__on_message_received_server')
    print (data)
    return


def __on_message_received_client(data):
    print ('__on_message_received_client')
    print (data)
    return


def __on_get_receipt(data):
    print ('__on_get_receipt')
    print (data)
    return


def __on_get_group_message(data):
    print ('__on_get_group_message')
    print (data)
    return


def __on_get_message(data):
    print ('__on_get_message')
    print (data)
    return


def __find_event_handler(name):
    handlers = {
        'onmessagereceivedserver': __on_message_received_server,
        'onmessagereceivedclient': __on_message_received_client,
        'ongetreceipt': __on_get_receipt,
        'ongetgroupimage': __on_get_group_message,
        'ongetmessage': __on_get_message,
    }
    return handlers.get(name)
