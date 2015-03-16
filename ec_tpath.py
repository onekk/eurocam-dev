
# simple parallel finish toolpath example
# Anders Wallin 2014-02-23

import time
import vtk  # visualization
import math

import ocl        # https://github.com/aewallin/opencamlib
import camvtk     # ocl helper library
import ec_ngc_fw as ngc_fw     # G-code output is produced by this module
import ConfigParser

import ec_visu as ECV

machine = ""
preamble = ""
postamble = ""
t_name = ""

def trace():
    global machine,t_name,t_shape,diameter,feedrate,plungerate, safe_height, preamble, postamble    
     
    config = ConfigParser.SafeConfigParser()
    config.read("./pathgen.ini")
    if config.sections() is not []:

        # Tool data
        t_name = config.get("Tool","name")  
        shape = float(config.get("Tool","sha"))            
        diameter = float(config.get("Tool","dia")) 
        radius = float(config.get("Tool","rad")) 
        c_length = float(config.get("Tool","len"))
        length = float(config.get("Tool","ovl"))        
        #c_length = float(config.get("Tool","len"))        
        flutes = int(config.get("Tool", "flu"))
        c_cut =  int(config.get("Tool", "cc"))
        #t_note = config.get("Tool","opt")    
        t_shape = config.get("Tool","sna") 
        
        # Model data

        xmin = float(config.get("Model", "xmin"))
        xmax = float(config.get("Model", "xmax"))
        ymin = float(config.get("Model", "ymin"))    
        ymax = float(config.get("Model", "ymax"))
        zmin = float(config.get("Model", "zmin"))
        zmax = float(config.get("Model", "zmax"))

        # Machine data
        machine = config.get("Machine","mach_name") 
        preamble = config.get("Machine","preamble")  
        postamble = config.get("Machine","postamble")


        # Path construction data

        overlap = float(config.get("Path", "xyovl"))
        dircut = config.get("Path", "dir") 
        slices = int(config.get("Path", "slices"))
        action = config.get("Path", "action")
        feedrate = float(config.get("Path", "feedrate"))
        plungerate = float(config.get("Path", "plungerate")) 
        safe_height = float(config.get("Path", "safe_height"))
        basename = config.get("Path", "basename")
        stlfile = config.get("Path", "stlfile")        
        zslices = []
        for s_index in xrange(1,slices+1):
            zslices.append(float(config.get("Path","slice-{}".format(s_index))))
    else:
        print "file vuoto"



    # For the "sha" field the conversion is the following:
    #
    # 0 = "cylinder" CylCutter(diameter, length)
    # 1 = "sphere"   BallCutter(diameter, length)
    # 2 = "toroid"   BullCutter(diameter, corner_radius, length)
    # 3 = "cone"     ConeCutter(diameter, angle, length)

    if shape == 0:
        cutter = ocl.CylCutter(diameter, length)
    elif shape == 1:    
        cutter = ocl.BallCutter(diameter, length)
    elif shape == 2: 
        cutter = ocl.BullCutter(diameter, radius, length)
    elif shape == 3: 
        angle = math.pi/4 #TODO what is the unit for angle?
        cutter = ocl.ConeCutter(diameter, angle, length)
    elif shape == 4: 
        cutter = cutter.offsetCutter(diameter)

    step = overlap

    t_before = time.time()    
    if dircut == "Y":
        passes = ymax/step
        Ny= int(math.ceil(passes)) #number of lines in the y-direction
        paths = YdirectionZigPath(xmin,xmax,ymin,ymax,Ny)
    elif dircut =="X":
        passes = xmax/step
        Nx= int(math.ceil(passes)) #number of lines in the x-direction
        paths = XdirectionZigPath(xmin,xmax,ymin,ymax,Nx)
    else:
        print "Default values used for test"
        paths = YdirectionZigPath(xmin,xmax,ymin,ymax,6)

    t_path = time.time() - t_before      
    print "prima di adaptive dropcutter = > ", t_path

   # now project onto the STL surface
    t_before = time.time()

    surface = STLSurfaceSource(stlfile)    

    (raw_toolpath, n_raw) = adaptive_path_drop_cutter(surface,cutter,paths)
    t1 = time.time() - t_before
    print " Calcolo adpc ",t1," N punti = ",n_raw

    # filter raw toolpath to reduce size
    tolerance = 0.001
    (fil_tps, n_filtered) = filterCLPaths(raw_toolpath, tolerance=0.001)
    print " Punti dopo filtro = ",n_filtered
    toolpaths = fil_tps
    for z_h in zslices:    
        toolpaths = sliceCLPaths(fil_tps,tolerance,z_h)
        if action == "ngc":
            suffix = str(z_h).replace(".", "p")
            filename = "-".join((basename,suffix,".ngc"))
            write_gcode_file(filename, stlfile, surface.size() , z_h, toolpaths)
        else:
            pass


        ECV.vtk_visualize_toolpath(stlfile, toolpaths)

# create a simple "Zig" pattern where we cut only in one direction.
# the first line is at ymin
# the last line is at ymax
def YdirectionZigPath(xmin,xmax,ymin,ymax,Ny):
    paths = []
    dy = float(ymax-ymin)/(Ny-1)  # the y step-over
    for n in xrange(0,Ny):
        path = ocl.Path()
        y = ymin+n*dy # current y-coordinate
        if (n==Ny-1):
            assert( y==ymax)
        elif (n==0):
            assert( y==ymin)
        p1 = ocl.Point(xmin,y,0)   # start-point of line
        p2 = ocl.Point(xmax,y,0)   # end-point of line
        l = ocl.Line(p1,p2)        # line-object
        path.append( l )           # add the line to the path
           
        paths.append(path)
    return paths

