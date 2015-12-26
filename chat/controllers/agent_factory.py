#! /usr/bin/env python
# -*- coding: utf-8 -*-

from wagent import WinduAgent

def get_agent (account):
    return WinduAgent.WinduAgent (account.id, account.nick, account.password)