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

class BayHiddenButton(Gtk.Box):
    def __init__(self, bay:mx.BayBase) -> None:
        Gtk.Box.__init__(self)
        self.bay = bay
        if (bay is not None):
            hide_button = Gtk.ToggleButton.new_with_label('Hidden')
            hide_button.set_property('margin-start', 5)
            hide_button.set_property('margin-end', 5)
            visible_button = Gtk.ToggleButton.new_with_label('Visible')
            visible_button.set_property('margin-start', 5)
            visible_button.set_property('margin-end', 5)
            if bay.hidden:
                hide_button.set_active(True)
            else:
                visible_button.set_active(True)
            self.append(visible_button)
            self.append(hide_button)
            hide_button.connect('toggled', self._on_hide)
            visible_button.connect('toggled', self._on_show)

    def _on_hide(self, button) -> None:
        if not self.bay.hidden:
            asyncio.get_event_loop().create_task(self.bay.set_hidden(hidden=True))

    def _on_show(self, button) -> None:
        if self.bay.hidden:
            asyncio.get_event_loop().create_task(self.bay.set_hidden(hidden=False))
