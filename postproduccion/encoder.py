#encoding: utf-8
from configuracion import config
from postproduccion import utils
import subprocess
import shlex
import os
import re

"""
Llama al mediainfo y para obtener la información completa del fichero y
devuelve una lista con los datos en XML y los datos en texto plano.
"""
def get_file_info(filename):
    command = "'%s' --Output=XML '%s'" % (config.get_option('MEDIAINFO_PATH'), filename)
    xml_data = subprocess.Popen(shlex.split(str(command)), stdout=subprocess.PIPE).communicate()[0]

    command = "'%s' '%s'" % (config.get_option('MEDIAINFO_PATH'), filename)
    txt_data = subprocess.Popen(shlex.split(str(command)), stdout=subprocess.PIPE).communicate()[0]
    
    return [xml_data, txt_data]

"""
Comprueba si el fichero dado contiene pista de vídeo.
"""
def is_video_file(filename):
    command = "'%s' '%s'" % (config.get_option('MEDIAINFO_PATH'), filename)
    media_data = subprocess.Popen(shlex.split(str(command)), stdout=subprocess.PIPE).communicate()[0]

    return re.search("^Video", media_data, re.M) is not None

"""
Llama al avconv para obtener la duracion del vídeo en segundos con decimales.
"""
def get_video_duration(filename):
    command = "'%s' -i '%s' -acodec copy -vcodec copy -f null /dev/null" % (config.get_option('AVCONV_PATH'), filename)
    data = subprocess.Popen(shlex.split(str(command)), stderr=subprocess.PIPE).communicate()[1]

    return utils.time_to_seconds(re.findall(' time=([^=]*) ', data)[-1])

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
Incrusta la metadata al video final
"""
def embed_metadata(filename, metadata):
    command = "'%s' -config %s %s '%s'" % (config.get_option('EXIFTOOL_PATH'), config.get_option('EXIFTOOL_CONFIG'), metadata, filename)
    p = subprocess.Popen(shlex.split(str(command)), stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    out, err = p.communicate() # Esperar a finalizar

    # Borrar video original
    try:
        os.unlink(filename + '_original')
    except:
        pass

"""
Realiza el montaje de un video
"""
def encode_mixed_video(mltfile, outfile, logfile, pid_notifier = None):
    command = "'%s' -progress -verbose '%s' -consumer 'avformat:/%s' deinterlace=1 acodec=aac ab=348k ar=48000 pix_fmt=yuv420p f=mp4 vcodec=libx264 minrate=0 vb=850k aspect=@16/9 s=1280x720i r=25 threads=0 %s" % (config.get_option('MELT_PATH'), mltfile, outfile, x264_presets())
    p = subprocess.Popen(shlex.split(str(command)), stderr=logfile)

    if pid_notifier:
        pid_notifier(p.pid)

    return os.waitpid(p.pid, 0)[1]

def encode_preview(filename, outfile, size, logfile, pid_notifier = None):
    command = "'%s' -y -i '%s' -f flv -vcodec flv -r 25 -b 512000 -s %sx%s -aspect %s -acodec libmp3lame -ab 128000 -ar 22050 '%s'" % (config.get_option('AVCONV_PATH'), filename, size['width'], size['height'], size['ratio'], outfile)
    p = subprocess.Popen(shlex.split(str(command)), stderr=logfile)

    if pid_notifier:
        pid_notifier(p.pid)

    return os.waitpid(p.pid, 0)[1]

def make_streamable(filename, logfile, pid_notifier = None):
    command = "'%s' -inter 0.5 '%s' -tmp '%s'" % (config.get_option('MP4BOX_PATH'), filename, os.path.dirname(filename))
    p = subprocess.Popen(shlex.split(str(command)), stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

    if pid_notifier:
        pid_notifier(p.pid)

    os.write(logfile, p.communicate()[0])
