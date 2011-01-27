#encoding: utf-8
from configuracion import config
import subprocess
import shlex
import os
import re

"""
Llama al ffmpeg y para obtener la información completa del fichero y
devuelve la información procesada en un hash.
"""
def get_file_info(filename):
    command = "%s -i %s -acodec copy -vcodec copy -f null /dev/null" % (config.get_option('FFMPEG_PATH'), filename)
    data = subprocess.Popen(shlex.split(str(command)), stderr=subprocess.PIPE).communicate()[1]

    info = dict()

    info['size'] = os.stat(filename).st_size

    # Comprueba el mensaje final de la codificación
    m = re.search('video:([0-9]+)kB audio:([0-9]+)kB global headers:[0-9]+kB muxing overhead', data)
    if m:
        (video_size, audio_size) = m.group(1, 2) 
    else:
        return False

    # Comprueba el último mensaje de actualización de la codificación
    m = re.search('(frame=([^=]*) fps=[^=]* q=[^=]* L)?size=[^=]*kB time=([^=]*) bitrate=[^=]*kbits/s[^=]*$', data)
    if m:
        frame_count = float(m.group(2)) if m.group(2) else 0;
        info['duration'] = float(m.group(3))
        info['bitrate'] = int(info['size'] * 8 / 1024 / info['duration'])
    else:
        return False

    info['video_rate'] = float(frame_count) / float(info['duration']) if frame_count > 0 else None
    info['video_bitrate'] = float(video_size) / float(info['duration']) if video_size > 0 else None
    info['audio_bitrate'] = float(audio_size) / float(info['duration']) if audio_size > 0 else None

    m = re.search('Input #0, ([^ ]+), from', data)
    info['format'] = m.group(1) if m else "N/A"

    # Obtiene la información del vídeo
    m = re.search('Video: ([^ ]+), ([^ ]+), ([0-9]+)x([0-9]+)( \[PAR ([0-9]+):([0-9]+) DAR ([0-9]+):([0-9]+)\])?', data)
    if m:
        (info['video_codec'], info['video_color'], info['video_width'], info['video_height']) = m.group(1, 2, 3, 4)

        if m.group(5):
            (par1, par2, dar1, dar2) = m.group(6, 7, 8, 9)
            if int(dar1) > 0 and int(dar2) > 0 and int(par1) > 0 and int(par2) > 0:
                info['video_wh_ratio'] = (float(dar1) / float(dar2)) / (float(par1) / float(par2))

        # No hay información sobre la relación de aspecto, asumimos píxeles cuadrados.
        if 'video_wh_ratio' not in info:
            info['video_wh_ratio'] = float(info['video_width']) / float(info['video_height'])

    # Obtiene la información del audio
    m = re.search('Audio: ([^ ]+), ([0-9]+) Hz, ([^\n,]*)', data)
    if m:
        (info['audio_codec'], info['audio_rate'], info['audio_channels']) = m.group(1, 2, 3)
     
    return info

"""
Devuelve los parámetros preestablecidos para el codec x264
"""
def x264_presets():
    params = [
        [ 'coder',        '1'],
        [ 'flags',        '+loop'],
        [ 'cmp',          '+chroma'],
        [ 'partitions',   '+parti8x8+parti4x4+partp8x8+partb8x8'],
        [ 'me_method',    'hex'],
        [ 'subq',         '7'],
        [ 'me_range',     '16'],
        [ 'g',            '250'],
        [ 'keyint_min',   '25'],
        [ 'sc_threshold', '40'],
        [ 'i_qfactor',    '0.71'],
        [ 'b_strategy',   '1'],
        [ 'qcomp',        '0.6'],
        [ 'qmin',         '10'],
        [ 'qmax',         '51'],
        [ 'qdiff',        '4'],
        [ 'bf',           '3'],
        [ 'refs',         '3'],
        [ 'directpred',   '1'],
        [ 'trellis',      '1'],
        [ 'flags2',       '+bpyramid+mixed_refs+wpred+dct8x8+fastpskip'],
        [ 'wpredp',       '2'],
    ]

    return " ".join(map(lambda x: "%s=%s" % tuple(x), params))

"""
Realiza el montaje de un video
"""
def encode_mixed_video(mltfile, outfile, logfile, pid_notifier = None):
    command = "%s -progress -verbose %s -consumer avformat:/%s deinterlace=1 acodec=libfaac ab=348k ar=48000 pix_fmt=yuv420p f=mp4 vcodec=libx264 minrate=0 b=1000k aspect=@16/9 s=1280x720i %s" % (config.get_option('MELT_PATH'), mltfile, outfile, x264_presets())
    p = subprocess.Popen(shlex.split(str(command)), stderr=logfile)

    if pid_notifier:
        pid_notifier(p.pid)

    return os.waitpid(p.pid, 0)[1]

def encode_preview(filename, outfile, size, logfile, pid_notifier = None):
    command = "%s -y -i %s -f flv -vcodec flv -r 30 -b 512000 -s %sx%s -aspect %s -acodec libmp3lame -ab 128000 -ar 22050 %s" % (config.get_option('FFMPEG_PATH'), filename, size['width'], size['height'], size['ratio'], outfile)
    p = subprocess.Popen(shlex.split(str(command)), stderr=logfile)

    if pid_notifier:
        pid_notifier(p.pid)

    return os.waitpid(p.pid, 0)[1]
