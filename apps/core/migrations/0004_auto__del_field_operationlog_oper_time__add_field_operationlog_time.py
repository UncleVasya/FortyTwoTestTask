# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'OperationLog.oper_time'
        db.delete_column(u'core_operationlog', 'oper_time')

        # Adding field 'OperationLog.time'
        db.add_column(u'core_operationlog', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 7, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'OperationLog.oper_time'
        db.add_column(u'core_operationlog', 'oper_time',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 11, 7, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'OperationLog.time'
        db.delete_column(u'core_operationlog', 'time')


    models = {
        u'core.operationlog': {
            'Meta': {'object_name': 'OperationLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'obj_class': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'obj_module': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'obj_pk': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'operation': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['core']