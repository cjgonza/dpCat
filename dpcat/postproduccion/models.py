#encoding: utf-8
from django.db import models
from django.contrib.auth.models import User
from postproduccion import utils

import os
import signal

# Create your models here.

class PlantillaFDV(models.Model):   # (Fondo-Disapositiva-Video)
    nombre = models.CharField(max_length = 50)

    fondo = models.ImageField(upload_to = 'plantillas')

    class Meta:
        verbose_name = u'Plantilla Fondo-Diapositiva-Vídeo'

    def __unicode__(self):
        return self.nombre

class TipoVideo(models.Model):
    nombre = models.CharField(max_length = 30)
    plantilla =  models.ForeignKey(PlantillaFDV)

    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()
    ancho = models.PositiveSmallIntegerField()
    alto = models.PositiveSmallIntegerField()
    mix = models.PositiveSmallIntegerField(default = 100)

    def __unicode__(self):
        return self.nombre

class Video(models.Model):
    VIDEO_STATUS = (
        ('INC', u'Incompleto'),                  # Creado pero sin ficheros de entrada.
        ('DEF', u'Definido'),                    # Definidos los ficheros de entrada (en cola para ser procesado).
        ('PRV', u'Procesando vídeo'),            # Está siendo procesado (montaje o copia).
        ('COM', u'Completado'),                  # Procesamiento completado (en cola para generar previsualización).
        ('PRP', u'Procesando previsualización'), # Está siendo generada la previsualización.
        ('PTU', u'Pendiente del usuario'),       # A la espera de que el usuario rellene los metadatos y acepte el vídeo.
        ('PTO', u'Pendiente del operador'),      # A la espera de que el operador rellene los metadatos.
        ('ACE', u'Aceptado'),                    # Aceptado por el usuario, a la espera de que lo valide el operador.
        ('REC', u'Rechazado'),                   # Rechazado por el usuario, a la espera de que el operador tome las medidas necesarias.
        ('LIS', u'Listo'),                       # Validado por el operador, todos los procedimientos terminados.
    )

    fichero = models.CharField(max_length = 255, editable = False)
    status = models.CharField(max_length = 3, choices = VIDEO_STATUS, editable = False, default = 'INC')
    plantilla = models.ForeignKey(PlantillaFDV, null = True, blank = True)

 
    titulo = models.CharField(max_length = 255)
    autor = models.CharField(max_length = 255)
    email = models.EmailField()

    def __unicode__(self):
        return self.titulo

    def delete(self, *args, **kwargs):
        for task in self.cola_set.all():
            task.delete()
        if self.fichero:
            utils.remove_file_path(self.fichero)
        if hasattr(self, 'previsualizacion'):
            self.previsualizacion.delete()
        super(Video, self).delete(*args, **kwargs)

    def set_status(self, st):
        self.status = st
        self.save()

    class Meta:
        permissions = (
            ("video_manager", u"Puede gestionar la creación de vídeos"),
            ("video_library", u"Puede consultar la videoteca"),
        )

class InformeProduccion(models.Model):
    video = models.OneToOneField(Video, editable = False)
    operador = models.ForeignKey(User, editable = False)
    observacion = models.TextField(null = True, blank = True)
    fecha_grabacion = models.DateTimeField()
    fecha_produccion = models.DateTimeField(auto_now_add = True)
    fecha_validacion = models.DateTimeField(null = True)
    aprobacion = models.BooleanField(default = True)

class IncidenciaProduccion(models.Model):
    WHO = (
        ('O', u'Operador'),
        ('U', u'Usuario'),
    )

    
    informe = models.ForeignKey(InformeProduccion, editable = False)
    emisor = models.CharField(max_length = 1, choices = WHO, editable = False)
    comentario = models.TextField(null = True)
    fecha =  models.DateTimeField(auto_now_add = True)
    aceptado = models.NullBooleanField()

