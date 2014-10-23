# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RequestLog'
        db.create_table(u'requestlog_requestlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('query', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True, blank=True)),
            ('time_start', self.gf('django.db.models.fields.DateTimeField')()),
            ('time_end', self.gf('django.db.models.fields.DateTimeField')()),
            ('response_code', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'requestlog', ['RequestLog'])


    def backwards(self, orm):
        # Deleting model 'RequestLog'
        db.delete_table(u'requestlog_requestlog')


    models = {
        u'requestlog.requestlog': {
            'Meta': {'object_name': 'RequestLog'},
            'address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'response_code': ('django.db.models.fields.IntegerField', [], {}),
            'time_end': ('django.db.models.fields.DateTimeField', [], {}),
            'time_start': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['requestlog']