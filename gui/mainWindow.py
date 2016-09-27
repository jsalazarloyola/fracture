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
        self.set_border_width(5)
        self.set_title("Fractures")
        self.resize(width,height)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Maybe this should be more complex in the future
        self.connect("destroy", Gtk.main_quit)

        # Call the input creations
        self.inputGrid = self.__createInputs()
        # The draw area for the cairo canvas
        self.darea = Gtk.DrawingArea()

        # Grid for holding the drawing area (right) and the inputs
        self.grid = Gtk.Grid()
        self.grid.add(self.inputGrid)
        self.grid.add(self.darea)
        
        self.add(self.grid)

        # Show everything on the window
        self.show_all()

        #def expose(self, widget, event):

    # Main loop
    def start(self):
        Gtk.main()

    # Method for setting all the inputs in the window
    # TODO: -Move the box to a grid
    #       -Add labels to everything
    #       -Figure a way to have a default value for the ComboBox
    def __createInputs(self):
        vgrid = Gtk.Grid()
        vgrid.set_orientation(Gtk.Orientation.VERTICAL)

        # Speed of fracture
        self.speedEntry = Gtk.Entry()
        self.speedEntry.set_text("Speed of fractures")
        vgrid.add(self.speedEntry)

        # Size of... something.
        self.sizeEntry = Gtk.Entry()
        self.sizeEntry.set_text("Size")
        vgrid.add(self.sizeEntry)

        # Distance of source?
        self.distanceEntry = Gtk.Entry()
        self.distanceEntry.set_text("Distance")
        vgrid.add(self.distanceEntry)
        
        # Number of sources
        self.sourceNumber = Gtk.Entry()
        self.sourceNumber.set_text("Sources number")
        vgrid.add(self.sourceNumber)

        domainStore = Gtk.ListStore(str, str)
        domainStore.append(['circ', 'Circle'])
        domainStore.append(['rect', 'Rectangle'])

        # Domain combo box
        self.domain = Gtk.ComboBox.new_with_model(domainStore)
        self.domain.connect("changed", self.onSelectionChange)
        renderer = Gtk.CellRendererText()
        self.domain.pack_start(renderer, True)
        self.domain.add_attribute(renderer, "text", 1)
        
        vgrid.add(self.domain)

        # Start algorithm button
        startButton = Gtk.Button.new_with_label("Start")
        startButton.connect("clicked", self.startAlgorithm)
        self.runSpinner = Gtk.Spinner()
        #table = Gtk.Grid()
        #table.attach(startButton, 1, 0, 1, 1)
        #table.attach(self.runSpinner, 1, 2, 2, 3)
        # The button stays at the end
        #vgrid.pack_end(self.runSpinner, False, False, False)
        #vgrid.pack_end(startButton, False, False, False)
        vgrid.add(startButton)
        vgrid.add(self.runSpinner)

        # End of function
        return vgrid
        
    # What to do when the selection changes in the list of domain options
    def onSelectionChange(self, combo):
        treeiter = combo.get_active_iter()
        if treeiter != None:
            model = combo.get_model()
            print("Selected:",model[treeiter][0])

    # This function will call the algorithm
    def startAlgorithm(self, button):
        # Remember in the future to stop spinning
        self.runSpinner.start()
        print("At this point, the algorithm will be executed.")
        