class HistoricoCodificacion(models.Model):
    TASK_TYPE = (
        ('COP', u'Copia'),
        ('PIL', u'Píldora'),
        ('PRE', u'Previsualización')
    )

    informe = models.ForeignKey(InformeProduccion, editable = False)
    tipo = models.CharField(max_length = 3, choices = TASK_TYPE)
    fecha = models.DateTimeField()
    status = models.BooleanField()

class FicheroEntrada(models.Model):
    video = models.ForeignKey(Video, editable = False)
    tipo = models.ForeignKey(TipoVideo, editable = False, null = True)
    fichero = models.CharField(max_length = 255)

    def __unicode__(self):
        if self.tipo:
            return "%s (%s)" % (self.video.titulo, self.tipo.nombre)
        return self.video.titulo

class TecData(models.Model):
    duration = models.FloatField(null = True)
    xml_data = models.TextField(null = True)
    txt_data = models.TextField(null = True)

    video = models.OneToOneField(Video)

    class Meta:
        verbose_name = u'Información técnica'
        verbose_name_plural = u'Informaciones técnicas'

    def __unicode__(self):
        return self.video.titulo

class Previsualizacion(models.Model):
    video = models.OneToOneField(Video)
    fichero = models.CharField(max_length = 255)

    def delete(self, *args, **kwargs):
        if self.fichero:
            utils.remove_file_path(self.fichero)
        super(Previsualizacion, self).delete(*args, **kwargs)

