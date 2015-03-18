from PySide import QtGui, QtCore
from modelview_ui import Ui_ModelWindow

backend = 'pyside'
import visvis as vv


# Create a visvis app instance, which wraps a qt4 application object.
# This needs to be done *before* instantiating the main window. 
plot = vv.use(backend)

class ModelWindow(QtGui.QMainWindow, Ui_ModelWindow):
        # maybe a spash screen goes here?
    def __init__(self, parent=None):
        super(ModelWindow, self).__init__(parent)
        self.setupUi(self)        
 
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

        self.but12.pressed.connect(self.triX)
        self.but13.pressed.connect(self.trdX)
        self.but14.pressed.connect(self.triY)
        self.but15.pressed.connect(self.trdY)
        self.but16.pressed.connect(self.triZ)
        self.but17.pressed.connect(self.trdZ)

        self.msg01 = '<span style="color:red">{0:6.3f}</span>'
        self.msg02 = '<span style="color:green">{0:6.3f}</span>'
        self.msg03 = '<span style="color:blue">{0:6.3f}</span>'
        
        self.show()       
        
 
    def load_data(self,filename): 
        self.surf = vv.meshRead(filename)
        self.Plot(self.surf)
        dimx,dimy,dimz = self.getBB(self.t)
        self.vmx.setText(self.msg01.format(dimx.min))
        self.vmy.setText(self.msg02.format(dimy.min))
        self.vmz.setText(self.msg03.format(dimz.min))
        self.vMx.setText(self.msg01.format(dimx.max))
        self.vMy.setText(self.msg02.format(dimy.max))
        self.vMz.setText(self.msg03.format(dimz.max))    
        
        xdim = dimx.max - dimx.min        
        ydim = dimy.max - dimy.min
        zdim = dimz.max - dimz.min 
        
        # set the wp dims as those in the model
        
        #self.wp((dimx,dimy,dimz))
        
        self.valx.setText(self.msg01.format(xdim))        
        self.valy.setText(self.msg02.format(ydim))
        self.valz.setText(self.msg03.format(zdim))                 
        
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
        
        self.draw_wp(self.cube((0,0,0),(self.wpox,self.wpoy,self.wpoz)))

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

 
    def cube(self,dims,offs):
        pp = vv.Pointset(3)
        pp.append(offs[0], offs[1], offs[2])
        pp.append(offs[0] + dims[0],offs[1],offs[2])
        pp.append(offs[0] + dims[0],offs[1] + dims[1],offs[2])
        pp.append(offs[0], offs[1] + dims[1],offs[2])
        pp.append(offs[0], offs[1], offs[2]) 
        pp.append(offs[0], offs[1], offs[2] + dims[2])
        pp.append(offs[0] + dims[0], offs[1], offs[2] + dims[2])
        pp.append(offs[0] + dims[0], offs[1] + dims[1], offs[2] + dims[2])
        pp.append(offs[0], offs[1] + dims[1], offs[2] + dims[2])
        pp.append(offs[0], offs[1], offs[2] + dims[2])        

        return pp


    def redraw_cube(self):
        pp = self.cube((self.wpx, self.wpy, self.wpz),
                       (self.wpox, self.wpoy,self.wpoz))
        self.wp.visible = False
        self.draw_wp(pp)        

     
    def incX(self):
        self.wpx = self.wpx + 5
        self.redraw_cube()
        
    def decX(self):
        self.wpx = self.wpx - 5
        self.redraw_cube()        


    def incY(self):
        self.wpy = self.wpy + 5
        self.redraw_cube()

        
    def decY(self):
        self.wpy = self.wpy - 5
        self.redraw_cube()
        
    def incZ(self):
        self.wpz = self.wpz + 5
        self.redraw_cube()        
        
    def decZ(self):
        self.wpz = self.wpz - 5
        self.redraw_cube()
        
    def triX(self):
        self.wpox = self.wpox + 5
        self.redraw_cube()
        
    def trdX(self):
        self.wpox = self.wpox - 5
        self.redraw_cube()        

    def triY(self):
        self.wpoy = self.wpoy + 5
        self.redraw_cube()
        
    def trdY(self):
        self.wpoy = self.wpoy - 5
        self.redraw_cube()
        
    def triZ(self):
        self.wpoz = self.wpoz + 5
        self.redraw_cube()        
        
    def trdZ(self):
        self.wpoz = self.wpoz - 5
        self.redraw_cube()        


if __name__ == "__main__":
    # The visvis way. Will run in interactive mode when used in IEP or IPython.
    plot.Create()
    m = ModelWindow()
    filename = "./stl/pycam-textbox.stl"    
    m.load_data(filename)
    plot.Run()