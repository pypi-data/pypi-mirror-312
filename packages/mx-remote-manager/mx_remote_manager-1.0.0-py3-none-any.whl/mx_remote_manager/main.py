##################################################
##         MX Remote Manager GUI                ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

import argparse
from .const import APP_PACKAGE
import gi
import importlib.resources as importlib_resources
import logging
import mx_remote
from typing import Any

_LOGGER = logging.getLogger(__name__)

gi.require_version("Gtk", "4.0")
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, Gdk, GLib

# import pdb_attach
# pdb_attach.listen(50000)

def _load_resources():
    '''load embedded resources'''
    resource_data = importlib_resources.read_binary(APP_PACKAGE, 'ui.gresource')
    resource = Gio.Resource.new_from_data(GLib.Bytes(resource_data))
    resource._register()
    theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
    theme.add_resource_path("/icons/")

def _check_show_gui(param:Any, args:argparse.Namespace) -> bool:
    return (args.output is None) and (args.input is None) and (param or args.ui)

def _main_extra_args_callback(param:Any, argparser:argparse.ArgumentParser) -> None:
    argparser.add_argument("-u", dest='ui', help='show the user interface', required=False, type=bool)

def _main_log_level_callback(param:Any, args:argparse.Namespace) -> int:
    return logging.INFO if param else logging.DEBUG

def _main_entry_callback(param:Any, args:argparse.Namespace) -> bool:
    if _check_show_gui(param=param, args=args):
        _load_resources()
        from .Interface import MxrGui
        gui = MxrGui(local_ip=args.local_ip, broadcast=(args.broadcast is not None and args.broadcast))
        gui.start()
        return True
    return False

def mxr_main():
    mx_remote.mxr_main(extra_args_callback=_main_extra_args_callback,
                       log_level_callback=_main_log_level_callback,
                       entry_callback=_main_entry_callback,
                       callback_param=False)

def mxr_ui():
    mx_remote.mxr_main(extra_args_callback=_main_extra_args_callback,
                       log_level_callback=_main_log_level_callback,
                       entry_callback=_main_entry_callback,
                       callback_param=True)