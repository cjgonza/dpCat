# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('clave', models.CharField(unique=True, max_length=30)),
                ('valor', models.TextField()),
            ],
            options={
                'verbose_name': 'configuraci\xf3n',
                'verbose_name_plural': 'configuraciones',
            },
        ),
    ]
