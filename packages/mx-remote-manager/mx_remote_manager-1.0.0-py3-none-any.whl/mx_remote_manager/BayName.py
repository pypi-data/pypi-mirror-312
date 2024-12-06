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
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

class BayName(Gtk.Box):
    def __init__(self, bay:mx.BayBase) -> None:
        Gtk.Box.__init__(self)
        self.bay = bay
        self.entry = Adw.EntryRow()
        self.entry.set_property('show-apply-button', True)
        self.append(self.entry)
        self.update(bay=bay)
        self.entry.connect("apply", self._on_apply)

    def _on_apply(self, _):
        asyncio.get_event_loop().create_task(self.bay.set_name(name=self.entry.get_text()))
        self.entry.set_title(self.entry.get_text())

    def update(self, bay:mx.BayBase) -> None:
        text = bay.user_name if bay is not None else ''
        self.entry.set_title(text)