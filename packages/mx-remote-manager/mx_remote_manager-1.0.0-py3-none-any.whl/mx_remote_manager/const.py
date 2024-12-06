##################################################
##         MX Remote Manager GUI                ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

""" constant definitions for mx_remote_ui """
import os

VERSION = '1.0.0'
__version__ = VERSION

APP_PACKAGE = 'mx_remote_manager'
APP_ID = f'eu.opdenkamp.{APP_PACKAGE}'
APP_NAME = 'MX Remote Manager'
APP_REPOSITORY = 'https://github.com/opdenkamp/mx-remote-manager'
BASE_PATH = os.path.dirname(__file__)
DEFAULT_TX_ADDRESS = '234.88.88.88'