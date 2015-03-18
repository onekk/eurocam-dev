# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 14:21:10 2015

@author: carlo-m
"""

from PySide import QtGui, QtCore

class Ui_ModelWindow(object):
    def setupUi(self, ModelWindow):
        ModelWindow.setObjectName("ModelWindow")
        
        ModelWindow.resize(780, 600)
     
        #create the top zone holding the x,y,z

        self.tW = QtGui.QWidget(self)
        self.tW.setGeometry(QtCore.QRect(0, 0, 781, 116))
        self.tW.setObjectName("tW")

        # create a grid layout

        self.tL = QtGui.QGridLayout(self.tW)
        self.tL.setContentsMargins(5, 5, 5, 5)
        self.tL.setObjectName("TL")
        self.tL.setColumnMinimumWidth(4, 10)

        self.desc =("Min.","Max.","Dim.")        

        font = QtGui.QFont()
        font.setPointSize(9)          

        self.labx = QtGui.QLabel(self.tW)
        self.laby = QtGui.QLabel(self.tW)
        self.labz = QtGui.QLabel(self.tW)
        self.lminx = QtGui.QLabel(self.tW)
        self.lminy = QtGui.QLabel(self.tW)
        self.lminz = QtGui.QLabel(self.tW)
        self.lmaxx = QtGui.QLabel(self.tW)        
        self.lmaxy = QtGui.QLabel(self.tW)
        self.lmaxz = QtGui.QLabel(self.tW)        
        self.ldimx = QtGui.QLabel(self.tW)
        self.ldimy = QtGui.QLabel(self.tW)        
        self.ldimz = QtGui.QLabel(self.tW)

        for obj in (self.labx,self.laby,self.labz,self.lminx, self.lminy, 
                    self.lminz, self.lmaxx, self.lmaxy, self.lmaxz, self.ldimx,
                    self.ldimy, self.ldimz):
            obj.setFont(font)            

        
        
        self.labx.setText('X')
        self.laby.setText('Y')
        self.labz.setText('Z')

        for obj in (self.labx, self.laby, self.labz):
            obj.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)        
      

        self.lminx.setText(self.desc[0])
        self.lminy.setText(self.desc[0])          
        self.lminz.setText(self.desc[0])         
        

        self.lmaxx.setText(self.desc[1])
        self.lmaxy.setText(self.desc[1])          
        self.lmaxz.setText(self.desc[1])          


        self.ldimx.setText(self.desc[2])
        self.ldimy.setText(self.desc[2])
        self.ldimz.setText(self.desc[2])

        for obj in (self.ldimx, self.ldimy, self.ldimz):        
            obj.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)        

     
        self.valx = QtGui.QLabel(self.tW)
        self.valy = QtGui.QLabel(self.tW)
        self.valz = QtGui.QLabel(self.tW)
        self.vmx = QtGui.QLabel(self.tW)
        self.vmy = QtGui.QLabel(self.tW)
        self.vmz = QtGui.QLabel(self.tW)
        self.vMx = QtGui.QLabel(self.tW)
        self.vMy = QtGui.QLabel(self.tW)        
        self.vMz = QtGui.QLabel(self.tW)


        for obj in (self.valx,self.valy,self.valz,self.vmx,self.vmy,self.vmz,
                    self.vMx,self.vMy,self.vMz):        
            obj.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            #obj.setReadOnly(True)        
            obj.setFont(font)
        
        # create and places the units label 

        self.labu = QtGui.QLabel(self.tW)
        self.labu.setText('units = {0}'.format("mm"))

        self.tL.addWidget(self.labu, 3, 0, 1, 1)


        # create the lines defining the zone in the grid

        self.line = QtGui.QFrame(self.tW)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        
        self.line1 = QtGui.QFrame(self.tW)
        self.line1.setFrameShape(QtGui.QFrame.VLine)
        self.line1.setFrameShadow(QtGui.QFrame.Sunken)
        self.line1.setObjectName("line1")       

        self.line2 = QtGui.QFrame(self.tW)
        self.line2.setFrameShape(QtGui.QFrame.VLine)
        self.line2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line2.setObjectName("line2")

        # place the lines in the grid

        self.tL.addWidget(self.line, 1, 0, 1, 15)
        self.tL.addWidget(self.line1, 1, 5, 4, 1)
        self.tL.addWidget(self.line2, 1, 10, 4, 1)       

        # place the content of the grid 

        # X values
        
        self.tL.addWidget(self.labx, 2, 1, 1, 4)

        self.tL.addWidget(self.lminx, 3, 1, 1, 1)
        self.tL.addWidget(self.vmx, 3, 2, 1, 1)        
        self.tL.addWidget(self.lmaxx, 3, 3, 1, 1)        
        self.tL.addWidget(self.vMx, 3, 4, 1, 1) 
        self.tL.addWidget(self.ldimx, 4, 2, 1, 1)
        self.tL.addWidget(self.valx, 4, 3, 1 ,2)

        # Y values
    
        self.tL.addWidget(self.laby, 2, 6, 1, 4)

        self.tL.addWidget(self.lminy,3, 6, 1, 1)
        self.tL.addWidget(self.vmy, 3, 7, 1, 1)
        self.tL.addWidget(self.lmaxy, 3, 8, 1 ,1)
        self.tL.addWidget(self.vMy, 3, 9, 1, 1)
        self.tL.addWidget(self.ldimy, 4, 7, 1, 1)          
        self.tL.addWidget(self.valy, 4, 8, 1, 2)

      
        # Z values
      
        self.tL.addWidget(self.labz, 2, 11, 1, 4)
        
        self.tL.addWidget(self.lminz, 3, 11, 1, 1)
        self.tL.addWidget(self.vmz, 3, 12, 1, 1)
        self.tL.addWidget(self.lmaxz, 3, 13, 1 ,1)
        self.tL.addWidget(self.vMz, 3, 14, 1, 1)
        self.tL.addWidget(self.ldimz, 4, 12, 1, 1)         
        self.tL.addWidget(self.valz, 4, 13, 1, 2)         


        # create the central zone with buttons


         
        self.vLW = QtGui.QWidget(self)
        self.vLW.setGeometry(QtCore.QRect(0, 116, 781, 101))
        self.vLW.setObjectName("vLW")
        self.vL = QtGui.QGridLayout(self.vLW)
        self.vL.setContentsMargins(5, 5, 5, 5)
        self.vL.setObjectName("vL")
       

        self.line3 = QtGui.QFrame(self.vLW)
        self.line3.setFrameShape(QtGui.QFrame.HLine)
        self.line3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line3.setObjectName("line3")
        
        self.line4 = QtGui.QFrame(self.vLW)
        self.line4.setFrameShape(QtGui.QFrame.VLine)
        self.line4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line4.setObjectName("line4")       


        self.but1 = QtGui.QPushButton(self.vLW)
        self.but1.setText('X')  
        self.but2 = QtGui.QPushButton(self.vLW)
        self.but2.setText('Y')
        self.but3 = QtGui.QPushButton(self.vLW)
        self.but3.setText('Z')
        self.but4 = QtGui.QPushButton(self.vLW)
        self.but4.setText('Ortho')                      
        self.but5 = QtGui.QPushButton(self.vLW)
        self.but5.setText('Show')           
        # WP dimension
        self.but6 = QtGui.QPushButton(self.vLW)
        self.but6.setText("X +")
        self.but7 = QtGui.QPushButton(self.vLW)
        self.but7.setText('X -')           
        self.but8 = QtGui.QPushButton(self.vLW)
        self.but8.setText('Y +')           
        self.but9 = QtGui.QPushButton(self.vLW)
        self.but9.setText('Y -')           
        self.but10 = QtGui.QPushButton(self.vLW)
        self.but10.setText('Z +')           
        self.but11 = QtGui.QPushButton(self.vLW)
        self.but11.setText('Z -')                  
        # WP Translate Buttons
        self.but12 = QtGui.QPushButton(self.vLW)
        self.but12.setText('X +')           
        self.but13 = QtGui.QPushButton(self.vLW)
        self.but13.setText('X -')           
        self.but14 = QtGui.QPushButton(self.vLW)
        self.but14.setText('Y +')           
        self.but15 = QtGui.QPushButton(self.vLW)
        self.but15.setText('Y -')           
        self.but16 = QtGui.QPushButton(self.vLW)
        self.but16.setText('Z +')           
        self.but17 = QtGui.QPushButton(self.vLW)
        self.but17.setText('Z -')                          

        for obj in (self.but6, self.but7, self.but12, self.but13):
            obj.setStyleSheet("color: red")
            
        for obj in (self.but8, self.but9, self.but14, self.but15):
            obj.setStyleSheet("color: green")

        for obj in (self.but10, self.but11, self.but16, self.but17):
            obj.setStyleSheet("color: blue")            
        
        self.vL.addWidget(self.but1, 1, 0, 1, 1)
        self.vL.addWidget(self.but2, 1, 1, 1, 1) 
        self.vL.addWidget(self.but3, 1, 2, 1, 1)
        self.vL.addWidget(self.but4, 1, 3, 1, 1)
        self.vL.addWidget(self.but5, 1, 4, 1, 1)
        self.vL.addWidget(self.line3, 2 , 0 , 1, 12)
        self.vL.addWidget(self.line4, 2 , 5 , 4, 1)

        #add WP translation buttons
        self.vL.addWidget(self.but12, 4, 3, 1, 1)
        self.vL.addWidget(self.but13, 4, 1, 1, 1)        
        self.vL.addWidget(self.but14, 3, 2, 1, 1)
        self.vL.addWidget(self.but15, 5, 2, 1, 1)
        self.vL.addWidget(self.but16, 4, 4, 1, 1)
        self.vL.addWidget(self.but17, 5, 4, 1, 1)

        # Add WP dimension buttons        
        self.vL.addWidget(self.but6, 4, 9, 1, 1)
        self.vL.addWidget(self.but7, 4, 7, 1, 1)        
        self.vL.addWidget(self.but8, 3, 8, 1, 1)
        self.vL.addWidget(self.but9, 5, 8, 1, 1)
        self.vL.addWidget(self.but10, 4, 11, 1, 1)
        self.vL.addWidget(self.but11, 5, 11, 1, 1)

        
        # create the bottom zone with the graphic window

        self.vLW2 = QtGui.QWidget(self)
        self.vLW2.setGeometry(QtCore.QRect(0, 225, 781, 391))
        self.vLW2.setObjectName("vLW2")
        self.vL2 = QtGui.QVBoxLayout(self.vLW2)
        self.vL2.setContentsMargins(0, 0, 0, 0)
        self.vL2.setObjectName("vL2")
        
        QtCore.QMetaObject.connectSlotsByName(ModelWindow)
