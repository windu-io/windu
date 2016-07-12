#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from django.utils import timezone

from threading import Timer

from agent_factory import create_agent
from event_handlers import __find_event_handler


def __process_event(account, name, data):
    handler = __find_event_handler (account, name)
    if handler is None:
        return
    handler(account, data)


def __process_events(account, events):
    for event in events:
        name = event.get('name')
        data = event.get('data')
        if name is None or data is None:
            continue
        __process_event(account, name, data)


def __agent(account):
    return create_agent(account)


def __peek_events(account):
    result = {}
    agent = __agent(account)
    try:
        events = agent.peekEvents()
        return {'code': '200', 'events': events}
    except Exception as e:
        result['error'] = 'Error peeking events: ' + str(e)
        result['code'] = '500'
    return result


def __flush_events(account):
    result = __peek_events(account)

    status_code = result.get('code')

    if status_code is None or status_code[0] != '2':
        return result

    __process_events(account, result.get('events'))
    return result


def __schedule_flush_events(account):
    t = Timer(15.0, __flush_events, [account])
    t.start()


def __can_check_events(last_check):

    if last_check is None:
        return True
    delta = timezone.now() - last_check
    elapsed_seconds = delta.total_seconds()

    if elapsed_seconds > 45:
        return True
    return False


def check_events(account):
    if not __can_check_events(account.last_check_events):
        return

    __schedule_flush_events (account)

    account.last_check_events = datetime.utcnow()
    account.save()


def check_events_now(account):
    # if not __can_check_events(account.last_check_events):
    #     return None

    result = __flush_events(account)

    status_code = result.get('code')

    if status_code is None or status_code[0] != '2':
        return result

    account.last_check_events = datetime.utcnow()
    account.save()
    return result
