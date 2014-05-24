import re
from django.contrib.auth.models import User
from django.db import models
from updown.fields import RatingField


class Tag(models.Model):
    text = models.CharField(max_length=64, unique=True)

    @staticmethod
    def make_valid_tag(text):
        return re.sub('\W+', '', text).lower()[:64]

    def __unicode__(self):
        return self.text


class Quote(models.Model):
    text = models.TextField()
    submitter = models.ForeignKey(User, related_name='quotes')
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='quotes')
    rating = RatingField(can_change_vote=True)

    def __unicode__(self):
        return unicode(self.text)[:32]
