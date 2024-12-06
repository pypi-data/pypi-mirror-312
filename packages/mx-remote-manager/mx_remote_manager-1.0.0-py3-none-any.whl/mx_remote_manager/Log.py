##################################################
##         MX Remote Manager GUI                ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

import gi
import mx_remote as mx
import logging

_LOGGER = logging.getLogger(__name__)

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

@Gtk.Template(resource_path=f'/builder/device_log.ui')
class DeviceLog(Gtk.Window):
    __gtype_name__ = 'device_log_tpl'
    child_text = Gtk.Template.Child('text')

    def __init__(self, device:mx.DeviceBase, data:str) -> None:
        Gtk.Window.__init__(self)
        self.set_title(str(device.serial))
        buffer = Gtk.TextBuffer()
        buffer.set_text(data)
        self.child_text.set_buffer(buffer)
