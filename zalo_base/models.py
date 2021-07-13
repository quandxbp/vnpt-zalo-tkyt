from django.db import models
from django.db.models import fields


class ZaloUser(models.Model):

    name = models.CharField(max_length=200)
    user_id = models.CharField(max_length=200)
    # address = models.CharField(max_length=200)
    # city = models.CharField(max_length=200)
    # district = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)

    def __str__(self):
        return "[%s] %s - %s" % (self.user_id,self.name, self.phone)
    

class ZaloMessage(models.Model):

    message_id = models.IntegerField()
    content = models.CharField(max_length=200)
    timestamp = fields.DateTimeField()
    regist_phone = fields.CharField(max_length=200)
    regist_code = fields.CharField(max_length=200)

    def __str__(self):
        return self.content

    # @classmethod
    # def insert_history(cls, field1, field2, field3):
