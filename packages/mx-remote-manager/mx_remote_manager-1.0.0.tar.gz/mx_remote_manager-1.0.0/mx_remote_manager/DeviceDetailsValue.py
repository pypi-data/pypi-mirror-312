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

@Gtk.Template(resource_path=f'/builder/device_details_label.ui')
class DeviceDetailsLabel(Gtk.Box):
    __gtype_name__ = 'device_details_label'
    child_device_label = Gtk.Template.Child("device_label")

    def __init__(self, label:str) -> None:
        Gtk.Box.__init__(self)
        self.child_device_label.set_text(f'{label}:')

@Gtk.Template(resource_path=f'/builder/device_details_value.ui')
class DeviceDetailsValue(Gtk.Box):
    __gtype_name__ = 'device_details_value'
    child_device_label = Gtk.Template.Child("device_details")

    def __init__(self, updater:callable) -> None:
        Gtk.Box.__init__(self)
        self._updater = updater
        self._label = ''
        self.child_device_label.set_selectable(True)
        # self.child_device_label.connect('clicked', self._copy_clipboard)

    def update(self, device:mx.DeviceBase):
        self.label = self._updater(device)

    @property
    def label(self) -> str:
        return self._label

    # def _copy_clipboard(self, _) -> None:
    #     if not '<' in self.label:
    #         import pyperclip
    #         pyperclip.copy(self.label)
    #         _LOGGER.info(f'copied "{self.label}" to clipboard')

    @label.setter
    def label(self, value:str) -> None:
        self._label = value
        self.child_device_label.set_markup(value)
