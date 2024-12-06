##################################################
##         MX Remote Manager GUI                ##
##                                              ##
## author: Lars Op den Kamp (lars@opdenkamp.eu) ##
## copyright (c) 2024 Op den Kamp IT Solutions  ##
##################################################

import aes3tool as ae
import asyncio
from .const import *
import gi
import logging
import mx_remote as mx
import os
import platform
import sys
_LOGGER = logging.getLogger(__name__)

gi.require_version("Gtk", "4.0")
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, Adw

from .Devices import DevicesTab
from .Sources import SourcesTab
from .ControlBar import ControlBar
from .NetworkInterface import NetworkInterfaceList, NetworkInterfaceMulticast, NetworkTxAddress

class ShowSerialsSetting:
    def __init__ (self, devices:DevicesTab) -> None:
        self.devices = devices
        box = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        button1 = Gtk.ToggleButton.new_with_label("Serials")
        button1.connect("toggled", self._on_button1)
        box.append(button1)

        button2 = Gtk.ToggleButton.new_with_label("Names")
        button2.set_group(button1)
        button2.set_active(True)
        button2.connect("toggled", self._on_button2)
        box.append(button2)

        self.action_row = Adw.ActionRow.new()
        self.action_row.add_prefix(
            widget=Gtk.Image.new_from_icon_name(
                icon_name='emblem-shared'
            ),
        )
        self.action_row.set_title(title='Show Serials')
        self.action_row.set_subtitle(subtitle='Show serials instead of device names in the device list')
        self.action_row.add_suffix(widget=box)

    def _on_button1(self, button) -> None:
        if button.get_active():
            self.devices.show_serials = True

    def _on_button2(self, button) -> None:
        if button.get_active():
            self.devices.show_serials = False

class AudioSampleRate:
    def __init__ (self, changed_callback:callable) -> None:
        self._callback = changed_callback
        box = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        button1 = Gtk.ToggleButton.new_with_label("32KHz")
        button1.connect("toggled", self._on_button1)
        box.append(button1)

        button2 = Gtk.ToggleButton.new_with_label("44.1Khz")
        button2.set_group(button1)
        button2.connect("toggled", self._on_button2)
        box.append(button2)

        button3 = Gtk.ToggleButton.new_with_label("48Khz")
        button3.set_group(button1)
        button3.set_active(True)
        button3.connect("toggled", self._on_button3)
        box.append(button3)

        self.action_row = Adw.ActionRow.new()
        self.action_row.add_prefix(
            widget=Gtk.Image.new_from_icon_name(
                icon_name='network-wired'
            ),
        )
        self.action_row.set_title(title='Sample Rate')
        self.action_row.set_subtitle(subtitle='Audio sample rate')
        self.action_row.add_suffix(widget=box)

    def _on_button1(self, button) -> None:
        if button.get_active():
            self._callback(rate=32000)

    def _on_button2(self, button) -> None:
        if button.get_active():
            self._callback(rate=44100)

    def _on_button3(self, button) -> None:
        if button.get_active():
            self._callback(rate=48000)

