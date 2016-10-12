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

    def __int__(self):
        """Cast the content to integer

        If the content is float, it returns its floor
        """
        try:
            return int(self.get_text())
        except:
            return int(float(self.get_text()))

    def __float__(self):
        """Cast the content to float"""
        return float(self.get_text())


class ExportDialog(Gtk.FileChooserDialog):
    """Class which handles name finding for exportation of pictures

    This class extends Gtk.FileChooserDialog in order to take into account
    that the fracture images could be exported to PNG or SVG formats.

    It creates the Gtk.FileChooserDialog and sets all its features so the
    main window doesn't have to set it for itself, while also allowing
    further configuration through normal methods of the base class.
    """
    def __init__(self, message, parent=None):
        buttons = (Gtk.STOCK_CANCEL,
                   Gtk.ResponseType.CANCEL,
                   Gtk.STOCK_OPEN,
                   Gtk.ResponseType.OK)
        Gtk.FileChooserDialog.__init__(self, message, parent,
                                       Gtk.FileChooserAction.SAVE,
                                       buttons)

        # Sets filters for images
        self.setFilters()

        return

    def setFilters(self):
        """Dictionary that holds the filter list with its associated extensions"""
        self.filters = {}

        # Filter for PNG images
        filterPng = Gtk.FileFilter()
        filterPng.set_name("PNG images")
        filterPng.add_mime_type("image/png")
        self.add_filter(filterPng)
        self.filters[filterPng.get_name()] = ".png"

        # Filter for SVG images
        filterSvg = Gtk.FileFilter()
        filterSvg.set_name("SVG images")
        filterSvg.add_mime_type("image/svg+xml")
        self.add_filter(filterSvg)
        self.filters[filterSvg.get_name()] = ".svg"
        
        return

    def getFileType(self):
        return self.filters[self.get_filter().get_name()]
