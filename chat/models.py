from django.db import  models

class Chat(models.Model):
    class Meta:
        unique_together = (('account_id', 'entity_id'),)
    account_id = models.CharField (max_length=64, db_index=True,null=False)
    entity_id  = models.CharField (max_length=64, db_index=True,null=False)
    title  = models.CharField (max_length=256)
    snippet  = models.CharField (max_length=64)
    time = models.DateTimeField ()

class Message (models.Model):
    class Meta:
        unique_together = (('account_id', 'message_id'),)
    account_id = models.CharField (max_length=64, db_index=True,null=False)
    message_id = models.CharField (max_length=64, db_index=True,null=False)
    entity_id = models.CharField (max_length=64, db_index=True,null=False)
    send_type = models.CharField (max_length=1)
    message_type = models.CharField (max_length=1)
    time = models.DateTimeField ()
    data = models.TextField ()
    url = models.URLField ()
    longitute = models.FloatField ()
    latitude = models.FloatField ()
    mimetype = models.CharField (max_length=64)
    file_hash = models.CharField (max_length=128)
    height = models.SmallIntegerField ()
    size = models.SmallIntegerField ()
    vcodec = models.CharField (max_length=12)
    acodec = models.CharField (max_length=12)
    duration = models.SmallIntegerField()
    caption = models.CharField (max_length=256)
    participant = models.CharField (max_length=64)
    sent = models.DateTimeField ()
    delivered = models.DateTimeField ()
    read = models.DateTimeField ()

class Contact (models.Model):
    class Meta:
        unique_together = (('account_id', 'entity_id'),)
    account_id = models.CharField (max_length=64, db_index=True,null=False)
    entity_id  = models.CharField (max_length=64, db_index=True,null=False)
    title  = models.CharField (max_length=256)
    status = models.CharField (max_length=256)
    last_seen = models.DateTimeField ()
    picture = models.URLField ()
# Create your models here.

