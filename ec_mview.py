from PySide import QtGui, QtCore
backend = 'pyside'
import visvis as vv


# Create a visvis app instance, which wraps a qt4 application object.
# This needs to be done *before* instantiating the main window. 
plot = vv.use(backend)

class ModelWindow(QtGui.QWidget):
    def __init__(self, parent = None):
        super(ModelWindow,self).__init__(parent)
        #QtGui.QWidget.__init__(self, *args)
        
        # Make a panel with a button
        self.panel = QtGui.QWidget(self)

        self.tW = QtGui.QWidget(self)
        self.tW.setGeometry(QtCore.QRect(0, 0, 801, 61))
        self.tW.setObjectName("tW")
        self.tL = QtGui.QGridLayout(self.tW)
        self.tL.setContentsMargins(5, 5, 5, 5)
        self.tL.setObjectName("TL")
        
        #create the top label with dimensions
        self.labx = QtGui.QLabel(self.tW)
        self.labx.setText('Dim. X')
        self.laby = QtGui.QLabel(self.tW)
        self.laby.setText('Dim. Y')          
        self.labz = QtGui.QLabel(self.tW)
        self.labz.setText('Dim. Z')         
        
        self.valx = QtGui.QLineEdit(self.tW)
        self.valx.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.valy = QtGui.QLineEdit(self.tW)
        self.valy.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.valz = QtGui.QLineEdit(self.tW)
        self.valz.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

        self.dlabx = QtGui.QLabel(self.tW)
        self.dlabx.setText('mm')
        self.dlaby = QtGui.QLabel(self.tW)
        self.dlaby.setText('mm')          
        self.dlabz = QtGui.QLabel(self.tW)
        self.dlabz.setText('mm')         

       
        self.tL.addWidget(self.labx,1, 0, 1, 1)
        self.tL.addWidget(self.valx,1, 1, 1 ,1)
        self.tL.addWidget(self.dlabx,1, 2, 1, 1)
        self.tL.addWidget(self.laby, 1, 4, 1, 1)
        self.tL.addWidget(self.valy, 1, 5, 1, 1)
        self.tL.addWidget(self.dlaby, 1, 6, 1, 1)
      
        self.tL.addWidget(self.labz, 1, 8, 1, 1)
        self.tL.addWidget(self.valz, 1, 9, 1, 1,)         
        self.tL.addWidget(self.dlabz, 1, 10, 1, 1)


         
        self.vLW = QtGui.QWidget(self)
        self.vLW.setGeometry(QtCore.QRect(0, 60, 801, 31))
        self.vLW.setObjectName("vLW")
        self.vL = QtGui.QHBoxLayout(self.vLW)
        self.vL.setContentsMargins(5, 5, 5, 5)
        self.vL.setObjectName("vL")
       

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
        
        self.vL.addWidget(self.but1)
        self.vL.addWidget(self.but2) 
        self.vL.addWidget(self.but3)
        self.vL.addWidget(self.but4)
        self.vL.addWidget(self.but5)
        

        self.vLW2 = QtGui.QWidget(self)
        self.vLW2.setGeometry(QtCore.QRect(0, 90, 801, 511))
        self.vLW2.setObjectName("vLW2")
        self.vL2 = QtGui.QVBoxLayout(self.vLW2)
        self.vL2.setContentsMargins(5, 5, 5, 5)
        self.vL2.setObjectName("vL2")

        Figure = plot.GetFigureClass()
        self.fig = Figure(self.vLW2)
        self.vL2.addWidget(self.fig._widget)
        
        #set the actions of the window

        self.but1.pressed.connect(self.camX)
        self.but2.pressed.connect(self.camY)
        self.but3.pressed.connect(self.camZ)
        self.but4.pressed.connect(self.camO)        
        self.but5.pressed.connect(self.showData)        

        # Show window

        self.resize(800, 600)
        self.setWindowTitle('EuroCAM - Model View')
        self.show()


 
    def load_data(self,filename): 
        self.surf = vv.meshRead(filename)
        self.Plot(self.surf)
        dimx,dimy,dimz = self.getBB()
        self.valx.setText("{0:6.3f} - {1:6.3f}".format(dimx.min,dimx.max))        
        self.valy.setText("{0:6.3f} - {1:6.3f}".format(dimy.min,dimy.max))
        self.valz.setText("{0:6.3f} - {1:6.3f}".format(dimz.min,dimz.max))                 
        
        
    def Plot(self,surf):
        
        # Make sure our figure is the active one. 
        # If only one figure, this is not necessary.
        #vv.figure(self.fig.nr)

        # Clear it
        vv.clf()
        # show
        vv.xlabel('x axis')
        vv.ylabel('y axis')
        vv.zlabel('z axis')

        self.t = vv.mesh(surf)
        #t.color(0,0,1)


        # Get axes and set camera to orthographic mode (with a field of view of 70)
        self.a = vv.gca()
        self.a.axis.showGrid = True
        self.a.axis.showMinorGrid = True
        self.a.axis.axisColor = (0.5,0,0.5)
        self.a.camera.fov = 45

        #vv.legend(['this is a line'])        
        self.fig.DrawNow()

    def getBB(self):
        dims =  self.t._GetLimits()
        dimx,dimy,dimz = dims
        return dimx,dimy,dimz
        
    def showData(self):
        dims =  self.t._GetLimits()
        dimx,dimy,dimz = dims
        print "X min = ", dimx.min
        print "X max = ",dimx.max
        print dimy
        print dimz
        print self.a.camera.azimuth
        print self.a.camera.elevation
        print self.a.camera.roll                
        #print self.a.axis.lw

        
    def camX(self):
        self.a.camera.azimuth = 0.0
        self.a.camera.elevation = 0.0
        self.a.camera.roll = 0.0                
     
        
    def camY(self):         
        self.a.camera.azimuth = 90.0
        self.a.camera.elevation = 0.0
        self.a.camera.roll = 0.0           

    def camZ(self):         
        self.a.camera.azimuth = 90.0
        self.a.camera.elevation = 90.0
        self.a.camera.roll = 0.0            

    def camO(self):         
        self.a.camera.azimuth = -10.0
        self.a.camera.elevation = 30.0
        self.a.camera.roll = 0.0            

 
    def dummy():
        # Corners of a cube in relative coordinates
        self._corners = tmp = Pointset(3)
        tmp.append(0,0,0);  tmp.append(1,0,0);  tmp.append(0,1,0);
        tmp.append(0,0,1);  tmp.append(1,1,0);  tmp.append(1,0,1);
        tmp.append(0,1,1);  tmp.append(1,1,1);
        
        # Indices of the base corners for each dimension.
        # The order is very important, don't mess it up...
        self._cornerIndicesPerDirection = [ [0,2,6,3], [3,5,1,0], [0,1,4,2] ]
        # And the indices of the corresponding pair corners
        self._cornerPairIndicesPerDirection = [ [1,4,7,5], [6,7,4,2], [3,5,7,6] ]        


if __name__ == "__main__":
    # The visvis way. Will run in interactive mode when used in IEP or IPython.
    plot.Create()
    m = ModelWindow()
    filename = "./stl/pycam-textbox.stl"    
    m.load_data(filename)
    plot.Run()