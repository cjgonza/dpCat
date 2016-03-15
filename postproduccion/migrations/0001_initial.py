# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cola',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'PEN', max_length=3, choices=[(b'PEN', b'Pendiente'), (b'PRO', b'Procesando'), (b'HEC', b'Hecho'), (b'ERR', b'Error')])),
                ('tipo', models.CharField(max_length=3, choices=[(b'COP', 'Copia'), (b'PIL', 'Producci\xf3n'), (b'PRE', 'Previsualizaci\xf3n')])),
                ('comienzo', models.DateTimeField(null=True, blank=True)),
                ('fin', models.DateTimeField(null=True, blank=True)),
                ('logfile', models.FileField(null=True, upload_to=b'logs', blank=True)),
                ('pid', models.IntegerField(null=True, editable=False)),
            ],
            options={
                'verbose_name': 'tarea',
                'verbose_name_plural': 'tareas',
            },
        ),
        migrations.CreateModel(
            name='FicheroEntrada',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fichero', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='HistoricoCodificacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=3, choices=[(b'COP', 'Copia'), (b'PIL', 'P\xedldora'), (b'PRE', 'Previsualizaci\xf3n')])),
                ('fecha', models.DateTimeField()),
                ('status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='IncidenciaProduccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comentario', models.TextField(null=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('aceptado', models.NullBooleanField()),
                ('emisor', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InformeProduccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('observacion', models.TextField(null=True, blank=True)),
                ('fecha_grabacion', models.DateTimeField()),
                ('fecha_produccion', models.DateTimeField(auto_now_add=True)),
                ('fecha_validacion', models.DateTimeField(null=True, blank=True)),
                ('aprobacion', models.BooleanField(default=True)),
                ('operador', models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MetadataGen',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('knowledge_areas', models.CharField(max_length=2, verbose_name='Clasificaci\xf3n Universidad', choices=[('Ciencias de la Salud', ((b'AB', 'Anatom\xeda Patol\xf3gica [020]'), (b'AC', 'Anatom\xeda y Anatom\xeda Patol\xf3gica Comparadas [025]'), (b'AD', 'Anatom\xeda y Embriolog\xeda Humana [027]'), (b'FC', 'Antropolog\xeda F\xedsica [028]'), (b'CJ', 'Biolog\xeda Celular [050]'), (b'AE', 'Cirug\xeda [090]'), (b'AF', 'Dermatolog\xeda [183]'), (b'AG', 'Enfermer\xeda [255]'), (b'AH', 'Estomatolog\xeda [275]'), (b'AI', 'Farmacia y Tecnolog\xeda Farmac\xe9utica [310]'), (b'AJ', 'Farmacolog\xeda [315]'), (b'CP', 'Fisiolog\xeda [410]'), (b'AK', 'Fisioterapia [413]'), (b'CR', 'Gen\xe9tica [420]'), (b'AL', 'Histolog\xeda [443]'), (b'AM', 'Inmunolog\xeda [566]'), (b'AN', 'Medicina [610]'), (b'AO', 'Medicina Legal y Forense [613]'), (b'AP', 'Medicina Preventiva y Salud P\xfablica [615]'), (b'AQ', 'Medicina y Cirug\xeda Animal [617]'), (b'AR', 'Nutrici\xf3n y Bromatolog\xeda [640]'), (b'AS', 'Obstetricia y Ginecolog\xeda [645]'), (b'AT', 'Oftalmolog\xeda [646]'), (b'AV', 'Otorrinolaringolog\xeda [653]'), (b'AW', 'Parasitolog\xeda [660]'), (b'AX', 'Pediatr\xeda [670]'), (b'BY', 'Personalidad, Evaluaci\xf3n y Tratamiento Psicol\xf3gico [680]'), (b'AY', 'Psicobiolog\xeda [725]'), (b'AZ', 'Psiquiatr\xeda [745]'), (b'BA', 'Radiolog\xeda y Medicina F\xedsica [770]'), (b'DB', 'Sanidad Animal [773]'), (b'BB', 'Toxicolog\xeda [807]'))), ('Ciencias Sociales y Jur\xeddicas', ((b'FB', 'An\xe1lisis Geogr\xe1fico Regional [010]'), (b'FD', 'Antropolog\xeda Social [030]'), (b'BD', 'Biblioteconom\xeda y Documentaci\xf3n [040]'), (b'BE', 'Ciencia Pol\xedtica y de la Administraci\xf3n [070]'), (b'BF', 'Comercializaci\xf3n e Investigaci\xf3n de Mercados [095]'), (b'BG', 'Comunicaci\xf3n Audiovisual y Publicidad [105]'), (b'BH', 'Derecho Administrativo [125]'), (b'BI', 'Derecho Civil [130]'), (b'BJ', 'Derecho Constitucional [135]'), (b'BK', 'Derecho del Trabajo y de la Seguridad Social [140]'), (b'BL', 'Derecho Eclesi\xe1stico del Estado [145]'), (b'BM', 'Derecho Financiero y Tributario [150]'), (b'BN', 'Derecho Internacional Privado [155]'), (b'BO', 'Derecho Internacional P\xfablico y Relaciones Internacionales [160]'), (b'BP', 'Derecho Mercantil [165]'), (b'BQ', 'Derecho Penal [170]'), (b'BR', 'Derecho Procesal [175]'), (b'BS', 'Derecho Romano [180]'), (b'FG', 'Did\xe1ctica de la Expresi\xf3n Corporal [187]'), (b'FH', 'Did\xe1ctica de la Expresi\xf3n Musical [189]'), (b'FI', 'Did\xe1ctica de la Expresi\xf3n Musical, Pl\xe1stica y Corporal (Desagregada) [190]'), (b'FJ', 'Did\xe1ctica de la Expresi\xf3n Pl\xe1stica [193]'), (b'FK', 'Did\xe1ctica de la Lengua y la Literatura [195]'), (b'FL', 'Did\xe1ctica de la Matem\xe1tica [200]'), (b'FM', 'Did\xe1ctica de las Ciencias Experimentales [205]'), (b'FN', 'Did\xe1ctica de las Ciencias Sociales [210]'), (b'FO', 'Did\xe1ctica y Organizaci\xf3n Escolar [215]'), (b'FQ', 'Educaci\xf3n F\xedsica y Deportiva [245]'), (b'BT', 'Econom\xeda Aplicada [225]'), (b'BU', 'Econom\xeda Financiera y Contabilidad [230]'), (b'BV', 'Econom\xeda, Sociolog\xeda y Pol\xedtica Agraria [235]'), (b'BW', 'Fundamentos del An\xe1lisis Econ\xf3mico [415]'), (b'GK', 'Geograf\xeda F\xedsica [430]'), (b'GL', 'Geograf\xeda Humana [435]'), (b'HC', 'Metodolog\xeda de las Ciencias del Comportamiento [620]'), (b'HD', 'M\xe9todos de Investigaci\xf3n y Diagn\xf3stico en Educaci\xf3n [625]'), (b'BX', 'Periodismo [675]'), (b'BZ', 'Psicolog\xeda B\xe1sica [730]'), (b'CA', 'Psicolog\xeda Evolutiva y de la Educaci\xf3n [735]'), (b'CB', 'Psicolog\xeda Social [740]'), (b'CC', 'Sociolog\xeda [775]'), (b'HJ', 'Teor\xeda e Historia de la Educaci\xf3n [805]'), (b'CE', 'Trabajo Social y Servicios Sociales [813]'), (b'CD', 'Urban\xedstica y Ordenaci\xf3n del Territorio [815]'))), ('Ciencias', ((b'CG', '\xc1lgebra [005]'), (b'CH', 'An\xe1lisis Matem\xe1tico [015]'), (b'CI', 'Astronom\xeda y Astrof\xedsica [038]'), (b'CK', 'Bioqu\xedmica y Biolog\xeda Molecular [060]'), (b'CL', 'Bot\xe1nica [063]'), (b'DL', 'Cristalograf\xeda y Mineralog\xeda [120]'), (b'CM', 'Ecolog\xeda [220]'), (b'DM', 'Edafolog\xeda y Qu\xedmica Agr\xedcola [240]'), (b'DN', 'Electromagnetismo [247]'), (b'CN', 'Estad\xedstica e Investigaci\xf3n Operativa [265]'), (b'DP', 'Estratigraf\xeda [280]'), (b'DT', 'F\xedsica Aplicada [385]'), (b'DU', 'F\xedsica At\xf3mica, Molecular y Nuclear [390]'), (b'DV', 'F\xedsica de la Materia Condensada [395]'), (b'DW', 'F\xedsica de la Tierra [398]'), (b'CO', 'F\xedsica Te\xf3rica [405]'), (b'CQ', 'Fisiolog\xeda Vegetal [412]'), (b'DX', 'Geodin\xe1mica Externa [427]'), (b'DY', 'Geodin\xe1mica Interna [428]'), (b'CS', 'Geometr\xeda y Topolog\xeda [440]'), (b'CT', 'Matem\xe1tica Aplicada [595]'), (b'CU', 'Microbiolog\xeda [630]'), (b'AU', '\xd3ptica [647]'), (b'ES', 'Petrolog\xeda y Geoqu\xedmica [685]'), (b'CZ', 'Producci\xf3n Animal [700]'), (b'DA', 'Producci\xf3n Vegetal [705]'), (b'CV', 'Qu\xedmica Anal\xedtica [750]'), (b'CW', 'Qu\xedmica F\xedsica [755]'), (b'CX', 'Qu\xedmica Inorg\xe1nica [760]'), (b'CY', 'Qu\xedmica Org\xe1nica [765]'), (b'DC', 'Zoolog\xeda [819]'))), ('Arquitectura e Ingenier\xeda', ((b'DE', 'Arquitectura y Tecnolog\xeda de Computadores [035]'), (b'DF', 'Ciencia de los Materiales e Ingenier\xeda Metal\xfargica [065]'), (b'DG', 'Ciencia de la Computaci\xf3n e Inteligencia Artificial [075]'), (b'DH', 'Ciencias y T\xe9cnicas de la Navegaci\xf3n [083]'), (b'DI', 'Composici\xf3n Arquitect\xf3nica [100]'), (b'DJ', 'Construcciones Arquitect\xf3nicas [110]'), (b'DK', 'Construcciones Navales [115]'), (b'DO', 'Electr\xf3nica [250]'), (b'DQ', 'Explotaci\xf3n de Minas [295]'), (b'DR', 'Expresi\xf3n Gr\xe1fica Arquitect\xf3nica [300]'), (b'DS', 'Expresi\xf3n Gr\xe1fica en la Ingenier\xeda [305]'), (b'DZ', 'Ingenier\xeda Aeroespacial [495]'), (b'EA', 'Ingenier\xeda Agroforestal [500]'), (b'EB', 'Ingenier\xeda Cartogr\xe1fica, Geod\xe9sica y Fotogrametr\xeda [505]'), (b'EC', 'Ingenier\xeda de la Construcci\xf3n [510]'), (b'ED', 'Ingenier\xeda de los Procesos de Fabricaci\xf3n [515]'), (b'EE', 'Ingenier\xeda de Sistemas y Autom\xe1tica [520]'), (b'EF', 'Ingenier\xeda del Terreno [525]'), (b'EG', 'Ingenier\xeda e Infraestructura de los Transportes [530]'), (b'EH', 'Ingenier\xeda El\xe9ctrica [535]'), (b'EI', 'Ingenier\xeda Hidr\xe1ulica [540]'), (b'EJ', 'Ingenier\xeda Mec\xe1nica [545]'), (b'EK', 'Ingenier\xeda Nuclear [550]'), (b'EL', 'Ingenier\xeda Qu\xedmica [555]'), (b'EM', 'Ingenier\xeda Telem\xe1tica [560]'), (b'EN', 'Ingenier\xeda Textil y Papelera [565]'), (b'EO', 'Lenguajes y Sistemas Inform\xe1ticos [570]'), (b'EP', 'M\xe1quinas y Motores T\xe9rmicos [590]'), (b'EQ', 'Mec\xe1nica de Flu\xeddos [600]'), (b'ER', 'Mec\xe1nica de Medios Cont\xednuos y Teor\xeda de Estructuras [605]'), (b'ET', 'Prospecci\xf3n e Investigaci\xf3n Minera [710]'), (b'EU', 'Proyectos Arquitect\xf3nicos [715]'), (b'EV', 'Proyectos de Ingenier\xeda [720]'), (b'EW', 'Tecnolog\xeda de Alimentos [780]'), (b'EX', 'Tecnolog\xeda Electr\xf3nica [785]'), (b'EY', 'Tecnolog\xedas del Medio Ambiente [790]'), (b'EZ', 'Teor\xeda de la Se\xf1al y Comunicaciones [800]'))), ('Artes y Humanidades', ((b'FE', 'Arqueolog\xeda [033]'), (b'FF', 'Ciencias y T\xe9cnicas Historiogr\xe1ficas [085]'), (b'FP', 'Dibujo [185]'), (b'FR', 'Escultura [260]'), (b'FS', 'Est\xe9tica y Teor\xeda de las Artes [270]'), (b'FT', 'Estudios Arabes e Isl\xe1micos [285]'), (b'FU', 'Estudios de As\xeda Oriental (BOE 27/02/2003) [568]'), (b'FV', 'Estudios Hebreos y Arameos [290]'), (b'FW', 'Filolog\xeda Alemana [320]'), (b'FX', 'Filolog\xeda Catalana [325]'), (b'FY', 'Filolog\xeda Eslava [327]'), (b'FZ', 'Filolog\xeda Francesa [335]'), (b'GA', 'Filolog\xeda Griega [340]'), (b'GB', 'Filolog\xeda Inglesa [345]'), (b'GC', 'Filolog\xeda Italiana [350]'), (b'GD', 'Filolog\xeda Latina [355]'), (b'GE', 'Filolog\xeda Rom\xe1nica [360]'), (b'GF', 'Filolog\xeda Vasca [365]'), (b'GG', 'Filolog\xeda Gallega y Portuguesa [370]'), (b'GH', 'Filosof\xeda [375]'), (b'GI', 'Filosof\xeda del Derecho [381]'), (b'GJ', 'Filosof\xeda Moral [383]'), (b'GM', 'Historia Antigua [445]'), (b'GN', 'Historia Contempor\xe1nea [450]'), (b'GO', 'Historia de Am\xe9rica [455]'), (b'GP', 'Historia de la Ciencia [460]'), (b'GQ', 'Historia del Arte [465]'), (b'GR', 'Historia del Derecho y de las Instituciones [470]'), (b'GS', 'Historia del Pensamiento y de los Movimientos Sociales [475]'), (b'GT', 'Historia e Instituciones Econ\xf3micas [480]'), (b'GU', 'Historia Medieval [485]'), (b'GV', 'Historia Moderna [490]'), (b'GW', 'Lengua Espa\xf1ola [567]'), (b'GX', 'Lengua y Cultura del Extremo Oriente [568]'), (b'GY', 'Ling\xfc\xedstica General [575]'), (b'GZ', 'Ling\xfc\xedstica Indoeuropea [580]'), (b'HA', 'Literatura Espa\xf1ola [583]'), (b'HB', 'L\xf3gica y Filosof\xeda de la Ciencia [585]'), (b'HE', 'M\xfasica [635]'), (b'HF', 'Paleontolog\xeda [655]'), (b'HG', 'Pintura [690]'), (b'HH', 'Prehistoria [695]'), (b'HI', 'Teor\xeda de la Literatura y Literatura Comparada [796]'), (b'HK', 'Traducci\xf3n e Interpretaci\xf3n [814]'))), ('Difusi\xf3n de proyectos de investigaci\xf3n', ((b'HM', 'Ciencias de la Salud'), (b'HN', 'Ciencias Sociales'), (b'HO', 'Ciencias Experimentales'), (b'HP', 'Arquitectura e Ingenier\xeda'), (b'HQ', 'Humanidades'))), ('Institucional', ((b'HS', 'Centros Acad\xe9micos'), (b'HT', 'Centros Culturales'), (b'HU', 'Vicerrectorados'), (b'HV', 'Rectorado'), (b'HW', 'UDV'))), (b'HX', 'Divulgaci\xf3n')])),
                ('title', models.CharField(max_length=100, verbose_name='T\xedtulo completo de la producci\xf3n')),
                ('creator', models.CharField(max_length=255, verbose_name='Autor/es o creador/es')),
                ('keyword', models.CharField(help_text='Pude incluir tantas como quiera siempre y cuando se separen por comas.', max_length=255, verbose_name='Palabras clave o etiquetas')),
                ('description', models.TextField(verbose_name='Descripci\xf3n breve')),
                ('license', models.CharField(help_text='Si el contenido dispone de alguna limitaci\xf3n de uso, incluya aqu\xed una referencia a su licencia.', max_length=2, verbose_name='Licencia de uso', choices=[(b'CR', 'Todos los derechos reservados.'), (b'MD', 'Creative Commons: Reconocimiento - No Comercial'), (b'SA', 'Creative Commons: Reconocimiento - No Comercial - Compartir Igual'), (b'ND', 'Creative Commons: Reconocimiento - No Comercial - Sin Obra Derivada')])),
                ('contributor', models.CharField(help_text='Aquellas personas, entidades u organizaciones que han participado en la creaci\xf3n de esta producci\xf3n', max_length=255, null=True, verbose_name='Colaborador/es', blank=True)),
                ('language', models.CharField(default='Espa\xf1ol', max_length=255, null=True, verbose_name='Idioma', blank=True)),
                ('location', models.CharField(help_text='Por ejemplo: el nombre de la instituci\xf3n, departamento, edificio, etc.', max_length=255, null=True, verbose_name='Localizaci\xf3n', blank=True)),
                ('venue', models.CharField(default='San Crist\xf3bal de La Laguna, Tenerife (Espa\xf1a)', max_length=255, blank=True, help_text='Por ejemplo: San Crist\xf3bal de La Laguna, Tenerife (Espa\xf1a)', null=True, verbose_name='Lugar de celebraci\xf3n')),
            ],
            options={
                'verbose_name': 'Metadatos de Producci\xf3n Gen\xe9rica',
                'verbose_name_plural': 'Metadatos de Producciones Gen\xe9ricas',
            },
        ),
        migrations.CreateModel(
            name='MetadataOA',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('knowledge_areas', models.CharField(max_length=2, verbose_name='Clasificaci\xf3n Universidad', choices=[('Ciencias de la Salud', ((b'AB', 'Anatom\xeda Patol\xf3gica [020]'), (b'AC', 'Anatom\xeda y Anatom\xeda Patol\xf3gica Comparadas [025]'), (b'AD', 'Anatom\xeda y Embriolog\xeda Humana [027]'), (b'FC', 'Antropolog\xeda F\xedsica [028]'), (b'CJ', 'Biolog\xeda Celular [050]'), (b'AE', 'Cirug\xeda [090]'), (b'AF', 'Dermatolog\xeda [183]'), (b'AG', 'Enfermer\xeda [255]'), (b'AH', 'Estomatolog\xeda [275]'), (b'AI', 'Farmacia y Tecnolog\xeda Farmac\xe9utica [310]'), (b'AJ', 'Farmacolog\xeda [315]'), (b'CP', 'Fisiolog\xeda [410]'), (b'AK', 'Fisioterapia [413]'), (b'CR', 'Gen\xe9tica [420]'), (b'AL', 'Histolog\xeda [443]'), (b'AM', 'Inmunolog\xeda [566]'), (b'AN', 'Medicina [610]'), (b'AO', 'Medicina Legal y Forense [613]'), (b'AP', 'Medicina Preventiva y Salud P\xfablica [615]'), (b'AQ', 'Medicina y Cirug\xeda Animal [617]'), (b'AR', 'Nutrici\xf3n y Bromatolog\xeda [640]'), (b'AS', 'Obstetricia y Ginecolog\xeda [645]'), (b'AT', 'Oftalmolog\xeda [646]'), (b'AV', 'Otorrinolaringolog\xeda [653]'), (b'AW', 'Parasitolog\xeda [660]'), (b'AX', 'Pediatr\xeda [670]'), (b'BY', 'Personalidad, Evaluaci\xf3n y Tratamiento Psicol\xf3gico [680]'), (b'AY', 'Psicobiolog\xeda [725]'), (b'AZ', 'Psiquiatr\xeda [745]'), (b'BA', 'Radiolog\xeda y Medicina F\xedsica [770]'), (b'DB', 'Sanidad Animal [773]'), (b'BB', 'Toxicolog\xeda [807]'))), ('Ciencias Sociales y Jur\xeddicas', ((b'FB', 'An\xe1lisis Geogr\xe1fico Regional [010]'), (b'FD', 'Antropolog\xeda Social [030]'), (b'BD', 'Biblioteconom\xeda y Documentaci\xf3n [040]'), (b'BE', 'Ciencia Pol\xedtica y de la Administraci\xf3n [070]'), (b'BF', 'Comercializaci\xf3n e Investigaci\xf3n de Mercados [095]'), (b'BG', 'Comunicaci\xf3n Audiovisual y Publicidad [105]'), (b'BH', 'Derecho Administrativo [125]'), (b'BI', 'Derecho Civil [130]'), (b'BJ', 'Derecho Constitucional [135]'), (b'BK', 'Derecho del Trabajo y de la Seguridad Social [140]'), (b'BL', 'Derecho Eclesi\xe1stico del Estado [145]'), (b'BM', 'Derecho Financiero y Tributario [150]'), (b'BN', 'Derecho Internacional Privado [155]'), (b'BO', 'Derecho Internacional P\xfablico y Relaciones Internacionales [160]'), (b'BP', 'Derecho Mercantil [165]'), (b'BQ', 'Derecho Penal [170]'), (b'BR', 'Derecho Procesal [175]'), (b'BS', 'Derecho Romano [180]'), (b'FG', 'Did\xe1ctica de la Expresi\xf3n Corporal [187]'), (b'FH', 'Did\xe1ctica de la Expresi\xf3n Musical [189]'), (b'FI', 'Did\xe1ctica de la Expresi\xf3n Musical, Pl\xe1stica y Corporal (Desagregada) [190]'), (b'FJ', 'Did\xe1ctica de la Expresi\xf3n Pl\xe1stica [193]'), (b'FK', 'Did\xe1ctica de la Lengua y la Literatura [195]'), (b'FL', 'Did\xe1ctica de la Matem\xe1tica [200]'), (b'FM', 'Did\xe1ctica de las Ciencias Experimentales [205]'), (b'FN', 'Did\xe1ctica de las Ciencias Sociales [210]'), (b'FO', 'Did\xe1ctica y Organizaci\xf3n Escolar [215]'), (b'FQ', 'Educaci\xf3n F\xedsica y Deportiva [245]'), (b'BT', 'Econom\xeda Aplicada [225]'), (b'BU', 'Econom\xeda Financiera y Contabilidad [230]'), (b'BV', 'Econom\xeda, Sociolog\xeda y Pol\xedtica Agraria [235]'), (b'BW', 'Fundamentos del An\xe1lisis Econ\xf3mico [415]'), (b'GK', 'Geograf\xeda F\xedsica [430]'), (b'GL', 'Geograf\xeda Humana [435]'), (b'HC', 'Metodolog\xeda de las Ciencias del Comportamiento [620]'), (b'HD', 'M\xe9todos de Investigaci\xf3n y Diagn\xf3stico en Educaci\xf3n [625]'), (b'BX', 'Periodismo [675]'), (b'BZ', 'Psicolog\xeda B\xe1sica [730]'), (b'CA', 'Psicolog\xeda Evolutiva y de la Educaci\xf3n [735]'), (b'CB', 'Psicolog\xeda Social [740]'), (b'CC', 'Sociolog\xeda [775]'), (b'HJ', 'Teor\xeda e Historia de la Educaci\xf3n [805]'), (b'CE', 'Trabajo Social y Servicios Sociales [813]'), (b'CD', 'Urban\xedstica y Ordenaci\xf3n del Territorio [815]'))), ('Ciencias', ((b'CG', '\xc1lgebra [005]'), (b'CH', 'An\xe1lisis Matem\xe1tico [015]'), (b'CI', 'Astronom\xeda y Astrof\xedsica [038]'), (b'CK', 'Bioqu\xedmica y Biolog\xeda Molecular [060]'), (b'CL', 'Bot\xe1nica [063]'), (b'DL', 'Cristalograf\xeda y Mineralog\xeda [120]'), (b'CM', 'Ecolog\xeda [220]'), (b'DM', 'Edafolog\xeda y Qu\xedmica Agr\xedcola [240]'), (b'DN', 'Electromagnetismo [247]'), (b'CN', 'Estad\xedstica e Investigaci\xf3n Operativa [265]'), (b'DP', 'Estratigraf\xeda [280]'), (b'DT', 'F\xedsica Aplicada [385]'), (b'DU', 'F\xedsica At\xf3mica, Molecular y Nuclear [390]'), (b'DV', 'F\xedsica de la Materia Condensada [395]'), (b'DW', 'F\xedsica de la Tierra [398]'), (b'CO', 'F\xedsica Te\xf3rica [405]'), (b'CQ', 'Fisiolog\xeda Vegetal [412]'), (b'DX', 'Geodin\xe1mica Externa [427]'), (b'DY', 'Geodin\xe1mica Interna [428]'), (b'CS', 'Geometr\xeda y Topolog\xeda [440]'), (b'CT', 'Matem\xe1tica Aplicada [595]'), (b'CU', 'Microbiolog\xeda [630]'), (b'AU', '\xd3ptica [647]'), (b'ES', 'Petrolog\xeda y Geoqu\xedmica [685]'), (b'CZ', 'Producci\xf3n Animal [700]'), (b'DA', 'Producci\xf3n Vegetal [705]'), (b'CV', 'Qu\xedmica Anal\xedtica [750]'), (b'CW', 'Qu\xedmica F\xedsica [755]'), (b'CX', 'Qu\xedmica Inorg\xe1nica [760]'), (b'CY', 'Qu\xedmica Org\xe1nica [765]'), (b'DC', 'Zoolog\xeda [819]'))), ('Arquitectura e Ingenier\xeda', ((b'DE', 'Arquitectura y Tecnolog\xeda de Computadores [035]'), (b'DF', 'Ciencia de los Materiales e Ingenier\xeda Metal\xfargica [065]'), (b'DG', 'Ciencia de la Computaci\xf3n e Inteligencia Artificial [075]'), (b'DH', 'Ciencias y T\xe9cnicas de la Navegaci\xf3n [083]'), (b'DI', 'Composici\xf3n Arquitect\xf3nica [100]'), (b'DJ', 'Construcciones Arquitect\xf3nicas [110]'), (b'DK', 'Construcciones Navales [115]'), (b'DO', 'Electr\xf3nica [250]'), (b'DQ', 'Explotaci\xf3n de Minas [295]'), (b'DR', 'Expresi\xf3n Gr\xe1fica Arquitect\xf3nica [300]'), (b'DS', 'Expresi\xf3n Gr\xe1fica en la Ingenier\xeda [305]'), (b'DZ', 'Ingenier\xeda Aeroespacial [495]'), (b'EA', 'Ingenier\xeda Agroforestal [500]'), (b'EB', 'Ingenier\xeda Cartogr\xe1fica, Geod\xe9sica y Fotogrametr\xeda [505]'), (b'EC', 'Ingenier\xeda de la Construcci\xf3n [510]'), (b'ED', 'Ingenier\xeda de los Procesos de Fabricaci\xf3n [515]'), (b'EE', 'Ingenier\xeda de Sistemas y Autom\xe1tica [520]'), (b'EF', 'Ingenier\xeda del Terreno [525]'), (b'EG', 'Ingenier\xeda e Infraestructura de los Transportes [530]'), (b'EH', 'Ingenier\xeda El\xe9ctrica [535]'), (b'EI', 'Ingenier\xeda Hidr\xe1ulica [540]'), (b'EJ', 'Ingenier\xeda Mec\xe1nica [545]'), (b'EK', 'Ingenier\xeda Nuclear [550]'), (b'EL', 'Ingenier\xeda Qu\xedmica [555]'), (b'EM', 'Ingenier\xeda Telem\xe1tica [560]'), (b'EN', 'Ingenier\xeda Textil y Papelera [565]'), (b'EO', 'Lenguajes y Sistemas Inform\xe1ticos [570]'), (b'EP', 'M\xe1quinas y Motores T\xe9rmicos [590]'), (b'EQ', 'Mec\xe1nica de Flu\xeddos [600]'), (b'ER', 'Mec\xe1nica de Medios Cont\xednuos y Teor\xeda de Estructuras [605]'), (b'ET', 'Prospecci\xf3n e Investigaci\xf3n Minera [710]'), (b'EU', 'Proyectos Arquitect\xf3nicos [715]'), (b'EV', 'Proyectos de Ingenier\xeda [720]'), (b'EW', 'Tecnolog\xeda de Alimentos [780]'), (b'EX', 'Tecnolog\xeda Electr\xf3nica [785]'), (b'EY', 'Tecnolog\xedas del Medio Ambiente [790]'), (b'EZ', 'Teor\xeda de la Se\xf1al y Comunicaciones [800]'))), ('Artes y Humanidades', ((b'FE', 'Arqueolog\xeda [033]'), (b'FF', 'Ciencias y T\xe9cnicas Historiogr\xe1ficas [085]'), (b'FP', 'Dibujo [185]'), (b'FR', 'Escultura [260]'), (b'FS', 'Est\xe9tica y Teor\xeda de las Artes [270]'), (b'FT', 'Estudios Arabes e Isl\xe1micos [285]'), (b'FU', 'Estudios de As\xeda Oriental (BOE 27/02/2003) [568]'), (b'FV', 'Estudios Hebreos y Arameos [290]'), (b'FW', 'Filolog\xeda Alemana [320]'), (b'FX', 'Filolog\xeda Catalana [325]'), (b'FY', 'Filolog\xeda Eslava [327]'), (b'FZ', 'Filolog\xeda Francesa [335]'), (b'GA', 'Filolog\xeda Griega [340]'), (b'GB', 'Filolog\xeda Inglesa [345]'), (b'GC', 'Filolog\xeda Italiana [350]'), (b'GD', 'Filolog\xeda Latina [355]'), (b'GE', 'Filolog\xeda Rom\xe1nica [360]'), (b'GF', 'Filolog\xeda Vasca [365]'), (b'GG', 'Filolog\xeda Gallega y Portuguesa [370]'), (b'GH', 'Filosof\xeda [375]'), (b'GI', 'Filosof\xeda del Derecho [381]'), (b'GJ', 'Filosof\xeda Moral [383]'), (b'GM', 'Historia Antigua [445]'), (b'GN', 'Historia Contempor\xe1nea [450]'), (b'GO', 'Historia de Am\xe9rica [455]'), (b'GP', 'Historia de la Ciencia [460]'), (b'GQ', 'Historia del Arte [465]'), (b'GR', 'Historia del Derecho y de las Instituciones [470]'), (b'GS', 'Historia del Pensamiento y de los Movimientos Sociales [475]'), (b'GT', 'Historia e Instituciones Econ\xf3micas [480]'), (b'GU', 'Historia Medieval [485]'), (b'GV', 'Historia Moderna [490]'), (b'GW', 'Lengua Espa\xf1ola [567]'), (b'GX', 'Lengua y Cultura del Extremo Oriente [568]'), (b'GY', 'Ling\xfc\xedstica General [575]'), (b'GZ', 'Ling\xfc\xedstica Indoeuropea [580]'), (b'HA', 'Literatura Espa\xf1ola [583]'), (b'HB', 'L\xf3gica y Filosof\xeda de la Ciencia [585]'), (b'HE', 'M\xfasica [635]'), (b'HF', 'Paleontolog\xeda [655]'), (b'HG', 'Pintura [690]'), (b'HH', 'Prehistoria [695]'), (b'HI', 'Teor\xeda de la Literatura y Literatura Comparada [796]'), (b'HK', 'Traducci\xf3n e Interpretaci\xf3n [814]'))), ('Difusi\xf3n de proyectos de investigaci\xf3n', ((b'HM', 'Ciencias de la Salud'), (b'HN', 'Ciencias Sociales'), (b'HO', 'Ciencias Experimentales'), (b'HP', 'Arquitectura e Ingenier\xeda'), (b'HQ', 'Humanidades'))), ('Institucional', ((b'HS', 'Centros Acad\xe9micos'), (b'HT', 'Centros Culturales'), (b'HU', 'Vicerrectorados'), (b'HV', 'Rectorado'), (b'HW', 'UDV'))), (b'HX', 'Divulgaci\xf3n')])),
                ('title', models.CharField(max_length=100, verbose_name='T\xedtulo completo de la producci\xf3n')),
                ('creator', models.CharField(max_length=255, verbose_name='Autor/es o creador/es')),
                ('keyword', models.CharField(help_text='Pude incluir tantas como quiera siempre y cuando se separen por comas.', max_length=255, verbose_name='Palabras clave o etiquetas')),
                ('description', models.TextField(verbose_name='Descripci\xf3n breve')),
                ('license', models.CharField(help_text='Si el contenido dispone de alguna limitaci\xf3n de uso, incluya aqu\xed una referencia a su licencia.', max_length=2, verbose_name='Licencia de uso', choices=[(b'CR', 'Todos los derechos reservados.'), (b'MD', 'Creative Commons: Reconocimiento - No Comercial'), (b'SA', 'Creative Commons: Reconocimiento - No Comercial - Compartir Igual'), (b'ND', 'Creative Commons: Reconocimiento - No Comercial - Sin Obra Derivada')])),
                ('guideline', models.CharField(max_length=2, verbose_name='\xc1rea de conocimiento UNESCO', choices=[(b'AA', 'Ciencias de la salud'), (b'AB', 'Ciencias experimentales'), (b'AC', 'Ciencias jur\xeddico-sociales'), (b'AD', 'Ciencias tecnol\xf3gicas'), (b'AE', 'Humanidades')])),
                ('contributor', models.CharField(help_text='Aquellas personas, entidades u organizaciones que han participado en la creaci\xf3n de esta producci\xf3n', max_length=255, verbose_name='Colaborador/es')),
                ('audience', models.CharField(max_length=2, verbose_name='Audiencia o p\xfablico objetivo', choices=[(b'AA', 'Profesor'), (b'AB', 'Autor'), (b'AC', 'Alumno'), (b'AD', 'Coordinador'), (b'AE', 'Otro')])),
                ('typical_age_range', models.CharField(max_length=255, verbose_name='Edad de la audiencia o p\xfablico objetivo')),
                ('source', models.CharField(help_text='Si el contenido es derivado de otra material, indique aqu\xed la referencia al original', max_length=255, null=True, verbose_name='Identificador de obra derivada', blank=True)),
                ('language', models.CharField(default='Espa\xf1ol', max_length=255, verbose_name='Idioma')),
                ('ispartof', models.CharField(max_length=255, null=True, verbose_name='Serie a la que pertenece', blank=True)),
                ('location', models.CharField(help_text='Por ejemplo: el nombre de la instituci\xf3n, departamento, edificio, etc.', max_length=255, verbose_name='Localizaci\xf3n')),
                ('venue', models.CharField(default='San Crist\xf3bal de La Laguna, Tenerife (Espa\xf1a)', help_text='Por ejemplo: San Crist\xf3bal de La Laguna, Tenerife (Espa\xf1a)', max_length=255, verbose_name='Lugar de celebraci\xf3n')),
                ('temporal', models.TextField(help_text='Si en la producci\xf3n intervienen diferentes actores, indique aqu\xed el nombre y el momento en el que interviene cada uno de ellos.', null=True, verbose_name='Intervalo de tiempo', blank=True)),
                ('rightsholder', models.CharField(max_length=255, verbose_name='Persona, entidad u organizaci\xf3n responsable de la gesti\xf3n de los derechos de autor')),
                ('date', models.DateTimeField(verbose_name='Fecha de grabaci\xf3n', editable=False)),
                ('created', models.DateTimeField(help_text='La fecha de producci\xf3n ser\xe1 incluida de manera autom\xe1tica por el sistema', verbose_name='Fecha de producci\xf3n', editable=False)),
                ('valid', models.DateTimeField(help_text='La fecha de validaci\xf3n ser\xe1 incluida de manera autom\xe1tica por el sistema.', verbose_name='Fecha de validaci\xf3n', null=True, editable=False, blank=True)),
                ('type', models.CharField(max_length=2, verbose_name='Tipo de producci\xf3n', choices=[(b'AA', 'Conferencia'), (b'AB', 'Documental'), (b'AC', 'Coloquio'), (b'AD', 'Curso'), (b'AE', 'Institucional'), (b'AF', 'Ficci\xf3n'), (b'AG', 'Mesa redonda'), (b'AH', 'Exposici\xf3n de trabajos'), (b'AI', 'Apertura'), (b'AJ', 'Clausura'), (b'AK', 'Conferencia inaugural'), (b'AL', 'Conferencia de clausura'), (b'AM', 'Preguntas y respuestas'), (b'AN', 'Intervenci\xf3n'), (b'AO', 'Presentaci\xf3n'), (b'AP', 'Demostraci\xf3n'), (b'AQ', 'Entrevista'), (b'AR', 'Video promocional'), (b'AS', 'Videoconferencia')])),
                ('interactivity_type', models.CharField(max_length=2, verbose_name='Tipo de interacci\xf3n con la audiencia o p\xfablico objetivo', choices=[(b'AA', 'Activa'), (b'AB', 'Expositiva'), (b'AC', 'Combinada (activa y expositiva)'), (b'AD', 'Otra')])),
                ('interactivity_level', models.CharField(max_length=2, verbose_name='Nivel de interacci\xf3n', choices=[(b'AA', 'Muy bajo: Documento, imagen, video, sonido, etc. de car\xe1cter expositivo.'), (b'AB', 'Bajo: Conjunto de documentos, im\xe1genes, v\xeddeos, sonidos, etc. enlazados.'), (b'AC', 'Medio: El contenido dispone de elementos interactivos'), (b'AD', 'Alto: Cuestionario, consulta, encuesta, examen, ejercicio, etc.'), (b'AE', 'Muy alto: Juego, simulaci\xf3n, etc.')])),
                ('learning_resource_type', models.CharField(max_length=2, verbose_name='Tipo de recurso educativo', choices=[(b'AA', 'Ejercicio'), (b'AB', '\xcdndice'), (b'AC', 'Experimento'), (b'AD', 'Diagrama'), (b'AE', 'Narraci\xf3n'), (b'AF', 'Simulaci\xf3n'), (b'AG', 'Presentaci\xf3n'), (b'AH', 'Enunciado del problema'), (b'AI', 'Figura'), (b'AJ', 'Texto'), (b'AK', 'Cuestionario'), (b'AL', 'Tabla'), (b'AM', 'Autoevaluaci\xf3n'), (b'AN', 'Gr\xe1fico'), (b'AO', 'Examen')])),
                ('semantic_density', models.CharField(max_length=2, verbose_name='Densidad sem\xe1ntica del contenido', choices=[(b'AA', 'Muy bajo: contenido de car\xe1cter irrelevante.'), (b'AB', 'Bajo: contiene elementos interactivos para el usuario.'), (b'AC', 'Medio: contenido audiovisual complejo, etc.'), (b'AD', 'Alto: gr\xe1ficos, tablas, diagramas complejos, etc.'), (b'AE', 'Muy alto: presentaciones gr\xe1ficas complejas o producciones audiovisuales. ')])),
                ('context', models.CharField(max_length=2, verbose_name='Contexto educativo', choices=[(b'AA', 'Educaci\xf3n primaria'), (b'AB', 'Educaci\xf3n secundaria'), (b'AC', 'Educaci\xf3n superior'), (b'AD', 'Universitario de primer ciclo'), (b'AE', 'Universitario de segundo ciclo'), (b'AF', 'Universitario de posgrado'), (b'AG', 'Escuela t\xe9cnica de primer ciclo'), (b'AH', 'Escuela t\xe9cnica de segundo ciclo'), (b'AI', 'Formaci\xf3n profesional'), (b'AJ', 'Formaci\xf3n continua'), (b'AK', 'Formaci\xf3n vocacional')])),
                ('dificulty', models.CharField(max_length=2, verbose_name='Nivel de Dificultad', choices=[(b'AA', 'Muy f\xe1cil: Conocimiento, comprensi\xf3n, etc.'), (b'AB', 'F\xe1cil: Aplicaci\xf3n'), (b'AC', 'Dificultad media: An\xe1lisis'), (b'AD', 'Dif\xedcil: S\xedntesis'), (b'AE', 'Muy dif\xedcil: Evaluaci\xf3n')])),
                ('typical_learning_time', models.CharField(help_text='Ejemplo: 2 horas', max_length=255, verbose_name='Tiempo estimado para la adquisici\xf3n de conocimientos')),
                ('educational_language', models.CharField(max_length=2, verbose_name='Caracter\xedsticas del lenguaje educativo', choices=[(b'AA', 'Expositivo'), (b'AB', 'Sem\xe1ntico'), (b'AC', 'Lexico')])),
                ('purpose', models.CharField(max_length=2, verbose_name='Objetivo del contenido', choices=[(b'AA', 'Multidisciplinar'), (b'AB', 'Descripci\xf3n de concepto / idea'), (b'AC', 'Requisito educativo'), (b'AD', 'Mejora de competencias educativas')])),
                ('unesco', models.CharField(max_length=2, verbose_name='Dominio de conocimiento', choices=[(b'AA', 'Antropolog\xeda'), (b'AB', 'Artes y letras'), (b'AC', 'Astronom\xeda y Astrof\xedsica'), (b'AD', 'Ciencias Jur\xeddicas y Derecho'), (b'AE', 'Ciencias Agron\xf3micas y Veterinarias'), (b'AF', 'Ciencias de la Tecnolog\xeda'), (b'AG', 'Ciencias de la Tierra y el Cosmos'), (b'AH', 'Ciencias de la Vida'), (b'AI', 'Ciencias Econ\xf3micas'), (b'AJ', 'Ciencias Pol\xedticas'), (b'AK', 'Corporativo'), (b'AL', 'Demograf\xeda'), (b'AM', '\xc9tica'), (b'AN', 'Filosof\xeda'), (b'AO', 'F\xedsica'), (b'AP', 'Geograf\xeda'), (b'AQ', 'Historia'), (b'AR', 'Ling\xfcistica'), (b'AS', 'L\xf3gica'), (b'AT', 'Matem\xe1ticas'), (b'AU', 'Medicina y patolog\xedas humanas'), (b'AV', 'Noticias'), (b'AW', 'Pedagog\xeda'), (b'AX', 'Psicolog\xeda'), (b'AY', 'Qu\xedmica'), (b'AZ', 'Sociolog\xeda'), (b'BA', 'Vida universitaria')])),
            ],
            options={
                'verbose_name': 'Metadatos de Objeto de Aprendizaje',
                'verbose_name_plural': 'Metadatos de Objetos de Aprendizaje',
            },
        ),
        migrations.CreateModel(
            name='PlantillaFDV',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('fondo', models.ImageField(upload_to=b'plantillas')),
            ],
            options={
                'verbose_name': 'Plantilla Fondo-Diapositiva-V\xeddeo',
            },
        ),
        migrations.CreateModel(
            name='Previsualizacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fichero', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroPublicacion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('enlace', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'registro de publicaci\xf3n',
                'verbose_name_plural': 'registro de publicaciones',
            },
        ),
        migrations.CreateModel(
            name='TecData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('duration', models.FloatField(null=True)),
                ('xml_data', models.TextField(null=True)),
                ('txt_data', models.TextField(null=True)),
            ],
            options={
                'verbose_name': 'Informaci\xf3n t\xe9cnica',
                'verbose_name_plural': 'Informaciones t\xe9cnicas',
            },
        ),
        migrations.CreateModel(
            name='TipoVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=30)),
                ('x', models.PositiveSmallIntegerField()),
                ('y', models.PositiveSmallIntegerField()),
                ('ancho', models.PositiveSmallIntegerField()),
                ('alto', models.PositiveSmallIntegerField()),
                ('mix', models.PositiveSmallIntegerField(default=100)),
                ('plantilla', models.ForeignKey(to='postproduccion.PlantillaFDV')),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(unique=True, max_length=25)),
                ('instante', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fichero', models.CharField(max_length=255, editable=False)),
                ('status', models.CharField(default=b'INC', max_length=3, editable=False, choices=[(b'INC', 'Incompleto'), (b'DEF', 'Definido'), (b'PRV', 'Procesando v\xeddeo'), (b'COM', 'Completado'), (b'PRP', 'Procesando previsualizaci\xf3n'), (b'PTU', 'Pendiente del usuario'), (b'PTO', 'Pendiente del operador'), (b'ACE', 'Aceptado'), (b'REC', 'Rechazado'), (b'LIS', 'Listo')])),
                ('titulo', models.CharField(max_length=100)),
                ('autor', models.CharField(max_length=255, verbose_name='Responsable')),
                ('email', models.EmailField(max_length=254, verbose_name='Email del responsable')),
                ('objecto_aprendizaje', models.BooleanField(default=True, verbose_name='Objeto de aprendizaje')),
                ('plantilla', models.ForeignKey(blank=True, to='postproduccion.PlantillaFDV', null=True)),
            ],
            options={
                'permissions': (('video_manager', 'Puede gestionar la creaci\xf3n de v\xeddeos'), ('video_library', 'Puede consultar la videoteca')),
            },
        ),
        migrations.AddField(
            model_name='token',
            name='video',
            field=models.OneToOneField(to='postproduccion.Video'),
        ),
        migrations.AddField(
            model_name='tecdata',
            name='video',
            field=models.OneToOneField(to='postproduccion.Video'),
        ),
        migrations.AddField(
            model_name='registropublicacion',
            name='video',
            field=models.ForeignKey(to='postproduccion.Video'),
        ),
        migrations.AddField(
            model_name='previsualizacion',
            name='video',
            field=models.OneToOneField(to='postproduccion.Video'),
        ),
        migrations.AddField(
            model_name='metadataoa',
            name='video',
            field=models.OneToOneField(editable=False, to='postproduccion.Video'),
        ),
        migrations.AddField(
            model_name='metadatagen',
            name='video',
            field=models.OneToOneField(editable=False, to='postproduccion.Video'),
        ),
        migrations.AddField(
            model_name='informeproduccion',
            name='video',
            field=models.OneToOneField(editable=False, to='postproduccion.Video'),
        ),
        migrations.AddField(
            model_name='incidenciaproduccion',
            name='informe',
            field=models.ForeignKey(editable=False, to='postproduccion.InformeProduccion'),
        ),
        migrations.AddField(
            model_name='historicocodificacion',
            name='informe',
            field=models.ForeignKey(editable=False, to='postproduccion.InformeProduccion'),
        ),
        migrations.AddField(
            model_name='ficheroentrada',
            name='tipo',
            field=models.ForeignKey(editable=False, to='postproduccion.TipoVideo', null=True),
        ),
        migrations.AddField(
            model_name='ficheroentrada',
            name='video',
            field=models.ForeignKey(editable=False, to='postproduccion.Video'),
        ),
        migrations.AddField(
            model_name='cola',
            name='video',
            field=models.ForeignKey(to='postproduccion.Video'),
        ),
    ]
