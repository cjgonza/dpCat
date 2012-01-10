# encoding: utf-8
from django.shortcuts import render_to_response
from configuracion import config

import urllib
import os
import shutil
import json

def get_category_id(category_name):
    f = urllib.urlopen("%s/plugins/dpcat_ull/get_categories.php" %  config.get_option('CB_PUBLISHER_CLIPBUCKET_URL'))
    categorias = json.loads(f.read())

    # Si hay varias nos quedamos con la última
    for c in categorias:
        if c['category_name'] == category_name:
            category_id = c['category_id']

    return category_id

def execute_upload(v):
    localfile = os.path.join(config.get_option('CB_PUBLISHER_LOCAL_DIR'), os.path.basename(v.fichero))
    remotefile = os.path.join(config.get_option('CB_PUBLISHER_REMOTE_DIR'), os.path.basename(v.fichero))
    data = {
        'user' : config.get_option('CB_PUBLISHER_USERNAME'),
        'pass' : config.get_option('CB_PUBLISHER_PASSWORD'),
        'file' : remotefile,
        'title' : v.metadata.title.encode('utf-8'),
        'description' : v.metadata.description.encode('utf-8'),
        'tags' : v.metadata.keyword.encode('utf-8'),
        'category' : get_category_id(v.metadata.get_knowledge_areas_display()),
        'license' : v.metadata.license,
    }

    shutil.copy(v.fichero, localfile)

    params = urllib.urlencode(data)
    f = urllib.urlopen("%s/plugins/dpcat_ull/uploader.php" %  config.get_option('CB_PUBLISHER_CLIPBUCKET_URL'), params)
    messages = f.read()

    os.remove(localfile)

    if not messages:
        return None
    else:
        return messages