@Gtk.Template(resource_path=f'/builder/main.ui')
class MxrGuiApplication(Adw.ApplicationWindow):
    __gtype_name__ = 'MxRemoteWindow'
    child_main_content = Gtk.Template.Child('main_content')
    child_sidebar_toggle = Gtk.Template.Child('sidebar_toggle')
    child_dark_mode_toggle = Gtk.Template.Child('dark_mode_toggle')
    child_app_button = Gtk.Template.Child('app_button')
    child_sidebar = Gtk.Template.Child('sidebar')
    child_sidebar_stack = Gtk.Template.Child('sidebar_stack')
    child_tab_devices = Gtk.Template.Child('devices_box')
    child_tab_sources = Gtk.Template.Child('sources_box')
    child_settings_box = Gtk.Template.Child('settings_box')
    child_settings_network = Gtk.Template.Child('settings_network')
    child_settings_gui = Gtk.Template.Child('settings_gui')
    child_settings_audio = Gtk.Template.Child('settings_audio')
    child_stack_switch = Gtk.Template.Child('stack_switch')
    child_control_bar = Gtk.Template.Child('control_bar')
    child_app_menu = Gtk.Template.Child('app_menu')

    def __init__(self, application:'MxrGui', mxr:mx.Remote) -> None:
        Adw.ApplicationWindow.__init__(self, application=application)
        self.set_icon_name(APP_ID)
        self.style_manager = Adw.StyleManager().get_default()
        self.style_manager.set_color_scheme(Adw.ColorScheme.PREFER_DARK)

        self.mxr = mxr
        self.tab_devices = DevicesTab(player=self.control_bar.player)
        self.tab_sources = SourcesTab(player=self.control_bar.player)
        self.child_tab_devices.append(self.tab_devices)
        self.child_tab_sources.append(self.tab_sources)
        self.create_action('about', self.menu_handler)
        self.create_action('quit', self.menu_handler)
        self.child_settings_network.add(NetworkInterfaceList(ip=self.mxr.local_ip, changed_callback=self._on_local_ip_changed).action_row)
        self.child_settings_network.add(NetworkInterfaceMulticast(mxr=self.mxr).action_row)
        self.child_settings_gui.add(ShowSerialsSetting(devices=self.tab_devices).action_row)
        self.child_settings_audio.add(AudioSampleRate(changed_callback=self._on_sample_rate_changed).action_row)
        self.child_settings_audio.add(NetworkTxAddress(ip=DEFAULT_TX_ADDRESS, changed_callback=self._on_tx_address_changed).action_row)
        self.child_dark_mode_toggle.connect('clicked', self.on_dark_mode_toggled)
        self.child_sidebar_toggle.connect('clicked', self.on_sidebar_toggle)
        self.control_bar.set_local_ip(address=self.mxr.local_ip)

    def _on_tx_address_changed(self, address:str) -> None:
        self.control_bar.set_target_ip(address=address)

    def _on_local_ip_changed(self, address:str) -> None:
        self.control_bar.set_local_ip(address=address)
        asyncio.get_event_loop().create_task(self.mxr.update_config(local_ip=address))

    def set_target_ip(self, address:str) -> None:
        self.control_bar.set_target_ip(address=address)

    def _on_sample_rate_changed(self, rate:int) -> None:
        self.control_bar.set_sample_rate(rate=rate)

    def on_dark_mode_toggled(self, button):
        if self.style_manager.get_dark():
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        else:
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)

    def on_sidebar_toggle(self, widget):
        self.child_sidebar.set_reveal_flap(not self.child_sidebar.get_reveal_flap())

    def menu_handler(self, action, state):
        name = action.get_name()
        if name == 'quit':
            self.close()
        if name == 'about':
            self.about()

    def about(self) -> None:
        dialog = Adw.AboutWindow(transient_for=self)
        dialog.set_application_name(APP_NAME)
        dialog.set_version(VERSION) 
        dialog.set_license_type(Gtk.License(Gtk.License.BSD_3)) 
        dialog.set_comments(
"""Application for managing MX Remote compatible devices.

Currently supported products:
  <a href="https://www.pulse-eight.com/p/246/oneip-tz">Pulse-Eight OneIP</a>
  <a href="https://www.pulse-eight.com/p/214/neox">Pulse-Eight neo:X</a>
  <a href="https://www.pulse-eight.com/p/245/neo-xsr">Pulse-Eight neo:XSR</a>
  Pulse-Eight neo:XMR
  <a href="https://www.pulse-eight.com/p/216/neo8a">Pulse-Eight neo:8a / neo8</a>
  <a href="https://www.pulse-eight.com/p/230/neo6a">Pulse-Eight neo:6a</a>
  <a href="https://www.pulse-eight.com/p/155/neo4-hdbaset-video-matrix-with-poh-receivers">Pulse-Eight neo:4</a>
  <a href="https://www.pulse-eight.com/p/219/proamp-8">Pulse-Eight ProAmp8</a>

Please upgrade MatrixOS to the latest release to use all features of this application.""")
        dialog.set_debug_info(
f"""mxr-remote-ui: v{VERSION}
mx-remote: v{mx.VERSION}
aes3tool: v{ae.VERSION}
protocol: v{mx.MXR_PROTOCOL_VERSION}
network protocol min: v{self.mxr.net_protocol_version_min}
network protocol max: v{self.mxr.net_protocol_version_max}
interface: {self.mxr.local_ip}
broadcast: {self.mxr.broadcast}
os: {platform.platform()} ({os.name} - {platform.machine()})
interpreter: {sys.version}
devices: {[f'{dev.serial}-{dev.version}' for _, dev in self.mxr.remotes.items()]}
""")
        dialog.set_release_notes_version(VERSION)
        dialog.set_website(APP_REPOSITORY) 
        dialog.set_copyright("© 2024 <a href='mailto:lars@opdenkamp.eu'>Op den Kamp IT Solutions</a>")
        dialog.set_developers(["Lars Op den Kamp https://github.com/opdenkamp/"])
        dialog.add_credit_section("Supported Hardware", ["Pulse-Eight https://pulse-eight.com/"])
        dialog.set_support_url("https://support.pulse-eight.com/")
        dialog.set_application_icon(APP_ID)
        dialog.set_visible(True)

    @property
    def control_bar(self) -> ControlBar:
        return self.child_control_bar

    def on_device_update(self, dev:mx.DeviceBase) -> None:
        self.control_bar.on_device_update(dev)
        self.tab_devices.on_device_update(dev)
        self.tab_sources.on_device_update(dev)

    def create_action(self, name, callback):
        """ Add an Action and connect to a callback """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)

class MxrGui(Adw.Application, mx.MxrCallbacks):
    def __init__(self, local_ip:str, broadcast:bool) -> None:
        Adw.Application.__init__(self,
                                 application_id=APP_ID,
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)

        # init mx_remote
        mx.MxrCallbacks.__init__(self)
        self.mxr = mx.Remote(local_ip=local_ip,
                             broadcast=broadcast,
                             callbacks=self)

    def on_device_update(self, dev:mx.DeviceBase) -> None:
        # forward device updates to the window
        self.win.on_device_update(dev)

    def start(self) -> None:
        # set the event loop so we can run asyncio
        from gi.events import GLibEventLoopPolicy
        asyncio.set_event_loop_policy(GLibEventLoopPolicy())
        self.run()

    def do_activate(self) -> None:
        if not self.props.active_window:
            # create a new app
            self.win = MxrGuiApplication(application=self,
                                         mxr=self.mxr)
            asyncio.get_event_loop().create_task(self.mxr.start_async())
        self.win.present()
