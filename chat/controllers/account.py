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

    def update_privacy_settings (self, settings):

        agent = self.__agent()
        result = {}

        status_message = settings.get ('status_message')
        if status_message is not None:
            r = agent.sendSetPrivacySettings('status', status_message)
            code = r.get ('code')
            if code is None or code != '200':
                return r
            result['status_message'] = r['values']['status']

        photo = settings.get ('photo')
        if photo is not None:
            r = agent.sendSetPrivacySettings('profile', photo)
            code = r.get ('code')
            if code is None or code != '200':
                return r
            result['photo'] = r['values']['profile']

        last_seen = settings.get ('last_seen')
        if last_seen is not None:
            r = agent.sendSetPrivacySettings('last', last_seen)
            code = r.get ('code')
            if code is None or code != '200':
                return r
            result['last_seen'] = r['values']['last']

        result ['code'] = '200'
        return result

    def privacy_settings (self):
        result = {}
        agent = self.__agent()
        ret = agent.sendGetPrivacySettings()
        result['code'] = ret['code']
        result['status_message'] = ret['values']['status']
        result['photo'] = ret['values']['profile']
        result['last_seen'] = ret['values']['last']
        return result

    def remove_account (self, feedback):
        agent = self.__agent()
        return agent.sendRemoveAccount(feedback)