class Metadata(models.Model):
    video = models.OneToOneField(Video, editable = False)

    KNOWLEDGE_AREAS_KEYS = (
        ('AA', 'Ciencias de la Salud'),
        ('AB', '- Anatomía Patológica [020]'),
        ('AC', '- Anatomía y Anatomía Patológica Comparadas [025]'),
        ('AD', '- Anatomía y Embriología Humana [027]'),
        ('AE', '- Cirugía [090]'),
        ('AF', '- Dermatología [183]'),
        ('AG', '- Enfermería [255]'),
        ('AH', '- Estomatología [275]'),
        ('AI', '- Farmacia y Tecnología Farmacéutica [310]'),
        ('AJ', '- Farmacología [315]'),
        ('AK', '- Fisioterapia [413]'),
        ('AL', '- Histología [443]'),
        ('AM', '- Inmunología [566]'),
        ('AN', '- Medicina [610]'),
        ('AO', '- Medicina Legal y Forense [613]'),
        ('AP', '- Medicina Preventiva y Salud Pública [615]'),
        ('AQ', '- Medicina y Cirugía Animal [617]'),
        ('AR', '- Nutrición y Bromatología [640]'),
        ('AS', '- Obstetricia y Ginecología [645]'),
        ('AT', '- Oftalmología [646]'),
        ('AU', '- Óptica [647]'),
        ('AV', '- Otorrinolaringología [653]'),
        ('AW', '- Parasitología [660]'),
        ('AX', '- Pediatría [670]'),
        ('AY', '- Psicobiología [725]'),
        ('AZ', '- Psiquiatría [745]'),
        ('BA', '- Radiología y Medicina Física [770]'),
        ('BB', '- Toxicología [807]'),
        ('BC', 'Ciencias Sociales'),
        ('BD', '- Biblioteconomía y Documentación [040]'),
        ('BE', '- Ciencia Política y de la Administración [070]'),
        ('BF', '- Comercialización e Investigación de Mercados [095]'),
        ('BG', '- Comunicación Audiovisual y Publicidad [105]'),
        ('BH', '- Derecho Administrativo [125]'),
        ('BI', '- Derecho Civil [130]'),
        ('BJ', '- Derecho Constitucional [135]'),
        ('BK', '- Derecho del Trabajo y de la Seguridad Social [140]'),
        ('BL', '- Derecho Eclesiástico del Estado [145]'),
        ('BM', '- Derecho Financiero y Tributario [150]'),
        ('BN', '- Derecho Internacional Privado [155]'),
        ('BO', '- Derecho Internacional Público y Relaciones Internacionales [160]'),
        ('BP', '- Derecho Mercantil [165]'),
        ('BQ', '- Derecho Penal [170]'),
        ('BR', '- Derecho Procesal [175]'),
        ('BS', '- Derecho Romano [180]'),
        ('BT', '- Economía Aplicada [225]'),
        ('BU', '- Economía Financiera y Contabilidad [230]'),
        ('BV', '- Economía, Sociología y Política Agraria [235]'),
        ('BW', '- Fundamentos del Análisis Económico [415]'),
        ('BX', '- Periodismo [675]'),
        ('BY', '- Personalidad, Evaluación y Tratamiento Psicológico [680]'),
        ('BZ', '- Psicología Básica [730]'),
        ('CA', '- Psicología Evolutiva y de la Educación [735]'),
        ('CB', '- Psicología Social [740]'),
        ('CC', '- Sociología [775]'),
        ('CD', '- Urbanística y Ordenación del Territorio [815]'),
        ('CE', '- Trabajo Social y Servicios Sociales [813]'),
        ('CF', 'Ciencias Experimentales'),
        ('CG', '- Álgebra [005]'),
        ('CH', '- Análisis Matemático [015]'),
        ('CI', '- Astronomía y Astrofísica [038]'),
        ('CJ', '- Biología Celular [050]'),
        ('CK', '- Bioquímica y Biología Molecular [060]'),
        ('CL', '- Botánica [063]'),
        ('CM', '- Ecología [220]'),
        ('CN', '- Estadística e Investigación Operativa [265]'),
        ('CO', '- Física Teórica [405]'),
        ('CP', '- Fisiología [410]'),
        ('CQ', '- Fisiología Vegetal [412]'),
        ('CR', '- Genética [420]'),
        ('CS', '- Geometría y Topología [440]'),
        ('CT', '- Matemática Aplicada [595]'),
        ('CU', '- Microbiología [630]'),
        ('CV', '- Química Analítica [750]'),
        ('CW', '- Química Física [755]'),
        ('CX', '- Química Inorgánica [760]'),
        ('CY', '- Química Orgánica [765]'),
        ('CZ', '- Producción Animal [700]'),
        ('DA', '- Producción Vegetal [705]'),
        ('DB', '- Sanidad Animal [773]'),
        ('DC', '- Zoología [819]'),
        ('DD', 'Arquitectura e Ingeniería'),
        ('DE', '- Arquitectura y Tecnología de Computadores [035]'),
        ('DF', '- Ciencia de los Materiales e Ingeniería Metalúrgica [065]'),
        ('DG', '- Ciencia de la Computación e Inteligencia Artificial [075]'),
        ('DH', '- Ciencias y Técnicas de la Navegación [083]'),
        ('DI', '- Composición Arquitectónica [100]'),
        ('DJ', '- Construcciones Arquitectónicas [110]'),
        ('DK', '- Construcciones Navales [115]'),
        ('DL', '- Cristalografía y Mineralogía [120]'),
        ('DM', '- Edafología y Química Agrícola [240]'),
        ('DN', '- Electromagnetismo [247]'),
        ('DO', '- Electrónica [250]'),
        ('DP', '- Estratigrafía [280]'),
        ('DQ', '- Explotación de Minas [295]'),
        ('DR', '- Expresión Gráfica Arquitectónica [300]'),
        ('DS', '- Expresión Gráfica en la Ingeniería [305]'),
        ('DT', '- Física Aplicada [385]'),
        ('DU', '- Física Atómica, Molecular y Nuclear [390]'),
        ('DV', '- Física de la Materia Condensada [395]'),
        ('DW', '- Física de la Tierra [398]'),
        ('DX', '- Geodinámica Externa [427]'),
        ('DY', '- Geodinámica Interna [428]'),
        ('DZ', '- Ingeniería Aeroespacial [495]'),
        ('EA', '- Ingeniería Agroforestal [500]'),
        ('EB', '- Ingeniería Cartográfica, Geodésica y Fotogrametría [505]'),
        ('EC', '- Ingeniería de la Construcción [510]'),
        ('ED', '- Ingeniería de los Procesos de Fabricación [515]'),
        ('EE', '- Ingeniería de Sistemas y Automática [520]'),
        ('EF', '- Ingeniería del Terreno [525]'),
        ('EG', '- Ingeniería e Infraestructura de los Transportes [530]'),
        ('EH', '- Ingeniería Eléctrica [535]'),
        ('EI', '- Ingeniería Hidráulica [540]'),
        ('EJ', '- Ingeniería Mecánica [545]'),
        ('EK', '- Ingeniería Nuclear [550]'),
        ('EL', '- Ingeniería Química [555]'),
        ('EM', '- Ingeniería Telemática [560]'),
        ('EN', '- Ingeniería Textil y Papelera [565]'),
        ('EO', '- Lenguajes y Sistemas Informáticos [570]'),
        ('EP', '- Máquinas y Motores Térmicos [590]'),
        ('EQ', '- Mecánica de Fluídos [600]'),
        ('ER', '- Mecánica de Medios Contínuos y Teoría de Estructuras [605]'),
        ('ES', '- Petrología y Geoquímica [685]'),
        ('ET', '- Prospección e Investigación Minera [710]'),
        ('EU', '- Proyectos Arquitectónicos [715]'),
        ('EV', '- Proyectos de Ingeniería [720]'),
        ('EW', '- Tecnología de Alimentos [780]'),
        ('EX', '- Tecnología Electrónica [785]'),
        ('EY', '- Tecnologías del Medio Ambiente [790]'),
        ('EZ', '- Teoría de la Señal y Comunicaciones [800]'),
        ('FA', 'Humanidades'),
        ('FB', '- Análisis Geográfico Regional [010]'),
        ('FC', '- Antropología Física [028]'),
        ('FD', '- Antropología Social [030]'),
        ('FE', '- Arqueología [033]'),
        ('FF', '- Ciencias y Técnicas Historiográficas [085]'),
        ('FG', '- Didáctica de la Expresión Corporal [187]'),
        ('FH', '- Didáctica de la Expresión Musical [189]'),
        ('FI', '- Didáctica de la Expresión Musical, Plástica y Corporal (Desagregada) [190]'),
        ('FJ', '- Didáctica de la Expresión Plástica [193]'),
        ('FK', '- Didáctica de la Lengua y la Literatura [195]'),
        ('FL', '- Didáctica de la Matemática [200]'),
        ('FM', '- Didáctica de las Ciencias Experimentales [205]'),
        ('FN', '- Didáctica de las Ciencias Sociales [210]'),
        ('FO', '- Didáctica y Organización Escolar [215]'),
        ('FP', '- Dibujo [185]'),
        ('FQ', '- Educación Física y Deportiva [245]'),
        ('FR', '- Escultura [260]'),
        ('FS', '- Estética y Teoría de las Artes [270]'),
        ('FT', '- Estudios Arabes e Islámicos [285]'),
        ('FU', '- Estudios de Asía Oriental (BOE 27/02/2003) [568]'),
        ('FV', '- Estudios Hebreos y Arameos [290]'),
        ('FW', '- Filología Alemana [320]'),
        ('FX', '- Filología Catalana [325]'),
        ('FY', '- Filología Eslava [327]'),
        ('FZ', '- Filología Francesa [335]'),
        ('GA', '- Filología Griega [340]'),
        ('GB', '- Filología Inglesa [345]'),
        ('GC', '- Filología Italiana [350]'),
        ('GD', '- Filología Latina [355]'),
        ('GE', '- Filología Románica [360]'),
        ('GF', '- Filología Vasca [365]'),
        ('GG', '- Filología Gallega y Portuguesa [370]'),
        ('GH', '- Filosofía [375]'),
        ('GI', '- Filosofía del Derecho [381]'),
        ('GJ', '- Filosofía Moral [383]'),
        ('GK', '- Geografía Física [430]'),
        ('GL', '- Geografía Humana [435]'),
        ('GM', '- Historia Antigua [445]'),
        ('GN', '- Historia Contemporánea [450]'),
        ('GO', '- Historia de América [455]'),
        ('GP', '- Historia de la Ciencia [460]'),
        ('GQ', '- Historia del Arte [465]'),
        ('GR', '- Historia del Derecho y de las Instituciones [470]'),
        ('GS', '- Historia del Pensamiento y de los Movimientos Sociales [475]'),
        ('GT', '- Historia e Instituciones Económicas [480]'),
        ('GU', '- Historia Medieval [485]'),
        ('GV', '- Historia Moderna [490]'),
        ('GW', '- Lengua Española [567]'),
        ('GX', '- Lengua y Cultura del Extremo Oriente [568]'),
        ('GY', '- Lingüística General [575]'),
        ('GZ', '- Lingüística Indoeuropea [580]'),
        ('HA', '- Literatura Española [583]'),
        ('HB', '- Lógica y Filosofía de la Ciencia [585]'),
        ('HC', '- Metodología de las Ciencias del Comportamiento [620]'),
        ('HD', '- Métodos de Investigación y Diagnóstico en Educación [625]'),
        ('HE', '- Música [635]'),
        ('HF', '- Paleontología [655]'),
        ('HG', '- Pintura [690]'),
        ('HH', '- Prehistoria [695]'),
        ('HI', '- Teoría de la Literatura y Literatura Comparada [796]'),
        ('HJ', '- Teoría e Historia de la Educación [805]'),
        ('HK', '- Traducción e Interpretación [814]'),
        ('HL', 'Difusión de proyectos de investigación'),
        ('HM', '- Ciencias de la Salud'),
        ('HN', '- Ciencias Sociales'),
        ('HO', '- Ciencias Experimentales'),
        ('HP', '- Arquitectura e Ingeniería'),
        ('HQ', '- Humanidades'),
        ('HR', 'Institucional'),
        ('HS', '- Centros Académicos'),
        ('HT', '- Centros Culturales'),
        ('HU', '- Vicerrectorados'),
        ('HV', '- Rectorado'),
    )

    AUDIENCE_KEYS = (
        ('AA', u'Profesor'),
        ('AB', u'Autor'),
        ('AC', u'Alumno'),
        ('AD', u'Coordinador'),
        ('AE', u'Otro'),
    )

    LICENSE_KEYS = (
        ('CR', u'Todos los derechos reservados.'),
        ('MD', u'Creative Commons: Reconocimiento - No Comercial'),
        ('SA', u'Creative Commons: Reconocimiento - No Comercial - Compartir Igual'),
        ('ND', u'Creative Commons: Reconocimiento - No Comercial - Sin Obra Derivada'),
    )

    TYPE_KEYS = (
        ('AA', u'Conferencia'),
        ('AB', u'Documental'),
        ('AC', u'Coloquio'),
        ('AD', u'Curso'),
        ('AE', u'Institucional'),
        ('AF', u'Ficción'),
        ('AG', u'Mesa redonda'),
        ('AH', u'Exposición de trabajos'),
        ('AI', u'Apertura'),
        ('AJ', u'Clausura'),
        ('AK', u'Conferencia inaugural'),
        ('AL', u'Conferencia de clausura'),
        ('AM', u'Preguntas y respuestas'),
        ('AN', u'Intervención'),
        ('AO', u'Presentación'),
        ('AP', u'Demostración'),
        ('AQ', u'Entrevista'),
        ('AR', u'Video promocional'),
        ('AS', u'Videoconferencia'),
    )

    INTERACTIVITY_TYPE_KEYS = (
        ('AA', u'Activa'),
        ('AB', u'Expositiva'),
        ('AC', u'Combinada (activa y expositiva)'),
        ('AD', u'Otra'),
    )

    LEARNING_RESOURCE_TYPE_KEYS = (
        ('AA', u'Ejercicio'),
        ('AB', u'Índice'),
        ('AC', u'Experimento'),
        ('AD', u'Diagrama'),
        ('AE', u'Narración'),
        ('AF', u'Simulación'),
        ('AG', u'Presentación'),
        ('AH', u'Enunciado del problema'),
        ('AI', u'Figura'),
        ('AJ', u'Texto'),
        ('AK', u'Cuestionario'),
        ('AL', u'Tabla'),
        ('AM', u'Autoevaluación'),
        ('AN', u'Gráfico'),
        ('AO', u'Examen'),
    )

    INTERACTIVITY_LEVEL_KEYS = (
        ('AA', u'Muy bajo: Documento, imagen, video, sonido, etc. de carácter expositivo.'),
        ('AB', u'Bajo: Conjunto de documentos, imágenes, vídeos, sonidos, etc. enlazados.'),
        ('AC', u'Medio: El contenido dispone de elementos interactivos'),
        ('AD', u'Alto: Cuestionario, consulta, encuesta, examen, ejercicio, etc.'),
        ('AE', u'Muy alto: Juego, simulación, etc.'),
    )

    SEMANTIC_DENSITY_KEYS = (
        ('AA', u'Muy bajo: contenido de carácter irrelevante.'),
        ('AB', u'Bajo: contiene elementos interactivos para el usuario.'),
        ('AC', u'Medio: contenido audiovisual complejo, etc.'),
        ('AD', u'Alto: gráficos, tablas, diagramas complejos, etc.'),
        ('AE', u'Muy alto: presentaciones gráficas complejas o producciones audiovisuales. '),
    )

    CONTEXT_KEYS = (
        ('AA', u'Educación primaria'),
        ('AB', u'Educación secundaria'),
        ('AC', u'Educación superior'),
        ('AD', u'Universitario de primer ciclo'),
        ('AE', u'Universitario de segundo ciclo'),
        ('AF', u'Universitario de posgrado'),
        ('AG', u'Escuela técnica de primer ciclo'),
        ('AH', u'Escuela técnica de segundo ciclo'),
        ('AI', u'Formación profesional'),
        ('AJ', u'Formación continua'),
        ('AK', u'Formación vocacional'),
    )

    DIFICULTY_KEYS = (
        ('AA', u'Muy fácil: Conocimiento, comprensión, etc.'),
        ('AB', u'Fácil: Aplicación'),
        ('AC', u'Dificultad media: Análisis'),
        ('AD', u'Difícil: Síntesis'),
        ('AE', u'Muy difícil: Evaluación'),
    )

    EDUCATIONAL_LANGUAGE_KEYS = (
        ('AA', u'Expositivo'),
        ('AB', u'Semántico'),
        ('AC', u'Lexico'),
    )

    PURPOSE_KEYS = (
        ('AA', u'Multidisciplinar'),
        ('AB', u'Descripción de concepto / idea'),
        ('AC', u'Requisito educativo'),
        ('AD', u'Mejora de competencias educativas'),
    )

    GUIDELINE_KEYS = (
        ('AA', u'Ciencias de la salud'),
        ('AB', u'Ciencias experimentales'),
        ('AC', u'Ciencias jurídico-sociales'),
        ('AD', u'Ciencias tecnológicas'),
        ('AE', u'Humanidades'),
    )

    UNESCO_KEYS = (
        ('AA', u'Antropología'),
        ('AB', u'Artes y letras'),
        ('AC', u'Astronomía y Astrofísica'),
        ('AD', u'Ciencias Jurídicas y Derecho'),
        ('AE', u'Ciencias Agronómicas y Veterinarias'),
        ('AF', u'Ciencias de la Tecnología'),
        ('AG', u'Ciencias de la Tierra y el Cosmos'),
        ('AH', u'Ciencias de la Vida'),
        ('AI', u'Ciencias Económicas'),
        ('AJ', u'Ciencias Políticas'),
        ('AK', u'Corporativo'),
        ('AL', u'Demografía'),
        ('AM', u'Ética'),
        ('AN', u'Filosofía'),
        ('AO', u'Física'),
        ('AP', u'Geografía'),
        ('AQ', u'Historia'),
        ('AR', u'Lingüistia'),
        ('AS', u'Lógica'),
        ('AT', u'Matemáticas'),
        ('AU', u'Medicina y patologías humanas'),
        ('AV', u'Noticias'),
        ('AW', u'Pedagogía'),
        ('AX', u'Psicología'),
        ('AY', u'Química'),
        ('AZ', u'Sociología'),
        ('BA', u'Vida universitaria'),
    )

    knowledge_areas = models.CharField(max_length = 2, choices = KNOWLEDGE_AREAS_KEYS, verbose_name = u'Área de conocimiento')
    title = models.CharField(max_length = 255, verbose_name = u'Título completo de la producción')
    creator = models.CharField(max_length = 255, verbose_name = u'Autor/es o creador/es')
    contributor = models.CharField(max_length = 255, verbose_name = u'Colaborador/es', help_text = u'Aquellas personas, entidades u organizaciones que han participado en la creación de esta producción')
    keyword = models.CharField(max_length = 255, verbose_name = u'Palabras clave o etiquetas', help_text = u'Pude incluir tantas como quiera siempre y cuando se separen por comas.')
    description = models.TextField(verbose_name = u'Descripción breve')
    audience = models.CharField(max_length = 2, choices = AUDIENCE_KEYS, verbose_name = u'Audiencia o público objetivo')
    typical_age_range = models.CharField(max_length = 255, verbose_name = u'Edad de la audiencia o público objetivo')
    source = models.CharField(max_length = 255, null = True, blank = True, verbose_name = u'Identificador de obra derivada', help_text = u'Si el contenido es derivado de otra material, indique aquí la referencia al original')
    language = models.CharField(max_length = 255, verbose_name = u'Idioma')
    ispartof = models.CharField(max_length = 255, null = True, blank = True, verbose_name = u'Serie a la que pertenece')
    location = models.CharField(max_length = 255, verbose_name = u'Localización', help_text = u'Por ejemplo: el nombre de la institución, departamento, edificio, etc.')
    venue = models.CharField(max_length = 255, verbose_name = u'Lugar de celebración', help_text = u'Por ejemplo: San Cristóbal de La Laguna, Tenerife (España)')
    temporal = models.TextField(null = True, blank = True, verbose_name = u'Intervalo de tiempo', help_text = u'Si en la producción intervienen diferentes actores, indique aquí el nombre y el momento en el que interviene cada uno de ellos.')
    license = models.CharField(max_length = 2, choices = LICENSE_KEYS, verbose_name = u'Licencia de uso', help_text = u'Si el contenido dispone de alguna limitación de uso, incluya aquí una referencia a su licencia.')
    rightsholder = models.CharField(max_length = 255, verbose_name = u'Persona, entidad u organización responsable de la gestión de los derechos de autor')
    date = models.DateTimeField(verbose_name = u'Fecha de grabación', editable = False)
    created = models.DateTimeField(verbose_name = u'Fecha de producción', editable = False, help_text = u'La fecha de producción será incluida de manera automática por el sistema')
    valid = models.DateTimeField(null = True, blank = True, editable = False, verbose_name = u'Fecha de validación', help_text = u'La fecha de validación será incluida de manera automática por el sistema.')
    type = models.CharField(max_length = 2, choices = TYPE_KEYS, verbose_name = u'Tipo de producción')
    interactivity_type = models.CharField(max_length = 2, choices = INTERACTIVITY_TYPE_KEYS, verbose_name = u'Tipo de interacción con la audiencia o público objetivo')
    interactivity_level = models.CharField(max_length = 2, choices = INTERACTIVITY_LEVEL_KEYS, verbose_name = u'Nivel de interacción')
    learning_resource_type = models.CharField(max_length = 2, choices = LEARNING_RESOURCE_TYPE_KEYS, verbose_name = u'Tipo de recurso educativo')
    semantic_density = models.CharField(max_length = 2, choices = SEMANTIC_DENSITY_KEYS, verbose_name = u'Densidad semántica del contenido')
    context = models.CharField(max_length = 2, choices = CONTEXT_KEYS, verbose_name = u'Contexto educativo')
    dificulty = models.CharField(max_length = 2, choices = DIFICULTY_KEYS, verbose_name = u'Nivel de Dificultad')
    typical_learning_time = models.CharField(max_length = 255, verbose_name = u'Tiempo estimado para la adquisición de conocimientos', help_text = u'Ejemplo: 2 horas')
    educational_language = models.CharField(max_length = 2, choices = EDUCATIONAL_LANGUAGE_KEYS, verbose_name = u'Características del lenguaje educativo')
    purpose = models.CharField(max_length = 2, choices = PURPOSE_KEYS, verbose_name = u'Objetivo del contenido')
    guideline = models.CharField(max_length = 2, choices = GUIDELINE_KEYS, verbose_name = u'Área de conocimiento')
    unesco = models.CharField(max_length = 2, choices = UNESCO_KEYS, verbose_name = u'Dominio de conocimiento')

    class Meta:
        verbose_name = u'Metadatos'
        verbose_name_plural = u'Metadatos'

    def __unicode__(self):
        return self.video.titulo


