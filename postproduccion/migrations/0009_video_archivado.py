# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postproduccion', '0008_auto_20160330_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='archivado',
            field=models.BooleanField(default=False, verbose_name='Archivar'),
        ),
    ]
