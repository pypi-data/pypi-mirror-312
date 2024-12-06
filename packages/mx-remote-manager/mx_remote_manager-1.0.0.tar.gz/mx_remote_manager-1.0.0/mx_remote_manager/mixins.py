##################################################
##         MX Remote Manager GUI                ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

from abc import ABC, abstractmethod
import mx_remote as mx

class AesPlayer(ABC):
    _player_source_callbacks:list[callable] = []
    _player_state_callbacks:list[callable] = []
    _recorder_state_callbacks:list[callable] = []

    @property
    @abstractmethod
    def target_address(self) -> str:
        pass

    @target_address.setter
    @abstractmethod
    def target_address(self, address:str) -> None:
        pass

    @property
    @abstractmethod
    def player_active(self) -> bool:
        pass

    @property
    @abstractmethod
    def recorder_active(self) -> bool:
        pass

    @property
    @abstractmethod
    def player_source(self) -> mx.BayBase|None:
        pass

    @abstractmethod
    def start_player(self, bay:mx.BayBase) -> bool:
        pass

    @abstractmethod
    def reset_player(self) -> None:
        pass

    @abstractmethod
    def stop_player(self) -> None:
        pass

    @abstractmethod
    def start_transmitter(self) -> bool:
        pass

    @abstractmethod
    def stop_transmitter(self) -> None:
        pass

    def register_player_source_callback(self, callback:callable) -> None:
        self._player_source_callbacks.append(callback)

    def unregister_player_source_callback(self, callback:callable) -> None:
        self._player_source_callbacks.remove(callback)

    def notify_player_source_callback(self, source:mx.BayBase) -> None:
        for cb in self._player_source_callbacks:
            cb(source)

    def register_player_state_callback(self, callback:callable) -> None:
        self._player_state_callbacks.append(callback)

    def unregister_player_state_callback(self, callback:callable) -> None:
        self._player_state_callbacks.remove(callback)

    def notify_player_state_callback(self, source:mx.BayBase) -> None:
        for cb in self._player_state_callbacks:
            cb(self)

    def register_recorder_state_callback(self, callback:callable) -> None:
        self._recorder_state_callbacks.append(callback)

    def unregister_recorder_state_callback(self, callback:callable) -> None:
        self._recorder_state_callbacks.remove(callback)

    def notify_recorder_state_callback(self, source:mx.BayBase) -> None:
        for cb in self._recorder_state_callbacks:
            cb(self)

    @abstractmethod
    def set_local_ip(self, address:str) -> None:
        pass

    @abstractmethod
    def set_sample_rate(self, rate:int) -> None:
        pass
