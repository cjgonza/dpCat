"""
from configuracion import config

defaults = [
    [ 'CB_PUBLISHER_CLIPBUCKET_URL', 'http://192.168.56.101/clipbucket' ],
    [ 'CB_PUBLISHER_USERNAME' ,       'dpcat' ], 
    [ 'CB_PUBLISHER_PASSWORD',        'dpcat1234' ],
    [ 'CB_PUBLISHER_LOCAL_DIR', '/tmp' ],
    [ 'CB_PUBLISHER_REMOTE_DIR', '/tmp' ],
]

for op in defaults:
    config.get_option(op[0]) or config.set_option(op[0], op[1])

from cb_publisher.forms import ConfigForm
from cb_publisher.functions import execute_upload as publish
"""
