##################################################
##         MX Remote Manager GUI                ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

import gi
import mx_remote as mx
import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

@Gtk.Template(resource_path=f'/builder/device_status.ui')
class DeviceStatusValue(Gtk.Box):
    __gtype_name__ = 'device_status'
    child_device_status = Gtk.Template.Child("device_status")
    child_device_status_image = Gtk.Template.Child("device_status_image")
    child_device_status_label = Gtk.Template.Child("device_status_label")

    def __init__(self, status:mx.DeviceStatus) -> None:
        super().__init__()
        self.update(status)

    def on_detach(self) -> None:
        pass

    def update(self, status:mx.DeviceStatus) -> None:
        self.child_device_status_label.set_text(str(status))
        if status == mx.DeviceStatus.OFFLINE:
            self.child_device_status_image.set_from_icon_name('network-wired-disconnected-symbolic')
        elif status == mx.DeviceStatus.ONLINE:
            self.child_device_status_image.set_from_icon_name('network-wired-symbolic')
        else:
            self.child_device_status_image.set_from_icon_name('network-wired-acquiring-symbolic')
