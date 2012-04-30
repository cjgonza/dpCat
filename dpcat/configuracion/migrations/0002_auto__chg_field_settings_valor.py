# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'Settings.valor'
        db.alter_column('configuracion_settings', 'valor', self.gf('django.db.models.fields.TextField')())
    
    
    def backwards(self, orm):
        
        # Changing field 'Settings.valor'
        db.alter_column('configuracion_settings', 'valor', self.gf('django.db.models.fields.CharField')(max_length=255))
    
    
    models = {
        'configuracion.settings': {
            'Meta': {'object_name': 'Settings'},
            'clave': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'valor': ('django.db.models.fields.TextField', [], {})
        }
    }
    
    complete_apps = ['configuracion']
