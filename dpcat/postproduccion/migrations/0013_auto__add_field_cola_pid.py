# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Cola.pid'
        db.add_column('postproduccion_cola', 'pid', self.gf('django.db.models.fields.IntegerField')(null=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Cola.pid'
        db.delete_column('postproduccion_cola', 'pid')
    
    
    models = {
        'postproduccion.cola': {
            'Meta': {'object_name': 'Cola'},
            'comienzo': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'fin': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pid': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PEN'", 'max_length': '3'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postproduccion.Video']"})
        },
        'postproduccion.ficheroentrada': {
            'Meta': {'object_name': 'FicheroEntrada'},
            'fichero': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postproduccion.TipoVideo']", 'null': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postproduccion.Video']"})
        },
        'postproduccion.plantillafdv': {
            'Meta': {'object_name': 'PlantillaFDV'},
            'fondo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'postproduccion.previsualizacion': {
            'Meta': {'object_name': 'Previsualizacion'},
            'fichero': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['postproduccion.Video']", 'unique': 'True'})
        },
        'postproduccion.tecdata': {
            'Meta': {'object_name': 'TecData'},
            'audio_bitrate': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'audio_channels': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'audio_codec': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'audio_rate': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'bitrate': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'duration': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'video': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['postproduccion.Video']", 'unique': 'True'}),
            'video_bitrate': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'video_codec': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'video_color': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'video_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'video_rate': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'video_wh_ratio': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'video_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        },
        'postproduccion.tipovideo': {
            'Meta': {'object_name': 'TipoVideo'},
            'alto': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'ancho': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mix': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '100'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'plantilla': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postproduccion.PlantillaFDV']"}),
            'x': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'y': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
        },
        'postproduccion.video': {
            'Meta': {'object_name': 'Video'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fecha_grabacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fichero': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'plantilla': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postproduccion.PlantillaFDV']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'INC'", 'max_length': '3'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }
    
    complete_apps = ['postproduccion']
