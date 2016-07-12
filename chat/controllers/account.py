#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from .agent import get_agent_and_check_events

from ..models import Account as ModelAccount


class Account:

    def __init__(self, account):
        self.__account = account

    @staticmethod
    def create_account (number, nickname, user):
        if user is None or not user.is_active:
            return {'error': 'Invalid user', 'code': '403'}

        if ModelAccount.objects.filter(account=number, user=user).exists():
            return {'error': 'Account already exists', 'code': '400'}

        account = ModelAccount.objects.create(account=number, nickname=nickname, user=user)
        controller = Account (account)
        result = controller.request_sms_code()
        status_code = result.get('code')
        if status_code is None or status_code[0] != '2':
            account.delete()
            result['error'] = 'Error creating account' + number
        return result

    @staticmethod
    def account_connected_status(account):
        controller = Account (account)
        status = controller.connected_status()
        return status.get('connected_status')

    def request_sms_code(self):
        result = {}
        agent = self.__agent()
        self.__account.code_requested = datetime.utcnow()
        self.__account.save(update_field=['code_requested'])
        try:
            result = agent.codeRequestSMS()
        except Exception as e:
            result['error'] = 'Error requesting SMS code: ' + str(e)
            result['code'] = '500'
        return result

    def request_voice_code(self):
        result = {}
        agent = self.__agent()
        self.__account.code_requested = datetime.utcnow()
        self.__account.save(update_field=['code_requested'])
        try:
            result = agent.codeRequestVoice()
        except Exception as e:
            result['error'] = 'Error requesting voice code: ' + str(e)
            result['code'] = '500'
        return result

    def __register_code(self, code):
        result = {}
        agent = self.__agent()
        try:
            result = agent.codeRegister(code)
        except Exception as e:
            result['error'] = 'Error registering code: ' + str(e)
            result['code'] = '500'
        return result

    def register_code(self,code):
        result = self.__register_code(code)
        status_code = result.get('code')
        if status_code is None or status_code[0] != '2':
            return result
        password = result.get ('pw')
        if not password:
            result['code'] = '501'
            result['error'] = 'Fail to register code, try again later'
            return result
        self.__account.password = password
        self.__account.save(update_fields=['password'])
        return result

    def __remove_account(self, feedback):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendRemoveAccount(feedback)
        except Exception as e:
            result['error'] = 'Error requesting voice code: ' + str(e)
            result['code'] = '500'
        return result

    def remove_account(self, feedback):
        if self.__account.is_registered():
            result = self.__remove_account(feedback)
            status_code = result.get('code')
            if status_code is None or status_code[0] != '2':
                result['error'] = 'Error removing account' + self.__account.account
                return result

        self.__account.delete()
        return result

    def __agent(self):
        return get_agent_and_check_events(self.__account)

    def __update_status_message(self, status_message):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendStatusUpdate(status_message)
        except Exception as e:
            result['error'] = 'Error updating status: ' + str(e)
            result['code'] = '500'
        return result

    def update_status_message(self, status_message):
        return self.__update_status_message(status_message)

    def __status_message(self):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendGetStatuses([self.__account.account])
        except Exception as e:
            result['error'] = 'Error getting status: ' + str(e)
            result['code'] = '500'
        return result

    def status_message (self):
        return self.__status_message()

    def __update_profile_photo(self, picture):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendSetProfilePicture(picture)
        except Exception as e:
            result['error'] = 'Error updating profile photo: ' + str(e)
            result['code'] = '500'
        return result

    def update_profile_photo(self, picture):
        return self.__update_profile_photo(picture)

    def __profile_photo(self):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendGetProfilePicture (self.__account.account)
        except Exception as e:
            result['error'] = 'Error getting profile photo: ' + str(e)
            result['code'] = '500'
        return result

    def profile_photo(self):
        return self.__profile_photo()

    def __remove_profile_photo(self):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendRemoveProfilePicture()
        except Exception as e:
            result['error'] = 'Error removing profile photo: ' + str(e)
            result['code'] = '500'
        return result

    def remove_profile_photo (self):
        return self.__remove_profile_photo()

    def __update_connected_status(self, connected_status):
        result = {}
        agent = self.__agent()
        try:
            result = agent.setConnectedStatus(connected_status)
        except Exception as e:
            result['error'] = 'Error updating connected status: ' + str(e)
            result['code'] = '500'
        return result

    def update_connected_status(self, connected_status):
        return self.__update_connected_status(connected_status)

    def __connected_status(self):
        result = {}
        agent = self.__agent()
        try:
            result = agent.getConnectedStatus()
        except Exception as e:
            result['error'] = 'Error getting connected status: ' + str(e)
            result['code'] = '500'
        return result

    def connected_status(self):
        return self.__connected_status()

    def __update_nickname(self, nickname):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendUpdateNickname(nickname)
        except Exception as e:
            result['error'] = 'Error updating nickname: ' + str(e)
            result['code'] = '500'
        return result

    def update_nickname (self, nickname):
        self.__update_account_nickname (nickname)
        return self.__update_nickname(nickname)

    def __update_account_nickname(self, nickname):
        self.__account.nickname = nickname
        self.__account.save(update_fields=['nickname'])

    def nickname(self):
        return {'nickname': self.__account.nickname, 'code': '200'}

    def __set_privacy_settings(self, setting, value):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendSetPrivacySettings(setting, value)
        except Exception as e:
            result['error'] = 'Error setting privacy setting: ' + str(e)
            result['code'] = '500'
        return result

    def update_privacy_settings(self, settings):

        result = {}

        status_message = settings.get ('status_message')
        if status_message is not None:
            r = self.__set_privacy_settings('status', status_message)
            code = r.get ('code')
            if code is None or code != '200':
                return r
            result['status_message'] = r['values']['status']

        photo = settings.get ('photo')
        if photo is not None:
            r = self.__set_privacy_settings('profile', photo)
            code = r.get ('code')
            if code is None or code != '200':
                return r
            result['photo'] = r['values']['profile']

        last_seen = settings.get ('last_seen')
        if last_seen is not None:
            r = self.__set_privacy_settings('last', last_seen)
            code = r.get ('code')
            if code is None or code != '200':
                return r
            result['last_seen'] = r['values']['last']

        result['code'] = '200'
        return result

    def __privacy_settings(self):
        result = {}
        agent = self.__agent()
        try:
            result = agent.sendGetPrivacySettings()
        except Exception as e:
            result['error'] = 'Error getting privacy setting: ' + str(e)
            result['code'] = '500'
        return result

    def privacy_settings(self):
        result = {}
        ret = self.__privacy_settings()
        result['code'] = ret['code']
        result['status_message'] = ret['values']['status']
        result['photo'] = ret['values']['profile']
        result['last_seen'] = ret['values']['last']
        return result



