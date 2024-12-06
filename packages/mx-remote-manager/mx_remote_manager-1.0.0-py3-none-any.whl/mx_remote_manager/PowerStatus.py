##################################################
##         MX Remote Manager GUI                ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

import asyncio
import gi
import mx_remote as mx
import logging
from typing import Any

_LOGGER = logging.getLogger(__name__)

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

@Gtk.Template(resource_path=f'/builder/device_power.ui')
class DevicePowerStatus(Gtk.Box):
    __gtype_name__ = 'device_power'
    child_power_button = Gtk.Template.Child("power_button")
    child_power_button_image = Gtk.Template.Child("power_button_image")
    child_power_button_label = Gtk.Template.Child("power_button_label")

    def __init__(self) -> None:
        super().__init__()
        self._bay:mx.BayBase = None
        self._detached = False
        self.child_power_button.connect('clicked', self._on_power_clicked)

    def on_detach(self) -> None:
        self._detached = True

    def set_bay(self, bay:mx.BayBase) -> None:
        if (self._bay != bay):
            if (self._bay is not None):
                self._bay.unregister_callback(self._on_bay_changed)
            self._bay = bay
            bay.register_callback(self._on_bay_changed)
        self.set_power(bay.powered_on)

    def _on_bay_changed(self, bay:mx.BayBase) -> None:
        self.set_power(bay.powered_on)

    def _on_power_clicked(self, button) -> None:
        if (self._bay is None):
            return
        _LOGGER.debug(f"power {'off' if self._bay.powered_on else 'on'} {self._bay}")
        if self._bay.powered_on:
            asyncio.get_event_loop().create_task(self._bay.power_off())
        else:
            asyncio.get_event_loop().create_task(self._bay.power_on())

    def set_power(self, on:bool) -> None:
        if self._detached:
            return
        if on:
            self.child_power_button_image.set_from_icon_name('weather-clear-symbolic')
            self.child_power_button_label.set_text('Powered On')
        else:
            self.child_power_button_image.set_from_icon_name('weather-clear-night-symbolic')
            self.child_power_button_label.set_text('Standby')