#! /usr/bin/env python
# -*- coding: utf-8 -*-

from models import Chat, Account, Message, Contact, User
from wagent import WinduAgent

def get_controller():
    return controller()

class controller:

    ACCOUNT_ID = '5511988448107'

    def chats(self):
        return Chat.objects.filter(account=controller.ACCOUNT_ID)

    def messages (self, id):
        return Message.objects.filter(account=controller.ACCOUNT_ID, entity_id=id)

    def contacts (self):
        return Contact.objects.filter(account=controller.ACCOUNT_ID)
