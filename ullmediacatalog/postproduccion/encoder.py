#encoding: utf-8
import subprocess
import os

"""
Llama al mplayer para obtener la información multimedia de un vídeo y
devuelve la información en un hash.
"""
def get_mm_info(filename):
    command = "mplayer -really-quiet -identify -nolirc %s -ao null -vo null -frames 0" % filename
    data = os.popen(command).read()
    return dict([s.split('=') for s in data.strip().split('\n')])

"""
Diccionario con los nombres de los formatos de codecs.
"""
format_types = {
    'ffdv' : {
        'short': 'dvvideo',
        'long' : 'DV_(Digital Video)'
    },
    'pcm' : {
        'short': 'pcm_s16le',
        'long' : 'PCM_signed 16bitlittleendian'
    },
    'ffwmv3' : {
        'short': 'wmv3',
        'long' : 'Windows_Media_Video_9'
    },
    'ffwmav2' : {
        'short': 'wmav2',
        'long' : 'Windows_Media_Audio_2'
    }
}


"""
Realiza el montaje de un video
"""
def encode_mixed_video(mltfile, outfile, logfile):
    command = "melt -progress -verbose %s -consumer avformat:/%s deinterlace=1 acodec=libfaac ab=348k ar=48000 pix_fmt=yuv420p f=mp4 vcodec=libx264 minrate=0 b=1000k aspect=@16/9 s=1280x720i fpre=lossless-max" % (mltfile, outfile)
    p = subprocess.Popen(command, shell = True, stderr=logfile)

    return os.waitpid(p.pid, 0)[1]
