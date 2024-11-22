from config import config
from widgets.battery import Battery
from widgets.clickcounter import ClickCounter
from widgets.hypridle import HyprIdle
from widgets.hyprsunset import HyprSunset
from widgets.language import LanguageBox
from widgets.mpris import Mpris
from widgets.stats import Cpu, Memory, Storage
from widgets.updates import Updates
from widgets.volume import AUDIO_WIDGET, VolumeWidget
from widgets.weather import Weather
from widgets.windowtitle import WindowTitle
from widgets.workspace import WorkSpaces
from fabric.system_tray.widgets import SystemTray
from fabric.widgets.box import Box
from fabric.widgets.centerbox import CenterBox
from fabric.widgets.datetime import DateTime
from fabric.widgets.wayland import WaylandWindow as Window


class StatusBar(Window):
    def __init__(
        self,
    ):
        super().__init__(
            name="bar",
            layer="top",
            anchor="left top right",
            margin="10px 10px -2px 10px",
            exclusivity="auto",
            visible=False,
            all_visible=False,
        )

        self.config = config

        battery_config = config["battery"]
        cpu_config = config["cpu"]
        updates_config = config["updates"]
        updates_config = config["updates"]

        self.widgets_list = {
            # Workspaces: Displays the list of workspaces or desktops
            "workspaces": WorkSpaces(),
            # WindowTitle: Shows the title of the current window
            "windowtitle": WindowTitle(config=config),
            # LanguageBox: Displays the current language selection
            "language": LanguageBox(),
            # DateTime: Displays the current date and time
            "datetime": DateTime(name="date-time"),
            # SystemTray: Represents the system tray with various icons (e.g., battery, network)
            "systemtray": SystemTray(name="system-tray", spacing=4),
            # HyprSunset: Provides information about the sunset time based on location
            "hyprsunset": HyprSunset(config=config).create(),
            # HyprIdle: Shows the idle time for the system
            "hypridle": HyprIdle(config=config).create(),
            # Battery: Displays the battery status with optional label and tooltip
            "battery": Battery(
                enable_label=battery_config["enable_label"],
                enable_tooltip=battery_config["enable_tooltip"],
                interval=battery_config["interval"],
            ),
            # Cpu: Displays CPU usage information with optional label and tooltip
            "cpu": Cpu(
                icon=cpu_config["icon"],
                enable_label=cpu_config["enable_label"],
                enable_tooltip=cpu_config["enable_tooltip"],
                interval=cpu_config["interval"],
            ),
            # ClickCounter: Tracks the number of clicks on a widget or component
            "clickcounter": ClickCounter(),
            # Memory: Displays the system's memory usage
            "memory": Memory(),
            # Storage: Shows the system's storage usage (e.g., disk space)
            "storage": Storage(),
            # Weather: Displays the weather for a given city (e.g., Kathmandu)
            "weather": Weather("kathmandu"),
            # Player: Displays information about the current media player status
            "player": Mpris(),
            # Updates: Shows available system updates based on the OS
            "updates": Updates(os=updates_config["os"]),
        }

        layout = self.make_layout()

        self.system_tray = SystemTray(name="system-tray", spacing=4)

        self.hyprsunset = HyprSunset(config=config).create()
        self.hypridle = HyprIdle(config=config).create()

        self.status_container = Box(
            name="widgets-container",
            spacing=4,
            orientation="h",
        )
        self.status_container.add(VolumeWidget()) if AUDIO_WIDGET is True else None

        self.battery = Battery(
            enable_label=battery_config["enable_label"],
            enable_tooltip=battery_config["enable_tooltip"],
            interval=battery_config["interval"],
        )

        self.cpu = Cpu(
            icon=cpu_config["icon"],
            enable_label=cpu_config["enable_label"],
            enable_tooltip=cpu_config["enable_tooltip"],
            interval=cpu_config["interval"],
        )

        self.click_counter = ClickCounter()

        self.memory = Memory()
        self.storage = Storage()
        self.weather = Weather("kathmandu")
        self.player = Mpris()
        self.updates = Updates(os=updates_config["os"], icon=updates_config["icon"])

        self.children = CenterBox(
            name="bar-inner",
            start_children=Box(
                name="start-container",
                spacing=4,
                orientation="h",
                children=layout["left_children"],
            ),
            center_children=Box(
                name="center-container",
                spacing=4,
                orientation="h",
                children=layout["middle_children"],
            ),
            end_children=Box(
                name="end-container",
                spacing=4,
                orientation="h",
                children=[
                    self.updates,
                    self.memory,
                    self.battery,
                    self.status_container,
                    self.system_tray,
                ],
            ),
        )

        self.show_all()

    def make_layout(self):
        layout = {"left_children": [], "middle_children": [], "right_children": []}

        # firset set of widgets (Left)
        layout["left_children"].extend(
            self.widgets_list[widget] for widget in self.config["layout"]["left"]
        )

        # second set of widgets (Center)
        layout["middle_children"].extend(
            self.widgets_list[widget] for widget in self.config["layout"]["middle"]
        )

        return layout
