# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RequestLog.priority'
        db.add_column(u'requestlog_requestlog', 'priority',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RequestLog.priority'
        db.delete_column(u'requestlog_requestlog', 'priority')


    models = {
        u'requestlog.requestlog': {
            'Meta': {'object_name': 'RequestLog'},
            'address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'priority': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'query': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'response_code': ('django.db.models.fields.IntegerField', [], {}),
            'time_end': ('django.db.models.fields.DateTimeField', [], {}),
            'time_start': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['requestlog']