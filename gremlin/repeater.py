# -*- coding: utf-8; -*-

# Copyright (C) 2015 - 2017 Lionel Ott
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


import threading
import time

from PyQt5 import QtCore

from . import common, event_handler


class Repeater(QtCore.QObject):

    """Responsible to repeatedly emit a set of given events.

    The class receives a list of events that are to be emitted in
    sequence. The events are emitted in a separate thread and the
    emission cannot be aborted once it started. While events are
    being emitted a change of events is not performed to prevent
    continuous emitting of events.
    """

    def __init__(self, events, update_func):
        """Creates a new instance.

        :param events the list of events to emit
        """
        QtCore.QObject.__init__(self)
        self.is_running = False
        self._events = events
        self._thread = threading.Thread(target=self.emit_events)
        self._start_timer = threading.Timer(1.0, self.run)
        self._stop_timer = threading.Timer(5.0, self.stop)
        self._update_func = update_func
        self._timeout = time.time()

    @property
    def events(self):
        return self._events

    @events.setter
    def events(self, event_list):
        """Sets the list of events to execute and queues execution.

        Starts emitting the list of events after a short delay. If a
        new list of events is received before the timeout, the old timer
        is destroyed and replaced with a new one for the new list of
        events. Once events are being emitted all change requests will
        be ignored.

        :param event_list the list of events to emit
        """
        # Only proceed when waiting for input and valid input is provided
        if self.is_running or len(event_list) == 0:
            return
        # Discard inputs that arrive in too quick of a succession
        if time.time() - self._timeout < 0.25:
            return

        self._events = event_list
        if self._start_timer:
            self._start_timer.cancel()
        self._start_timer = threading.Timer(1.0, self.run)
        self._start_timer.start()
        self._update_func("Received input")
        self._timeout = time.time()

    def stop(self):
        """Stops the event dispatch thread."""
        self.is_running = False
        self._thread.join()

    def run(self):
        """Starts the event dispatch thread."""
        if self._thread.is_alive():
            return
        self.is_running = True
        self._stop_timer = threading.Timer(5.0, self.stop)
        self._stop_timer.start()
        self._thread = threading.Thread(target=self.emit_events)
        self._thread.start()

    def emit_events(self):
        """Emits events until stopped."""
        index = 0
        el = event_handler.EventListener()

        # Repeatedly send events until the thread is interrupted
        while self.is_running:
            if self._events[0].event_type == common.InputType.Keyboard:
                el.keyboard_event.emit(self._events[index])
            else:
                el.joystick_event.emit(self._events[index])

            self._update_func("{} {}".format(
                common.input_type_to_name[self._events[index].event_type],
                str(self._events[index].identifier)
            ))

            index = (index + 1) % len(self._events)
            time.sleep(0.25)

        # This timeout prevents the below state reset to cause the
        # program to trigger another round of repeats with the same
        # input
        self._timeout = time.time()

        # Ensure we leave the input in a neutral state when done
        event = self._events[0].clone()
        if event.event_type == common.InputType.JoystickButton:
            event.is_pressed = False
        elif event.event_type == common.InputType.JoystickAxis:
            event.value = 0.0
        elif event.event_type == common.InputType.JoystickHat:
            event.value = (0, 0)
        el.joystick_event.emit(event)
        self._update_func("Waiting for input")
