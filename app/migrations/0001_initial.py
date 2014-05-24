# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'app_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
        ))
        db.send_create_signal(u'app', ['Tag'])

        # Adding model 'Quote'
        db.create_table(u'app_quote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='quotes', to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('num_upvotes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('num_downvotes', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'app', ['Quote'])

        # Adding M2M table for field tags on 'Quote'
        m2m_table_name = db.shorten_name(u'app_quote_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('quote', models.ForeignKey(orm[u'app.quote'], null=False)),
            ('tag', models.ForeignKey(orm[u'app.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['quote_id', 'tag_id'])

        # Adding model 'Upvote'
        db.create_table(u'app_upvote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quote', self.gf('django.db.models.fields.related.ForeignKey')(related_name='upvotes', to=orm['app.Quote'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='upvotes', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'app', ['Upvote'])

        # Adding model 'Downvote'
        db.create_table(u'app_downvote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quote', self.gf('django.db.models.fields.related.ForeignKey')(related_name='downvotes', to=orm['app.Quote'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='downvotes', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'app', ['Downvote'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table(u'app_tag')

        # Deleting model 'Quote'
        db.delete_table(u'app_quote')

        # Removing M2M table for field tags on 'Quote'
        db.delete_table(db.shorten_name(u'app_quote_tags'))

        # Deleting model 'Upvote'
        db.delete_table(u'app_upvote')

        # Deleting model 'Downvote'
        db.delete_table(u'app_downvote')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
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