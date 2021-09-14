"""
Created on Tuesday 7th September,2021
Version: Beta

A Snip and translate tool for Programmers - This program enables users to snip
                                            portions of screen, grab text from it and translate to spanish

@author: Sattwik
"""

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QComboBox, QLabel, QPushButton, QGroupBox, QShortcut,QLineEdit
import tkinter as tk
import sys
from PIL import ImageGrab
import easyocr
import os
import cv2
import numpy as np
from translate import Translator

class Communicate(QObject):
  snip_saved = pyqtSignal()

class MyWindow(QMainWindow):
  def __init__(self):
    super(MyWindow, self).__init__()
    self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    self.setGeometry(0,0,400,300)
    self.setWindowTitle("Abhilipi")
    self.initUI()

  def initUI(self):
    self.shortcut_open = QShortcut(QKeySequence('Ctrl+Q'), self)
    self.shortcut_open.activated.connect(self.on_open)
    self.activateWindow()
    self.label = QtWidgets.QLabel(self)
    self.label.setText("Welcome to Abhilipi!")
    self.label.move(50,50)
    self.update()
    

    self.b1 = QtWidgets.QPushButton(self)
    self.b1.setText("Snip and Translate")
    self.b1.adjustSize()
    self.b1.clicked.connect(self.bclicked)

  def on_open(self):
    print('Ctrl Q fired')
    msg = 'Blank msg'
    self.snipWin = SnipWidget()
    self.snipWin.show()
    self.update()


  def bclicked(self):
    self.snipWin = SnipWidget()
    self.snipWin.show()
    self.update()

  def update(self):
    self.label.adjustSize()


class SnipWidget(QMainWindow):

  notification_signal = pyqtSignal()

  def __init__(self):
    super(SnipWidget, self).__init__()
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    self.label2 = QtWidgets.QLabel(self)
    self.setGeometry(0,0, screen_width, screen_height)
    self.setWindowTitle(' ')
    self.begin = QtCore.QPoint()
    self.end = QtCore.QPoint()
    self.setWindowOpacity(0.3)
    self.is_snipping = False
    QtWidgets.QApplication.setOverrideCursor(
      QtGui.QCursor(QtCore.Qt.CrossCursor)
      )
    self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    self.c = Communicate()
    self.c.snip_saved.connect(self.GrabTxt)

  def paintEvent(self, event):
    if self.is_snipping:
      brush_color = (0,0,0,0)
      lw = 0
      opacity = 0
    else:
      brush_color = (128,128,255,128)
      lw = 3
      opacity = 0.30

    self.setWindowOpacity(opacity)
    qp = QtGui.QPainter(self)
    qp.setPen(QtGui.QPen(QtGui.QColor('black'),lw))
    qp.setBrush(QtGui.QColor(*brush_color))
    qp.drawRect(QtCore.QRect(self.begin,self.end))

  def keyPressEvent(self, event):
    if event.key() == QtCore.Qt.Key_Escape:
      print('Quit')
      QtWidgets.QApplication.restoreOverrideCursor();
      self.notification_signal.emit()
      self.close()

  def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

  def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

  def mouseReleaseEvent(self, event):
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        self.is_snipping = True        
        self.repaint()
        QtWidgets.QApplication.processEvents()
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.is_snipping = False
        self.repaint()
        QtWidgets.QApplication.processEvents()
        img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        self.snipped_image = img
        QtWidgets.QApplication.restoreOverrideCursor();
        self.c.snip_saved.emit()
        self.close()
        self.msg = 'snip complete'
        self.notification_signal.emit()
        
  def GrabTxt(self):
        img = self.snipped_image
        output = reader.readtext(img)
        

        final_txt = ' '
        transfer_txt = ' '

        for detection in output:
          read_txt = detection[1]
          final_txt = final_txt + '\n' + read_txt
        
       
        transfer_txt = self.tran_txt(final_txt)
        
        self.msg = QMessageBox()
        self.msg.setWindowTitle('Abhilipi- The Translation tool')
        self.msg.setText(final_txt)
        self.msg.setInformativeText('Click on Show Details to view the German translation')
        self.msg.setDetailedText(transfer_txt)
        self.msg.exec_()

  def tran_txt(self,orig):
        
        translator = Translator(to_lang="German")
        trans_txt  = translator.translate(orig)

        return trans_txt

       


def window():
  app = QApplication(sys.argv)
  win = MyWindow()
  win.show()
  sys.exit(app.exec())



reader = easyocr.Reader(['en'])
window()

