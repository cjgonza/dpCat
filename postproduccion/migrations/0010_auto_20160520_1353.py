# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postproduccion', '0009_video_archivado'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coleccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=100, verbose_name='T\xedtulo de Colecci\xf3n')),
                ('autor', models.CharField(default=b'', max_length=255, verbose_name='Responsable')),
                ('email', models.EmailField(default=b'', max_length=254, verbose_name='Email del responsable')),
                ('tipoVideo', models.CharField(default=b'UNK', max_length=3, verbose_name=b'Tipo Producci\xc3\xb3n', choices=[(b'UNK', 'Sin definir'), (b'PIL', 'P\xedldora formativa'), (b'VID', 'Videotutoriales'), (b'EDU', 'V\xeddeos Educativos'), (b'EVE', 'Grabaci\xf3n de Eventos'), (b'OTR', 'Otros')])),
                ('objecto_aprendizaje', models.BooleanField(default=True, verbose_name='Objeto de aprendizaje')),
                ('fecha', models.DateTimeField(null=True, verbose_name='Fecha de creaci\xf3n', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='video',
            name='coleccion',
            field=models.ForeignKey(blank=True, to='postproduccion.Coleccion', null=True),
        ),
    ]
