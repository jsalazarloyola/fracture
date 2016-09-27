#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
import re

class NumberEntry(Gtk.Entry):
    def __init__(self):
        Gtk.Entry.__init__(self)
        self.connect('changed', self.on_changed)

        # Regular expression in order to find if the entry is really a
        # number
        # TODO: include the possibility of having integers
        #self.rx = re.compile("^\d+?\.\d+?$",re.VERBOSE)
        self.rx = re.compile("\d*\.?\d*",re.VERBOSE)

    # Checks if the text is really numbers, otherwise, it will put a blank.
    def on_changed(self,*args):
        # Finds if the text is really numbers...
        text = self.rx.findall(self.get_text().strip())
        if len(text):
            self.set_text(text[0])
        else:
            self.set_text('')
