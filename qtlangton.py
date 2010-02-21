# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'langton.ui'
#
# Created: Sun Feb 21 18:26:16 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Langton(object):
    def setupUi(self, Langton):
        Langton.setObjectName("Langton")
        Langton.resize(650, 600)
        Langton.setMinimumSize(QtCore.QSize(250, 100))
        self.centralwidget = QtGui.QWidget(Langton)
        self.centralwidget.setMinimumSize(QtCore.QSize(300, 200))
        self.centralwidget.setObjectName("centralwidget")
        self.canvas = QtGui.QGraphicsView(self.centralwidget)
        self.canvas.setGeometry(QtCore.QRect(0, 0, 256, 192))
        self.canvas.setObjectName("canvas")
        Langton.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(Langton)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 650, 30))
        self.menubar.setObjectName("menubar")
        self.menuMainmenu = QtGui.QMenu(self.menubar)
        self.menuMainmenu.setObjectName("menuMainmenu")
        self.menuEdit_menu = QtGui.QMenu(self.menubar)
        self.menuEdit_menu.setObjectName("menuEdit_menu")
        self.menuSimu_menu = QtGui.QMenu(self.menubar)
        self.menuSimu_menu.setObjectName("menuSimu_menu")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        Langton.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(Langton)
        self.statusbar.setObjectName("statusbar")
        Langton.setStatusBar(self.statusbar)
        self.actionSave = QtGui.QAction(Langton)
        self.actionSave.setObjectName("actionSave")
        self.actionQuit = QtGui.QAction(Langton)
        self.actionQuit.setObjectName("actionQuit")
        self.actionSetup = QtGui.QAction(Langton)
        self.actionSetup.setObjectName("actionSetup")
        self.actionStart = QtGui.QAction(Langton)
        self.actionStart.setObjectName("actionStart")
        self.actionStop = QtGui.QAction(Langton)
        self.actionStop.setObjectName("actionStop")
        self.actionAbout = QtGui.QAction(Langton)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAbout_Qt = QtGui.QAction(Langton)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.menuMainmenu.addAction(self.actionSave)
        self.menuMainmenu.addAction(self.actionQuit)
        self.menuEdit_menu.addAction(self.actionSetup)
        self.menuSimu_menu.addAction(self.actionStart)
        self.menuSimu_menu.addAction(self.actionStop)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menubar.addAction(self.menuMainmenu.menuAction())
        self.menubar.addAction(self.menuEdit_menu.menuAction())
        self.menubar.addAction(self.menuSimu_menu.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(Langton)
        QtCore.QMetaObject.connectSlotsByName(Langton)

    def retranslateUi(self, Langton):
        Langton.setWindowTitle(QtGui.QApplication.translate("Langton", "Langton", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMainmenu.setTitle(QtGui.QApplication.translate("Langton", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit_menu.setTitle(QtGui.QApplication.translate("Langton", "&Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuSimu_menu.setTitle(QtGui.QApplication.translate("Langton", "&Simulation", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("Langton", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("Langton", "&Save", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("Langton", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("Langton", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("Langton", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSetup.setText(QtGui.QApplication.translate("Langton", "Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStart.setText(QtGui.QApplication.translate("Langton", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStop.setText(QtGui.QApplication.translate("Langton", "Stop", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("Langton", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_Qt.setText(QtGui.QApplication.translate("Langton", "About Qt", None, QtGui.QApplication.UnicodeUTF8))

