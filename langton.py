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

__version__ = "Revision: 3.0 "


import random
import numpy as np 
import numpy.random as nrand
import sys
from PyQt4 import QtGui, QtCore, QtOpenGL
from qtlangton import Ui_Langton

NORTH=0
EAST=1
SOUTH=2
WEST=3

class Grid(object):
    "Grid for the ants to move on"
    
    def __init__(self, n):
        "Init the nxn index grid "
        self.grid = np.zeros((n,n), dtype=np.uint8)

        # Index vector for periodic boundary conditions
        #__foo = list(range(n))
        #__foo.append(n-1)
        #__foo.insert(0,0)
        #self.index = np.array(__foo)

    def _get_n(self):
        return self.grid.shape[0]

    def _set_n(self, val):
        raise AttributeError, "Can't set attribute n."

    def _del_n(self):
        raise AttributeError, "Can't delete attribute n."

    n = property(_get_n, _set_n, _del_n, "Grid size.")

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
        currentcolor = self.grid.grid[self.pos_x, self.pos_y]
        # Now, change the color of the grid cell according to program
        self.grid.grid[self.pos_x, self.pos_y] = self.color[currentcolor]
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
class LangtonCanvas(object):
    """The canvas where the ants move around"""
    def __init__(self, parent, config=None, gl=False):

        self.parent = parent
        self.view = parent.ui.canvas # QGraphicsView

        self.working = False
        if not config:
            config = {"numColors": 2, "numAnts": 10, "gridSize": 300, 
                      "gl": gl}
        self.set_config(config)

    def set_config(self, config):
        """Update the config."""
        restartwork = False
        if self.working:
            self.working = False
            restartwork = True
        self.config = config
        # Set up colors (random)
        self.colors = nrand.randint(0, 256, config["numColors"] * 3) \
                .astype(np.uint8).reshape(config["numColors"], 3)

        # Init the Grid
        self.grid = Grid(config["gridSize"])

        # Init ants
        self.ants = []
        for nant in xrange(config["numAnts"]):
            self.ants.append(Ant(self.grid, config))

        # Init display
        if self.config['gl']:
            self.view.setViewport(QtOpenGL.QGLWidget())
        self.scene = QtGui.QGraphicsScene()
        self.scene.addPixmap(self.numpy2pixmap())
        self.view.setScene(self.scene)
        self.view.adjustSize()
        self.view.show()

        if restartwork:
            self.working = True

    def numpy2pixmap(self):
        g = self.grid.grid
        return QtGui.QPixmap.fromImage(QtGui.QImage(
                g.tostring(),
                g.shape[1],
                g.shape[0],
                QtGui.QImage.Format_Indexed8))

    def start(self):
        if not self.working:
            self.working = True
            self.parent.ui.statusbar.showMessage("Simulation running!")
            while 1:
                QtGui.QApplication.processEvents()
                if not self.working:
                    break
                for oneant in self.ants:
                    oneant.run()
                self.view.items()[0].setPixmap(self.numpy2pixmap())
                self.view.items()[0].update()

    def stop(self):
        if self.working:
            self.working = False
            self.parent.ui.statusbar.showMessage("Simulation stopped!")


class Langton(QtGui.QMainWindow):
    def __init__(self, parent=None, gl=False):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Langton()
        self.ui.setupUi(self)
        self.canvas = LangtonCanvas(self, gl=gl)
        self.resize(self.ui.canvas.size().width(), self.ui.canvas.size().height())
        self.connect(self.ui.actionQuit, QtCore.SIGNAL("triggered()"), 
                               self.quit_app)
        self.connect(self.ui.actionSave, QtCore.SIGNAL("triggered()"),
                     self.show_save_dialog)
        self.connect(self.ui.actionAbout, QtCore.SIGNAL("triggered()"),
                     self.show_about_dialog)
        self.connect(self.ui.actionAbout_Qt, QtCore.SIGNAL("triggered()"),
                     QtGui.QApplication.aboutQt)
        self.connect(self.ui.actionStart, QtCore.SIGNAL("triggered()"),
                     self.canvas.start)
        self.connect(self.ui.actionStop, QtCore.SIGNAL("triggered()"),
                     self.canvas.stop)

    def show_save_dialog(self):
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Save file')
        self.canvas.numpy2pixmap().save(filename)
        #file=open(filename)
        #data = file.read()

    def show_about_dialog(self):
        dlg = QtGui.QMessageBox(self)
        dlg.setText("PyQt Langton's ant %s" % __version__)
        dlg.addButton('Ok', QtGui.QMessageBox.AcceptRole)
        dlg.exec_()
        response = dlg.clickedButton()

    def quit_app(self):
        if self.canvas.working:
            self.canvas.stop()
        self.close()

def main(argv, gl):
    app = QtGui.QApplication(argv)
    my_app = Langton(gl=gl)
    my_app.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-g', '--gl', dest='gl', action='store_true', 
                      help='Use OpenGL')
    (options, args) = parser.parse_args()
    main(sys.argv, options.gl)
