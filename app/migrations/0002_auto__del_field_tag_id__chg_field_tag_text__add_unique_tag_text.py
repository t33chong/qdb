# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Tag.id'
        db.delete_column(u'app_tag', u'id')


        # Changing field 'Tag.text'
        db.alter_column(u'app_tag', 'text', self.gf('django.db.models.fields.CharField')(max_length=64, primary_key=True))
        # Adding unique constraint on 'Tag', fields ['text']
        db.create_unique(u'app_tag', ['text'])


    def backwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['text']
        db.delete_unique(u'app_tag', ['text'])


        # User chose to not deal with backwards NULL issues for 'Tag.id'
        raise RuntimeError("Cannot reverse this migration. 'Tag.id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Tag.id'
        db.add_column(u'app_tag', u'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True),
                      keep_default=False)


        # Changing field 'Tag.text'
        db.alter_column(u'app_tag', 'text', self.gf('django.db.models.fields.CharField')(max_length=64))

    models = {
        u'app.downvote': {
            'Meta': {'object_name': 'Downvote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quote': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'downvotes'", 'to': u"orm['app.Quote']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'downvotes'", 'to': u"orm['auth.User']"})
        },
        u'app.quote': {
            'Meta': {'object_name': 'Quote'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_downvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_upvotes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quotes'", 'to': u"orm['auth.User']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'quotes'", 'symmetrical': 'False', 'to': u"orm['app.Tag']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'app.tag': {
            'Meta': {'object_name': 'Tag'},
            'text': ('django.db.models.fields.CharField', [], {'max_length': '64', 'primary_key': 'True'})
        },
        u'app.upvote': {
            'Meta': {'object_name': 'Upvote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quote': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'upvotes'", 'to': u"orm['app.Quote']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'upvotes'", 'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['app']