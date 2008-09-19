#!/usr/bin/python

#  Copyright (c) 2003-2004 Janne Blomqvist

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

__version__ = "$Revision: 1.6 $"


import random,Numeric, RandomArray,sys
from wxPython.wx import *
from doubleBuffer import *

NORTH=0
EAST=1
SOUTH=2
WEST=3

FORWARD=0
RIGHT=1
BACK=3
LEFT=4

ID_ABOUT=101
ID_EXIT=102
ID_START=103
ID_STOP=104
ID_DEBUG=105
ID_SETUP=106
ID_SETUP_OK=107
ID_SAVEFILE=108

class Grid:
    "Grid for the ants to move on"
    
    def __init__(self,n,colours):
        "Init the nxn index grid "
        self.grid = Numeric.zeros((n,n), Numeric.Int8)
        # Init nxnx3 RGB grid
        self.cgrid = Numeric.zeros((n,n,3),Numeric.UnsignedInt8)
        self.n = n
        self.colours = colours
        self.cgrid[:,:]= self.colours[0]

        # Index vector for periodic boundary conditions
        self.__foo = list(range(n))
        self.__foo.append(n-1)
        self.__foo.insert(0,0)
        self.index = Numeric.array(self.__foo)

    def getColor(self,pos_x, pos_y):
        "return color value of a grid point"
        return self.grid[pos_x,pos_y]

    def setColor(self,pos_x,pos_y, colour):
        "set the color value of a grid point"
        self.grid[pos_x,pos_y] = colour
        self.cgrid[pos_x,pos_y,:] = self.colours[colour]

    def printGrid(self, event=None):
        "print the grid"
        print self.grid
        #print "Now comes the colour values:\n"
        #print self.cgrid
    

class Ant:
    "Represents an ant that moves around on the grid"

    def __init__(self, grid, config):
        "Init the ant"
        self.grid = grid
        self.config = config
        self.pos_x = random.randrange(0,self.grid.n)
        self.pos_y = random.randrange(0,self.grid.n)
        self.heading = random.randrange(0,4) # north, east etc.
        self.color = RandomArray.permutation(config["numColors"])
        self.dir = RandomArray.randint(0,4,config["numColors"])


    def run(self):
        "Run the ant for one timestep"
        # Which color is the current grid cell?
        self.currentcolor = self.grid.getColor(self.pos_x,self.pos_y)
        # Now, change the color of the grid cell according to program
        self.grid.setColor(self.pos_x,self.pos_y,self.color[self.currentcolor])
        # And move ant in the direction specified in its program
        self.move()
        
    def move(self):
        "Move ant"
        # First decide which direction to turn to

        self.heading = (self.heading + self.dir[self.currentcolor]) % 3
        #self.heading = self.heading % 3

        if (self.heading == NORTH):
            self.pos_y += 1
        elif (self.heading == EAST):
            self.pos_x += 1
        elif (self.heading == SOUTH):
            self.pos_y -= 1
        elif (self.heading == WEST):
            self.pos_x -= 1
        else:
            print "BIIG error\n"
            print self.heading
            sys.exit(0)
            
        # Finally, correct coordinates if they are over bounds
        self.pos_x = self.pos_x % self.config["gridSize"]
        self.pos_y = self.pos_y % self.config["gridSize"]


# Now the gui stuff
class LangtonCanvas(wxBufferedWindow):
    """The canvas where the ants move around"""
    def __init__(self, parent, ID, width=300, height=300, config=None):

#        self.bitmap.SetUserScale(width/GRIDSIZE, height/GRIDSIZE)
        self.parent = parent
        self.Width=width
        self.Height=height
        self.config = config

        # Set up colours (random)
        self.colours = Numeric.zeros((config["numColors"], 3), Numeric.UnsignedInt8)
        for i in range(0,3):
            self.colours[:,i] = (RandomArray.randint(0,255,config["numColors"])).astype(Numeric.UnsignedInt8)

        # Init the Grid
        self.grid = Grid(config["gridSize"], self.colours)

        # Init ants
        self.ant = []
        for nant in xrange(config["numAnts"]):
            self.ant.append(Ant(self.grid, config))

        self.working = 0
        wxBufferedWindow.__init__(self, parent, ID)
        self.SetSize(wxSize(width, height))

    def OnStart(self, event):
        if not self.working:
            self.working = 1
            self.parent.SetStatusText("Simulation running!")
            while 1:
                wxYield()
                if not self.working:
                    break
                for oneant in self.ant:
                    oneant.run()
                self.UpdateDrawing()

    def OnStop(self, event):
        if self.working:
            self.working = 0
            self.parent.SetStatusText("Simulation stopped!")

    def Draw(self,dc):
        dc.BeginDrawing()
        array = self.grid.cgrid
        self.image = wxEmptyImage(self.config["gridSize"],self.config["gridSize"])
        self.image.SetData(array.tostring())
        self.image.Rescale(self.Width,self.Height)
        self.bitmap = self.image.ConvertToBitmap()
        dc.DrawBitmap(self.bitmap,0,0,false)
        dc.EndDrawing()


