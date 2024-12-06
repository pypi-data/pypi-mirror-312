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

_LOGGER = logging.getLogger(__name__)

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject, Gio

class EdidProfileSelectItem(GObject.Object):
    __gtype_name__ = 'EdidProfileSelectItem'

    def __init__(self, profile:mx.EdidProfile):
        super().__init__()
        self.profile = profile

    @GObject.Property
    def key(self) -> int:
        return self.profile.value

    @GObject.Property
    def value(self) -> str:
        return str(self.profile)

    def getKey(self) -> int:
        return self.key

    def getValue(self) -> str:
        return self.value

class EdidProfileSelectList(Gtk.Box):
    factory = Gtk.SignalListItemFactory()

    def __init__ (self) -> None:
        Gtk.Box.__init__(self)
        self.model = Gio.ListStore(item_type=EdidProfileSelectItem)
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
        if (self.selected_device is not None):
            self.selected_device.unregister_callback(self._on_device_changed)
        self.selected_device = device
        if device is not None:
            self.selected_device.register_callback(self._on_device_changed)
        self._update_profile()

    def nb_master_sinks(self) -> int:
        master = self.selected_device.mesh_master
        if (master is None):
            return 0
        return len(master.outputs)

    def _update_profile(self) -> None:
        self._updating = True
        self.model.remove_all()
        if (self.selected_device is None):
            self._updating = False
            return
        idx = 0
        self.selected_profile = self.selected_device.first_input.edid_profile
        for key, _ in mx.EdidProfile.values(self.nb_master_sinks()).items():
            profile = EdidProfileSelectItem(profile=mx.EdidProfile(key))
            self.model.append(profile)
            if (self.selected_profile == profile.profile):
                self.dropdown.set_selected(idx)
            idx += 1
        self._updating = False

    def _on_device_changed(self, device:mx.DeviceBase) -> None:
        if self.selected_profile != self.selected_device.first_input.edid_profile:
            self._update_profile()
   
    def _on_factory_setup(self, factory, list_item):
        list_item.set_child(Gtk.Label())

    def _on_factory_bind(self, factory, list_item):
        item:EdidProfileSelectItem = list_item.get_item()
        list_item.get_child().set_text(item.value)

    def _on_selected_item_changed(self, dropdown, _):
        if self._detached or self._updating or (self.selected_device is None) or (self.selected_device.first_input is None):
            return
        item:EdidProfileSelectItem = dropdown.get_selected_item()
        if (item is None):
            return
        _LOGGER.debug(f"change edid profile on {self.selected_device.first_input} to {item.value}")
        asyncio.get_event_loop().create_task(self.selected_device.first_input.select_edid_profile(profile=item.profile))
