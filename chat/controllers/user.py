#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User as ModelUser
from .mail import Mail

class User:

    def __init__(self, user):
        self.__user = user

    @staticmethod
    def create_user(username, password, email, first_name, last_name):

        if ModelUser.objects.filter(username=username).exists():
            return {'error': 'User name already in use', 'code': '400'}
        if ModelUser.objects.filter(email=email).exists():
            return {'error': 'E-mail already in use', 'code': '400'}

        try:
            user = ModelUser.objects.create_user(username, email, password)
        except Exception as e:
            return { 'error': 'Error creating user:' + str(e), 'code': '500'}

        user.first_name = first_name[:30]
        user.last_name = last_name[:30]
        user.save()


        return {'code': '200'}


