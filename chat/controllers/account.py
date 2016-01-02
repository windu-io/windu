#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from .agent_factory import get_agent

from ..models import Account as ModelAccount


class Account:

    def __init__(self, account):
        self.__account = account

    @staticmethod
    def create_account (number, nickname, user):
        if user is None or not user.is_active:
            return {'error':'Invalid user', 'code': '403'}

        if ModelAccount.objects.filter(account=number, user=user).exists():
            return {'error':'Account already exists', 'code': '400'}

        account = ModelAccount.objects.create(account=number, nickname=nickname, user=user)
        controller = Account (account)
        result = controller.request_sms_code()
        status_code = result.get('code')
        if status_code is None or status_code[0] != '2':
            account.delete()
            result['error'] = 'Error creating account' + number
        return result

    def request_sms_code(self):
        result = {}
        agent = self.__agent()
        self.__account.code_requested = datetime.datetime.now()
        self.__account.save()
        try:
            result = agent.codeRequestSMS()
        except Exception as e:
            result['error'] = str(e)
            result['code'] = '500'
        return result

    def request_voice_code(self):
        agent = self.__agent()
        self.__account.code_requested = datetime.datetime.now()
        self.__account.save()
        try:
            result = agent.codeRequestVoice()
        except Exception as e:
            result['error'] = str(e)
            result['code'] = '500'
        return result

    def register_code(self,code):
        agent = self.__agent()
        result = agent.codeRegister(code)
        status_code = result.get('code')
        if status_code is None or status_code[0] != '2':
            return result
        password = result.get ('pw')
        if not password:
            result['code'] = '501'
            result['error'] = 'Fail to register code, try again later'
            return result
        self.__account.password = password
        self.__account.save()
        return result

    def remove_account(self, feedback):
        if self.__account.is_registered():
            agent = self.__agent()
            result = agent.sendRemoveAccount(feedback)
            status_code = result.get('code')
            if status_code is None or status_code[0] != '2':
                result['error'] = 'Error removing account' + self.__account.account
                return result

        self.__account.delete()
        return result

    def __agent(self):
        return get_agent (self.__account)

    def update_status_message(self, status_message):
        agent = self.__agent()
        return agent.sendStatusUpdate(status_message)

    def status_message (self):
        agent = self.__agent()
        return agent.sendGetStatuses([self.__account.account])

    def update_profile_photo(self, picture):
        agent = self.__agent()
        return agent.sendSetProfilePicture(picture)

    def profile_photo(self):
        agent = self.__agent()
        return agent.sendGetProfilePicture (self.__account.account)

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
        self.__account.nickname = nickname
        self.__account.save ()

    def nickname (self):
        return {'nickname': self.__account.nickname, 'code': '200'}

    def update_privacy_settings(self, settings):

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

    def privacy_settings(self):
        result = {}
        agent = self.__agent()
        ret = agent.sendGetPrivacySettings()
        result['code'] = ret['code']
        result['status_message'] = ret['values']['status']
        result['photo'] = ret['values']['profile']
        result['last_seen'] = ret['values']['last']
        return result



