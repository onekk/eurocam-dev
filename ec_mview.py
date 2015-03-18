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
        

        self.labx = QtGui.QLabel(self.tW)
        self.labx.setText('X')
        self.labx.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)        
        self.laby = QtGui.QLabel(self.tW)
        self.laby.setText('Y')
        self.laby.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)          
        self.labz = QtGui.QLabel(self.tW)
        self.labz.setText('Z')         
        self.labz.setAlignment(QtCore.Qt.AlignCenter|QtCore.Qt.AlignVCenter)
        
        self.lminx = QtGui.QLabel(self.tW)
        self.lminx.setText(self.desc[0])
        self.lminy = QtGui.QLabel(self.tW)
        self.lminy.setText(self.desc[0])          
        self.lminz = QtGui.QLabel(self.tW)
        self.lminz.setText(self.desc[0])         

        
        self.lmaxx = QtGui.QLabel(self.tW)
        self.lmaxx.setText(self.desc[1])
        self.lmaxy = QtGui.QLabel(self.tW)
        self.lmaxy.setText(self.desc[1])          
        self.lmaxz = QtGui.QLabel(self.tW)
        self.lmaxz.setText(self.desc[1])          

        self.ldimx = QtGui.QLabel(self.tW)
        self.ldimx.setText(self.desc[2])
        self.ldimx.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)        
        self.ldimy = QtGui.QLabel(self.tW)
        self.ldimy.setText(self.desc[2])
        self.ldimy.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)           
        self.ldimz = QtGui.QLabel(self.tW)
        self.ldimz.setText(self.desc[2])
        self.ldimz.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)         

     
        self.valx = QtGui.QLineEdit(self.tW)
        self.valx.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.valy = QtGui.QLineEdit(self.tW)
        self.valy.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.valz = QtGui.QLineEdit(self.tW)
        self.valz.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

        self.vmx = QtGui.QLineEdit(self.tW)
        self.vmx.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.vmy = QtGui.QLineEdit(self.tW)
        self.vmy.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.vmz = QtGui.QLineEdit(self.tW)
        self.vmz.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

        self.vMx = QtGui.QLineEdit(self.tW)
        self.vMx.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.vMy = QtGui.QLineEdit(self.tW)
        self.vMy.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.vMz = QtGui.QLineEdit(self.tW)
        self.vMz.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

        # create and places the units label 

        self.labu = QtGui.QLabel(self.tW)
        self.labu.setText('units = {0}'.format("mm"))

        self.tL.addWidget(self.labu, 0, 0, 1, 3)


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
        self.vLW.setGeometry(QtCore.QRect(0, 116, 781, 31))
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
        self.but6 = QtGui.QPushButton(self.vLW)
        self.but6.setText(' X +')           
        self.but7 = QtGui.QPushButton(self.vLW)
        self.but7.setText(' X -')           
        self.but8 = QtGui.QPushButton(self.vLW)
        self.but8.setText(' Y +')           
        self.but9 = QtGui.QPushButton(self.vLW)
        self.but9.setText(' Y -')           
        self.but10 = QtGui.QPushButton(self.vLW)
        self.but10.setText(' Z +')           
        self.but11 = QtGui.QPushButton(self.vLW)
        self.but11.setText(' Z -')           
        
        self.vL.addWidget(self.but1)
        self.vL.addWidget(self.but2) 
        self.vL.addWidget(self.but3)
        self.vL.addWidget(self.but4)
        self.vL.addWidget(self.but5)
        self.vL.addWidget(self.but6)
        self.vL.addWidget(self.but7)        
        self.vL.addWidget(self.but8)
        self.vL.addWidget(self.but9)
        self.vL.addWidget(self.but10)
        self.vL.addWidget(self.but11)
        
        # create the bottom zone with the graphic window

        self.vLW2 = QtGui.QWidget(self)
        self.vLW2.setGeometry(QtCore.QRect(0, 150, 781, 491))
        self.vLW2.setObjectName("vLW2")
        self.vL2 = QtGui.QVBoxLayout(self.vLW2)
        self.vL2.setContentsMargins(5, 5, 5, 5)
        self.vL2.setObjectName("vL2")

        self.Figure = plot.GetFigureClass()
        self.fig = self.Figure(self.vLW2)
        self.vL2.addWidget(self.fig._widget)
        
        #set the actions of the window

        self.but1.pressed.connect(self.camX)
        self.but2.pressed.connect(self.camY)
        self.but3.pressed.connect(self.camZ)
        self.but4.pressed.connect(self.camO)        
        self.but5.pressed.connect(self.showData)        
        self.but6.pressed.connect(self.incX)
        self.but7.pressed.connect(self.decX)
        self.but8.pressed.connect(self.incY)
        self.but9.pressed.connect(self.decY)
        self.but10.pressed.connect(self.incZ)
        self.but11.pressed.connect(self.decZ)
        
        # Show window

        self.resize(780, 600)
        self.setWindowTitle('EuroCAM - Model View')
        self.show()


 
    def load_data(self,filename): 
        self.surf = vv.meshRead(filename)
        self.Plot(self.surf)
        dimx,dimy,dimz = self.getBB(self.t)
        self.vmx.setText("{0:6.3f}".format(dimx.min))
        self.vmy.setText("{0:6.3f}".format(dimy.min))
        self.vmz.setText("{0:6.3f}".format(dimz.min))
        self.vMx.setText("{0:6.3f}".format(dimx.max))
        self.vMy.setText("{0:6.3f}".format(dimy.max))
        self.vMz.setText("{0:6.3f}".format(dimz.max))    
        
        xdim = dimx.max - dimx.min        
        ydim = dimy.max - dimy.min
        zdim = dimz.max - dimz.min 
        
        # set the wp dims as those in the model
        
        #self.wp((dimx,dimy,dimz))
        
        self.valx.setText("{0:6.3f}".format(xdim))        
        self.valy.setText("{0:6.3f}".format(ydim))
        self.valz.setText("{0:6.3f}".format(zdim))                 
        
