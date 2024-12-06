##################################################
##         MX Remote Manager GUI                ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

import aes3tool as ae
import asyncio
import logging
from .mixins import AesPlayer
from .const import DEFAULT_TX_ADDRESS
import mx_remote as mx
import time

_LOGGER = logging.getLogger(__name__)

class Player(AesPlayer):
    player_started = 0
    receiver:ae.Aes3Receiver = None
    transmitter:ae.Aes3Transmitter = None
    player_config = ae.Aes3ToolConfig()
    recorder_config = ae.Aes3ToolConfig()
    source_address:str = None
    _target_address:str = DEFAULT_TX_ADDRESS
    bay:mx.BayBase = None

    def __init__(self, player_stats_callback:callable, recorder_stats_callback:callable) -> None:
        super().__init__()
        self.player_config.stats_callback = player_stats_callback
        # self.player_config.detect_bitstreams = False
        self.recorder_config.stats_callback = recorder_stats_callback

    @property
    def player_active(self) -> bool:
        return (self.receiver is not None)

    @property
    def recorder_active(self) -> bool:
        return (self.transmitter is not None)

    def set_local_ip(self, address:str) -> None:
        if (self.source_address != address):
            self.source_address = address
            if (self.receiver is not None):
                self.reset_player()
            if (self.transmitter is not None):
                self.reset_transmitter()

    @property
    def target_address(self) -> str:
        return self._target_address

    @target_address.setter
    def target_address(self, address:str) -> None:
        if (self._target_address != address):
            self._target_address = address
            if (self.transmitter is not None):
                self.reset_transmitter()

    def set_sample_rate(self, rate:int) -> None:
        if (self.player_config.audio_sample_rate != rate):
            self.player_config.audio_sample_rate = rate
            if (self.transmitter is not None):
                self.reset_transmitter()

    def start_transmitter(self) -> bool:
        self.stop_transmitter()
        _LOGGER.debug(f"start audio transmitter to {self.target_address}")
        self.transmitter = ae.Aes3Transmitter(config=self.recorder_config, target_ip=self.target_address, interface_ip=self.source_address)
        asyncio.get_event_loop().create_task(self.transmitter.start())
        self.notify_recorder_state_callback(self)

    def stop_transmitter(self) -> None:
        if (self.transmitter is not None):
            _LOGGER.debug(f"stopping audio transmitter")
            asyncio.get_event_loop().create_task(self.transmitter.close())
            self.transmitter = None
            self.notify_recorder_state_callback(self)

    def start_player(self, bay:mx.BayBase) -> bool:
        self.stop_player()
        if bay is None:
            return False
        self.bay = bay
        _LOGGER.debug(f"starting audio player for {self.bay}")
        self.receiver = ae.Aes3Receiver(config=self.player_config, source_ip=bay.v2ip_source.audio.ip, interface_ip=self.source_address)
        asyncio.get_event_loop().create_task(self.receiver.start())
        self.player_started = time.time()
        self.notify_player_source_callback(bay)
        self.notify_player_state_callback(self)
        return True

    def stop_player(self) -> None:
        if self.player_active:
            _LOGGER.debug(f"stopping audio player for {self.bay}")
            asyncio.get_event_loop().create_task(self.receiver.close())
            self.receiver = None
            self.notify_player_source_callback(None)
            self.notify_player_state_callback(self)

    def reset_player(self) -> None:
        bay = self.bay
        self.stop_player()
        self.start_player(bay=bay)

    def reset_transmitter(self) -> None:
        self.stop_transmitter()
        self.start_transmitter()

    @property
    def player_source(self) -> mx.BayBase|None:
        return self.bay