## COLA ##

class ColaManager(models.Manager):
    """
    Devuelve el número de trabajos que están siendo codificados en este momento.
    """
    def count_actives(self):
        return super(ColaManager, self).get_query_set().filter(status = 'PRO').count()

    """
    Devuelve el número de trabajos que están pendientes de ser procesados
    """
    def count_pendings(self):
        return super(ColaManager, self).get_query_set().filter(status = 'PEN').count()

    """
    Devuelve la lista de vídeos pendientes de ser procesados.
    """
    def get_pendings(self):
         return super(ColaManager, self).get_query_set().filter(status = 'PEN').order_by('id')

class Cola(models.Model):
    QUEUE_STATUS = (
        ('PEN', 'Pendiente'),
        ('PRO', 'Procesando'),
        ('HEC', 'Hecho'),
        ('ERR', 'Error'),
    )

    QUEUE_TYPE = (
        ('COP', u'Copia'),
        ('PIL', u'Producción'),
        ('PRE', u'Previsualización')
    )

    objects = ColaManager()

    video = models.ForeignKey(Video)
    status = models.CharField(max_length = 3, choices = QUEUE_STATUS, default = 'PEN')
    tipo = models.CharField(max_length = 3, choices = QUEUE_TYPE)
    comienzo = models.DateTimeField(null = True, blank = True)
    fin = models.DateTimeField(null = True, blank = True)
    logfile = models.FileField(upload_to = "logs", null = True, blank = True)
    pid = models.IntegerField(null = True, editable = False)

    def __unicode__(self):
       return dict(self.QUEUE_TYPE)[self.tipo] + ": " + self.video.__unicode__()

    def set_status(self, st):
        self.status = st
        self.save()

    def delete(self, *args, **kwargs):
        if self.status == 'PRO' and self.pid:
            try:
                os.kill(self.pid, signal.SIGTERM)
            except:
                self.status = 'ERR'
                self.save()
            while Cola.objects.get(pk=self.id).status == 'PRO': pass
        super(Cola, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = u'tarea'
        verbose_name_plural = u'tareas'

class Token(models.Model):

    token = models.CharField(max_length = 25)
    instante = models.DateTimeField(auto_now_add = True)
    video = models.OneToOneField(Video)

    def __unicode__(self):
        return self.video.titulo
