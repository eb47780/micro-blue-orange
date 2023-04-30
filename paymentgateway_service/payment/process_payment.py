import time
import logging


def checkout_session(data):
    logging.warning(data)
    logging.warning('Processing Payment Simulation')
    time.sleep(10)
    return 'Remote Invoice Id Dummy'
