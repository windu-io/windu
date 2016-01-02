from django.db import  models
from django.contrib.auth.models import  User


class Account(models.Model):
    class Meta:
        unique_together = (('account', 'user'),)
    account = models.CharField (max_length=64)
    password = models.CharField (max_length=64, null=True, blank=False)
    code_requested = models.DateTimeField (null=True)
    nickname = models.CharField (max_length=256, null=True, blank=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.nickname + " (" + self.account + ")"

    def is_registered(self):
        return self.password is not None


class Chat(models.Model):
    class Meta:
        unique_together = (('account', 'entity_id'),)
    account = models.ForeignKey (Account)
    entity_id  = models.CharField (max_length=64, db_index=True,null=False)
    title  = models.CharField (max_length=256,null=False)
    snippet  = models.CharField (max_length=64, null=False)
    time = models.DateTimeField (null=True,blank=True)

    def __str__(self):
        return self.title


class Message(models.Model):
    class Meta:
        unique_together = (('account', 'message_id'),)
    account = models.ForeignKey (Account)
    message_id = models.CharField (max_length=64, db_index=True,null=False)
    entity_id = models.CharField (max_length=64, db_index=True,null=False)
    send_type = models.CharField (max_length=1, null=False)
    message_type = models.CharField (max_length=1, null=False)
    time = models.DateTimeField (null=False)
    data = models.TextField (null=False)
    url = models.URLField (null=True,blank=True)
    longitude = models.FloatField (null=True,blank=True)
    latitude = models.FloatField (null=True,blank=True)
    mimetype = models.CharField (max_length=64, null=True,blank=True)
    file_hash = models.CharField (max_length=128, null=True, blank=True)
    height = models.SmallIntegerField (null=True, blank=True)
    size = models.SmallIntegerField (null=True, blank=True)
    vcodec = models.CharField (max_length=12, null=True, blank=True)
    acodec = models.CharField (max_length=12, null=True, blank=True)
    duration = models.SmallIntegerField(null=True, blank=True)
    caption = models.CharField (max_length=256, null=True, blank=True)
    participant = models.CharField (max_length=64, null=True, blank=True)
    sent = models.DateTimeField (null=True, blank=True)
    delivered = models.DateTimeField (null=True, blank=True)
    read = models.DateTimeField (null=True, blank=True)

    def __str__(self):
        return self.message_id + ' ' + self.data


class Contact (models.Model):
    class Meta:
        unique_together = (('account', 'contact_id'),)
    account = models.ForeignKey (Account)
    contact_id  = models.CharField (max_length=64, db_index=True, null=False)
    title  = models.CharField (max_length=256, null=True, blank=True)
    status = models.CharField (max_length=256, null=True, blank=True)
    last_seen = models.DateTimeField (null=True, blank=True)

    def __str__(self):
        return self.title


class Picture (models.Model):
    class Meta:
        unique_together = (('account', 'entity_id'),)
    account = models.ForeignKey (Account)
    entity_id  = models.CharField (max_length=64, db_index=True, null=False)
    updated = models.DateTimeField (null=False,auto_now=True)
    picture = models.URLField (null=False)

    def __str__(self):
        return self.picture


