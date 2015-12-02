# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.CharField(max_length=64, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=64)),
                ('nick', models.CharField(max_length=256, null=True, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity_id', models.CharField(max_length=64, db_index=True)),
                ('title', models.CharField(max_length=256)),
                ('snippet', models.CharField(max_length=64)),
                ('time', models.DateTimeField(null=True, blank=True)),
                ('account', models.ForeignKey(to='chat.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_id', models.CharField(max_length=64, db_index=True)),
                ('title', models.CharField(max_length=256, null=True, blank=True)),
                ('status', models.CharField(max_length=256, null=True, blank=True)),
                ('last_seen', models.DateTimeField(null=True, blank=True)),
                ('account', models.ForeignKey(to='chat.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message_id', models.CharField(max_length=64, db_index=True)),
                ('entity_id', models.CharField(max_length=64, db_index=True)),
                ('send_type', models.CharField(max_length=1)),
                ('message_type', models.CharField(max_length=1)),
                ('time', models.DateTimeField()),
                ('data', models.TextField()),
                ('url', models.URLField(null=True, blank=True)),
                ('longitute', models.FloatField(null=True, blank=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('mimetype', models.CharField(max_length=64, null=True, blank=True)),
                ('file_hash', models.CharField(max_length=128, null=True, blank=True)),
                ('height', models.SmallIntegerField(null=True, blank=True)),
                ('size', models.SmallIntegerField(null=True, blank=True)),
                ('vcodec', models.CharField(max_length=12, null=True, blank=True)),
                ('acodec', models.CharField(max_length=12, null=True, blank=True)),
                ('duration', models.SmallIntegerField(null=True, blank=True)),
                ('caption', models.CharField(max_length=256, null=True, blank=True)),
                ('participant', models.CharField(max_length=64, null=True, blank=True)),
                ('sent', models.DateTimeField(null=True, blank=True)),
                ('delivered', models.DateTimeField(null=True, blank=True)),
                ('read', models.DateTimeField(null=True, blank=True)),
                ('account', models.ForeignKey(to='chat.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entity_id', models.CharField(max_length=64, db_index=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('picture', models.URLField()),
                ('account', models.ForeignKey(to='chat.Account')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='picture',
            unique_together=set([('account', 'entity_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='message',
            unique_together=set([('account', 'message_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together=set([('account', 'contact_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='chat',
            unique_together=set([('account', 'entity_id')]),
        ),
    ]
