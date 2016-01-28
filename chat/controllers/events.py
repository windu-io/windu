#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils import timezone

from threading import Timer

from agent_factory import create_agent
from event_handlers import __find_event_handler


def __process_event(name, data):
    handler = __find_event_handler (name)
    if handler is None:
        return
    handler(data)


def __process_events(events):
    for event in events:
        name = event.get('name')
        data = event.get('data')
        if name is None or data is None:
            continue
        __process_event(name, data)


def __agent(account):
    return create_agent(account)


def __flush_events(account):
    agent = __agent(account)
    events = agent.peekEventsForce()
    __process_events (events)


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

    account.last_check_events = timezone.now()
    account.save()
