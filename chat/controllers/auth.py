#! /usr/bin/env python
# -*- coding: utf-8 -*-

from wagent import WinduAgent
from ..models import User, Account

class auth:

    def __init__(self, account_number, user_id):
        self.account_number = account_number
        self.user_id

    def _agent(self):
        return None

    def accessToken (self):
        return None

    @staticmethod
    def credentialsFromToken (token):
        return None

    def requestSMS(self):
        return None

    def requestCall(self):
        return None

    def registerCode(self, code):
        return None


