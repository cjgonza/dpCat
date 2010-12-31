# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'PlantillaFDV.diapositiva_alto'
        db.delete_column('postproduccion_plantillafdv', 'diapositiva_alto')

        # Deleting field 'PlantillaFDV.diapositiva_ancho'
        db.delete_column('postproduccion_plantillafdv', 'diapositiva_ancho')

        # Deleting field 'PlantillaFDV.video_mix'
        db.delete_column('postproduccion_plantillafdv', 'video_mix')

        # Deleting field 'PlantillaFDV.video_alto'
        db.delete_column('postproduccion_plantillafdv', 'video_alto')

        # Deleting field 'PlantillaFDV.diapositiva_mix'
        db.delete_column('postproduccion_plantillafdv', 'diapositiva_mix')

        # Deleting field 'PlantillaFDV.diapositiva_y'
        db.delete_column('postproduccion_plantillafdv', 'diapositiva_y')

        # Deleting field 'PlantillaFDV.diapositiva_x'
        db.delete_column('postproduccion_plantillafdv', 'diapositiva_x')

        # Deleting field 'PlantillaFDV.video_tipo'
        db.delete_column('postproduccion_plantillafdv', 'video_tipo_id')

        # Deleting field 'PlantillaFDV.diapositiva_tipo'
        db.delete_column('postproduccion_plantillafdv', 'diapositiva_tipo_id')

        # Deleting field 'PlantillaFDV.video_y'
        db.delete_column('postproduccion_plantillafdv', 'video_y')

        # Deleting field 'PlantillaFDV.video_x'
        db.delete_column('postproduccion_plantillafdv', 'video_x')

        # Deleting field 'PlantillaFDV.video_ancho'
        db.delete_column('postproduccion_plantillafdv', 'video_ancho')
    
    
    def backwards(self, orm):
        
        # Adding field 'PlantillaFDV.diapositiva_alto'
        db.add_column('postproduccion_plantillafdv', 'diapositiva_alto', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0), keep_default=False)

        # Adding field 'PlantillaFDV.diapositiva_ancho'
        db.add_column('postproduccion_plantillafdv', 'diapositiva_ancho', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0), keep_default=False)

        # Adding field 'PlantillaFDV.video_mix'
        db.add_column('postproduccion_plantillafdv', 'video_mix', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=100), keep_default=False)

        # Adding field 'PlantillaFDV.video_alto'
        db.add_column('postproduccion_plantillafdv', 'video_alto', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0), keep_default=False)

        # Adding field 'PlantillaFDV.diapositiva_mix'
        db.add_column('postproduccion_plantillafdv', 'diapositiva_mix', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=100), keep_default=False)

        # Adding field 'PlantillaFDV.diapositiva_y'
        db.add_column('postproduccion_plantillafdv', 'diapositiva_y', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0), keep_default=False)

        # Adding field 'PlantillaFDV.diapositiva_x'
        db.add_column('postproduccion_plantillafdv', 'diapositiva_x', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0), keep_default=False)

        # Adding field 'PlantillaFDV.video_tipo'
        db.add_column('postproduccion_plantillafdv', 'video_tipo', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='t_vid', to=orm['postproduccion.TipoVideo']), keep_default=False)

        # Adding field 'PlantillaFDV.diapositiva_tipo'
        db.add_column('postproduccion_plantillafdv', 'diapositiva_tipo', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='t_diap', to=orm['postproduccion.TipoVideo']), keep_default=False)

        # Adding field 'PlantillaFDV.video_y'
        db.add_column('postproduccion_plantillafdv', 'video_y', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0), keep_default=False)

        # Adding field 'PlantillaFDV.video_x'
        db.add_column('postproduccion_plantillafdv', 'video_x', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0), keep_default=False)

        # Adding field 'PlantillaFDV.video_ancho'
        db.add_column('postproduccion_plantillafdv', 'video_ancho', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0), keep_default=False)
    
    
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '30'})
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
