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

        border = 5
        #self.inputSpace = width - n - 2*border
        
        # Title and window stuff
        self.set_border_width(border)
        self.set_title("Fractures")
        self.resize(width,height)
        self.set_position(Gtk.WindowPosition.CENTER)

        # Maybe this should be more complex in the future
        self.connect("destroy", self.__quit)

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

    # Function to finish the program
    def __quit(self, button=None):
        Gtk.main_quit()
        
    # Main loop
    def start(self):
        Gtk.main()

    # Method for setting all the inputs in the window
    # TODO: -Move the box to a grid
    #       -Add labels to everything
    #       -Figure a way to have a default value for the ComboBox
    def __createInputs(self):
        # Grid which holds the elements of the interface
        vgrid = Gtk.Grid()
        vgrid.set_orientation(Gtk.Orientation.VERTICAL)

        # Dictionary which holds the widgets, as the entries
        # TODO: evaluate whether to keep the entries as dictionary only
        #       or as members of the class
        self.inputsDict = {}
        
        # A nice example picture
        # TODO: get a smaller picture
        from gi.repository import GdkPixbuf
        imageName = './img/img1.png'
        imageBuff = GdkPixbuf.Pixbuf.new_from_file_at_scale(imageName,
                                                            width=200,
                                                            height=200,
                                                            preserve_aspect_ratio=True)
        image = Gtk.Image()
        image.set_from_pixbuf(imageBuff)
        vgrid.add(image)

        # Size of... something.
        sizeLabel = Gtk.Label("Size")
        self.sizeEntry = Gtk.Entry()
        self.sizeEntry.set_text("Size")
        self.inputsDict["size"] = self.sizeEntry
        vgrid.add(sizeLabel)
        vgrid.add(self.sizeEntry)
        
        # Stroke width, whatever that is
        self.strokeWidth = Gtk.Entry()
        self.strokeWidth.set_text("Stroke")
        self.inputsDict["stroke"] = self.strokeWidth
        vgrid.add(Gtk.Label("Stroke width"))
        vgrid.add(self.strokeWidth)

        # Speed of fracture
        speedLabel = Gtk.Label("Speed")
        self.speedEntry = Gtk.Entry()
        self.speedEntry.set_text("Speed of fractures")
        self.inputsDict["speed"] = self.speedEntry
        vgrid.add(speedLabel)
        vgrid.add(self.speedEntry)

        # Distance of source?
        distanceLabel = Gtk.Label("Distance")
        self.distanceEntry = Gtk.Entry()
        self.distanceEntry.set_text("Distance")
        self.inputsDict["distance"] = self.distance
        vgrid.add(distanceLabel)
        vgrid.add(self.distanceEntry)
        
        # Number of sources
        sourceLabel = Gtk.Label("Number of sources")
        self.sourceNumber = Gtk.Entry()
        self.sourceNumber.set_text("Sources number")
        self.inputsDict["source"] = self.sourceNumber
        vgrid.add(sourceLabel)
        vgrid.add(self.sourceNumber)

        # Frequency information
        #separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        self.frequency = Gtk.Entry()
        self.frequency.set_text("Frequency")
        self.inputsDict["frequency"] = self.frequency

        self.freqDim = Gtk.Entry()
        self.freqDim.set_text("Diminishing")
        self.inputsDict["freqDim"] = self.freqDim
        
        #vgrid.add(separator)
        vgrid.add(Gtk.Label("Frequency of fractures"))
        vgrid.add(self.frequency)
        vgrid.add(Gtk.Label("Frequency diminishing"))
        vgrid.add(self.freqDim)

        ########################################
        # Domain selection
        domainLabel = Gtk.Label("Domain")
        domainStore = Gtk.ListStore(str, str)
        domainStore.append(['circ', 'Circle'])
        domainStore.append(['rect', 'Rectangle'])

        # Domain combo box
        self.domain = Gtk.ComboBox.new_with_model(domainStore)
        self.domain.connect("changed", self.onSelectionChange)
        renderer = Gtk.CellRendererText()
        self.domain.pack_start(renderer, True)
        self.domain.add_attribute(renderer, "text", 1)
        # Set default value
        self.domain.set_active(0)
        vgrid.add(domainLabel)
        vgrid.add(self.domain)

        # Start algorithm button
        startButton = Gtk.Button.new_with_label("Start")
        startButton.connect("clicked", self.startAlgorithm)
        self.runSpinner = Gtk.Spinner()

        vgrid.add(startButton)
        vgrid.add(self.runSpinner)

        # Close button, just in case
        closeButton = Gtk.Button.new_with_label("Close")
        closeButton.connect("clicked", self.__quit)
        vgrid.add(closeButton)
        
        # End of function
        return vgrid
        
    # What to do when the selection changes in the list of domain options
    def onSelectionChange(self, combo):
        treeiter = combo.get_active_iter()
        if treeiter != None:
            model = combo.get_model()
            print("Selected:", model[treeiter][0])

    # This function will call the algorithm
    def startAlgorithm(self, button):
        # Remember in the future to stop spinning
        self.runSpinner.start()
        print("At this point, the algorithm will be executed.")
        
