import logging
import logging.config
import os
from core.filter import TraceIDFilter  # make sure this path is correct

LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(trace_id)s] %(name)s (%(filename)s:%(lineno)d): %(message)s',
        },
    },

    'filters': {
        'trace_id_filter': {
            '()': TraceIDFilter,
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['trace_id_filter'],
            'level': 'DEBUG',
        },
        'hotel_file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'hotel.log'),
            'formatter': 'verbose',
            'filters': ['trace_id_filter'],
            'level': 'DEBUG',
        },
        'food_file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'food.log'),
            'formatter': 'verbose',
            'filters': ['trace_id_filter'],
            'level': 'DEBUG',
        },
        'address_file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'address.log'),
            'formatter': 'verbose',
            'filters': ['trace_id_filter'],
            'level': 'DEBUG',
        },
        'authenticate_file': {
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'authenticate.log'),
            'formatter': 'verbose',
            'filters': ['trace_id_filter'],
            'level': 'DEBUG',
        },
    },

    'loggers': {
        'hotel': {
            'handlers': ['hotel_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'food': {
            'handlers': ['food_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'address': {
            'handlers': ['address_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'authenticate': {
            'handlers': ['authenticate_file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
