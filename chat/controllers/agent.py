#! /usr/bin/env python
# -*- coding: utf-8 -*-


from events import check_events
from agent_factory import create_agent


def get_agent_and_check_events (account):
    agent = create_agent(account)
    check_events(account)
    return agent
