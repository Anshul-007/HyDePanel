from fabric.widgets.box import Box
from fabric.widgets.datetime import DateTime


class DateTimeBox(Box):
    def __init__(self, **kwargs):
        super().__init__(name="date-time", style_classes="panel-box", **kwargs)

        self.date_time = DateTime()
        self.children = self.date_time
