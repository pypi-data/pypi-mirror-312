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
from .DeviceDetails import DeviceDetailsTabs
from .mixins import AesPlayer

_LOGGER = logging.getLogger(__name__)

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GObject

class DeviceItem(Gtk.Box):
    '''entry in the list of devices'''
    __gtype_name__ = 'DeviceItem'
    text = GObject.Property(type=GObject.TYPE_STRING, default="")

    def __init__(self, tab:'DevicesTab', dev:mx.DeviceBase) -> None:
        Gtk.Box.__init__(self)
        self.dev = dev
        self.tab = tab
        self.label = Gtk.Label(label='')
        self.label.set_property('margin-top', 3)
        self.label.set_property('margin-start', 10)
        self.label.set_property('halign', 'start')
        self.mesh_master = None
        self.append(self.label)
        self.update()
        self.dev.register_callback(self._on_device_changed)

    def update(self) -> None:
        label = self.dev.serial if self.tab.show_serials else self.dev.name
        if not self.dev.online:
            label = f'<i>{label}</i>'
        self.label.set_markup(label)
        self.set_property('text', label)

        if self.dev.is_mesh_master:
            if self.mesh_master is None:
                self.mesh_master = Gtk.Image.new_from_icon_name('starred-symbolic')
                self.mesh_master.set_property('icon_size', 1)
                self.mesh_master.set_property('margin-start', 5)
                self.mesh_master.set_property('halign', 'end')
                self.append(self.mesh_master)
        else:
            if self.mesh_master is not None:
                self.remove(self.mesh_master)
                self.mesh_master = None

    def __del__(self) -> None:
        self.dev.unregister_callback(self._on_device_changed)

    def _on_device_changed(self, device:mx.DeviceBase) -> None:
        self.update()

class ScanSpinner(Gtk.Spinner):
    '''show a spinner while scanning for devices and the list of device is empty'''
    __gtype_name__ = 'ScanSpinner'
    text = GObject.Property(type=GObject.TYPE_STRING, default="")

@Gtk.Template(resource_path=f'/builder/devices.ui')
class DevicesTab(Gtk.Box):
    '''the device information tab'''
    __gtype_name__ = 'DevicesTab'
    child_container = Gtk.Template.Child('container')
    child_list_devices = Gtk.Template.Child('list_devices')

    _devices: dict[mx.MxrDeviceUid, DeviceItem] = {}
    devices_store = Gio.ListStore()
    _spinner = None
    _show_serials = False
    _details:DeviceDetailsTabs = None

    def __init__(self, player:AesPlayer) -> None:
        Gtk.Box.__init__(self)
        def _create_device_list_item(item) -> Gtk.Widget:
            # if isinstance(item, DeviceItem):
            #     return item.label
            return item

        self.sort_model = Gtk.SortListModel.new(self.devices_store,
                                           Gtk.StringSorter.new(Gtk.PropertyExpression.new(DeviceItem, None, "text")))
        self.child_list_devices.bind_model(self.sort_model, _create_device_list_item)
        self._player = player
        self.mxr:mx.Remote = None
        self._spinner = ScanSpinner()
        self.devices_store.append(self._spinner)
        self._spinner.start()

    @property
    def show_serials(self) -> bool:
        return self._show_serials

    @show_serials.setter
    def show_serials(self, serials:bool) -> None:
        self._show_serials = serials
        for ptr in range(self.devices_store.get_n_items()):
            self.devices_store.get_item(ptr).update()

    @Gtk.Template.Callback()
    def on_device_selected(self, list, device):
        if (device is None):
            return
        model_item = self.sort_model[device.get_index()]
        if isinstance(model_item, ScanSpinner):
            return
        device:mx.DeviceBase = model_item.dev
        if self._details is not None:
            self._details.on_detach()
        self._details = DeviceDetailsTabs(player=self._player, device=device)
        self.child_container.set_end_child(self._details)

    def _add_device(self, item:DeviceItem) -> None:
        if self._spinner is not None:
            self.devices_store.remove_all()
            self._spinner = None
        self.devices_store.append(item)

    def on_device_update(self, dev:mx.DeviceBase) -> None:
        if not dev.configuration_complete:
            return
        if dev.remote_id not in self._devices.keys():
            item = DeviceItem(tab=self, dev=dev)
            self._devices[dev.remote_id] = item
            self._add_device(item=item)