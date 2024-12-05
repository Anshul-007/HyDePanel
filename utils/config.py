from typing import List, TypedDict

from utils.functions import read_config

# Default poll interval for widgets that need not be updated frequently
high_poll_interval = 1000 * 60 * 10  # 10 minutes

# Default configuration values
DEFAULT_CONFIG = {
    "layout": {
        "left_section": ["workspaces", "window_title"],
        "middle_section": ["datetime", "player"],
        "right_section": [
            "weather",
            "battery",
            "system_tray",
            "updates",
            "hypr_idle",
            "hypr_sunset",
        ],
    },
    "hypr_sunset": {
        "temperature": "2800k",
        "enabled_icon": "󱩌",
        "disabled_icon": "󰛨",
        "icon_size": "12px",
        "interval": 2000,
        "enable_label": True,
        "enable_tooltip": True,
    },
    "hypr_idle": {
        "enabled_icon": "",
        "disabled_icon": "",
        "icon_size": "12px",
        "interval": 2000,
        "enable_label": True,
        "enable_tooltip": True,
    },
    "battery": {
        "enable_label": True,
        "enable_tooltip": True,
        "interval": 2000,
        "hide_label_when_full": True,
    },
    "cpu": {
        "icon": "",
        "icon_size": "12px",
        "interval": 2000,
        "enable_label": True,
        "enable_tooltip": True,
    },
    "memory": {
        "icon": "",
        "interval": 2000,
        "icon_size": "12px",
        "enable_label": True,
        "enable_tooltip": True,
    },
    "storage": {
        "icon": "󰋊",
        "interval": 2000,
        "icon_size": "14px",
        "enable_label": True,
        "enable_tooltip": True,
    },
    "workspaces": {"count": 8, "occupied": True},
    "window_title": {"length": 20, "enable_icon": True},
    "updates": {
        "os": "arch",
        "icon": "󱧘",
        "icon_size": "14px",
        "interval": high_poll_interval,
        "enable_tooltip": True,
        "enable_label": True,
    },
    "weather": {
        "location": "Kathmandu",
        "interval": high_poll_interval,
        "enable_tooltip": True,
        "enable_label": True,
    },
    "keyboard": {
        "icon": "󰌌",
        "icon_size": "14px",
        "enable_label": True,
        "enable_tooltip": True,
    },
    "player": {
        "length": 30,
        "enable_tooltip": True,
    },
    "language": {"length": 3},
    "task_bar": {"icon_size": 22},
    "system_tray": {"icon_size": 22},
}


class BaseConfig(TypedDict):
    """Common configuration for some sections"""

    icon_size: str
    enable_label: bool
    enable_tooltip: bool
    interval: int


class Layout(TypedDict):
    """ayout configuration for different sections of the bar"""

    left: List[str]
    middle: List[str]
    right: List[str]


class HyprSunset(TypedDict, BaseConfig):
    """Configuration for hyprsunset"""

    temperature: str
    enabled_icon: str
    disabled_icon: str


class TaskBar(TypedDict):
    """Configuration for taskbar"""

    icon_size: int


class SystemTray(TypedDict):
    """Configuration for system tray"""

    icon_size: int


class HyprIdle(TypedDict, BaseConfig):
    """Configuration for hypridle"""

    enabled_icon: str
    disabled_icon: str


class Battery(TypedDict):
    """Configuration for battery"""

    enable_label: bool
    enable_tooltip: bool
    hide_label_when_full: bool
    interval: int


class Cpu(TypedDict, BaseConfig):
    """Configuration for Cpu"""

    icon: str


class Player(TypedDict, BaseConfig):
    """Configuration for bar player"""

    length: int


class Memory(TypedDict, BaseConfig):
    """Configuration for window"""

    icon: str


class Storage(TypedDict, BaseConfig):
    """Configuration for storage"""

    icon: str


class Workspaces(TypedDict):
    """Configuration for Workspaces"""

    count: int
    occupied: bool


class WindowTitle(TypedDict):
    """Configuration for Window"""

    length: int
    enable_icon: bool


class Updates(TypedDict, BaseConfig):
    """Configuration for updates"""

    os: str
    icon: str


class Weather(TypedDict):
    """Configuration for weather"""

    location: str
    interval: int
    enable_tooltip: bool
    enable_label: bool


class Keyboard(TypedDict, BaseConfig):
    """Configuration for keyboard"""

    icon: str


class Language(TypedDict):
    """Configuration for language"""

    length: int


class BarConfig(TypedDict):
    """Main configuration that includes all other configurations"""

    battery: Battery
    cpu: Cpu
    hypr_sunset: HyprSunset
    hypr_idle: HyprIdle
    keyboard: Keyboard
    language: Language
    layout: Layout
    memory: Memory
    player: Player
    storage: Storage
    system_tray: SystemTray
    task_bar: TaskBar
    updates: Updates
    workspaces: Workspaces
    window_title: WindowTitle
    weather: Weather


# Read the configuration from the JSON file
parsed_data = read_config()


# Merge the parsed data with the default configuration
def merge_defaults(data: dict, defaults: dict):
    return {**defaults, **data}


# Now, `parsed_data` is a Python dictionary
# You can access individual items like this:
layout = parsed_data["layout"]


for key, value in parsed_data.items():
    if key in DEFAULT_CONFIG:
        parsed_data[key] = merge_defaults(value, DEFAULT_CONFIG[key])


## TODO: validate the name of widget is within the dict

# Optionally, cast the parsed data to match our TypedDict using type hints
config: BarConfig = parsed_data
