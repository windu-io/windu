#! /usr/bin/env python
# -*- coding: utf-8 -*-

from wagent import WinduAgent


def create_agent(account):
    return WinduAgent.WinduAgent(phoneNumber=account.account,
                                 nickName=account.nickname,
                                 password=account.password,
                                 autoReply=WinduAgent.WinduAgent.AUTOREPLY_DELIVERED)