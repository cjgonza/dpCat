# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'Metadata.subtitulo'
        db.delete_column('postproduccion_metadata', 'subtitulo')

        # Deleting field 'Metadata.autor'
        db.delete_column('postproduccion_metadata', 'autor')

        # Deleting field 'Metadata.descripcion'
        db.delete_column('postproduccion_metadata', 'descripcion')

        # Deleting field 'Metadata.titulo'
        db.delete_column('postproduccion_metadata', 'titulo')

        # Adding field 'Metadata.dificulty'
        db.add_column('postproduccion_metadata', 'dificulty', self.gf('django.db.models.fields.CharField')(default=' ', max_length=2), keep_default=False)

        # Adding field 'Metadata.creator'
        db.add_column('postproduccion_metadata', 'creator', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Adding field 'Metadata.typical_age_range'
        db.add_column('postproduccion_metadata', 'typical_age_range', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Adding field 'Metadata.contributor'
        db.add_column('postproduccion_metadata', 'contributor', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Adding field 'Metadata.interactivity_level'
        db.add_column('postproduccion_metadata', 'interactivity_level', self.gf('django.db.models.fields.CharField')(default=' ', max_length=2), keep_default=False)

        # Adding field 'Metadata.learning_resource_type'
        db.add_column('postproduccion_metadata', 'learning_resource_type', self.gf('django.db.models.fields.CharField')(default=' ', max_length=2), keep_default=False)

        # Adding field 'Metadata.educational_language'
        db.add_column('postproduccion_metadata', 'educational_language', self.gf('django.db.models.fields.CharField')(default=' ', max_length=2), keep_default=False)

        # Adding field 'Metadata.title'
        db.add_column('postproduccion_metadata', 'title', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Adding field 'Metadata.temporal'
        db.add_column('postproduccion_metadata', 'temporal', self.gf('django.db.models.fields.TextField')(null=True), keep_default=False)

        # Adding field 'Metadata.guideline'
        db.add_column('postproduccion_metadata', 'guideline', self.gf('django.db.models.fields.CharField')(default=' ', max_length=2), keep_default=False)

        # Adding field 'Metadata.source'
        db.add_column('postproduccion_metadata', 'source', self.gf('django.db.models.fields.CharField')(max_length=255, null=True), keep_default=False)

        # Adding field 'Metadata.interactivity_type'
        db.add_column('postproduccion_metadata', 'interactivity_type', self.gf('django.db.models.fields.CharField')(default=' ', max_length=2), keep_default=False)

        # Adding field 'Metadata.valid'
        db.add_column('postproduccion_metadata', 'valid', self.gf('django.db.models.fields.DateTimeField')(default=datetime.date(2011, 6, 2)), keep_default=False)

        # Adding field 'Metadata.location'
        db.add_column('postproduccion_metadata', 'location', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Adding field 'Metadata.ispartof'
        db.add_column('postproduccion_metadata', 'ispartof', self.gf('django.db.models.fields.CharField')(max_length=255, null=True), keep_default=False)

        # Adding field 'Metadata.type'
        db.add_column('postproduccion_metadata', 'type', self.gf('django.db.models.fields.CharField')(default=' ', max_length=2), keep_default=False)

        # Adding field 'Metadata.description'
        db.add_column('postproduccion_metadata', 'description', self.gf('django.db.models.fields.TextField')(default=' '), keep_default=False)

        # Adding field 'Metadata.format'
        db.add_column('postproduccion_metadata', 'format', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Adding field 'Metadata.intented_end_user_role'
        db.add_column('postproduccion_metadata', 'intented_end_user_role', self.gf('django.db.models.fields.CharField')(default=' ', max_length=2), keep_default=False)

        # Adding field 'Metadata.language'
        db.add_column('postproduccion_metadata', 'language', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Adding field 'Metadata.purpose'
        db.add_column('postproduccion_metadata', 'purpose', self.gf('django.db.models.fields.CharField')(default=' ', max_length=2), keep_default=False)

        # Adding field 'Metadata.extent'
        db.add_column('postproduccion_metadata', 'extent', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Adding field 'Metadata.date'
        db.add_column('postproduccion_metadata', 'date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.date(2011, 6, 2)), keep_default=False)

        # Adding field 'Metadata.unesco'
        db.add_column('postproduccion_metadata', 'unesco', self.gf('django.db.models.fields.CharField')(default=' ', max_length=2), keep_default=False)

        # Adding field 'Metadata.typical_learning_time'
        db.add_column('postproduccion_metadata', 'typical_learning_time', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Adding field 'Metadata.semantic_density'
        db.add_column('postproduccion_metadata', 'semantic_density', self.gf('django.db.models.fields.CharField')(default=' ', max_length=2), keep_default=False)

        # Adding field 'Metadata.publisher'
        db.add_column('postproduccion_metadata', 'publisher', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Adding field 'Metadata.keyword'
        db.add_column('postproduccion_metadata', 'keyword', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Adding field 'Metadata.license'
        db.add_column('postproduccion_metadata', 'license', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Adding field 'Metadata.created'
        db.add_column('postproduccion_metadata', 'created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.date(2011, 6, 2)), keep_default=False)

        # Adding field 'Metadata.rightsholder'
        db.add_column('postproduccion_metadata', 'rightsholder', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Adding field 'Metadata.venue'
        db.add_column('postproduccion_metadata', 'venue', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)

        # Adding field 'Metadata.modified'
        db.add_column('postproduccion_metadata', 'modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.date(2011, 6, 2)), keep_default=False)

        # Adding field 'Metadata.audience'
        db.add_column('postproduccion_metadata', 'audience', self.gf('django.db.models.fields.CharField')(default=' ', max_length=2), keep_default=False)

        # Adding field 'Metadata.context'
        db.add_column('postproduccion_metadata', 'context', self.gf('django.db.models.fields.CharField')(default=' ', max_length=2), keep_default=False)

        # Adding field 'Metadata.relation'
        db.add_column('postproduccion_metadata', 'relation', self.gf('django.db.models.fields.CharField')(max_length=255, null=True), keep_default=False)

        # Adding field 'Metadata.identifier'
        db.add_column('postproduccion_metadata', 'identifier', self.gf('django.db.models.fields.CharField')(default=' ', max_length=255), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Adding field 'Metadata.subtitulo'
        db.add_column('postproduccion_metadata', 'subtitulo', self.gf('django.db.models.fields.CharField')(default=' ', max_length=100), keep_default=False)

        # Adding field 'Metadata.autor'
        db.add_column('postproduccion_metadata', 'autor', self.gf('django.db.models.fields.CharField')(default=' ', max_length=30), keep_default=False)

        # Adding field 'Metadata.descripcion'
        db.add_column('postproduccion_metadata', 'descripcion', self.gf('django.db.models.fields.TextField')(default=' '), keep_default=False)

        # Adding field 'Metadata.titulo'
        db.add_column('postproduccion_metadata', 'titulo', self.gf('django.db.models.fields.CharField')(default=' ', max_length=30), keep_default=False)

        # Deleting field 'Metadata.dificulty'
        db.delete_column('postproduccion_metadata', 'dificulty')

        # Deleting field 'Metadata.creator'
        db.delete_column('postproduccion_metadata', 'creator')

        # Deleting field 'Metadata.typical_age_range'
        db.delete_column('postproduccion_metadata', 'typical_age_range')

        # Deleting field 'Metadata.contributor'
        db.delete_column('postproduccion_metadata', 'contributor')

        # Deleting field 'Metadata.interactivity_level'
        db.delete_column('postproduccion_metadata', 'interactivity_level')

        # Deleting field 'Metadata.learning_resource_type'
        db.delete_column('postproduccion_metadata', 'learning_resource_type')

        # Deleting field 'Metadata.educational_language'
        db.delete_column('postproduccion_metadata', 'educational_language')

        # Deleting field 'Metadata.title'
        db.delete_column('postproduccion_metadata', 'title')

        # Deleting field 'Metadata.temporal'
        db.delete_column('postproduccion_metadata', 'temporal')

        # Deleting field 'Metadata.guideline'
        db.delete_column('postproduccion_metadata', 'guideline')

        # Deleting field 'Metadata.source'
        db.delete_column('postproduccion_metadata', 'source')

        # Deleting field 'Metadata.interactivity_type'
        db.delete_column('postproduccion_metadata', 'interactivity_type')

        # Deleting field 'Metadata.valid'
        db.delete_column('postproduccion_metadata', 'valid')

        # Deleting field 'Metadata.location'
        db.delete_column('postproduccion_metadata', 'location')

        # Deleting field 'Metadata.ispartof'
        db.delete_column('postproduccion_metadata', 'ispartof')

        # Deleting field 'Metadata.type'
        db.delete_column('postproduccion_metadata', 'type')

        # Deleting field 'Metadata.description'
        db.delete_column('postproduccion_metadata', 'description')

        # Deleting field 'Metadata.format'
        db.delete_column('postproduccion_metadata', 'format')

        # Deleting field 'Metadata.intented_end_user_role'
        db.delete_column('postproduccion_metadata', 'intented_end_user_role')

        # Deleting field 'Metadata.language'
        db.delete_column('postproduccion_metadata', 'language')

        # Deleting field 'Metadata.purpose'
        db.delete_column('postproduccion_metadata', 'purpose')

        # Deleting field 'Metadata.extent'
        db.delete_column('postproduccion_metadata', 'extent')

        # Deleting field 'Metadata.date'
        db.delete_column('postproduccion_metadata', 'date')

        # Deleting field 'Metadata.unesco'
        db.delete_column('postproduccion_metadata', 'unesco')

        # Deleting field 'Metadata.typical_learning_time'
        db.delete_column('postproduccion_metadata', 'typical_learning_time')

        # Deleting field 'Metadata.semantic_density'
        db.delete_column('postproduccion_metadata', 'semantic_density')

        # Deleting field 'Metadata.publisher'
        db.delete_column('postproduccion_metadata', 'publisher')

        # Deleting field 'Metadata.keyword'
        db.delete_column('postproduccion_metadata', 'keyword')

        # Deleting field 'Metadata.license'
        db.delete_column('postproduccion_metadata', 'license')

        # Deleting field 'Metadata.created'
        db.delete_column('postproduccion_metadata', 'created')

        # Deleting field 'Metadata.rightsholder'
        db.delete_column('postproduccion_metadata', 'rightsholder')

        # Deleting field 'Metadata.venue'
        db.delete_column('postproduccion_metadata', 'venue')

        # Deleting field 'Metadata.modified'
        db.delete_column('postproduccion_metadata', 'modified')

        # Deleting field 'Metadata.audience'
        db.delete_column('postproduccion_metadata', 'audience')

        # Deleting field 'Metadata.context'
        db.delete_column('postproduccion_metadata', 'context')

        # Deleting field 'Metadata.relation'
        db.delete_column('postproduccion_metadata', 'relation')

        # Deleting field 'Metadata.identifier'
        db.delete_column('postproduccion_metadata', 'identifier')
    
    
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
            'audience': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'context': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'contributor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {}),
            'creator': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'dificulty': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'educational_language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'extent': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'format': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'guideline': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'intented_end_user_role': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'interactivity_level': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'interactivity_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'ispartof': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'learning_resource_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'publisher': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'relation': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'rightsholder': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'semantic_density': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'temporal': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'typical_age_range': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'typical_learning_time': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'unesco': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'valid': ('django.db.models.fields.DateTimeField', [], {}),
            'venue': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fichero': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plantilla': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['postproduccion.PlantillaFDV']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'INC'", 'max_length': '3'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['postproduccion']
