#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')

from iutils.render import Render
from gi.repository import Gtk

class MainApp(Gtk.Window, Render):
    """Main window for the program

    This is the main view of the program, where every control is present,
    as buttons and text boxes.

    """
    def __init__(self,
                 front, back,
                 step=None,
                 width=1200, height=700):
        # Window initialization
        Gtk.Window.__init__(self)

        # Render initialization
        n = int(height*0.9)
        Render.__init__(self,n, front, back)

        # Title and window stuff
        self.set_title("Fractures")
        self.resize(width,height)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Maybe this should be more complex in the future
        self.connect("destroy", Gtk.main_quit)

        # Call the input creations
        self.__createInputs()
        
        # The draw area for the cairo canvas
        self.darea = Gtk.DrawingArea()
        #self.add(self.darea)

        # Show everything on the window
        self.show_all()

        #def expose(self, widget, event):

    # Main loop
    def start(self):
        Gtk.main()

    def __createInputs(self):
        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                           spacing=6)

        self.add(self.vbox)

        # Speed of fracture
        self.speedEntry = Gtk.Entry()
        self.speedEntry.set_text("Speed of fractures")
        self.vbox.pack_start(self.speedEntry, True, False, 0)

        # Size of... something.
        self.sizeEntry = Gtk.Entry()
        self.sizeEntry.set_text("Size")
        self.vbox.pack_start(self.sizeEntry, True, False, 0)

        # Distance of source?
        self.distanceEntry = Gtk.Entry()
        self.distanceEntry.set_text("Distance")
        self.vbox.pack_start(self.distanceEntry, True, False, 0)
        
        # Number of sources
        self.sourceNumber = Gtk.Entry()
        self.sourceNumber.set_text("Sources number")
        self.vbox.pack_start(self.sourceNumber, True, False, 0)

        domainStore = Gtk.ListStore(str, str)
        domainStore.append(['circ', 'Circle'])
        domainStore.append(['rect', 'Rectangle'])

        # Domain combo box
        self.domain = Gtk.ComboBox.new_with_model(domainStore)
        self.domain.connect("changed", self.onSelectionChange)
        renderer = Gtk.CellRendererText()
        self.domain.pack_start(renderer, True)
        self.domain.add_attribute(renderer, "text", 1)
        
        self.vbox.pack_start(self.domain, False, False, True)

    # What to do when the selection changes in the list of domain options
    def onSelectionChange(self, combo):
        treeiter = combo.get_active_iter()
        if treeiter != None:
            model = combo.get_model()
            print("Selected:",model[treeiter][0])
