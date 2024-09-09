from core import config
from logging import config as logging_config
from core.logger import LOGGING

logging_config.dictConfig(LOGGING)
settings = config.Settings()
