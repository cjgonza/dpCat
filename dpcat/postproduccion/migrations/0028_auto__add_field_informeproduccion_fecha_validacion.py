# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'InformeProduccion.fecha_validacion'
        db.add_column('postproduccion_informeproduccion', 'fecha_validacion', self.gf('django.db.models.fields.DateTimeField')(null=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'InformeProduccion.fecha_validacion'
        db.delete_column('postproduccion_informeproduccion', 'fecha_validacion')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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
        'postproduccion.historicocodificacion': {
            'Meta': {'object_name': 'HistoricoCodificacion'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'informe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postproduccion.InformeProduccion']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        'postproduccion.incidenciaproduccion': {
            'Meta': {'object_name': 'IncidenciaProduccion'},
            'aceptado': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'comentario': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'emisor': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'informe': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postproduccion.InformeProduccion']"})
        },
        'postproduccion.informeproduccion': {
            'Meta': {'object_name': 'InformeProduccion'},
            'aprobacion': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'fecha_grabacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fecha_validacion': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observacion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'operador': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'video': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['postproduccion.Video']", 'unique': 'True'})
        },
        'postproduccion.metadata': {
            'Meta': {'object_name': 'Metadata'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'descripcion': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subtitulo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'video': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['postproduccion.Video']", 'unique': 'True'})
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
            'duration': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'txt_data': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'video': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['postproduccion.Video']", 'unique': 'True'}),
            'xml_data': ('django.db.models.fields.TextField', [], {'null': 'True'})
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
        'postproduccion.token': {
            'Meta': {'object_name': 'Token'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instante': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'video': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['postproduccion.Video']", 'unique': 'True'})
        },
        'postproduccion.video': {
            'Meta': {'object_name': 'Video'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fichero': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plantilla': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postproduccion.PlantillaFDV']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'INC'", 'max_length': '3'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        }
    }
    
    complete_apps = ['postproduccion']
