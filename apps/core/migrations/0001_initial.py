# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OperationLog'
        db.create_table(u'core_operationlog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('oper_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('operation', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('obj_class', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('obj_module', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('obj_pk', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'core', ['OperationLog'])


    def backwards(self, orm):
        # Deleting model 'OperationLog'
        db.delete_table(u'core_operationlog')


    models = {
        u'core.operationlog': {
            'Meta': {'object_name': 'OperationLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'obj_class': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'obj_module': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'obj_pk': ('django.db.models.fields.IntegerField', [], {}),
            'oper_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'operation': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['core']