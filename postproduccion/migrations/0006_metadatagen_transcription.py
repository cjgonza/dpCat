# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postproduccion', '0005_auto_20160315_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='metadatagen',
            name='transcription',
            field=models.CharField(max_length=255, null=True, verbose_name='Transcripci\xf3n', blank=True),
        ),
    ]