#    def set_wp(self):
        self.wpxmin = dimx.min         
        self.wpxmax = dimx.max 
        self.wpymin = dimy.min         
        self.wpymax = dimy.max 
        self.wpzmin = dimz.min         
        self.wpzmax = dimz.max
        
        # set the offset of the workpiece 
        self.wpox = 0
        self.wpoy = 0
        self.wpoz = 0        

        self.wpx = self.wpxmax - self.wpxmin
        self.wpy = self.wpymax - self.wpymin        
        self.wpz = self.wpzmax - self.wpzmin
        
        self.draw_wp(self.cube((0,0,0)))

    def draw_wp(self,pp):
        self.wp = vv.Line(self.a,pp)
        self.wp.lw = 2
        self.wp.lc = (0.1,0.5,0.0)
        self.wp.visible = True
       
    def Plot(self,surf):
        
        # Make sure our figure is the active one. 
        # If only one figure, this is not necessary.
        #vv.figure(self.fig.nr)

        # Clear it
        vv.clf()

        vv.xlabel('x axis')
        vv.ylabel('y axis')
        vv.zlabel('z axis')
        
        # plot the model
        
        self.t = vv.mesh(surf)
        self.t.edgeColor = (0,0.05,0.05)
        self.t.faceColor = (0,0.8,0.8)
        self.t.specular = 0.2        
        self.t.faceShading = 'smooth'
        self.t.edgeShading = None        
        
        # Get axes and set camera to orthographic mode (with a field of view of 70)
        self.a = vv.gca()
        self.a.axis.showGrid = True
        self.a.axis.showMinorGrid = True
        self.a.axis.axisColor = (0.5,0,0.5)
        self.a.camera.fov = 45
        self.a.light0.ambient = 0.7 # 0.2 is default for light 0
        self.a.light0.diffuse = 1.0 # 1.0 is default

        # TODO control the lights and turn on one when in z projecton 
        # The other lights are off by default and are positioned at the origin
        #light1 = self.a.lights[1]
        #light1.On()
        #light1.ambient = 0.2 # 0.0 is default for other lights
        #light1.color = (0.1,0.1,0.1) # this light is red        

        #vv.legend(['this is a line'])        
        self.fig.DrawNow()

    def getBB(self,obj):
        dims =  obj._GetLimits()
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
        self.a.camera.azimuth = 0.0
        self.a.camera.elevation = 90.0
        self.a.camera.roll = 0.0            

    def camO(self):         
        self.a.camera.azimuth = -10.0
        self.a.camera.elevation = 30.0
        self.a.camera.roll = 0.0            

 
    def cube(self,dims):
        pp = vv.Pointset(3)
        pp.append(0,0,0)
        pp.append(dims[0],0,0)
        pp.append(dims[0],dims[1],0)
        pp.append(0,dims[1],0)
        pp.append(0,0,0) 
        pp.append(0,0,dims[2])
        pp.append(dims[0],0,dims[2])
        pp.append(dims[0],dims[1],dims[2])
        pp.append(0,dims[1],dims[2])
        pp.append(0,0,dims[2])        

        return pp
        
     
    def incX(self):
        self.wpx = self.wpx + 5
        pp = self.cube((self.wpx,self.wpy,self.wpz))
        self.wp.visible = False
        self.draw_wp(pp)

        
    def decX(self):
        self.wpx = self.wpx - 5
        pp = self.cube((self.wpx,self.wpy,self.wpz))
        self.wp.visible = False        
        self.draw_wp(pp)    

    def incY(self):
        self.wpy = self.wpy + 5
        pp = self.cube((self.wpx,self.wpy,self.wpz))
        self.wp.visible = False
        self.draw_wp(pp)

        
    def decY(self):
        self.wpy = self.wpy - 5
        pp = self.cube((self.wpx,self.wpy,self.wpz))
        self.wp.visible = False        
        self.draw_wp(pp)    

    def incZ(self):
        self.wpz = self.wpz + 5
        pp = self.cube((self.wpx,self.wpy,self.wpz))
        self.wp.visible = False
        self.draw_wp(pp)

        
    def decZ(self):
        self.wpz = self.wpz - 5
        pp = self.cube((self.wpx,self.wpy,self.wpz))
        self.wp.visible = False        
        self.draw_wp(pp)    


if __name__ == "__main__":
    # The visvis way. Will run in interactive mode when used in IEP or IPython.
    plot.Create()
    m = ModelWindow()
    filename = "./stl/pycam-textbox.stl"    
    m.load_data(filename)
    plot.Run()