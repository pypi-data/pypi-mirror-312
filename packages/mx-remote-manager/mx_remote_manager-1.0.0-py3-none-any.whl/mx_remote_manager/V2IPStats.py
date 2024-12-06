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
gi.require_version('Adw', '1')
from gi.repository import Adw

from .DeviceDetailsValue import DeviceDetailsValue

class DeviceDecoderStats(Adw.ExpanderRow):
    def __init__(self, device:mx.DeviceBase) -> None:
        self.device = device
        Adw.ExpanderRow.__init__(self, title=self._decoder_status())
        self._SINK_V2IP_VALUES = {
            'Video Total': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.rx_per_minute.video_total) if self._has_values() else '')),
            'Video Dropped': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.rx_per_minute.video_dropped) if self._has_values() else '')),
            'Video Sequence Errors': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.rx_per_minute.video_sequence_errors) if self._has_values() else '')),
            'Audio Total': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.rx_per_minute.audio_total) if self._has_values() else '')),
            'Audio Dropped': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.rx_per_minute.audio_dropped) if self._has_values() else '')),
            'Audio Sequence Errors': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.rx_per_minute.audio_sequence_errors) if self._has_values() else '')),
            'Ancillary Total': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.rx_per_minute.anc_total) if self._has_values() else '')),
            'Ancillary Dropped': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.rx_per_minute.anc_dropped) if self._has_values() else '')),
            'Ancillary Sequence Errors': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.rx_per_minute.anc_sequence_errors) if self._has_values() else '')),
            'Watchdog Timeouts': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.rx_per_minute.wdt_timeout) if self._has_values() else '')),
        }

        for title, value in self._SINK_V2IP_VALUES.items():
            ar = Adw.ActionRow(title=title)
            value.set_property('margin-top', 0)
            value.set_property('margin-bottom', 0)
            value.set_property('halign', 'end')
            ar.add_suffix(value)
            self.add_row(ar)

        self.update_values()

    def _has_values(self) -> bool:
        return not self.device.first_output.decoder_disabled and self.device.v2ip_stats is not None

    def update_values(self) -> None:
        self.set_title(self._decoder_status())
        for _, item in self._SINK_V2IP_VALUES.items():
            if isinstance(item, DeviceDetailsValue):
                item.update(self.device)

    def _decoder_status(self) -> str:
        if self.device.is_v2ip and self.device.has_local_sink:
            if self.device.first_output.decoder_disabled:
                return 'Inactive'
            elif self.device.v2ip_stats is not None:
                return str(self.device.v2ip_stats.rx_per_minute.decoder_state)
            return 'Unknown'
        return 'Not Available'

class DeviceEncoderStats(Adw.ExpanderRow):
    def __init__(self, device:mx.DeviceBase) -> None:
        self.device = device
        Adw.ExpanderRow.__init__(self, title=self._encoder_status())
        self._SOURCE_V2IP_VALUES = {
            'Video': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.tx_per_minute.video) if self._has_values() else '')),
            'Audio': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.tx_per_minute.audio) if self._has_values() else '')),
            'Ancillary': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.tx_per_minute.anc) if self._has_values() else '')),
            'Stream Down': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.tx_per_minute.stream_down) if self._has_values() else '')),
            'Overflow': DeviceDetailsValue(updater=(lambda dev: str(dev.v2ip_stats.tx_per_minute.overflow) if self._has_values() else '')),
        }

        for title, value in self._SOURCE_V2IP_VALUES.items():
            ar = Adw.ActionRow(title=title)
            value.set_property('margin-top', 0)
            value.set_property('margin-bottom', 0)
            value.set_property('halign', 'end')
            ar.add_suffix(value)
            self.add_row(ar)

        self.update_values()

    def _has_values(self) -> bool:
        return not self.device.first_input.encoder_disabled and self.device.v2ip_stats is not None

    def update_values(self) -> None:
        self.set_title(self._encoder_status())
        for _, item in self._SOURCE_V2IP_VALUES.items():
            if isinstance(item, DeviceDetailsValue):
                item.update(self.device)

    def _encoder_status(self) -> str:
        if self.device.is_v2ip and self.device.has_local_source:
            if self.device.first_input.encoder_disabled:
                return 'Inactive'
            elif (self.device.v2ip_stats is not None):
                if (self.device.v2ip_stats.tx_per_minute.video > 0):
                    return 'Transmitting'
                return 'Not Transmitting'
            return 'Unknown'
        return 'Not Available'
