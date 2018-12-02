from django.db import models
from django.conf import settings


class TelegramBot(models.Model):
    username = models.CharField(max_length=64)
    token = models.CharField(max_length=80)
    webhook_url = models.CharField(max_length=64, unique=True)


class Checklist(models.Model):
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=32, unique=True)
    logo_image = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField()
    bot = models.ForeignKey(TelegramBot, models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    checklist = models.ForeignKey(Checklist, models.CASCADE)
    ordernum = models.IntegerField(default=0)
    text = models.CharField(max_length=512)
    answer_type = models.CharField(max_length=4, choices=[
        ('bool', 'Yes/No'),
        ('text', 'Text'),
    ], default='bool')

    def __str__(self):
        return self.text


# a set of answers of a User to items in a checklist
class Session(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    checklist = models.ForeignKey(Checklist, models.CASCADE)


class YesNoAnswer(models.Model):
    session = models.ForeignKey(Session, models.CASCADE)
    item = models.ForeignKey(Item, models.CASCADE)
    value = models.BooleanField()


class TextAnswer(models.Model):
    session = models.ForeignKey(Session, models.CASCADE)
    item = models.ForeignKey(Item, models.CASCADE)
    value = models.CharField(max_length=1024)
