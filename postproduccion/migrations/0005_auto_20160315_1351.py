# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postproduccion', '0004_auto_20160315_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Email del responsable'),
        ),
    ]
