##################################################
##         MX Remote Manager GUI                ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

import asyncio
import gi
import mx_remote as mx

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .Button import DeviceButton
from .Log import DeviceLog

class DeviceButtons(Gtk.Box):
    def __init__(self, device:mx.DeviceBase) -> None:
        Gtk.Box.__init__(self)
        self.device = device
        self.reboot_button = DeviceButton(label='Reboot', callback=self._reboot)
        self.append(self.reboot_button)
        self.log_button = DeviceButton(label='Device Log', callback=self._read_log)
        self.append(self.log_button)
        self.clear_log_button = DeviceButton(label='Clear Log', callback=self._clear_log)
        self.append(self.clear_log_button)
        self.mesh_promote_button = None
        self.mesh_remove_button = None
        self.update()

    @property
    def available(self) -> None:
        return self.device.online and not self.device.booting and not self.device.rebooting

    def update(self) -> None:
        self.reboot_button.set_enabled(self.available)
        self.reboot_button.set_spinner(not self.available)

        if self.device.features.mesh_member:
            if not self.device.is_mesh_master:
                if (self.mesh_promote_button is None):
                    self.mesh_promote_button = DeviceButton(label='Promote', callback=self._mesh_promote)
                    self.append(self.mesh_promote_button)
                self.mesh_promote_button.set_enabled(self.available)
            else:
                if (self.mesh_promote_button is not None):
                    self.remove(self.mesh_promote_button)
                    self.mesh_promote_button = None

            if (self.mesh_remove_button is None):
                self.mesh_remove_button = DeviceButton(label='Remove From Mesh', callback=self._mesh_remove)
                self.append(self.mesh_remove_button)
            self.mesh_remove_button.set_enabled(self.available)
        else:
            if (self.mesh_promote_button is not None):
                self.remove(self.mesh_promote_button)
                self.mesh_promote_button = None
            if (self.mesh_remove_button is not None):
                self.remove(self.mesh_remove_button)
                self.mesh_remove_button = None

    def _reboot(self) -> None:
        self.reboot_button.set_enabled(False)
        self.reboot_button.set_spinner(True)
        asyncio.get_event_loop().create_task(self.device.reboot())

    async def _read_log_async(self) -> None:
        log = await self.device.get_log()
        self.log_button.set_enabled(True)
        self.log_button.set_spinner(False)
        if log is not None:
            dialog = DeviceLog(device=self.device, data=log)
            dialog.show()

    def _read_log(self) -> None:
        self.log_button.set_enabled(False)
        self.log_button.set_spinner(True)
        asyncio.get_event_loop().create_task(self._read_log_async())

    def _clear_log(self) -> None:
        asyncio.get_event_loop().create_task(self.device.get_api('system/clearlog'))

    def _mesh_remove(self) -> None:
        asyncio.get_event_loop().create_task(self.device.mesh_remove())

    def _mesh_promote(self) -> None:
        asyncio.get_event_loop().create_task(self.device.mesh_promote())

