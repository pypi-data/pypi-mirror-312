##################################################
##         MX Remote Manager GUI                ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

import asyncio
import gi
import logging
import mx_remote as mx

_LOGGER = logging.getLogger(__name__)

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject, Gio, Adw

class NetworkInterfaceItem(GObject.Object):
    __gtype_name__ = 'NetworkInterfaceItem'

    def __init__(self, idx:int, address:str):
        super().__init__()
        self.idx = idx
        self.address = address

    @GObject.Property
    def key(self) -> int:
        return self.idx

    @GObject.Property
    def value(self) -> str:
        return self.address

    def getKey(self) -> int:
        return self.key

    def getValue(self) -> str:
        return self.value

class NetworkInterfaceList:
    model = Gio.ListStore(item_type=NetworkInterfaceItem)
    factory = Gtk.SignalListItemFactory()

    def __init__ (self, ip:str, changed_callback:callable) -> None:
        self._callback = changed_callback
        self.factory.connect("setup", self._on_factory_setup)
        self.factory.connect("bind", self._on_factory_bind)
        self.dropdown = Gtk.DropDown(model=self.model, factory=self.factory, hexpand=True)

        idx = 0
        for address in mx.mxr_valid_addresses():
            self.model.append(NetworkInterfaceItem(idx=idx, address=address))
            if (ip == address):
                self.dropdown.set_selected(idx)
            idx += 1

        self.action_row = Adw.ActionRow.new()
        self.action_row.add_prefix(
            widget=Gtk.Image.new_from_icon_name(
                icon_name='network-idle'
            ),
        )
        self.action_row.set_title(title='Network Interface')
        self.action_row.set_subtitle(subtitle='Network that\'s connected to OneIP')
        self.action_row.add_suffix(widget=self.dropdown)
        self.dropdown.connect("notify::selected-item", self._on_selected_item_changed)

    def _on_factory_setup(self, factory, list_item):
        list_item.set_child(Gtk.Label())

    def _on_factory_bind(self, factory, list_item):
        item:NetworkInterfaceItem = list_item.get_item()
        list_item.get_child().set_text(item.address)

    def _on_selected_item_changed(self, dropdown, _):
        item:NetworkInterfaceItem = dropdown.get_selected_item()
        if (item is None):
            return
        self._callback(address=item.address)

class NetworkInterfaceMulticast:
    def __init__ (self, mxr:mx.Remote) -> None:
        self._remote = mxr
        box = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        button1 = Gtk.ToggleButton.new_with_label("Broadcast")
        button1.connect("toggled", self._on_button1)
        box.append(button1)

        button2 = Gtk.ToggleButton.new_with_label("Multicast")
        button2.set_group(button1)
        button2.set_active(True)
        button2.connect("toggled", self._on_button2)
        box.append(button2)

        self.action_row = Adw.ActionRow.new()
        self.action_row.add_prefix(
            widget=Gtk.Image.new_from_icon_name(
                icon_name='network-wired'
            ),
        )
        self.action_row.set_title(title='Multicast')
        self.action_row.set_subtitle(subtitle='Communicate using multicast or broadcast (fallback)')
        self.action_row.add_suffix(widget=box)

    def _on_button1(self, button) -> None:
        if button.get_active():
            asyncio.get_event_loop().create_task(self._remote.update_config(broadcast=True))

    def _on_button2(self, button) -> None:
        if button.get_active():
            asyncio.get_event_loop().create_task(self._remote.update_config(broadcast=False))

class NetworkTxAddress:
    def __init__ (self, ip:str, changed_callback:callable) -> None:
        self._callback = changed_callback

        self.action_row = Adw.EntryRow.new()
        self.action_row.set_title(title="Multicast Destination Address")
        self.action_row.add_prefix(
            widget=Gtk.Image.new_from_icon_name(
                icon_name='preferences-system-network'
            ),
        )
        self.action_row.set_show_apply_button(show_apply_button=True)
        self.action_row.set_activates_default(activates=True)
        self.action_row.connect('apply', self.on_apply_button_pressed)
        self.action_row.set_text(ip)

    def on_apply_button_pressed(self, entry_row):
        self._callback(entry_row.get_text())
