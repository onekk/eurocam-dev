from PySide import QtGui, QtCore
from ec_mview_ui import Ui_ModelWindow

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
        self.but1b.pressed.connect(self.camXb)
        self.but2b.pressed.connect(self.camYb)
        self.but3b.pressed.connect(self.camZb)        
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
        self.but18.pressed.connect(self.off0)        


        self.butzi.pressed.connect(self.zoominc)
        self.butzd.pressed.connect(self.zoomdec)
        self.butz0.pressed.connect(self.zoomreset)

        self.butincn.pressed.connect(self.incN)
        self.butincf.pressed.connect(self.incF)
        self.butincs.pressed.connect(self.incS)
        
        self.msg01 = '<span style="color:red">{0:6.3f}</span>'
        self.msg02 = '<span style="color:green">{0:6.3f}</span>'
        self.msg03 = '<span style="color:blue">{0:6.3f}</span>'

        self.dspunit = ""        
        
        # FIXME in the definitive version this button will be not visible
        #self.but5.setVisible(False)        
        
        self.iscale = []
        self.incr = 0.5
        self.inc = 0
        self.zoom = 0.0
        self.zinc = 0.0
        self.dzoom = 0.0
        self.wpvisible = False
        self.dunit = "mm"
        self.wporig = ()
        self.show()       
        
 
    def load_data(self,filename): 
        self.surf = vv.meshRead(filename)
        self.Plot(self.surf)
        dimx,dimy,dimz = self.getBB("md")
        self.xdim = dimx.max - dimx.min        
        self.ydim = dimy.max - dimy.min
        self.zdim = dimz.max - dimz.min

        # set the limits of the grid larger than the model by an fixed
        # amount
        self.gscale = 0.33 
        self.lxmin = dimx.min - (self.xdim)*self.gscale
        self.lxmax = dimx.max + (self.xdim)*self.gscale
        self.lymin = dimy.min - (self.ydim)*self.gscale
        self.lymax = dimy.max + (self.ydim)*self.gscale
        self.lzmin = dimz.min - (self.zdim)*self.gscale
        self.lzmax = dimz.max + (self.zdim)*self.gscale
        self.a.SetLimits((self.lxmin,self.lxmax),
                         (self.lymin,self.lymax),
                         (self.lzmin,self.lzmax))      
        # draw the axes at the (origin) of the grid using the same color
        # as the labels in the display window
        self.draw_axes()        
        self.zoom = self.a.camera.zoom
        self.zinc = self.zoom/10.0
        self.dzoom = self.zoom        
        self.dspunit = 'units = {0}'.format(self.dunit)
  
        self.show_md_dim(dimx,dimy,dimz)
     
        return dimx,dimy,dimz


    def show_md_dim(self,dimx,dimy,dimz):
        # Show the model values in the interface
        self.vmx.setText(self.msg01.format(dimx.min))
        self.vmy.setText(self.msg02.format(dimy.min))
        self.vmz.setText(self.msg03.format(dimz.min))
        self.vMx.setText(self.msg01.format(dimx.max))
        self.vMy.setText(self.msg02.format(dimy.max))
        self.vMz.setText(self.msg03.format(dimz.max))    

        xdim = dimx.max - dimx.min        
        ydim = dimy.max - dimy.min
        zdim = dimz.max - dimz.min

        self.valx.setText(self.msg01.format(xdim))        
        self.valy.setText(self.msg02.format(ydim))
        self.valz.setText(self.msg03.format(zdim))         


    def wp_create(self, xmin, xmax, ymin, ymax, zmin, zmax, dunit):
        self.wpxmin = xmin         
        self.wpxmax = xmax 
        self.wpymin = ymin         
        self.wpymax = ymax 
        self.wpzmin = zmin         
        self.wpzmax = zmax
        # set the offset of the workpiece 
        self.wpox = 0
        self.wpoy = 0
        self.wpoz = 0        
        
        self.wporig = (xmin, xmax, ymin, ymax, zmin, zmax)        
        
        self.calc_increment()           
        
        if self.wpvisible ==  True:
            self.wp.visible = False
            self.redraw_cube()            
        else:
            pp = self.cube((xmin,xmax,ymin,ymax,zmin,zmax))        
            self.draw_wp(pp)        
            self.show_wp_dim()
            
                               

    def draw_wp(self,pp):
        self.wp = vv.Line(self.a,pp)
        self.wp.lw = 2
        self.wp.lc = (0.8,0.5,0.2)
        self.wp.ls = "+"
        self.wp.visible = True
        self.wpvisible = True

    def cube(self,dims):
        pp = vv.Pointset(3)
        pp.append(dims[0], dims[2], dims[4]) # A
        pp.append(dims[1], dims[2], dims[4]) # B
        pp.append(dims[1], dims[2], dims[4]) # B        
        pp.append(dims[1], dims[2], dims[5]) # C
        pp.append(dims[1], dims[2], dims[5]) # C        
        pp.append(dims[0], dims[2], dims[5]) # D
        pp.append(dims[0], dims[2], dims[5]) # D        
        pp.append(dims[0], dims[3], dims[5]) # E
        pp.append(dims[0], dims[3], dims[5]) # E        
        pp.append(dims[1], dims[3], dims[5]) # F
        pp.append(dims[1], dims[3], dims[5]) # F        
        pp.append(dims[1], dims[3], dims[4]) # G
        pp.append(dims[1], dims[3], dims[4]) # G        
        pp.append(dims[0], dims[3], dims[4]) # H
        pp.append(dims[0], dims[3], dims[4]) # H        
        pp.append(dims[0], dims[2], dims[4]) # A
        pp.append(dims[0], dims[2], dims[4]) # A
        pp.append(dims[0], dims[2], dims[5]) # D
        pp.append(dims[0], dims[3], dims[5]) # E
        pp.append(dims[0], dims[3], dims[4]) # H        
        pp.append(dims[1], dims[2], dims[5]) # C
        pp.append(dims[1], dims[3], dims[5]) # F
        pp.append(dims[1], dims[2], dims[4]) # B
        pp.append(dims[1], dims[3], dims[4]) # G               
        return pp

    def redraw_cube(self):
        pp = self.cube((self.wpxmin, self.wpxmax, self.wpymin,
                       self.wpymax, self.wpzmin, self.wpzmax))
        self.wp.visible = False
        self.wpvisible = False
        self.draw_wp(pp)        
        self.show_wp_dim()

    def get_wp_dim(self):
        return (self.wpxmin, self.wpxmax, self.wpymin, self.wpymax, 
                self.wpzmin,self.wpzmax, self.dunit) 


    def show_wp_dim(self):
        self.vwpmx.setText(self.msg01.format(self.wpxmin))
        self.vwpmy.setText(self.msg02.format(self.wpymin))
        self.vwpmz.setText(self.msg03.format(self.wpzmin))
        self.vwpMx.setText(self.msg01.format(self.wpxmax))
        self.vwpMy.setText(self.msg02.format(self.wpymax))
        self.vwpMz.setText(self.msg03.format(self.wpzmax))

        self.wpx = self.wpxmax - self.wpxmin
        self.wpy = self.wpymax - self.wpymin        
        self.wpz = self.wpzmax - self.wpzmin

        self.vwpx.setText(self.msg01.format(self.wpx))
        self.vwpy.setText(self.msg02.format(self.wpy))
        self.vwpz.setText(self.msg03.format(self.wpz))        

        self.vwpox.setText(self.msg01.format(self.wpox))
        self.vwpoy.setText(self.msg02.format(self.wpoy))
        self.vwpoz.setText(self.msg03.format(self.wpoz))
        self.lvinc.setText("incr = {0}".format(self.incr))


    def draw_axes(self):
        ppx = vv.Pointset(3)
        ppx.append(self.lxmin, self.lymin, self.lzmin)
        ppx.append(self.lxmax*1.25, self.lymin, self.lzmin)

        self.xas = vv.Line(self.a,ppx)
        self.xas.lw = 3
        self.xas.lc = (1.0,0.0,0.0)
        self.xas.ls = "+"
        self.xas.visible = True       

        ppy = vv.Pointset(3)
        ppy.append(self.lxmin, self.lymin, self.lzmin)
        ppy.append(self.lxmin, self.lymax*1.25, self.lzmin)

        self.yas = vv.Line(self.a,ppy)
        self.yas.lw = 3
        self.yas.lc = (0,1.0,0.0)
        self.yas.ls = "+"
        self.yas.visible = True       

        ppz = vv.Pointset(3)
        ppz.append(self.lxmin, self.lymin, self.lzmin)
        ppz.append(self.lxmin, self.lymin, self.lzmax*1.25)

        self.zas = vv.Line(self.a,ppz)
        self.zas.lw = 3
        self.zas.lc = (0.0,0.0,1.0)
        self.zas.ls = "+"
        self.zas.visible = True       
       
    def Plot(self,surf):
        
        # Make sure our figure is the active one. 
        # If only one figure, this is not necessary.
        #vv.figure(self.fig.nr)

        # Clear it
        vv.clf()

        #vv.xlabel('x axis')
        #vv.ylabel('y axis')
        #vv.zlabel('z axis')
        
        # plot the model
        
        self.t = vv.mesh(surf)
        self.t.edgeColor = (0,0.05,0.05,0.5)
        self.t.faceColor = (0,0.8,0.8,0.5)
        self.t.specular = 0.2        
        self.t.faceShading = 'smooth'
        self.t.edgeShading = None        
        
        # Get axes and set camera to orthographic mode (with a field of view of 70)
        self.a = vv.gca()
        self.a.axis.showMinorGrid = True
        self.a.axis.axisColor = (0.5,0,0.5)
        self.a.camera.fov = 45 # 45 
        self.a.light0.ambient = 0.7 # 0.2 is default for light 0
        self.a.light0.diffuse = 1.0 # 1.0 is default

        # TODO control the lights and turn on one when in z projecton 
        # The other lights are off by default and are positioned at the origin
        #light1 = self.a.lights[1]
        #light1.On()
        #light1.ambient = 0.2 # 0.0 is default for other lights
        #light1.color = (0.1,0.1,0.1) # this light is red        

        self.fig.DrawNow()

    def getBB(self,plotting):
        if plotting == "md":
            obj = self.t
        elif plotting == "wp":
            obj = self.wp
            
        dims =  obj._GetLimits()
        dimx,dimy,dimz = dims
        return dimx,dimy,dimz
        
    def showData(self):
        print self.a.GetView()
        print self.a.GetLimits()
        print self.a.camera.daspect
        #self.a.camera.loc = (70,50,0) 
        #print self.a.axis.lw


    def calc_increment(self):
        ''''
        
        define a base increment using the unit of the model
        
        '''
        if self.dunit == "mm":
            self.iscale = [0.01,0.05,0.1,0.5,1,2,5,10,25,50]
        elif self.dunit == "in":
            self.iscale = [0.005,0.01,0.05,0.1,0.5,1,2,5,10,25,50]
        self.incr = self.iscale[3]
        self.inc = 3        

    def incN(self):
        self.incr = self.iscale[3]
        self.inc = 3    
        self.lvinc.setText("incr = {0}".format(self.iscale[self.inc]))
        
    def incF(self):
        if self.inc < (len(self.iscale)-1):
            self.inc = self.inc + 1
            self.incr = self.iscale[self.inc]            
        self.lvinc.setText("incr = {0}".format(self.iscale[self.inc]))
        
    def incS(self):
        if self.inc > 0:
            self.inc= self.inc - 1
            self.incr = self.iscale[self.inc]
        self.lvinc.setText("incr = {0}".format(self.iscale[self.inc]))
        
    def camX(self):
        self.a.camera.azimuth = 0.0
        self.a.camera.elevation = 0.0
         
    def camY(self):         
        self.a.camera.azimuth = 90.0
        self.a.camera.elevation = 0.0

    def camZ(self):         
        self.a.camera.azimuth = 0.0
        self.a.camera.elevation = 180.0

    def camXb(self):
        self.a.camera.azimuth = 180.0
        self.a.camera.elevation = 0.0
         
    def camYb(self):         
        self.a.camera.azimuth = -90.0
        self.a.camera.elevation = 0.0

    def camZb(self):         
        self.a.camera.azimuth = 0.0
        self.a.camera.elevation = -90.0

    def zoominc(self):
        self.dzoom = self.dzoom + self.zinc
        self.a.camera.zoom = self.dzoom
        
    def zoomdec(self):
        self.dzoom = self.dzoom - self.zinc        
        self.a.camera.zoom = self.dzoom
        
    def zoomreset(self):
        self.dzoom = self.zoom
        self.a.camera.zoom = self.dzoom


    def camO(self):         
        self.a.camera.azimuth = -10.0
        self.a.camera.elevation = 30.0

    # Action on wp move     
     
    def incX(self):
        if self.wpvisible ==  True: 
            self.wpxmax = self.wpxmax + self.incr        
            self.redraw_cube()
        
    def decX(self):
        if self.wpvisible ==  True:        
            self.wpxmax = self.wpxmax - self.incr
            self.redraw_cube()        

    def incY(self):
        if self.wpvisible ==  True:                
            self.wpymax = self.wpymax + self.incr        
            self.redraw_cube()
        
    def decY(self):
        if self.wpvisible ==  True:        
            self.wpymax = self.wpymax - self.incr        
            self.redraw_cube()
        
    def incZ(self):
        if self.wpvisible ==  True: 
            self.wpzmax = self.wpzmax + self.incr        
            self.redraw_cube()        
        
    def decZ(self):
        if self.wpvisible ==  True: 
            self.wpzmax = self.wpzmax - self.incr
            self.redraw_cube()
        
    def triX(self):
        if self.wpvisible ==  True: 
            self.wpxmin = self.wpxmin + self.incr
            self.wpxmax = self.wpxmax + self.incr
            self.wpox = self.wpox + self.incr        
            self.redraw_cube()
        
    def trdX(self):
        if self.wpvisible ==  True: 
            self.wpxmin = self.wpxmin - self.incr
            self.wpxmax = self.wpxmax - self.incr
            self.wpox = self.wpox - self.incr        
            self.redraw_cube()        

    def triY(self):
        if self.wpvisible ==  True: 
            self.wpymin = self.wpymin + self.incr
            self.wpymax = self.wpymax + self.incr 
            self.wpoy = self.wpoy + self.incr
            self.redraw_cube()
     
    def trdY(self):
        if self.wpvisible ==  True: 
            self.wpymin = self.wpymin - self.incr
            self.wpymax = self.wpymax - self.incr
            self.wpoy = self.wpoy - self.incr        
            self.redraw_cube()
        
    def triZ(self):
        if self.wpvisible ==  True:         
            self.wpzmin = self.wpzmin + self.incr
            self.wpzmax = self.wpzmax + self.incr           
            self.wpoz = self.wpoz + self.incr
            self.redraw_cube()        
        
    def trdZ(self):
        if self.wpvisible ==  True: 
            self.wpzmin = self.wpzmin - self.incr
            self.wpzmax = self.wpzmax - self.incr           
            self.wpoz = self.wpoz - self.incr
            self.redraw_cube()        

    def off0(self):
        if self.wpvisible ==  True:         
            self.wpox = 0
            self.wpoy = 0
            self.wpoz = 0
            self.wpxmin, self.wpxmax, self.wpymin, self.wpymax, self.wpzmin, self.wpzmax = self.wporig
            self.redraw_cube()         

if __name__ == "__main__":
    # The visvis way. Will run in interactive mode when used in IEP or IPython.    
    filename = "./stl/pycam-textbox.stl"
    plot.Create()
    m = ModelWindow()
    dimx,dimy,dimz = m.load_data(filename)
            # set the wp dims as those in the model        
    m.wp_create(dimx.min, dimx.max, dimy.min, dimy.max, 
                       dimz.min, dimz.max, "mm")
    m.show_wp_dim()                       
    plot.Run()   
    
    