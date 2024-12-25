import re

from fabric.hyprland.widgets import ActiveWindow
from fabric.utils import FormattedString, truncate
from fabric.widgets.box import Box

from utils.config import WINDOW_TITLE_MAP
from utils.widget_config import BarConfig


# TODO: replace with actual image
class WindowTitleWidget(Box):
    """a widget that displays the title of the active window."""

    def __init__(self, widget_config: BarConfig, bar, **kwargs):
        super().__init__(style_classes="panel-box", name="window-box", **kwargs)

        # Store the configuration for the window title
        self.config = widget_config["window_title"]

        # Create an ActiveWindow widget to track the active window
        self.window = ActiveWindow(
            name="window",
            formatter=FormattedString(
                "{ '󰇄 Desktop' if not win_title else get_title(win_title, win_class)}",
                get_title=self.get_title,
            ),
        )

        # Add the ActiveWindow widget as a child
        self.children = self.window

    def get_title(self, win_title, win_class):
        # Truncate the window title based on the configured length
        win_title = (
            truncate(win_title, self.config["truncation_size"])
            if self.config["truncation"]
            else win_title
        )

        merged_titles = self.config["title_map"] + WINDOW_TITLE_MAP

        # Find a matching window class in the windowTitleMap
        matched_window = next(
            (wt for wt in merged_titles if re.search(wt[0], win_class.lower())),
            None,
        )
        # Return the formatted title with or without the icon
        if matched_window:
            return (
                f"{matched_window[1]} {matched_window[2]}"
                if self.config["enable_icon"]
                else f"{matched_window[2]}"
            )
