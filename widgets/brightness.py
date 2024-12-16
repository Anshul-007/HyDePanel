from fabric.widgets.box import Box
from fabric.widgets.circularprogressbar import CircularProgressBar
from fabric.widgets.eventbox import EventBox
from fabric.widgets.label import Label
from fabric.widgets.overlay import Overlay

import utils.functions as helpers
from utils.icons import brightness_text_icons
from utils.widget_config import BarConfig
from utils.config import brightness_service


class BrightnessWidget(EventBox):
    """a widget that displays and controls the brightness."""

    def __init__(self, widget_config: BarConfig, **kwargs):
        super().__init__(events=["scroll", "smooth-scroll"], **kwargs)

        self.change_brightness_by = 5

        # Initialize the audio service
        self.brightness_service = brightness_service

        self.config = widget_config["brightness"]

        normalized_brightness = helpers.convert_to_percent(
            self.brightness_service.screen_brightness,
            self.brightness_service.max_screen,
        )

        # Create a circular progress bar to display the brightness level

        self.progress_bar = CircularProgressBar(
            style_classes="overlay-progress-bar",
            pie=True,
            size=24,
            value=normalized_brightness / 100,
        )

        self.brightness_label = Label(
            visible=False,
            label=f"{normalized_brightness}%",
        )

        self.icon = helpers.text_icon(
            icon=brightness_text_icons["medium"],
            size=self.config["icon_size"],
            props={
                "style_classes": "panel-text-icon overlay-icon",
            },
        )

        # Create an event box to handle scroll events for brightness control
        self.box = Box(
            spacing=4,
            name="brightness",
            style_classes="panel-box",
            children=(
                Overlay(child=self.progress_bar, overlays=self.icon, name="overlay"),
                self.brightness_label,
            ),
        )
        # Connect the audio service to update the progress bar on brightness change
        self.brightness_service.connect("screen", self.on_brightness_changed)

        # Connect the event box to handle scroll events
        self.connect("scroll-event", self.on_scroll)

        # Add the event box as a child
        self.add(self.box)

        if self.config["enable_label"]:
            self.brightness_label.show()

    def on_scroll(self, _, event):
        # Adjust the brightness based on the scroll direction

        val_y = event.delta_y

        if val_y > 0:
            self.brightness_service.screen_brightness += self.change_brightness_by
        else:
            self.brightness_service.screen_brightness -= self.change_brightness_by

    def on_brightness_changed(self, *_):
        if self.config["enable_tooltip"]:
            self.set_tooltip_text("")

        self.update_brightness()

    def update_brightness(self, *_):
        normalized_brightness = helpers.convert_to_percent(
            self.brightness_service.screen_brightness,
            self.brightness_service.max_screen,
        )
        self.progress_bar.set_value(normalized_brightness / 100)

        self.brightness_label.set_text(f"{normalized_brightness}%")

        self.icon.set_text(
            helpers.get_brightness_icon_name(normalized_brightness)["text_icon"]
        )
