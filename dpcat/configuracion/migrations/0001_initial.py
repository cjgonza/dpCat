# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Settings'
        db.create_table('configuracion_settings', (
            ('clave', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('valor', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('configuracion', ['Settings'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Settings'
        db.delete_table('configuracion_settings')
    
    
    models = {
        'configuracion.settings': {
            'Meta': {'object_name': 'Settings'},
            'clave': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'valor': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['configuracion']
