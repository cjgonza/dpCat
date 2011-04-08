# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'TipoVideo'
        db.create_table('postproduccion_tipovideo', (
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('postproduccion', ['TipoVideo'])

        # Adding model 'PlantillaFDV'
        db.create_table('postproduccion_plantillafdv', (
            ('diapositiva_alto', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('diapositiva_ancho', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('fondo', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('video_mix', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=100)),
            ('video_alto', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('diapositiva_mix', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=100)),
            ('diapositiva_y', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('diapositiva_x', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('video_tipo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='t_vid', to=orm['postproduccion.TipoVideo'])),
            ('diapositiva_tipo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='t_diap', to=orm['postproduccion.TipoVideo'])),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('video_y', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('video_x', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('video_ancho', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('postproduccion', ['PlantillaFDV'])

        # Adding model 'Video'
        db.create_table('postproduccion_video', (
            ('status', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('plantilla', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['postproduccion.PlantillaFDV'], null=True, blank=True)),
            ('fichero', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('autor', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('caca', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('descripcion', self.gf('django.db.models.fields.TextField')()),
            ('titulo', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('postproduccion', ['Video'])

        # Adding model 'FicheroEntrada'
        db.create_table('postproduccion_ficheroentrada', (
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['postproduccion.Video'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['postproduccion.TipoVideo'])),
            ('fichero', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('postproduccion', ['FicheroEntrada'])

        # Adding model 'Cola'
        db.create_table('postproduccion_cola', (
            ('status', self.gf('django.db.models.fields.CharField')(default='PEN', max_length=3)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['postproduccion.Video'])),
            ('comienzo', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('logfile', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('fin', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('postproduccion', ['Cola'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'TipoVideo'
        db.delete_table('postproduccion_tipovideo')

        # Deleting model 'PlantillaFDV'
        db.delete_table('postproduccion_plantillafdv')

        # Deleting model 'Video'
        db.delete_table('postproduccion_video')

        # Deleting model 'FicheroEntrada'
        db.delete_table('postproduccion_ficheroentrada')

        # Deleting model 'Cola'
        db.delete_table('postproduccion_cola')
    
    
    models = {
        'postproduccion.cola': {
            'Meta': {'object_name': 'Cola'},
            'comienzo': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PEN'", 'max_length': '3'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postproduccion.Video']"})
        },
        'postproduccion.ficheroentrada': {
            'Meta': {'object_name': 'FicheroEntrada'},
            'fichero': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postproduccion.TipoVideo']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postproduccion.Video']"})
        },
        'postproduccion.plantillafdv': {
            'Meta': {'object_name': 'PlantillaFDV'},
            'diapositiva_alto': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'diapositiva_ancho': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'diapositiva_mix': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '100'}),
            'diapositiva_tipo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'t_diap'", 'to': "orm['postproduccion.TipoVideo']"}),
            'diapositiva_x': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'diapositiva_y': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'fondo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'video_alto': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'video_ancho': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'video_mix': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '100'}),
            'video_tipo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'t_vid'", 'to': "orm['postproduccion.TipoVideo']"}),
            'video_x': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'video_y': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'postproduccion.tipovideo': {
            'Meta': {'object_name': 'TipoVideo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'postproduccion.video': {
            'Meta': {'object_name': 'Video'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'caca': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fichero': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plantilla': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postproduccion.PlantillaFDV']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }
    
    complete_apps = ['postproduccion']
