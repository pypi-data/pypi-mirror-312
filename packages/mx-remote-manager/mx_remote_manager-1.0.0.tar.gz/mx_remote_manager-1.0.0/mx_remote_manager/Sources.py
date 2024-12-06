##################################################
##         MX Remote Manager GUI                ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

import gi
import mx_remote as mx
import logging

from .const import BASE_PATH
from .mixins import AesPlayer
from .Source import SourceEntry

_LOGGER = logging.getLogger(__name__)

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio

# @Gtk.Template(filename=f'{BASE_PATH}/builder/sources.ui')
@Gtk.Template(resource_path=f'/builder/sources.ui')
class SourcesTab(Gtk.Box):
    __gtype_name__ = 'SourcesTab'
    devices:dict[mx.MxrDeviceUid, SourceEntry] = {}
    sources_store = Gio.ListStore()
    child_container = Gtk.Template.Child('container')

    def __init__(self, player:AesPlayer) -> None:
        Gtk.Box.__init__(self)
        self._player = player
        self._spinner = Gtk.Spinner()
        self.child_container.attach(self._spinner, 1, 0, 2, 2)
        self._spinner.start()

    def on_device_update(self, dev:mx.DeviceBase) -> None:
        if not dev.configuration_complete:
            return
        if not dev.is_v2ip:
            return
        if (self._spinner is not None):
            self.child_container.remove(self._spinner)
            self._spinner = None
        if dev.remote_id not in self.devices.keys():
            if dev.first_input is not None:
                entry = SourceEntry(bay=dev.first_input, player=self._player, tx_source=False)
                entry.set_margin_top(20)
                entry.set_hexpand(True)
                self.child_container.attach(entry, len(self.devices) % 4, int(len(self.devices) / 4), 1, 1)
                self.devices[dev.remote_id] = entry
                self.sources_store.append(entry)
            else:
                self.devices[dev.remote_id] = False
