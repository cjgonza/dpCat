# encoding: utf-8
from django.shortcuts import render_to_response
from configuracion import config

import urllib
import subprocess
import json

def _remote_action(action, params = None):
    f = urllib.urlopen("%s/plugins/dpcat/%s.php" %  (config.get_option('CB_PUBLISHER_CLIPBUCKET_URL'), action))
    return f.read()

"""
def get_uploader_code(v, category):
    cb_path = config.get_option('CB_PUBLISHER_CLIPBUCKET_PATH')
    auth = { 'user' : config.get_option('CB_PUBLISHER_USERNAME'), 'pass' : config.get_option('CB_PUBLISHER_PASSWORD') }
    return render_to_response('cb_publisher/uploader.php', { 'v' : v, 'cb_path' : cb_path, 'auth' : auth, 'category' : category }).content

def execute_upload(v, category):
    php_path = config.get_option('CB_PUBLISHER_PHP_PATH')

    p = subprocess.Popen(php_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    messages = p.communicate(input=get_uploader_code(v, category))[0]

    if p.returncode == 0:
        return None
    else:
        return messages
"""

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