class SetupDialog(wxDialog):
    """Dialog for the user to configure the simulation"""
    def __init__(self, parent, config):
        wxDialog.__init__(self, parent, -1, "Setup", wxDefaultPosition, wxSize(100,150), wxDIALOG_MODAL, "LangtonSetupDialog")
        self.config = config
        self.parent = parent
        self.numColText = wxStaticText(self, -1, "Number of colors: ", wxPoint(10,10), wxDefaultSize, wxALIGN_LEFT)
        self.numColControl = wxTextCtrl(self, -1, str(config["numColors"]), wxPoint(150,10), wxDefaultSize)
        self.numAntsText = wxStaticText(self, -1, "Number of ants: ", wxPoint(10,50), wxDefaultSize, wxALIGN_LEFT)
        self.numAntsControl = wxTextCtrl(self, -1, str(config["numAnts"]), wxPoint(150,50), wxDefaultSize)
        self.gridSizeText = wxStaticText(self, -1, "Gridsize: ", wxPoint(10,90), wxDefaultSize, wxALIGN_LEFT)
        self.gridSizeControl = wxTextCtrl(self, -1, str(config["gridSize"]), wxPoint(150,90), wxDefaultSize)
        self.okButton = wxButton(self, ID_SETUP_OK, "Ok", wxPoint(50,130), wxDefaultSize)
        EVT_BUTTON(self, ID_SETUP_OK, self.OnOk)
        self.cancelButton = wxButton(self, wxID_CANCEL, "Cancel", wxPoint(140, 130), wxDefaultSize)
        self.SetAutoLayout(true)
        self.Centre(wxBOTH)
        self.Layout()
        self.Fit()
        #sz = self.GetClientSize()
        #self.SetClientSize(wxSize(100, 150))
        self.Show(true)

    def OnOk(self, event):
        """User pressed ok button, destroy the dialog and reset simulation"""
        # read values from the text controls and set config dict
        self.config["numColors"] = int(self.numColControl.GetValue())
        self.config["numAnts"] = int(self.numAntsControl.GetValue())
        self.config["gridSize"] = int(self.gridSizeControl.GetValue())
        # Cannot simply create new canvas, because events are bound to the old one!
        # So instead of creating a new canvas, call the constructor again!
        self.parent.canvas.__init__(self.parent, -1, config = self.config)
        self.EndModal(wxID_OK)


class Frame(wxFrame):
    def __init__(self, parent,ID, title):
        wxFrame.__init__(self,parent,ID,title,wxDefaultPosition,wxSize(300,300))
        self.CreateStatusBar()
        self.SetStatusText("Langtons ant")

        filemenu = wxMenu()
        filemenu.Append(ID_SAVEFILE, "&Save", "Save to file")
        filemenu.Append(ID_EXIT, "E&xit", "Terminate program")

        editmenu = wxMenu()
        editmenu.Append(ID_SETUP, "&Setup", "Configure the simulation") 

        simumenu = wxMenu()
        simumenu.Append(ID_START, "S&tart", "Start the simulation")
        simumenu.Append(ID_STOP, "Sto&p", "Stop the simulation")
        simumenu.Append(ID_DEBUG, "&Debug", "Print debug information")

        helpmenu = wxMenu()
        helpmenu.Append(ID_ABOUT, "&About",
                    "More info about program")

#        menu.AppendSeparator()

        menuBar = wxMenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(simumenu, "&Simulation")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)

        self.Centre(wxBOTH)

        # Set some default values for the configuration
        self.config = {"numColors": 2, "numAnts": 10, "gridSize": 100}
        self.canvas = LangtonCanvas(self, -1, config=self.config)

        self.SetAutoLayout(true)
        self.Layout()
        self.Fit()
        sz = self.GetClientSize()
        self.SetClientSize(wxSize(sz.width-7, sz.height-14))

        EVT_MENU(self, ID_ABOUT, self.OnAbout)
        EVT_MENU(self, ID_EXIT, self.OnExit)
        EVT_MENU(self, ID_START, self.canvas.OnStart)
        EVT_MENU(self, ID_STOP, self.canvas.OnStop)
        EVT_MENU(self, ID_DEBUG, self.printConfig)
        EVT_MENU(self, ID_SETUP, self.OnSetup)
        EVT_MENU(self, ID_SAVEFILE, self.saveToFile)

    def printConfig(self, event):
        """Print config information"""
        print self.config

    def saveToFile(self, event):
        """ Save the generated picture to a file. """
        dlg = wxFileDialog(self, "Choose a file name to save the image as a PNG to",
                           defaultDir = "", defaultFile = "", wildcard = "*.png", style=wxSAVE)
        if dlg.ShowModal() == wxID_OK:
            self.canvas.SaveToFile(dlg.GetPath(), wxBITMAP_TYPE_PNG)
        dlg.Destroy()
        
    def OnSetup(self, event):
        """Launch the setup dialog"""
        dlg = SetupDialog(self, self.config)
        dlg.ShowModal()
        dlg.Destroy()
        

    def OnAbout(self, event):
        message = "This is Langtons ant.\nVersion: " + __version__[10:-1]
        dlg = wxMessageDialog(self, message , "About Me", wxOK | wxICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        self.Close(true)

class Langton(wxApp):
    def OnInit(self):
        wxInitAllImageHandlers() # So we can save PNG image
        frame = Frame(NULL, -1, "Langtons ant")
        frame.Show(true)
        self.SetTopWindow(frame)
        return true

app = Langton(0)
app.MainLoop()
