# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postproduccion', '0002_video_tipovideo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='tipoVideo',
            field=models.CharField(default=b'UNK', max_length=3, choices=[(b'PIL', 'P\xedldora formativa'), (b'UNK', 'Sin definir'), (b'EXP', 'Expr\xe9sate'), (b'VID', 'Videotutoriales'), (b'EDU', 'V\xeddeos Educativos'), (b'PRA', 'V\xeddeo Pr\xe1cticas'), (b'INN', 'Innovaci\xf3n Educativa')]),
        ),
    ]
