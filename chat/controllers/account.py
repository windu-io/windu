#! /usr/bin/env python
# -*- coding: utf-8 -*-

from .agent_factory import get_agent


class Account:

    def __init__(self, account_number, account):
        self.__account_number = account_number
        self.__account = account

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

    def status_online(self):
        agent = self.__agent()
        return agent.sendActiveStatus()

    def status_offline(self):
        agent = self.__agent()
        return agent.sendOfflineStatus()

    def update_nickname (self, nickname):
        self.updateAccountNickname (nickname)
        agent = self.__agent()
        return agent.sendUpdateNickname(nickname)

    def nickname (self):
        return self.__account ().nickname

    def update_privacy_setting (self, setting, value):
        agent = self.__agent()
        return agent.sendSetPrivacySettings(setting, value)

    def privacy_setting (self):
        agent = self.__agent()
        return agent.sendGetPrivacySettings()

    def remove_account (self, feedback):
        agent = self.__agent()
        return agent.sendRemoveAccount(feedback)


