# encoding: utf-8
from django.shortcuts import render_to_response

import subprocess

def get_uploader_code(v):
    cb_path = '/var/www/clipbucket'
    auth = { 'user' : 'dpcat', 'pass' : 'dpcat1234' }
    return render_to_response('cb_publisher/uploader.php', { 'v' : v, 'cb_path' : cb_path, 'auth' : auth }).content

def execute_upload(v):
    php_path = '/usr/bin/php'

    p = subprocess.Popen(php_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    messages = p.communicate(input=get_uploader_code(v))[0]

    if p.returncode == 0:
        print "Todo OK"
    else:
        print "Error:"
        print messages

