##################################################
##         MX Remote Manager GUI                ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

import gi
import mx_remote as mx
import logging
import time
from .mixins import AesPlayer
from .Player import Player

from .const import BASE_PATH

_LOGGER = logging.getLogger(__name__)

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Adw

@Gtk.Template(resource_path=f'/builder/control_bar.ui')
class ControlBar(Adw.Bin):
    __gtype_name__ = 'ControlBar'
    child_playback_label = Gtk.Template.Child('playback_label')
    child_playback_address = Gtk.Template.Child('playback_address')
    child_playback_rate = Gtk.Template.Child('playback_rate')
    child_play_stop_button = Gtk.Template.Child('play_stop_button')
    child_play_stop_image = Gtk.Template.Child('play_stop_image')
    child_record_button = Gtk.Template.Child('record_button')
    child_record_image = Gtk.Template.Child('record_image')
    child_playback_duration = Gtk.Template.Child('playback_duration')
    child_playback_stats = Gtk.Template.Child('playback_stats')
    _sequence_errors = 0
    _underruns = 0
    _recording = False

    def __init__(self) -> None:
        Adw.Bin.__init__(self)
        self._player = Player(player_stats_callback=self._on_stats_callback, recorder_stats_callback=self._on_recorder_stats_callback)
        self._player.register_player_state_callback(self._on_player_state_changed)
        self._player.register_recorder_state_callback(self._on_recorder_state_changed)
        self.child_playback_label.set_text('[player inactive]')
        self.child_play_stop_button.connect('clicked', self._on_play_stop_clicked)
        self.child_record_button.connect('clicked', self._on_record_clicked)

    def _on_recorder_stats_callback(self, kbytes_read:int, frames_read:int, samples_read:int, underruns:int, sequence_errors:int, codec:str, codec_rate:int, sample_rate:int, audio_channels:int) -> None:
        pass

    def _on_stats_callback(self, kbytes_read:int, frames_read:int, samples_read:int, underruns:int, sequence_errors:int, codec:str, codec_rate:int, sample_rate:int, audio_channels:int) -> None:
        if self._player.player_active:
            self._underruns += underruns
            self._sequence_errors += sequence_errors
            total_secs = int(time.time() - self._player.player_started)
            self.child_playback_duration.set_text(f"{int(total_secs / 60):02d}:{(total_secs % 60):02d}")
            stats = f'[net:{kbytes_read}Kb/s] [frames:{frames_read}/s]'
            if self._underruns > 0:
                stats += f' [under:{self._underruns}]'
            if self._sequence_errors > 0:
                stats += f' [seq: {self._sequence_errors}]'
            self.child_playback_stats.set_text(stats)
            self.child_playback_rate.set_text(f'[{codec} {audio_channels}ch {round(sample_rate/1000, 1)}kHz {codec_rate}Kb/s]')
        else:
            self.child_playback_stats.set_text('')
            self.child_playback_rate.set_text('')

    @property
    def player(self) -> AesPlayer:
        return self._player

    def _on_recorder_state_changed(self, player:AesPlayer) -> None:
        if self.player.recorder_active:
            self.child_record_image.set_from_icon_name('media-record')
        else:
            self.child_record_image.set_from_icon_name('media-record-symbolic')

    def _on_player_state_changed(self, player:AesPlayer) -> None:
        if not player.player_active:
            self.child_play_stop_image.set_from_icon_name('media-playback-start-symbolic')
            self.child_playback_duration.set_text(f"00:00")
            self.child_playback_stats.set_text("")
            self._sequence_errors = 0
            self._underruns = 0
        else:
            self.child_playback_label.set_text(self.player.player_source.user_name)
            self.child_playback_address.set_text(f"[{self.player.player_source.v2ip_source.audio.ip}:{self.player.player_source.v2ip_source.audio.port}]")
            self.child_play_stop_image.set_from_icon_name('media-playback-stop-symbolic')

    def _on_play_stop_clicked(self, button) -> None:
        if self.player.player_active:
            self.player.stop_player()
        else:
            self.player.reset_player()

    def _on_record_clicked(self, button) -> None:
        if self.player.recorder_active:
            self.player.stop_transmitter()
        else:
            self.player.start_transmitter()

    def on_device_update(self, dev:mx.DeviceBase) -> None:
        pass #self.player.update_source_address(dev.registry.local_ip)

    def set_local_ip(self, address:str) -> None:
        self.player.set_local_ip(address=address)

    def set_target_ip(self, address:str) -> None:
        self.player.target_address = address

    def set_sample_rate(self, rate:int) -> None:
        self.player.set_sample_rate(rate=rate)
