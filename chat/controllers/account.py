#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .agent_factory import get_agent


class Account:

    def __init__(self, account):
        self.__account = account
        self.__account_number = account.id

    def __agent(self):
        return get_agent (self.__account)

    def __account(self):
        return None

    def update_status_message(self, status_message):
        agent = self.__agent()
        return agent.sendStatusUpdate(status_message)

    def status_message (self):
        agent = self.__agent()
        return agent.sendGetStatuses([self.__account_number])

    def update_profile_photo(self, picture):
        agent = self.__agent()
        return agent.sendSetProfilePicture(picture)

    def profile_photo(self):
        agent = self.__agent()
        return agent.sendGetProfilePicture (self.__account_number)

    def remove_profile_photo (self):
        agent = self.__agent()
        return agent.sendRemoveProfilePicture()

    def update_connected_status(self, status):
        agent = self.__agent()
        return agent.setConnectedStatus(status)

    def connected_status(self):
        agent = self.__agent()
        return agent.getConnectedStatus()

    def update_nickname (self, nickname):
        self.__update_account_nickname (nickname)
        agent = self.__agent()
        return agent.sendUpdateNickname(nickname)

    def __update_account_nickname(self, nickname):
        self.__account.nick = nickname
        self.__account.save ()

    def nickname (self):
        return {'nickname':self.__account.nick, 'code':'200'}

    def update_privacy_setting (self, setting, value):
        agent = self.__agent()
        return agent.sendSetPrivacySettings(setting, value)

    def privacy_setting (self):
        agent = self.__agent()
        return agent.sendGetPrivacySettings()

    def remove_account (self, feedback):
        agent = self.__agent()
        return agent.sendRemoveAccount(feedback)


