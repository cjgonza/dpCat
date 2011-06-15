from configuracion import config
from postproduccion.utils import which

defaults = [
    [ 'CB_PUBLISHER_CLIPBUCKET_PATH', '/var/www/clipbucket' ],
    [ 'CB_PUBLISHER_USERNAME' ,       'dpcat' ], 
    [ 'CB_PUBLISHER_PASSWORD',        'dpcat1234' ],
    [ 'CB_PUBLISHER_PHP_PATH',        which('php') ],
]

for op in defaults:
    config.get_option(op[0]) or config.set_option(op[0], op[1])

from cb_publisher.forms import ConfigForm, PublishingForm
from cb_publisher.functions import execute_upload as publish
