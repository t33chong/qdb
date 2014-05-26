from django.contrib import admin

from updown.models import Vote
from app.models import Tag, Quote

admin.site.register(Tag)
admin.site.register(Quote)
admin.site.register(Vote)
