# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postproduccion', '0003_auto_20151201_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicocodificacion',
            name='status',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='email',
            field=models.EmailField(max_length=75, verbose_name='Email del responsable'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='video',
            name='tipoVideo',
            field=models.CharField(default=b'UNK', max_length=3, verbose_name=b'Tipo Producci\xc3\xb3n', choices=[(b'UNK', 'Sin definir'), (b'PIL', 'P\xedldora formativa'), (b'VID', 'Videotutoriales'), (b'EDU', 'V\xeddeos Educativos'), (b'EVE', 'Grabaci\xf3n de Eventos'), (b'OTR', 'Otros')]),
            preserve_default=True,
        ),
    ]
