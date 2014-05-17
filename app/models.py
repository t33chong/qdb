from django.contrib.auth.models import User
from django.db import models


class Quote(models.Model):
    text = models.TextField()
    submitter = models.ForeignKey(User)
    date = models.DateTimeField()
    tags = models.ManyToManyField(Tag)
    num_upvotes = models.IntegerField(default=0)
    num_downvotes = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode(self.text)[:32]


class Tag(models.Model):
    text = models.CharField(max_length=64)

    def __unicode__(self):
        return self.text


class Upvote(models.Model):
    quote = models.ForeignKey(Quote, related_name='upvotes')
    user = models.ForeignKey(User, related_name='upvotes')


class Downvote(models.Model):
    quote = models.ForeignKey(Quote, related_name='downvotes')
    user = models.ForeignKey(User, related_name='downvotes')
