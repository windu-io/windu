# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-27 01:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='from_message',
        ),
    ]
