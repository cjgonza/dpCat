# encoding: utf-8
from django.shortcuts import render_to_response
from django.template import Template, Context
from django.core.mail import send_mail
from configuracion import config
from settings import MEDIA_ROOT
from cb_publisher.models import RegistroPublicacionCB
from postproduccion.utils import generate_token

import urllib
import json
import os
import shutil
import hashlib
import tempfile
from datetime import datetime

def _remote_action(action, params = None):
    if params:
        params = urllib.urlencode(params)
    f = urllib.urlopen("%s/plugins/dpcat/%s.php" %  (config.get_option('CB_PUBLISHER_CLIPBUCKET_URL'), action), params)
    return f.read()

def publish(task):
    task.status = 'EXE' # esto se debería hacer desde fuera en caso de multithread.
    task.save()
    v = task.video
    d = json.loads(task.data)

    rand_prefix = generate_token(5)
    localfile = os.path.join(config.get_option('CB_PUBLISHER_LOCAL_DIR'), rand_prefix + os.path.basename(v.fichero))
    remotefile = os.path.join(config.get_option('CB_PUBLISHER_REMOTE_DIR'), rand_prefix + os.path.basename(v.fichero))
    data = {
        'user' : config.get_option('CB_PUBLISHER_USERNAME'),
        'pass' : config.get_option('CB_PUBLISHER_PASSWORD'),
        'file' : remotefile,
        'title' : d['title'].encode('utf-8'),
        'description' : d['description'].encode('utf-8'),
        'tags' : d['tags'].encode('utf-8'),
        'category' : d['category'],
        'license' : d['license'],
        'collection' : d['collection'],
    }

    # Insertar en una colección.
    if d['collection'] is 1:
        data['add_to_collection'] = d['add_to_collection']
    if d['collection'] is 2:
        data['new_collection_name'] = d['new_collection_name'].encode('utf-8')
        data['new_collection_description'] = d['new_collection_description'].encode('utf-8')
        data['new_collection_tags'] = d['new_collection_tags'].encode('utf-8')
        data['new_collection_category'] = d['new_collection_category']

    shutil.copy(v.fichero, localfile)

    error_text = u"'%s' (%s)\n--\n\n" % (v, datetime.now())
    try:
        raw_data = _remote_action('uploader', data)
        ret_data = json.loads(raw_data)
    except IOError as (errno, strerror):
        error_text += "Error conectando al servidor({0}): {1}\n".format(errno, strerror)
        ret_data = None
    except ValueError:
        error_text += raw_data
        ret_data = None

    os.remove(localfile)

    if ret_data:
        if ret_data['cb_errors'] or ret_data['message']:
            if ret_data['cb_errors']:
                error_text += '--- Salida de error del clipbucket --\n'
                for line in ret_data['cb_errors']:
                    error_text += ' * ' + line + '\n'
            if ret_data['message']:
                error_text += '--- Salida de error del plugin --\n'
                error_text += ret_data['message'] + '\n'
        else:
            RegistroPublicacionCB(video = v, enlace = ret_data['vlink']).save()
            task.delete()
            return
        
    # Hubo algún error

    # Guarda el registro del error.
    (handle, path) = tempfile.mkstemp(suffix = '.pub.log', dir = MEDIA_ROOT + '/' + task.logfile.field.get_directory_name())
    task.logfile = task.logfile.field.get_directory_name() + '/' + os.path.basename(path)
    os.write(handle, error_text.encode('utf-8'))
    os.close(handle)

    # Si se creó la publicación en el ClipBucket se borra.
    if ret_data and ret_data['vid']:
        import time
        time.sleep(10)
        data = {
            'user' : config.get_option('CB_PUBLISHER_USERNAME'),
            'pass' : config.get_option('CB_PUBLISHER_PASSWORD'),
            'vid' : ret_data['vid']
        }
        _remote_action('delete_video', data)
    
    task.status = 'ERR'
    task.save()

def get_categories():
    categorias = json.loads(_remote_action('get_categories'))

    choices = list()
    def get_sub_categories(parent, level):
        for cat in categorias:
            if cat['parent_id'] == parent:
                choices.append((cat['category_id'], "- " * level  + cat['category_name']))
                get_sub_categories(cat['category_id'], level + 1)


    for cat in categorias:
        if int(cat['parent_id']) is 0:
            choices.append((cat['category_id'], cat['category_name']))
            get_sub_categories(cat['category_id'], 1)

    return choices

def get_category_id(category_name):
    categorias = json.loads(_remote_action('get_categories'))

    category_id = None # Se inicializa por si acaso no casa ninguna categoría.

    # Si hay varias nos quedamos con la última
    for c in categorias:
        if c['category_name'] == category_name:
            category_id = c['category_id']

    return category_id

def get_collection_categories():
    categorias = json.loads(_remote_action('get_collection_categories'))

    choices = list()
    for cat in categorias:
        choices.append((cat['category_id'], cat['category_name']))

    return choices

def get_collections():
    categorias = json.loads(_remote_action('get_collections'))

    choices = list()
    for cat in categorias:
        choices.append((cat['collection_id'], cat['collection_name']))

    return choices
