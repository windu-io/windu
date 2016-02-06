#! /usr/bin/env python
# -*- coding: utf-8 -*-


from ..models import ThirdAuthToken


class ThirdAuth:

    def __init__(self):
        pass

    @staticmethod
    def find_credentials (name):
        return ThirdAuthToken.objects.filter(name=name).first()

    @staticmethod
    def update_credentials (credentials, access_token, refresh_token):

        if credentials.access_token == access_token and credentials.refresh_token == refresh_token:
            return

        credentials.access_token = access_token
        credentials.refresh_token = refresh_token
        credentials.save(update_fields=['access_token', 'refresh_token'])
