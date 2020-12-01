import os
from importlib import import_module

settings = import_module(os.environ["APP_SETTINGS_MODULE"])