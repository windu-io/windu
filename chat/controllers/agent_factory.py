#! /usr/bin/env python
# -*- coding: utf-8 -*-

from wagent import WinduAgent


def create_agent(account):
    return WinduAgent.WinduAgent (account.account, account.nickname, account.password)