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
import time
from typing import Any

_LOGGER = logging.getLogger(__name__)

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from .BayHide import BayHiddenButton
from .BayName import BayName
from .DeviceButtons import DeviceButtons
from .DeviceDetailsValue import DeviceDetailsValue, DeviceDetailsLabel
from .DeviceStatus import DeviceStatusValue
from .EdidProfile import EdidProfileSelectList
from .PowerStatus import DevicePowerStatus
from .SourceSelect import SourceSelectList
from .Source import SourceEntry
from .V2IPStats import DeviceEncoderStats, DeviceDecoderStats
from .mixins import AesPlayer
from .const import BASE_PATH

@Gtk.Template(resource_path=f'/builder/device_details_tab.ui')
class DeviceDetailsTab(Gtk.Box):
    __gtype_name__ = 'device_details_tab_tpl'
    child_device_details = Gtk.Template.Child('device_details')

    def __init__(self, player:AesPlayer, values:dict[str, Any]) -> None:
        Gtk.Box.__init__(self)
        self._player = player
        self._values:dict[str, Any] = {}
        self._buttons:list[Gtk.Widget] = []
        self._dummy = None
        self.append_values(values=values)

    def append_values(self, values:dict[str, Any]) -> None:
        row = len(self._values) + len(self._buttons)
        for name, value in values.items():
            self.child_device_details.attach(DeviceDetailsLabel(label=name), 0, row, 1, 1)
            self.child_device_details.attach(value, 1, row, 1, 1)
            self._values[name] = value
            row += 1

    def attach_widget(self, widget:Gtk.Widget) -> None:
        self.child_device_details.attach(widget, 1, len(self._values) + len(self._buttons), 1, 1)
        self._buttons.append(widget)

    def detach_widget(self, widget:Gtk.Widget) -> None:
        if widget in self._buttons:
            self.child_device_details.remove(widget)
            self._buttons.remove(widget)

