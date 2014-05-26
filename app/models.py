import re
from django.contrib.auth.models import User
from django.db import models
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField
from ratings.models import Ratings


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
    ratings = Ratings()

    search_index = VectorField()
    objects = models.Manager()
    search_manager = SearchManager(
        fields=('text',), config='pg_catalog.english',
        search_field='search_index', auto_update_search_field=True)

    def user_has_rated(self, user):
        try:
            self.ratings.get(user=user)
        except:
            return False
        else:
            return True
        #return bool(self.ratings.filter(user=user).first())

    def __unicode__(self):
        return unicode(self.text)[:32]
