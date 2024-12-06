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
from gi.repository import Gtk, GObject, Gio

class SourceSelectItem(GObject.Object):
    __gtype_name__ = 'SourceSelectItem'

    def __init__(self, idx:int, bay:mx.BayBase):
        super().__init__()
        self.idx = idx
        self.bay = bay

    @GObject.Property
    def key(self) -> int:
        return self.idx

    @GObject.Property
    def value(self) -> mx.BayBase:
        return self.bay

    def getKey(self) -> int:
        return self.key

    def getValue(self) -> mx.BayBase:
        return self.value

class SourceSelectList(Gtk.Box):
    factory = Gtk.SignalListItemFactory()

    def __init__ (self) -> None:
        Gtk.Box.__init__(self)
        self.model = Gio.ListStore(item_type=SourceSelectItem)
        self._detached = False
        self._updating = False
        self.selected_device:mx.DeviceBase = None
        self.factory.connect("setup", self._on_factory_setup)
        self.factory.connect("bind", self._on_factory_bind)
        self.dropdown = Gtk.DropDown(model=self.model, factory=self.factory, hexpand=True)
        self.dropdown.set_property('margin-end', 10)
        self.dropdown.connect("notify::selected-item", self._on_selected_item_changed)
        self.append(self.dropdown)

    def on_detach(self) -> None:
        self._detached = True

    def set_device(self, device:mx.DeviceBase) -> None:
        if (self.selected_device == device):
            return
        _LOGGER.debug(f"device changed from {self.selected_device} to {device}")
        if (self.selected_device is not None):
            self.selected_device.unregister_callback(self._on_device_changed)
        self.selected_device = device
        if device is not None:
            self.selected_device.register_callback(self._on_device_changed)
        self._update_sources()

    def _update_sources(self) -> None:
        self._updating = True
        self.model.remove_all()
        if (self.selected_device is None):
            self._updating = False
            return
        idx = 0
        self.video_source = self.selected_device.first_output.video_source
        for _, source in self.selected_device.inputs.items():
            self.model.append(SourceSelectItem(idx=idx, bay=source))
            if (self.video_source == source):
                self.dropdown.set_selected(idx)
            idx += 1
        self._updating = False

    def _on_device_changed(self, device:mx.DeviceBase) -> None:
        video_source = self.selected_device.first_output.video_source
        if (self.video_source is None) or (self.video_source != video_source):
            self._update_sources()
   
    def _on_factory_setup(self, factory, list_item):
        list_item.set_child(Gtk.Label())

    def _on_factory_bind(self, factory, list_item):
        item:SourceSelectItem = list_item.get_item()
        list_item.get_child().set_text(item.bay.user_name)

    def _on_selected_item_changed(self, dropdown, _):
        if self._detached or self._updating or (self.selected_device is None) or (self.selected_device.first_output is None):
            return
        item:SourceSelectItem = dropdown.get_selected_item()
        if (item is None):
            return
        _LOGGER.debug(f"change source on {self.selected_device.first_output} to {item.bay}")
        asyncio.get_event_loop().create_task(self.selected_device.first_output.select_video_source(item.bay.bay))
