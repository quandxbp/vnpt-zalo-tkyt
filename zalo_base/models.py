from django.db import models
from django.db.models import fields


class ZaloUser(models.Model):

    name = models.CharField(max_length=200)
    user_id = models.IntegerField()

    def __str__(self):
        return self.name

class ZaloMessage(models.Model):

    message_id = models.IntegerField()
    content = models.CharField(max_length=200)
    timestamp = fields.DateTimeField()
    regist_phone = fields.CharField(max_length=200)
    regist_code = fields.CharField(max_length=200)

    def __str__(self):
        return self.content

    def parse_message_content(self):
        print(1)
