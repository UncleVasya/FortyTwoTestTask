# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'OperationLog.obj_pk'
        db.alter_column(u'core_operationlog', 'obj_pk', self.gf('django.db.models.fields.PositiveIntegerField')())

    def backwards(self, orm):

        # Changing field 'OperationLog.obj_pk'
        db.alter_column(u'core_operationlog', 'obj_pk', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'core.operationlog': {
            'Meta': {'object_name': 'OperationLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'obj_class': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'obj_module': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'obj_pk': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'oper_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'operation': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['core']