import nanolog as nl
import sys
from .errors import *

logger = None

def initLogger():
    try:
        log_file = open('run_gnc_log.txt', 'w')
    except OSError as err:
        logger.critical1("Error: Invalid args provided. See run_gnc help for more information.")
        sys.exit(LOG_CREATION_ERROR)

    logger = nl.Logger.create_logger(
        'main',
        stream=log_file,
        level='debug'
    )