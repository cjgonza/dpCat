# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postproduccion', '0007_auto_20160330_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metadatagen',
            name='transcription',
            field=models.TextField(help_text='Texto que se narra en el v\xeddeo.', null=True, verbose_name='Transcripci\xf3n', blank=True),
        ),
    ]
