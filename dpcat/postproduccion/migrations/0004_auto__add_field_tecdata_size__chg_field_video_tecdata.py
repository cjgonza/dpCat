# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'TecData.size'
        db.add_column('postproduccion_tecdata', 'size', self.gf('django.db.models.fields.PositiveIntegerField')(null=True), keep_default=False)

        # Changing field 'Video.tecdata'
        db.alter_column('postproduccion_video', 'tecdata_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['postproduccion.TecData'], unique=True, null=True, blank=True))
    
    
    def backwards(self, orm):
        
        # Deleting field 'TecData.size'
        db.delete_column('postproduccion_tecdata', 'size')

        # Changing field 'Video.tecdata'
        db.alter_column('postproduccion_video', 'tecdata_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['postproduccion.TecData'], unique=True, null=True))
    
    
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
        'postproduccion.tecdata': {
            'Meta': {'object_name': 'TecData'},
            'audio_bitrate': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'audio_channels': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'audio_codec': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'audio_rate': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'bitrate': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'duration': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'size': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'video_bitrate': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'video_codec': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'video_color': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'video_height': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'}),
            'video_rate': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'video_wh_ratio': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'video_width': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True'})
        },
        'postproduccion.tipovideo': {
            'Meta': {'object_name': 'TipoVideo'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'postproduccion.video': {
            'Meta': {'object_name': 'Video'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fichero': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plantilla': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postproduccion.PlantillaFDV']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'tecdata': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['postproduccion.TecData']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }
    
    complete_apps = ['postproduccion']
