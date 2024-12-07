import time
import traceback

from .core.Logger import Logger
from .utils.Start import PyWelcome

def run_ethopy(protocol=False):
    ERROR = None
    logger = Logger(protocol=protocol)   # setup logger

    # # # # Waiting for instructions loop # # # # #
    while logger.setup_status != 'exit':
        if logger.setup_status != 'running':
            PyWelcome(logger)
        if logger.setup_status == 'running':   # run experiment unless stopped
            try:
                if logger.update_protocol():
                    exec(open(logger.protocol_path, encoding='utf-8').read())
                else:
                    raise FileNotFoundError('Protocol file not found!')
            except Exception as e:
                ERROR = traceback.format_exc()
                logger.update_setup_info({'state': 'ERROR!', 'notes': str(e), 'status': 'exit'})
        time.sleep(.1)
    logger.cleanup()

    return ERROR
