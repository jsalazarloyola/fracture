#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gi
gi.require_version('Gtk', '3.0')

from iutils.render import Render
from gi.repository import Gtk

from gui.widgets import NumberEntry

class MainApp(Gtk.Window, Render):
    """Main window for the program

    This is the main view of the program, where every control is present,
    as buttons and text boxes.

    """
    def __init__(self,
                 front, back, light,
                 step=None,
                 width=1200, height=700):
        # Window initialization
        Gtk.Window.__init__(self)

        """Front line colors"""
        self.front = front
        """Light color

        Check if this nomenclature is correct
        """
        self.light = light
        
        # Render initialization
        """Size of the drawing area (pixels)"""
        self.dareaSize = int(height*0.9)
        """Width of the drawing lines"""
        self.linewidth = 1.1/self.dareaSize
        
        Render.__init__(self, self.dareaSize, front, back)

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
        """Grid that holds all the input data"""
        self.inputGrid = self.__createInputs()
        """Drawing area for the Cairo canvas"""
        self.darea = Gtk.DrawingArea()

        # Grid for holding the drawing area (right) and the inputs
        """Grid that holds the input data and the drawing area"""
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
                                                            width=150,
                                                            height=150,
                                                            preserve_aspect_ratio=True)
        image = Gtk.Image()
        image.set_from_pixbuf(imageBuff)
        vgrid.add(image)

        ########################################
        # Inputs as entries
        # Number of sources
        sourceLabel = Gtk.Label("Number of sources")
        self.sourceNumber = NumberEntry()
        self.sourceNumber.set_text("20000")
        self.inputsDict["sources"] = self.sourceNumber
        vgrid.add(sourceLabel)
        vgrid.add(self.sourceNumber)

        # Size of the used region
        sizeLabel = Gtk.Label("Size")
        self.sizeEntry = NumberEntry()
        self.sizeEntry.set_text("0.45")
        self.inputsDict["size"] = self.sizeEntry
        vgrid.add(sizeLabel)
        vgrid.add(self.sizeEntry)
         
        # Minimum distance between sources
        distanceLabel = Gtk.Label("Distance")
        self.distanceEntry = NumberEntry()
        self.distanceEntry.set_text(str(2/self.dareaSize))
        self.inputsDict["distance"] = self.distanceEntry
        vgrid.add(distanceLabel)
        vgrid.add(self.distanceEntry)
        
        # # Stroke width, whatever that is
        # self.strokeWidth = NumberEntry()
        # self.strokeWidth.set_text("Stroke")
        # self.inputsDict["stroke"] = self.strokeWidth
        # vgrid.add(Gtk.Label("Stroke width"))
        # vgrid.add(self.strokeWidth)

        ########################################
        # Frequency information
        # Speed of fracture
        self.speedEntry = NumberEntry()
        self.speedEntry.set_text("1.0")
        self.inputsDict["speed"] = self.speedEntry

        self.speedDiminish = NumberEntry()
        self.speedDiminish.set_text("0.997")
        self.inputsDict["speedDiminish"] = self.speedDiminish

        self.spawnDim = NumberEntry()
        self.spawnDim.set_text("0.9")
        self.inputsDict["spawnDim"] = self.spawnDim
        
        vgrid.add(Gtk.Label("Fracture speed"))
        vgrid.add(self.speedEntry)
        vgrid.add(Gtk.Label("Speed diminishing"))
        vgrid.add(self.speedDiminish)
        vgrid.add(Gtk.Label("Fracture spawn diminishing"))
        vgrid.add(self.spawnDim)

        ########################################
        # Spawn angle and factor
        self.spawnFactor = NumberEntry()
        self.spawnFactor.set_text("2.0")
        self.inputsDict["spawnFactor"] = self.spawnFactor

        self.spawnAngle = NumberEntry()
        self.spawnAngle.set_text("0.2")
        self.inputsDict["spawnAngle"] = self.spawnAngle

        vgrid.add(Gtk.Label("Spawn factor"))
        vgrid.add(self.spawnFactor)
        vgrid.add(Gtk.Label("Spawn angle"))
        vgrid.add(self.spawnAngle)
                
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

        ########################################
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
            self.domainSelection = model[treeiter][0]
            print("Selected:", model[treeiter][0])

    # This function will call the algorithm
    def startAlgorithm(self, button):
        # Remember in the future to stop spinning
        self.runSpinner.start()
        # All the fields will be disabled
        for key in self.inputsDict:
            self.inputsDict[key].set_editable(False)
            
        print("At this point, the algorithm will be executed.")
        self.setFractures()

        return

    # Sets the fractures, getting the information from the entries
    # And filling the blanks
    def setFractures(self):
        from modules.fracture import Fractures
        from fn import Fn
        fn = Fn(prefix='./res/',postfix='.2obj')

        fracDot = 0.85
        fracDst = 100./self.dareaSize
        fracStp = 2/self.dareaSize
        
        theFractures = Fractures(
            int(self.inputsDict["sources"]),
            float(self.inputsDict["size"]),
            float(self.inputsDict["distance"]),
            fracDot,
            fracDst,
            fracStp,
            float(self.inputsDict["speed"]),
            float(self.inputsDict["speedDiminish"]),
            float(self.inputsDict["spawnDim"]),
            self.domainSelection
        )

        # maybe this to logging.debug?
        print(theFractures.sources.shape)
        import numpy as np
        for _ in range(5):
            theFractures.blow(2, np.random.random(size=2))

        from gi.repository import GObject
        GObject.idle_add(self.step, theFractures, fn)
        return

    def step(self, theFractures, filename):
        spawnFactor = float(self.inputsDict["spawnFactor"])
        spawnAngle  = float(self.inputsDict["spawnAngle"])
        
        # if there are fractures remaining yet
        #fracturesRemaining = True
        #while fracturesRemaining:
        if not theFractures.i % 20:
            self.show(theFractures)
            self.write_to_png(filename.name()+'.png')

        theFractures.print_stats()
        fracturesRemaining = theFractures.step(dbg=False)
        spawned = theFractures.spawn_front(factor = spawnFactor,
                                               angle  = spawnAngle)
        print('spawned: {:d}'.format(spawned))
        self.expose()
        
        return fracturesRemaining

    ############################################################
    # Drawing functions for the canvas
    #
    # Function that draws the picture
    def expose(self):
        cairoFrame = self.darea.get_property('window').cairo_create()
        cairoFrame.set_source_surface(self.sur, 0, 0)
        cairoFrame.paint()
        return

    # Function to draw lines between sources, I pressume (addapted from main.py)
    # I don't know how to draw in Cairo, so I'm kind of blindfolded on this part.
    # TODO: Decide whether it's better that this were on its own drawer class, as
    #       a member of MainApp
    def drawLines(self, fractureSet, sources):
        for frac in fractureSet:
            start = frac.inds[0]
            self.ctx.move_to(*sources[start,:])
            for c in frac.inds[1:]:
                self.ctx.line_to(*sources[c,:])

            self.ctx.stroke()

        return

    def show(self, fractures):
        self.clear_canvas()
        # Draw twice, in order to give some blur effect
        # light, thick lines
        self.ctx.set_source_rgba(*self.light)
        self.ctx.set_line_width(3*self.linewidth)
        self.drawLines(fractures.alive_fractures+fractures.dead_fractures,
                       fractures.sources)

        # strong, thin lines
        self.ctx.set_source_rgba(*self.front)
        self.ctx.set_line_width(self.linewidth)
        self.drawLines(fractures.alive_fractures+fractures.dead_fractures,
                       fractures.sources)

        return

    
