# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postproduccion', '0008_auto_20160330_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitudReserva',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('fecha_reserva', models.DateTimeField()),
            ],
        ),
    ]
