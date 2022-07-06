import logging

from kapylan import algorithm
from kapylan import core
from kapylan import problem

__all__ = ['core', 'algorithm', 'operator', 'problem']

logger = logging.getLogger('kapylan')
logger.setLevel(logging.INFO)

# create a file handler
file_handler = logging.FileHandler('kapylan.log', delay=True)
file_handler.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()

# create a logging format
formatter = logging.Formatter('%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s')
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
