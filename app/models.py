import re
from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    text = models.CharField(max_length=64, primary_key=True)

    @staticmethod
    def make_valid_tag(text):
        return re.sub('\W+', '_', text).lower()[:64]

    def __unicode__(self):
        return self.text


class Quote(models.Model):
    text = models.TextField()
    submitter = models.ForeignKey(User, related_name='quotes')
    date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='quotes')
    num_upvotes = models.IntegerField(default=0)
    num_downvotes = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.text)[:32]


class Upvote(models.Model):
    quote = models.ForeignKey(Quote, related_name='upvotes')
    user = models.ForeignKey(User, related_name='upvotes')

    def __unicode__(self):
        return u'%s->%s' % (self.user.username, self.quote.text[:32])


class Downvote(models.Model):
    quote = models.ForeignKey(Quote, related_name='downvotes')
    user = models.ForeignKey(User, related_name='downvotes')

    def __unicode__(self):
        return u'%s->%s' % (self.user.username, self.quote.text[:32])
