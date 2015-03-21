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
        self.tW.setGeometry(QtCore.QRect(0, 0, 781, 101))
        self.tW.setObjectName("tW")

        # create a grid layout

        self.tL = QtGui.QGridLayout(self.tW)
        self.tL.setContentsMargins(2,2,2,2)
        self.tL.setObjectName("TL")
        self.tL.setColumnMinimumWidth(0, 0)
        self.tL.setVerticalSpacing(3)
        self.tL.setHorizontalSpacing(3)

        # create the central zone with buttons
        
        self.vLW = QtGui.QWidget(self)
        self.vLW.setGeometry(QtCore.QRect(0, 100, 781, 91))
        self.vLW.setObjectName("vLW")
        self.vL = QtGui.QGridLayout(self.vLW)
        self.vL.setContentsMargins(5, 5, 5, 5)
        self.vL.setObjectName("vL")
        self.vL.setVerticalSpacing(2)
        self.vL.setHorizontalSpacing(2)
       
        # create the bottom zone with the graphic window

        self.vLW2 = QtGui.QWidget(self)
        self.vLW2.setGeometry(QtCore.QRect(0, 190, 781, 391))
        self.vLW2.setObjectName("vLW2")
        self.vL2 = QtGui.QVBoxLayout(self.vLW2)
        self.vL2.setContentsMargins(0, 0, 0, 0)
        self.vL2.setObjectName("vL2")


        font = QtGui.QFont()
        font.setPointSize(9)          

        ###################
        #                 #
        # Populate the tW #
        #                 #
        ###################

        self.labx = QtGui.QLabel(self.tW)
        self.laby = QtGui.QLabel(self.tW)
        self.labz = QtGui.QLabel(self.tW)

        self.lwpx = QtGui.QLabel(self.tW)
        self.lwpy = QtGui.QLabel(self.tW)
        self.lwpz = QtGui.QLabel(self.tW)

        self.lmin = QtGui.QLabel(self.tW)
        self.lmax = QtGui.QLabel(self.tW)        
        self.ldim = QtGui.QLabel(self.tW)
        self.loff = QtGui.QLabel(self.tW)
 

        for obj in (self.lmin, self.lmax, self.ldim, self.loff):
            obj.setFont(font)            


        self.labx.setText('Model X')
        self.laby.setText('Model Y')
        self.labz.setText('Model Z')
        self.lwpx.setText('WP X')
        self.lwpy.setText('WP Y')
        self.lwpz.setText('WP Z')
        self.lmin.setText('Min.')
        self.lmax.setText('Max')
        self.ldim.setText('Dim')        
        self.loff.setText('Offset')    

                 
    
        self.valx = QtGui.QLabel(self.tW)
        self.valy = QtGui.QLabel(self.tW)
        self.valz = QtGui.QLabel(self.tW)
        self.vmx = QtGui.QLabel(self.tW)
        self.vmy = QtGui.QLabel(self.tW)
        self.vmz = QtGui.QLabel(self.tW)
        self.vMx = QtGui.QLabel(self.tW)
        self.vMy = QtGui.QLabel(self.tW)        
        self.vMz = QtGui.QLabel(self.tW)

        # wp data

        self.vwpx = QtGui.QLabel(self.tW)
        self.vwpy = QtGui.QLabel(self.tW)
        self.vwpz = QtGui.QLabel(self.tW)
        self.vwpmx = QtGui.QLabel(self.tW)
        self.vwpmy = QtGui.QLabel(self.tW)
        self.vwpmz = QtGui.QLabel(self.tW)
        self.vwpMx = QtGui.QLabel(self.tW)
        self.vwpMy = QtGui.QLabel(self.tW)        
        self.vwpMz = QtGui.QLabel(self.tW)
        self.vwpox = QtGui.QLabel(self.tW)
        self.vwpoy = QtGui.QLabel(self.tW)
        self.vwpoz = QtGui.QLabel(self.tW)


        
        for obj in (self.labx, self.laby, self.labz,
                    self.lwpx, self.lwpy, self.lwpz,
                    self.valx, self.valy, self.valz,
                    self.vmx, self. vmy, self.vmz,
                    self.vMx,self.vMy,self.vMz,
                    self.vwpx, self.vwpy, self.vwpz,
                    self.vwpmx, self.vwpmy, self.vwpmz,
                    self.vwpMx, self.vwpMy, self.vwpMz,
                    self.vwpox, self.vwpoy, self.vwpoz):
                        
            obj.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
            obj.setFont(font)
        
        # create the lines defining the zone in the grid

        self.line1 = QtGui.QFrame(self.tW)
        self.line1.setFrameShape(QtGui.QFrame.HLine)
        self.line1.setObjectName("line1")
        
        
        self.sep1 = QtGui.QFrame(self.tW)
        self.sep2 = QtGui.QFrame(self.tW)
        self.sep3 = QtGui.QFrame(self.tW)
        self.sep4 = QtGui.QFrame(self.tW)
        self.sep5 = QtGui.QFrame(self.tW)
        self.sep6 = QtGui.QFrame(self.tW)
        self.sep7 = QtGui.QFrame(self.tW)
        
        for obj in (self.sep1, self.sep2, self.sep3, self.sep4, self.sep5,
                    self.sep6,self.sep7):
            obj.setFrameShape(QtGui.QFrame.VLine)

        for obj in (self.line1, self.sep1, self.sep2,
                    self.sep3, self.sep4, self.sep5, self.sep6, self.sep7): 
            obj.setFrameShadow(QtGui.QFrame.Sunken)


        # place the lines in the grid

        self.tL.addWidget(self.line1, 2, 0, 1, 15)        
        self.tL.addWidget(self.sep1, 1, 2, 7, 1)
        self.tL.addWidget(self.sep2, 1, 6, 7, 1)
        self.tL.addWidget(self.sep3, 1, 10, 7, 1)
        self.tL.addWidget(self.sep4, 1, 4, 7, 1)
        self.tL.addWidget(self.sep5, 1, 8, 7, 1)
        self.tL.addWidget(self.sep6, 1, 12, 7, 1)
        self.tL.addWidget(self.sep7, 1, 14, 7, 1)        
        #self.tL.addWidget(self.line2, 8, 0, 1, 15)
        
        # place the content of the grid 

       
        self.tL.addWidget(self.lmin, 3, 1, 1, 1)
        self.tL.addWidget(self.lmax, 4, 1, 1, 1)
        self.tL.addWidget(self.ldim, 5, 1, 1, 1)
        self.tL.addWidget(self.loff, 6, 1, 1, 1)
        
        # X values

        self.tL.addWidget(self.labx, 1, 3, 1, 1)         
        self.tL.addWidget(self.vmx, 3, 3, 1, 1)        
        self.tL.addWidget(self.vMx, 4, 3, 1, 1) 
        self.tL.addWidget(self.valx, 5, 3, 1 ,1)

        # Y values
    
        self.tL.addWidget(self.laby, 1, 7, 1, 1)
        self.tL.addWidget(self.vmy, 3, 7, 1, 1)
        self.tL.addWidget(self.vMy, 4, 7, 1, 1)
        self.tL.addWidget(self.valy, 5, 7, 1, 1)

      
        # Z values
      
        self.tL.addWidget(self.labz, 1, 11, 1, 1)
        self.tL.addWidget(self.vmz, 3, 11, 1, 1)
        self.tL.addWidget(self.vMz, 4, 11, 1, 1)
        self.tL.addWidget(self.valz, 5, 11, 1, 1)         


        # WP values

        # X values

        self.tL.addWidget(self.lwpx, 1, 5, 1, 1)        
        self.tL.addWidget(self.vwpmx, 3, 5, 1, 1)        
        self.tL.addWidget(self.vwpMx, 4, 5, 1, 1) 
        self.tL.addWidget(self.vwpx, 5, 5, 1 ,1)
        self.tL.addWidget(self.vwpox, 6, 5, 1 ,1)
        
        # Y values

        self.tL.addWidget(self.lwpy, 1, 9, 1, 1)     
        self.tL.addWidget(self.vwpmy, 3, 9, 1, 1)
        self.tL.addWidget(self.vwpMy, 4, 9, 1, 1)
        self.tL.addWidget(self.vwpy, 5, 9, 1, 1)
        self.tL.addWidget(self.vwpoy, 6, 9, 1, 1)
        
        # Z values

        self.tL.addWidget(self.lwpz, 1, 13, 1, 1)         
        self.tL.addWidget(self.vwpmz, 3, 13, 1, 1)
        self.tL.addWidget(self.vwpMz, 4, 13, 1, 1)
        self.tL.addWidget(self.vwpz, 5, 13, 1, 1)         
        self.tL.addWidget(self.vwpoz, 6, 13, 1, 1) 
        

        #Create the visuals buttons 

        self.but1 = QtGui.QPushButton(self.tW)
        self.but1.setText('X')  
        self.but2 = QtGui.QPushButton(self.tW)
        self.but2.setText('Y')
        self.but3 = QtGui.QPushButton(self.tW)
        self.but3.setText('Z')
        self.but4 = QtGui.QPushButton(self.tW)
        self.but4.setText('Ortho')                      
        self.but5 = QtGui.QPushButton(self.tW)
        self.but5.setText('Show')           

        self.but1b = QtGui.QPushButton(self.tW)
        self.but1b.setText('X back')  
        self.but2b = QtGui.QPushButton(self.tW)
        self.but2b.setText('Y back')
        self.but3b = QtGui.QPushButton(self.tW)
        self.but3b.setText('Z back')

        self.tL.addWidget(self.but1, 3, 15, 1, 1)         
        self.tL.addWidget(self.but2, 4, 15, 1, 1)
        self.tL.addWidget(self.but3, 5, 15, 1, 1)

        self.tL.addWidget(self.but1b, 3, 16, 1, 1)         
        self.tL.addWidget(self.but2b, 4, 16, 1, 1)
        self.tL.addWidget(self.but3b, 5, 16, 1, 1)        

        self.tL.addWidget(self.but4, 6, 15, 1, 1)
        self.tL.addWidget(self.but5, 6, 16, 1, 1)
        
        ####################
        #                  #
        # Populate the vLW #
        #                  #
        ####################
        
        self.lwinc = QtGui.QLabel(self.vLW)        
        self.lwoff = QtGui.QLabel(self.vLW)
        self.lvinc = QtGui.QLabel(self.vLW)
        self.lvinc.setFont(font)
        self.lvinc.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        
        for obj in (self.lwinc,self.lwoff):
            obj.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
            obj.setFont(font)
            
        self.lwinc.setText('Workpiece Dimensions')        
        self.lwoff.setText('Workpiece Offset')

            
        self.line4 = QtGui.QFrame(self.vLW)
        self.line4.setFrameShape(QtGui.QFrame.HLine)
        self.line4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line4.setObjectName("line4")
        
        self.line5 = QtGui.QFrame(self.vLW)
        self.line5.setFrameShape(QtGui.QFrame.VLine)
        self.line5.setFrameShadow(QtGui.QFrame.Sunken)
        self.line5.setObjectName("line5")       

        self.line6 = QtGui.QFrame(self.vLW)
        self.line6.setFrameShape(QtGui.QFrame.VLine)
        self.line6.setFrameShadow(QtGui.QFrame.Sunken)
        self.line6.setObjectName("line6")       

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
        self.but18 = QtGui.QPushButton(self.vLW)
        self.but18.setText('Off. 0')                          

        self.butzi = QtGui.QPushButton(self.tW)
        self.butzi.setText('Zoom +')  
        self.butzd = QtGui.QPushButton(self.tW)
        self.butzd.setText('Zoom -')
        self.butz0 = QtGui.QPushButton(self.tW)
        self.butz0.setText('Zoom 0')

        self.butincn = QtGui.QPushButton(self.tW)
        self.butincn.setText('Inc R')  
        self.butincf = QtGui.QPushButton(self.tW)
        self.butincf.setText('Inc +')
        self.butincs = QtGui.QPushButton(self.tW)
        self.butincs.setText('Inc -')

        #TODO aggiungere botton per resettare le dimensioni e 
        # modificare il funzionamento di offset0

        for obj in (self.butzi, self.butzd, self.butz0, self.butincn, 
                    self.butincf, self.butincs ):
            obj.setFont(font)


        for obj in (self.but6, self.but7, self.but12, self.but13):
            obj.setStyleSheet("color: red")
            obj.setFont(font)
            
        for obj in (self.but8, self.but9, self.but14, self.but15):
            obj.setStyleSheet("color: green")
            obj.setFont(font)
            
        for obj in (self.but10, self.but11, self.but16, self.but17):
            obj.setStyleSheet("color: blue")            
            obj.setFont(font)
            
        self.vL.addWidget(self.line4, 0 , 0 , 1, 14)
        self.vL.addWidget(self.line5, 0 , 6 , 5, 1)
        self.vL.addWidget(self.line6, 0 , 8 , 5, 1)

        # add the labels and the offset value

        self.vL.addWidget(self.lwinc, 1, 9, 1, 3)
        self.vL.addWidget(self.lwoff, 1, 2, 1, 3)
        self.vL.addWidget(self.lvinc, 1, 7, 1, 1)


        # add the zoom buttons 

        self.vL.addWidget(self.butzi, 2, 14, 1, 1)
        self.vL.addWidget(self.butz0, 3, 14, 1, 1)        
        self.vL.addWidget(self.butzd, 4, 14, 1, 1)         

        # add the increment buttons

        self.vL.addWidget(self.butincn, 3, 7, 1, 1)
        self.vL.addWidget(self.butincf, 2, 7, 1, 1)        
        self.vL.addWidget(self.butincs, 4, 7, 1, 1)         

        
        #add WP translation buttons
        self.vL.addWidget(self.but12, 3, 4, 1, 1)
        self.vL.addWidget(self.but13, 3, 2, 1, 1)        
        self.vL.addWidget(self.but14, 2, 3, 1, 1)
        self.vL.addWidget(self.but15, 4, 3, 1, 1)
        self.vL.addWidget(self.but16, 2, 5, 1, 1)
        self.vL.addWidget(self.but17, 4, 5, 1, 1)
        self.vL.addWidget(self.but18, 3, 3, 1, 1)
        
        # Add WP dimension buttons        
        self.vL.addWidget(self.but6, 3, 11, 1, 1)
        self.vL.addWidget(self.but7, 3, 9, 1, 1)        
        self.vL.addWidget(self.but8, 2, 10, 1, 1)
        self.vL.addWidget(self.but9, 4, 10, 1, 1)
        self.vL.addWidget(self.but10, 2, 12, 1, 1)
        self.vL.addWidget(self.but11, 4, 12, 1, 1)


        
        QtCore.QMetaObject.connectSlotsByName(ModelWindow)
