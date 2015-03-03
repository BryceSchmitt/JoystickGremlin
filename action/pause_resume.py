# -*- coding: utf-8; -*-

# Copyright (C) 2015 Lionel Ott
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from mako.template import Template
from PyQt5 import QtWidgets
from xml.etree import ElementTree

from action.common import AbstractAction, AbstractActionWidget
import gremlin.event_handler


class PauseActionWidget(AbstractActionWidget):

    """Widget for the pause action."""

    def __init__(self, action_data, vjoy_devices, change_cb, parent=None):
        AbstractActionWidget.__init__(self, action_data, vjoy_devices, change_cb, parent)
        assert(isinstance(action_data, PauseAction))

    def _setup_ui(self):
        self.label = QtWidgets.QLabel("Pauses callback execution")
        self.main_layout.addWidget(self.label)

    def to_profile(self):
        self.action_data.is_valid = True

    def initialize_from_profile(self, action_data):
        pass


class PauseAction(AbstractAction):

    """Action for pausing the execution of callbacks."""

    icon = "gfx/icon_action.svg"
    name = "Pause"
    widget = PauseActionWidget
    input_types = [
        gremlin.event_handler.InputType.JoystickButton,
        gremlin.event_handler.InputType.Keyboard
    ]

    def __init__(self, parent):
        AbstractAction.__init__(self, parent)

    def _parse_xml(self, node):
        pass

    def _generate_xml(self):
        return ElementTree.Element("pause-action")

    def _generate_code(self):
        tpl = Template(filename="templates/pause_body.tpl")
        return {
            "body": tpl.render(
                entry=self
            )
        }


class ResumeActionWidget(AbstractActionWidget):

    """Widget for the resume action."""

    def __init__(self, action_data, vjoy_devices, change_cb, parent=None):
        AbstractActionWidget.__init__(self, action_data, vjoy_devices, change_cb, parent)
        assert(isinstance(action_data, ResumeAction))

    def _setup_ui(self):
        self.label = QtWidgets.QLabel("Resumes callback execution")
        self.main_layout.addWidget(self.label)

    def to_profile(self):
        self.action_data.is_valid = True

    def initialize_from_profile(self, action_data):
        pass


class ResumeAction(AbstractAction):

    """Action to resume callbac kexecution."""

    icon = "gfx/icon_action.svg"
    name = "Resume"
    widget = ResumeActionWidget
    input_types = [
        gremlin.event_handler.InputType.JoystickButton,
        gremlin.event_handler.InputType.Keyboard
    ]

    def __init__(self, parent):
        AbstractAction.__init__(self, parent)

    def _parse_xml(self, node):
        pass

    def _generate_xml(self):
        return ElementTree.Element("resume-action")

    def _generate_code(self):
        tpl = Template(filename="templates/resume_body.tpl")
        return {
            "body": tpl.render(
                entry=self
            )
        }