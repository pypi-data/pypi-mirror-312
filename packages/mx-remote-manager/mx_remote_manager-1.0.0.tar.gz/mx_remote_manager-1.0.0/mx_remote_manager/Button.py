##################################################
##         MX Remote Manager GUI                ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class DeviceButton(Gtk.Box):
    def __init__(self, label:str, callback:callable) -> None:
        Gtk.Box.__init__(self)
        self.callback = callback
        self.spinner = None
        self.enabled = True

        self.button_box = Gtk.Box()
        self.label = Gtk.Label()
        self.label.set_text(label)
        self.button_box.append(self.label)

        self.button = Gtk.Button()
        self.button.connect('clicked', self._on_click)
        self.button.set_property('margin-start', 5)
        self.button.set_property('margin-end', 5)
        self.button.set_child(self.button_box)
        self.append(self.button)

    def set_spinner(self, enable:bool) -> None:
        if enable:
            if self.spinner is None:
                self.spinner = Gtk.Spinner()
                self.button_box.append(self.spinner)
                self.spinner.start()
        else:
            if self.spinner is not None:
                self.button_box.remove(self.spinner)
                self.spinner = None

    def set_enabled(self, enable:bool) -> None:
        self.enabled = enable

    def _on_click(self, button) -> None:
        if self.enabled:
            self.callback()
