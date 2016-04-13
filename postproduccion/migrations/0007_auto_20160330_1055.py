# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postproduccion', '0006_metadatagen_transcription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metadatagen',
            name='transcription',
            field=models.TextField(null=True, verbose_name='Transcripci\xf3n', blank=True),
        ),
    ]
