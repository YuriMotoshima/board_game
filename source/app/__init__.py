
import logging
import warnings
from logging import getLogger

from app.config.collections_exceptions import collections_exceptions
from app.config.log import loginit

try:
    loginit()
    getLogger('google.auth').setLevel(logging.ERROR)
    getLogger('google.auth.transport').setLevel(logging.ERROR)
    getLogger('sqlalchemy').setLevel(logging.ERROR)
    getLogger('google.cloud').setLevel(logging.ERROR)
    getLogger('urllib3').setLevel(logging.ERROR)
    getLogger('google.api_core').setLevel(logging.ERROR)
    getLogger('httpx').setLevel(logging.ERROR)
    getLogger('httpcore').setLevel(logging.ERROR)
    getLogger('utils_api_pipefy').setLevel(logging.ERROR)
    
    warnings.filterwarnings('ignore')

except Exception as error:
    raise collections_exceptions(error)
