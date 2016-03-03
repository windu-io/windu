
from datetime import timedelta

from django.db import  models
from django.contrib.auth.models import User

from django.utils import timezone

from windu.settings import WINDU_PROFILE_PHOTO_CACHE_MINUTES


class ThirdAuthToken(models.Model):

    name = models.CharField(max_length=64, null=False, db_index=True, unique=True)
    client_id = models.CharField (max_length=64, null=False)
    client_secret = models.CharField (max_length=64, null=False)
    access_token = models.CharField (max_length=64, null=False)
    refresh_token = models.CharField (max_length=64, null=False)

    def __str__(self):
        return self.name + " (" + self.access_token + ")"


class Account(models.Model):

    class Meta:
        unique_together = (('account', 'user'),)

    account = models.CharField (max_length=64)
    password = models.CharField (max_length=64, null=True, blank=False)
    code_requested = models.DateTimeField (null=True, blank=True)
    nickname = models.CharField (max_length=256, null=True, blank=True)
    user = models.ForeignKey(User)
    last_check_events = models.DateTimeField(null=True, blank=True)
    last_sync_contacts = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.nickname + " (" + self.account + ")"

    def is_registered(self):
        return self.password is not None


class Chat(models.Model):

    class Meta:
        unique_together = (('account', 'entity_id'),)

    account = models.ForeignKey (Account)
    entity_id = models.CharField (max_length=64, db_index=True,null=False)
    title = models.CharField (max_length=256,null=False)
    snippet = models.CharField (max_length=64, null=False)
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


class MessageGroupRead(models.Model):

    class Meta:
        unique_together = (('message', 'participant'),)

    message = models.ForeignKey(Message)
    participant = models.CharField(max_length=64, null=True, blank=True)
    delivered = models.DateTimeField(null=True, blank=True)
    read = models.DateTimeField(null=True, blank=True)


class FileUpload (models.Model):

    hash = models.CharField(max_length=64, db_index=True, null=False, blank=False, unique=True)
    file_url = models.URLField(null=False)

    def __str__(self):
        return self.file_url


class Contact(models.Model):

    class Meta:
        unique_together = (('account', 'contact_id'),)

    account = models.ForeignKey(Account)
    contact_id = models.CharField(max_length=64, db_index=True, null=False)
    first_name = models.CharField(max_length=256, null=True, blank=True)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    status_message = models.CharField(max_length=256, null=False, blank=False)
    nickname = models.CharField(max_length=64, null=True,blank=True)
    connected_status = models.CharField(max_length=16, null=True,blank=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    photo = models.ForeignKey(FileUpload, on_delete=models.SET_NULL, blank=True, null=True, related_name='photo')
    photo_status = models.CharField(max_length=1, null=False, default='i')
    preview_photo = models.ForeignKey(FileUpload, on_delete=models.SET_NULL, blank=True, null=True, related_name='preview_photo')
    preview_photo_status = models.CharField (max_length=1, null=False, default='i')
    photo_hash = models.CharField(max_length=64, db_index=True, null=True)
    preview_photo_hash = models.CharField(max_length=64, db_index=True, null=True)
    preview_photo_updated = models.DateTimeField(null=False, blank=False, default=timezone.now() - timedelta(0, 0, 0, 0, WINDU_PROFILE_PHOTO_CACHE_MINUTES))
    photo_updated = models.DateTimeField(null=False, blank=False, default=timezone.now() - timedelta(0, 0, 0, 0, WINDU_PROFILE_PHOTO_CACHE_MINUTES))
    exists = models.BooleanField(null=False)

    def __str__(self):
        return self.first_name

    def get_photo(self, preview):
        if preview:
            return self.preview_photo
        return self.photo

    def get_photo_status(self, preview):
        if preview:
            return self.preview_photo_status
        return self.photo_status

    def get_photo_hash(self, preview):
        if preview:
            return self.preview_photo_hash
        return self.photo_hash

    def update_photo(self, preview, photo):
        if preview:
            self.preview_photo = photo
        else:
            self.photo = photo

    def update_photo_status(self, preview, status):
        if preview:
            self.preview_photo_status = status
        else:
            self.photo_status = status

    def update_photo_hash(self, preview, hash):
        if preview:
            self.preview_photo_hash = hash
        else:
            self.photo_hash = hash

    def get_photo_updated(self, preview):
        if preview:
            return self.preview_photo_updated
        return self.photo_updated

    def update_photo_updated(self, preview, updated):
        if preview:
            self.preview_photo_updated = updated
        else:
            self.photo_updated = updated

    def get_photo_url (self, preview):
        if preview:
            if self.preview_photo is None:
                return None
            return self.preview_photo.photo_url
        if self.photo is None:
            return None
        return self.photo.photo_url


class ContactsFromMessage(models.Model):
    class Meta:
        unique_together = (('account', 'contact_id'),)
    account = models.ForeignKey(Account)
    contact_id = models.CharField(max_length=64, db_index=True, null=False)
    current_nickname = models.CharField(max_length=64, null=True,blank=True)

    def __str__(self):
        return self.first_name


class ProfilePhoto(models.Model):
    account = models.ForeignKey(Account)
    contact_id = models.CharField(max_length=64, db_index=True, null=False)
    updated = models.DateTimeField (null=False,auto_now=True)
    photo = models.ForeignKey(FileUpload, on_delete=models.SET_NULL, blank=True, null=True)
    preview = models.BooleanField(null=False)
    photo_status = models.CharField(max_length=1, null=False, default='i')

    def __str__(self):
        return str(self.photo)


class StatusMessage(models.Model):
    account = models.ForeignKey(Account)
    contact_id = models.CharField(max_length=64, db_index=True, null=False)
    updated = models.DateTimeField(null=False, auto_now=True)
    status_message = models.CharField(max_length=256, null=False, blank=False)

    def __str__(self):
        return self.status


class ContactsNickname(models.Model):
    account = models.ForeignKey(Account)
    contact_id = models.CharField(max_length=64, db_index=True, null=False)
    nickname = models.CharField(max_length=64, null=True,blank=True)
    updated = models.DateTimeField(null=False, auto_now=True)

    def __str__(self):
        return self.nickname