def XdirectionZigPath(xmin,xmax,ymin,ymax,Nx):
    paths = []
    dx = float(xmax-xmin)/(Nx-1)  # the y step-over
    for n in xrange(0,Nx):
        path = ocl.Path()
        x = xmin+n*dx              # current y-coordinate
        if (n==Nx-1):
            assert( x==xmax)
        elif (n==0):
            assert( x==xmin)
        p1 = ocl.Point(x,ymin,0)   # start-point of line
        p2 = ocl.Point(x,ymax,0)   # end-point of line
        l = ocl.Line(p1,p2)        # line-object

        path.append( l )           # add the line to the path
        paths.append(path)
    return paths

# run the actual drop-cutter algorithm
def adaptive_path_drop_cutter(surface, cutter, paths):
    apdc = ocl.AdaptivePathDropCutter()
    apdc.setSTL(surface)
    apdc.setCutter(cutter)
    apdc.setSampling(0.04)      # maximum sampling or "step-forward" distance
                                # should be set so that we don't loose any detail of the STL model
                                # i.e. this number should be similar or smaller than the smallest triangle
    apdc.setMinSampling(0.01) # minimum sampling or step-forward distance
                                # the algorithm subdivides "steep" portions of the toolpath
                                # until we reach this limit.
    # 0.0008
    cl_paths=[]
    n_points=0
    for path in paths:
        apdc.setPath( path )
        apdc.run()
        cl_points = apdc.getCLPoints()
        n_points = n_points + len( cl_points )
        cl_paths.append( apdc.getCLPoints() )
    return (cl_paths, n_points)

# this could be any source of triangles
# as long as it produces an ocl.STLSurf() we can work with
def STLSurfaceSource(filename):
    stl = camvtk.STLSurf(filename)
    polydata = stl.src.GetOutput()
    s = ocl.STLSurf()
    camvtk.vtkPolyData2OCLSTL(polydata, s)
    return s

# filter a single path
def filter_path(path,tol):
    f = ocl.LineCLFilter()
    f.setTolerance(tol)
    for p in path:
        p2 = ocl.CLPoint(p.x,p.y,p.z)
        f.addCLPoint(p2)
    f.run()
    return  f.getCLPoints()


def slice_path(path,tol,z_h):
    f = ocl.LineCLFilter()
    f.setTolerance(tol)
    for p in path:
        if p.z < z_h:
            p2 = ocl.CLPoint(p.x,p.y,z_h)
        else:   
            p2 = ocl.CLPoint(p.x,p.y,p.z)
        f.addCLPoint(p2)
    f.run()
    return  f.getCLPoints()


def sliceCLPaths(paths,tol,z_h):
    sliced_paths = []
    for path in paths:
        sliced = slice_path(path,tol,z_h)
        sliced_paths.append(sliced)
    return sliced_paths



# to reduce the G-code size we filter here. (this is not strictly required and could be omitted)
# we could potentially detect G2/G3 arcs here, if there was a filter for that.
# idea:
# if a path in the raw toolpath has three points (p1,p2,p3)
# and point p2 lies within tolerance of the straight line p1-p3
# then we simplify the path to (p1,p3)
def filterCLPaths(cl_paths, tolerance=0.001):
    cl_filtered_paths = []
    n_filtered=0
    for cl_path in cl_paths:
        cl_filtered = filter_path(cl_path,tolerance)

        n_filtered = n_filtered + len(cl_filtered)
        cl_filtered_paths.append(cl_filtered)
    return (cl_filtered_paths, n_filtered)


def write_gcode_file(filename,sourcefile, n_triangles, z_h, toolpath):
    # uses ngc_fw and writes G-code to file
    ngc_fw.fileopen(filename)
    ngc_fw.safe_height = safe_height       # XY rapids at this height
    ngc_fw.feedrate = feedrate       # feedrate
    ngc_fw.plungerate = plungerate   # plungrate
    ngc_fw.comment( " OpenCAMLib %s" % ocl.version() )
    ngc_fw.comment( " STL surface  : {0}".format(sourcefile))
    ngc_fw.comment( "   triangles  : {0}".format(n_triangles))
    ngc_fw.comment( " Slice height : {0:.4}".format(z_h))
    ngc_fw.comment( " Machine Name : {0}".format(machine))
    ngc_fw.comment( "Tool name     : {0}".format(t_name))
    ngc_fw.comment( "Tool shape    : {0}".format(t_shape))
    ngc_fw.comment( "Tool diameter : {0:.4}".format(diameter))
    ngc_fw.comment( "Strategy      : {0}".format("strat"))
    ngc_fw.comment( "Direction     : {0} ".format("None")) 
    ngc_fw.filewrite(preamble+"\n")
    ngc_fw.comment( " End of preamble ")    
    #TODO modify this behaviuor
    for path in toolpath:
        ngc_fw.pen_up()
        first_pt = path[0]
        ngc_fw.xy_rapid_to( first_pt.x, first_pt.y)
        ngc_fw.pen_down(first_pt.z)
        for p in path[1:]:
            ngc_fw.line_to(p.x,p.y,p.z)
        ngc_fw.comment("end of path")    
    ngc_fw.comment( " Start postamble ") 
    # write postamble        
    ngc_fw.filewrite(postamble+"\n")
    # close the file
    ngc_fw.fileclose()
    
 



       
if __name__ == "__main__":
      
      trace()
