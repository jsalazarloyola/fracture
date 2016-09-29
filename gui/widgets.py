#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
import re

class NumberEntry(Gtk.Entry):
    """Class for numeric entries in the GUI.

    This class extends the Gtk.Entry class in order to
    take into account for the entries which are required to be
    numbers and not plain text.

    It takes integer and float numbers, but not exponent notation,
    nor long numbers.
    """
    def __init__(self):
        """Default constructor.

        Calls for the Gtk.Entry constructor, and sets functions to run
        when the input changes"""
        # Call base constructor
        Gtk.Entry.__init__(self)
        self.connect('changed', self.on_changed)

        # Regular expression which detects if the text
        # is a valid number. 
        self.rx = re.compile("\d*\.?\d*",re.VERBOSE)

    # Checks if the text is really numbers, otherwise, it will put a blank.
    def on_changed(self,*args):
        """Verifies that the input text is valid."""
        # Finds if the text is really numbers...
        text = self.rx.findall(self.get_text().strip())
        if len(text):
            self.set_text(text[0])
        else:
            self.set_text('')
