# -*- encoding: utf-8 -*-
from django.core.management.base import BaseCommand
from postproduccion.models import Video
from postproduccion import video


def parse_input(input):

    if 'all' in input:
        return Video.objects.all()

    videos = []

    for arg in input:
        if '-' in arg:
            limits = arg.split('-')
            try:
                min_, max_ = int(limits[0]), int(limits[-1])
            except:
                continue
            else:
                if not min_ < max_:
                    continue
            for id in xrange(min_, max_):
                try:
                    v = Video.objects.get(pk=id)
                except:
                    continue
                videos += [v]
        else:
            try:
                v = Video.objects.get(pk=int(arg))
            except:
                continue
            videos += [v]

    # Eliminar videos duplicados
    return sorted(set(videos))


class Command(BaseCommand):
    help = u'Incrutar metadata en los vídeos'

    def add_arguments(self, parser):
        # Positional argument
        parser.add_argument(
            'video_id',
            metavar='ID',
            type=str,
            nargs='+',
            help=u'Vídeos para incrustar metadata. Ej: 342 465 500-980'
        )

        # Named (optional) arguments
        parser.add_argument(
            '-a',
            '--add',
            action='store_true',
            dest='add',
            default=True,
            help=u'Incrustar metadata en el vídeo'
        )

        parser.add_argument(
            '-s',
            '--show',
            action='store_true',
            dest='show',
            default=False,
            help=u'Mostrar metadata del vídeo'
        )

    def handle(self, *args, **options):

        if options['show']:
            options['add'] = False
            for v in parse_input(options['video_id']):
                print '\n--->Video [%s]: %s' % (v.id, v)
                for metadata in video.get_metadata(v).split('-XMP:'):
                    if metadata:
                        print metadata

        if options['add']:
            for v in parse_input(options['video_id']):
                if video.add_metadata(v) and options['verbosity'] > 1:
                    print "Video [%s]: updated metadata!" % v.id
                elif options['verbosity'] > 1:
                    print "Video [%s]: it was not" \
                        "possible to add metadata..." % v.id
