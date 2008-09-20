#!/usr/bin/python

#  Copyright (c) 2003-2004, 2008 Janne Blomqvist

#  Langton is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.

#  Langton is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with Langton.  If not, see <http://www.gnu.org/licenses/>.

__version__ = "Revision: 2.0 "


import random
import numpy as npy 
import numpy.random as nrand
import sys
import wx
from bufferedwindow import *

NORTH=0
EAST=1
SOUTH=2
WEST=3

class Grid(object):
    "Grid for the ants to move on"
    
    def __init__(self,n,colors):
        "Init the nxn index grid "
        self.grid = npy.zeros((n,n), dtype=npy.int8)
        # Init nxnx3 RGB grid
        self.cgrid = npy.zeros((n,n,3),npy.uint8)
        self.colors = colors
        self.cgrid[:,:]= self.colors[0]

        # Index vector for periodic boundary conditions
        __foo = list(range(n))
        __foo.append(n-1)
        __foo.insert(0,0)
        self.index = npy.array(__foo)

    def _get_n(self):
        return self.grid.shape[0]

    def _set_n(self, val):
        raise AttributeError, "Can't set attribute n."

    def _del_n(self):
        raise AttributeError, "Can't delete attribute n."

    n = property(_get_n, _set_n, _del_n, "Grid size.")

    def getColor(self,pos_x, pos_y):
        "return color value of a grid point"
        return self.grid[pos_x,pos_y]

    def setColor(self,pos_x,pos_y, color):
        "set the color value of a grid point"
        self.grid[pos_x,pos_y] = color
        self.cgrid[pos_x,pos_y,:] = self.colors[color]

    def printGrid(self, event=None):
        "print the grid"
        print self.grid
        #print "Now comes the color values:\n"
        #print self.cgrid
    

class Ant(object):
    "Represents an ant that moves around on the grid"

    def __init__(self, grid, config):
        "Init the ant"
        self.grid = grid
        self.config = config
        self.pos_x = random.randrange(0,self.grid.n)
        self.pos_y = random.randrange(0,self.grid.n)
        self.heading = random.randrange(0,4) # north, east etc.
        self.color = nrand.permutation(config["numColors"])
        self.dir = nrand.randint(0,4,config["numColors"])


    def run(self):
        "Run the ant for one timestep"
        # Which color is the current grid cell?
        currentcolor = self.grid.getColor(self.pos_x,self.pos_y)
        # Now, change the color of the grid cell according to program
        self.grid.setColor(self.pos_x,self.pos_y,self.color[currentcolor])
        # And move ant in the direction specified in its program
        # First decide which direction to turn to
        
        self.heading = (self.heading + self.dir[currentcolor]) % 3
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
class LangtonCanvas(BufferedWindow):
    """The canvas where the ants move around"""
    def __init__(self, parent, ID, config=None):

        #self.bitmap.SetUserScale(width/GRIDSIZE, height/GRIDSIZE)
        self.parent = parent

        self.working = False
        self.set_config(config)

        BufferedWindow.__init__(self, parent, ID)
        #self.SetClientSize(wx.Size(width, height))

    def set_config(self, config):
        """Update the config."""
        restartwork = False
        if self.working:
            self.working = False
            restartwork = True
        self.config = config
        # Set up colors (random)
        self.colors = nrand.randint(0, 256, config["numColors"] * 3) \
                .astype(npy.uint8).reshape(config["numColors"], 3)

        # Init the Grid
        self.grid = Grid(config["gridSize"], self.colors)

        # Init ants
        self.ant = []
        for nant in xrange(config["numAnts"]):
            self.ant.append(Ant(self.grid, config))

        if restartwork:
            self.working = True


    def OnStart(self, event):
        if not self.working:
            self.working = True
            self.parent.SetStatusText("Simulation running!")
            while 1:
                wx.Yield()
                if not self.working:
                    break
                for ii in xrange(10):
                    for oneant in self.ant:
                        oneant.run()
                    self.UpdateDrawing()

    def OnStop(self, event):
        if self.working:
            self.working = False
            self.parent.SetStatusText("Simulation stopped!")

    def Draw(self,dc):
        #dc.BeginDrawing()
        dc.Clear()
        array = self.grid.cgrid
        image = wx.EmptyImage(self.config["gridSize"],self.config["gridSize"])
        image.SetData(array.tostring())
        w, h = self.GetClientSizeTuple()
        image.Rescale(w,h)
        bitmap = image.ConvertToBitmap()
        dc.DrawBitmap(bitmap,0,0,False)
        #dc.EndDrawing()


