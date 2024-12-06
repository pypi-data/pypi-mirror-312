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
from .mixins import AesPlayer
from .const import BASE_PATH

# @Gtk.Template(filename=f'{BASE_PATH}/builder/source.ui')
@Gtk.Template(resource_path=f'/builder/source.ui')
class SourceEntry(Gtk.Box):
    __gtype_name__ = 'Source'
    child_source_button = Gtk.Template.Child('source_button')
    child_device_label = Gtk.Template.Child('device_label')
    child_device_info = Gtk.Template.Child('device_info')
    child_source_icon = Gtk.Template.Child('source_icon')

    def __init__(self, bay:mx.BayBase, player:AesPlayer, tx_source:bool) -> None:
        Gtk.Box.__init__(self)
        self.bay = bay
        self._player = player
        self.child_source_button.connect('clicked', self._on_click)
        self.tx_source = tx_source
        if tx_source:
            self.child_device_label.set_text('Local -> Sink')
            self.child_device_info.set_text(f'{self._player.target_address}:50022')
        else:
            self._player.register_player_source_callback(self._on_source_changed)
            self.child_device_label.set_text(bay.user_name)
            if bay.v2ip_source is not None:
                self.child_device_info.set_text(f'{bay.v2ip_source.audio.ip}:{bay.v2ip_source.audio.port}')
                self.set_selected((player.player_source is not None) and (player.player_source.v2ip_source.audio == self.bay.v2ip_source.audio))

    def set_margin_top(self, margin:int) -> None:
        self.child_source_button.set_property('margin-top', margin)

    def _on_source_changed(self, source:mx.BayBase) -> None:
        self.set_selected((source is not None) and (source.v2ip_source.audio == self.bay.v2ip_source.audio))

    def set_selected(self, selected:bool) -> None:
        if selected:
            self.child_source_button.add_css_class('suggested-action')
        else:
            self.child_source_button.remove_css_class('suggested-action')

    def _on_click(self, button) -> None:
        if self.tx_source:
            self._player.start_transmitter()
            asyncio.get_event_loop().create_task(self.bay.select_audio_source(self._player.target_address))
        else:
            self._player.start_player(self.bay)
