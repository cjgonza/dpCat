# encoding: utf-8
from django.shortcuts import render_to_response
from configuracion import config

import urllib
import os
import shutil
import json

def execute_upload(v, category):
    localfile = os.path.join(config.get_option('CB_PUBLISHER_LOCAL_DIR'), os.path.basename(v.fichero))
    remotefile = os.path.join(config.get_option('CB_PUBLISHER_REMOTE_DIR'), os.path.basename(v.fichero))
    data = {
        'user' : config.get_option('CB_PUBLISHER_USERNAME'),
        'pass' : config.get_option('CB_PUBLISHER_PASSWORD'),
        'file' : remotefile,
        'title' : v.metadata.title.encode('utf-8'),
        'description' : v.metadata.description.encode('utf-8'),
        'tags' : v.metadata.keyword.encode('utf-8'),
        'category' : category,
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


def get_categories():
    f = urllib.urlopen("%s/plugins/dpcat_ull/get_categories.php" %  config.get_option('CB_PUBLISHER_CLIPBUCKET_URL'))
    categorias = json.loads(f.read())

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