class SetupDialog(wx.Dialog):
    """Dialog for the user to configure the simulation"""
    def __init__(self, parent, config):
        wx.Dialog.__init__(self, parent, -1, "Setup", wx.DefaultPosition, wx.Size(100,150), wx.DIALOG_MODAL, "LangtonSetupDialog")
        self.parent = parent
        self.numColText = wx.StaticText(self, -1, "Number of colors: ", wx.Point(10,10), wx.DefaultSize, wx.ALIGN_LEFT)
        self.numColControl = wx.TextCtrl(self, -1, str(config["numColors"]), wx.Point(150,10), wx.DefaultSize)
        self.numAntsText = wx.StaticText(self, -1, "Number of ants: ", wx.Point(10,50), wx.DefaultSize, wx.ALIGN_LEFT)
        self.numAntsControl = wx.TextCtrl(self, -1, str(config["numAnts"]), wx.Point(150,50), wx.DefaultSize)
        self.gridSizeText = wx.StaticText(self, -1, "Gridsize: ", wx.Point(10,90), wx.DefaultSize, wx.ALIGN_LEFT)
        self.gridSizeControl = wx.TextCtrl(self, -1, str(config["gridSize"]), wx.Point(150,90), wx.DefaultSize)
        okButton = wx.Button(self, wx.ID_OK, "Ok", wx.Point(50,130), wx.DefaultSize)
        self.Bind(wx.EVT_BUTTON, self.OnOk, okButton)
        cancelButton = wx.Button(self, wx.ID_CANCEL, "Cancel", wx.Point(140, 130), wx.DefaultSize)
        self.SetAutoLayout(True)
        self.Centre(wx.BOTH)
        self.Layout()
        self.Fit()
        #sz = self.GetClientSize()
        #self.SetClientSize(wx.Size(100, 150))
        self.Show(True)

    def OnOk(self, event):
        """User pressed ok button, destroy the dialog and reset simulation"""
        # read values from the text controls and set config dict
        config = {}
        config["numColors"] = int(self.numColControl.GetValue())
        config["numAnts"] = int(self.numAntsControl.GetValue())
        config["gridSize"] = int(self.gridSizeControl.GetValue())
        # Cannot simply create new canvas, because events are bound to the old one!
        # So instead of creating a new canvas, call the constructor again!
        #self.parent.canvas.__init__(self.parent, -1, config = self.config)
        self.parent.canvas.set_config(config)
        self.EndModal(wx.ID_OK)


class Frame(wx.Frame):
    def __init__(self, parent,ID, title):
        wx.Frame.__init__(self,parent,ID,title,wx.DefaultPosition,size = (300,350))
        self.CreateStatusBar()
        self.SetStatusText("Langtons ant")

        # Set some default values for the configuration
        config = {"numColors": 2, "numAnts": 10, "gridSize": 100}
        self.canvas = LangtonCanvas(self, -1, config=config)

        filemenu = wx.Menu()
        item = filemenu.Append(wx.ID_SAVE, "&Save", "Save to file")
        self.Bind(wx.EVT_MENU, self.saveToFile, item)
        item = filemenu.Append(wx.ID_EXIT, "E&xit", "Terminate program")
        self.Bind(wx.EVT_MENU, self.OnExit, item)

        editmenu = wx.Menu()
        item = editmenu.Append(wx.ID_SETUP, "&Setup", "Configure the simulation") 
        self.Bind(wx.EVT_MENU, self.OnSetup, item)

        simumenu = wx.Menu()
        item = simumenu.Append(-1, "S&tart", "Start the simulation")
        self.Bind(wx.EVT_MENU, self.canvas.OnStart, item)
        item = simumenu.Append(wx.ID_STOP, "Sto&p", "Stop the simulation")
        self.Bind(wx.EVT_MENU, self.canvas.OnStop, item)
        item = simumenu.Append(-1, "&Debug", "Print debug information")
        self.Bind(wx.EVT_MENU, self.printConfig, item)

        helpmenu = wx.Menu()
        item = helpmenu.Append(wx.ID_ABOUT, "&About",
                    "More info about program")
        self.Bind(wx.EVT_MENU, self.OnAbout, item)

        #menu.AppendSeparator()

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        menuBar.Append(simumenu, "&Simulation")
        menuBar.Append(helpmenu, "&Help")
        self.SetMenuBar(menuBar)

        self.Centre(wx.BOTH)


    def printConfig(self, event):
        """Print config information"""
        print self.canvas.config

    def saveToFile(self, event):
        """ Save the generated picture to a file. """
        dlg = wx.FileDialog(self, "Choose a file name to save the image as a PNG to",
                           defaultDir = "", defaultFile = "", wildcard = "*.png", style=wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.canvas.SaveToFile(dlg.GetPath(), wx.BITMAP_TYPE_PNG)
        dlg.Destroy()
        
    def OnSetup(self, event):
        """Launch the setup dialog"""
        dlg = SetupDialog(self, self.canvas.config)
        dlg.ShowModal()
        dlg.Destroy()
        

    def OnAbout(self, event):
        message = "This is Langtons ant.\nVersion: " + __version__[10:-1]
        dlg = wx.MessageDialog(self, message , "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        self.canvas.working = False
        self.Close(True)

class Langton(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers() # So we can save PNG image
        frame = Frame(None, -1, "Langtons ant")
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = Langton(0)
app.MainLoop()