class DeviceDetailsTabs(Gtk.Notebook):
    LABEL_NOT_AVAILABLE = 'Not Available'

    def __init__(self, player:AesPlayer, device:mx.DeviceBase) -> None:
        Gtk.Notebook.__init__(self)
        self.detached = False
        self.device = device
        self._player = player
        self.play_button = None
        self.source_play_button = None
        self.tx_button = None
        self.stats_enabled = 0

        self.source_select = SourceSelectList()
        self.edid_profile_select = EdidProfileSelectList()
        self.power_button = DevicePowerStatus()
        self.decoder_stats = DeviceDecoderStats(device=device)
        self.encoder_stats = DeviceEncoderStats(device=device)
        self.source_hide = BayHiddenButton(bay=device.first_input)
        self.sink_hide = BayHiddenButton(bay=device.first_output)
        self.buttons = DeviceButtons(device=device)
        self.source_name = BayName(bay=device.first_input)
        self.sink_name = BayName(bay=device.first_output)
        self.device_status = DeviceStatusValue(status=device.status)
        self.source_status = DeviceStatusValue(status=device.first_input.status if device.has_local_source else mx.DeviceStatus.OFFLINE)
        self.sink_status = DeviceStatusValue(status=device.first_output.status if device.has_local_sink else mx.DeviceStatus.OFFLINE)

        self._GENERAL_VALUES = {
            'Status': self.device_status,
            'Name': DeviceDetailsValue(updater=(lambda dev: dev.name if dev is not None else '')),
            'Serial': DeviceDetailsValue(updater=(lambda dev: dev.serial if dev is not None else '')),
            'Model': DeviceDetailsValue(updater=(lambda dev: dev.model_name if dev is not None else '')),
            'UID': DeviceDetailsValue(updater=(lambda dev: str(dev.remote_id) if dev is not None else '')),
            'Firmware': DeviceDetailsValue(updater=(lambda dev: dev.version if dev is not None else '')),
            'Address': DeviceDetailsValue(updater=(lambda dev: f'<a href="http://{dev.address}/">{dev.address}</a>' if dev is not None else '')),
            'Mesh Status': DeviceDetailsValue(updater=self._mesh_status),
            'Temperature': DeviceDetailsValue(updater=self._temperatures),
            'Network Speed': DeviceDetailsValue(updater=self._uplink_speed),
            'Network Status': DeviceDetailsValue(updater=self._uplink_status),
            'IGMP Querier': DeviceDetailsValue(updater=self._uplink_querier),
        }
        self._SINK_VALUES = {
            'Status': self.sink_status,
            'Video Signal': DeviceDetailsValue(updater=(lambda dev: dev.first_output.signal_type if (dev is not None) else '')),
            'Power': self.power_button,
            'Name': self.sink_name,
            'Visibility': self.sink_hide,
            'Video Source': self.source_select,
        }
        self._SINK_V2IP_VALUES = {
            'Receiver': self.decoder_stats,
        }
        self._SOURCE_VALUES = {
            'Status': self.source_status,
            'Video Signal': DeviceDetailsValue(updater=(lambda dev: dev.first_input.signal_type if (dev is not None) else '')),
            'Name': self.source_name,
            'Visibility': self.source_hide,
            'EDID Profile': self.edid_profile_select,
            'Control Method': DeviceDetailsValue(updater=(lambda dev: str(dev.first_input.rc_type) if (dev is not None) else '')),
        }
        self._SOURCE_V2IP_VALUES = {
            'Video Address': DeviceDetailsValue(updater=self._v2ip_source_video),
            'Audio Address': DeviceDetailsValue(updater=self._v2ip_source_audio),
            'Transmit Rate': DeviceDetailsValue(updater=(lambda dev: f"{dev.v2ip_details.tx_rate}0 MBit/s" if dev is not None else '')),
            'Transmitter': self.encoder_stats,
        }

        self._device_page = DeviceDetailsTab(player=player, values = self._GENERAL_VALUES)
        self._device_page.attach_widget(self.buttons)
        label = Gtk.Label()
        label.set_label('Device')
        self.append_page(self._device_page, label)

        if device.has_local_sink:
            self._sink_page = DeviceDetailsTab(player=player, values = self._SINK_VALUES)
            label = Gtk.Label()
            label.set_label('Sink')
            self.append_page(self._sink_page, label)

            if device.is_v2ip:
                self._sink_page.append_values(values=self._SINK_V2IP_VALUES)
                source = device.first_output.video_source
                if (source is not None) and source.device.is_v2ip and source.device.has_local_source and (source.v2ip_source is not None):
                    self.source_play_button = SourceEntry(bay=source, player=self._player, tx_source=False)
                    self._sink_page.attach_widget(self.source_play_button)

                self.tx_button = SourceEntry(bay=device.first_output, player=self._player, tx_source=True)
                self._sink_page.attach_widget(self.tx_button)
        else:
            self._sink_page = None

        if device.has_local_source:
            self._source_page = DeviceDetailsTab(player=player, values = self._SOURCE_VALUES)
            label = Gtk.Label()
            label.set_label('Source')
            self.append_page(self._source_page, label)

            if device.is_v2ip:
                self._source_page.append_values(values=self._SOURCE_V2IP_VALUES)
                self.play_button = SourceEntry(bay=device.first_input, player=self._player, tx_source=False)
                self._source_page.attach_widget(self.play_button)
        else:
            self._source_page = None

        device.register_callback(self._update_device)
        if device.has_local_sink:
            device.first_output.register_callback(self._update_bay)
        if device.has_local_source:
            device.first_input.register_callback(self._update_bay)

        self._update_device(device=device)

    def on_detach(self) -> None:
        self.detached = True
        self.edid_profile_select.on_detach()
        self.source_select.on_detach()
        self.power_button.on_detach()
        _LOGGER.debug(f'stopping stats dump from {self.device}')
        self._read_stats(enable=False)
        self.device.unregister_callback(self._update_device)
        if self.device.has_local_sink:
            self.device.first_output.unregister_callback(self._update_bay)
        if self.device.has_local_source:
            self.device.first_input.unregister_callback(self._update_bay)

    def __del__(self) -> None:
        self.on_detach()

    def _read_stats(self, enable:bool) -> None:
        asyncio.get_event_loop().create_task(self.device.read_stats(enable=enable))

    def _uplink(self, device:mx.DeviceBase) -> mx.NetworkPortStatus|None:
        for _, port in device.network_status.items():
            if port.name == 'FPGA':
                continue
            return port
        return None

    def _uplink_speed(self, device:mx.DeviceBase) -> str:
        port = self._uplink(device=device)
        if (port is not None):
            return str(port.link_speed)
        return 'Unknown'

    def _uplink_querier(self, device:mx.DeviceBase) -> str:
        port = self._uplink(device=device)
        if (port is not None):
            return port.querier
        return 'Unknown'

    def _uplink_status(self, device:mx.DeviceBase) -> str:
        port = self._uplink(device=device)
        if (port is not None):
            return str(port.errors)
        return 'Unknown'

    def _temperatures(self, device:mx.DeviceBase) -> str:
        if device is None:
            return ""
        rv = ""
        for label, temperature in device.temperatures.items():
            if rv != "":
                rv += ", "
            rv += f"{label}: {temperature}°C"
        return rv

    def _mesh_status(self, device:mx.DeviceBase) -> str:
        if device is None:
            return ""
        if device.is_mesh_master:
            return "Master"
        if device.features.mesh_member:
            master = device.mesh_master
            if (master is None):
                return f'Member - Master Offline'
            return f"Member of {master.serial} ({master.name})"
        return "Unregistered"

    def _v2ip_source_video(self, device:mx.DeviceBase) -> str:
        if device.is_v2ip and device.has_local_source:
            return f"{device.v2ip_source_local.video.ip}:{device.v2ip_source_local.video.port}"
        return self.LABEL_NOT_AVAILABLE

    def _v2ip_source_audio(self, device:mx.DeviceBase) -> str:
        if device.is_v2ip and device.has_local_source:
            return f"{device.v2ip_source_local.audio.ip}:{device.v2ip_source_local.audio.port}"
        return self.LABEL_NOT_AVAILABLE

    def _update_bay(self, bay:mx.BayBase) -> None:
        self._update_device(None)

    def _update_values(self, items:dict[str, Any]) -> None:
        for _, item in items.items():
            if isinstance(item, DeviceDetailsValue):
                item.update(self.device)

    def _update_device(self, device:mx.DeviceBase) -> None:
        if (self.device != device) or self.detached:
            return
        self.power_button.set_bay(bay=self.device.first_output if self.device.has_local_sink else None)
        self.source_select.set_device(device=(self.device if self.device.is_v2ip else None))
        self.edid_profile_select.set_device(device=self.device)
        self.decoder_stats.update_values()
        self.encoder_stats.update_values()
        self.buttons.update()
        self.device_status.update(device.status)
        self._update_values(items=self._GENERAL_VALUES)
        self._update_values(items=self._SINK_VALUES)
        self._update_values(items=self._SOURCE_VALUES)
        if device.has_local_sink:
            self.sink_status.update(status=device.first_output.status)
        if device.has_local_source:
            self.source_status.update(status=device.first_input.status)
        if self.device.is_v2ip:
            if self.device.has_local_sink:
                self._update_values(items=self._SINK_V2IP_VALUES)
            if self.device.has_local_source:
                self._update_values(items=self._SOURCE_V2IP_VALUES)
        if (time.time() - self.stats_enabled) > 45:
            _LOGGER.debug(f'request stats updates from {self.device}')
            self.stats_enabled = time.time()
            self._read_stats(enable=True)
