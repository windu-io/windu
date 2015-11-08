# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_id', models.CharField(max_length=64, db_index=True)),
                ('entity_id', models.CharField(max_length=64, db_index=True)),
                ('title', models.CharField(max_length=256)),
                ('snippet', models.CharField(max_length=64)),
                ('time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_id', models.CharField(max_length=64, db_index=True)),
                ('entity_id', models.CharField(max_length=64, db_index=True)),
                ('title', models.CharField(max_length=256)),
                ('status', models.CharField(max_length=256)),
                ('last_seen', models.DateTimeField()),
                ('picture', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('account_id', models.CharField(max_length=64, db_index=True)),
                ('message_id', models.CharField(max_length=64, db_index=True)),
                ('entity_id', models.CharField(max_length=64, db_index=True)),
                ('send_type', models.CharField(max_length=1)),
                ('message_type', models.CharField(max_length=1)),
                ('time', models.DateTimeField()),
                ('data', models.TextField()),
                ('url', models.URLField()),
                ('longitute', models.FloatField()),
                ('latitude', models.FloatField()),
                ('mimetype', models.CharField(max_length=64)),
                ('file_hash', models.CharField(max_length=128)),
                ('height', models.SmallIntegerField()),
                ('size', models.SmallIntegerField()),
                ('vcodec', models.CharField(max_length=12)),
                ('acodec', models.CharField(max_length=12)),
                ('duration', models.SmallIntegerField()),
                ('caption', models.CharField(max_length=256)),
                ('participant', models.CharField(max_length=64)),
                ('sent', models.DateTimeField()),
                ('delivered', models.DateTimeField()),
                ('read', models.DateTimeField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='message',
            unique_together=set([('account_id', 'message_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together=set([('account_id', 'entity_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='chat',
            unique_together=set([('account_id', 'entity_id')]),
        ),
    ]
