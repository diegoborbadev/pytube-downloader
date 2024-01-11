import os
from logging import config, getLogger

# Create the log directory if it does not exist
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Load the logging configuration
config.fileConfig('loggers.conf')

# Create the logger objects
root_logger = getLogger('root')
info_logger = getLogger('info')
error_logger = getLogger('errors')

info_logger.info('Loggers instantiated')