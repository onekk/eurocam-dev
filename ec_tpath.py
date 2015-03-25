# Eurocam Toolpath Generation Program
# (c) Dormeletti Carlo 2015 
# some routine is derived from
# Anders Wallin code (c) 2014 

import time
import os
import math
import ocl        # https://github.com/aewallin/opencamlib
import camvtk_mod as camvtk     # ocl helper library for VTK version > 5
import ConfigParser

import ec_visu as ECV

machine = ""
preamble = ""
postamble = ""
t_name = ""
debug = 0
dims =[]
show_path = 0
version = "0.1.0 Alpha"
ncout = None

def trace():
    global machine, t_name, t_shape, diameter, feedrate, plungerate, \
           safe_height, preamble, postamble, debug, show_path, dims, \
           slices, ec_version, gcmodel, gcmachine, gctool, gcworkp, \
           gctoolp, gcverbose, gcdecimal, ncout     
     
    config = ConfigParser.SafeConfigParser()
    config.read("./pathgen.ini")
    if config.sections() is not []:
        
        debug = int(config.get("General","debug"))
        ec_version = config.get("General","ec_version") 
        
        # Tool data
        t_name = config.get("Tool","name")  
        shape = float(config.get("Tool","sha"))            
        diameter = float(config.get("Tool","dia")) 
        radius = float(config.get("Tool","rad")) 
        c_length = float(config.get("Tool","len"))
        length = float(config.get("Tool","ovl"))        
        flutes = int(config.get("Tool", "flu"))
        c_cut =  int(config.get("Tool", "cc"))
        #t_note = config.get("Tool","opt")    
        t_shape = config.get("Tool","sna") 
        
        # WorkPiece data

        xmin = float(config.get("WorkPiece", "xmin"))
        xmax = float(config.get("WorkPiece", "xmax"))
        ymin = float(config.get("WorkPiece", "ymin"))    
        ymax = float(config.get("WorkPiece", "ymax"))
        zmin = float(config.get("WorkPiece", "zmin"))
        zmax = float(config.get("WorkPiece", "zmax"))
        
        dims = [xmin, xmax, ymin, ymax, zmin, zmax]

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

        gcmodel = int(config.get("G-Code","model"))
        gcmachine = int(config.get("G-Code","machine"))
        gctool = int(config.get("G-Code","tool")) 
        gcworkp = int(config.get("G-Code","workp"))        
        gctoolp = int(config.get("G-Code","toolpath"))   
        gcverbose = int(config.get("G-Code","verbose")) 
        show_path = int(config.get("G-Code","view"))
        gcdecimal = int(config.get("G-Code","decimals"))
        
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
    ydim = ymax - ymin
    xdim = xmax - xmin
    if dircut == "Y":
        passes = ydim/step
        Ny= int(math.ceil(passes)) #number of lines in the y-direction
        paths = YdirectionZigPath(dims,Ny)
    elif dircut =="X":
        passes = xdim/step
        Nx= int(math.ceil(passes)) #number of lines in the x-direction
        paths = XdirectionZigPath(dims,Nx)
    else:
        print "Default values used for test"
        paths = YdirectionZigPath(dims,6)

    t_path = time.time() - t_before

    if debug  == 1:      
        print "prima di adaptive dropcutter = > ", t_path

   # now project onto the STL surface
    t_before = time.time()

    surface = STLSurfaceSource(stlfile)    

    (raw_toolpath, n_raw) = adaptive_path_drop_cutter(surface,cutter,paths,zmin)
    t1 = time.time() - t_before
    if debug == 1:
        print " Calcolo adpc ",t1," N punti = ",n_raw

    # filter raw toolpath to reduce size
    tolerance = 0.001
    (fil_tps, n_filtered) = filterCLPaths(raw_toolpath, tolerance)
    if debug  == 1: 
        print " Punti dopo filtro = ",n_filtered

    toolpaths = fil_tps
    count = 0
    for z_h in zslices:    
        toolpaths = sliceCLPaths(fil_tps,tolerance,z_h)
        if action == "ngc":
            count = count + 1
            suffix = "-s" + str(count) + "o" + str(slices) 
            filename = "".join((basename,suffix,".ngc"))
            if debug == 1:
                print "Generating filename = ", os.path.basename(filename)
            write_gcode_file(filename, stlfile,z_h, count, toolpaths)
        else:
            pass

        if show_path == 1:
            ECV.vtk_visualize_toolpath(stlfile, toolpaths)

# create a simple "Zig" pattern where we cut only in one direction.
# the first line is at ymin
# the last line is at ymax
def YdirectionZigPath(dims,Ny):
    paths = []
    xmin = dims[0]
    xmax = dims[1]
    ymin = dims[2]
    ymax = dims[3]
    zmin = dims[4]
    zmax = dims[5]
    dy = float(ymax-ymin)/(Ny-1)  # the y step-over
    for n in xrange(0,Ny):
        path = ocl.Path()
        y = ymin+n*dy # current y-coordinate
        if (n==Ny-1):
            assert( y==ymax)
        elif (n==0):
            assert( y==ymin)
        p1 = ocl.Point(xmin,y,zmin)   # start-point of line
        p2 = ocl.Point(xmax,y,zmin)   # end-point of line
        l = ocl.Line(p1,p2)        # line-object
        path.append( l )           # add the line to the path
           
        paths.append(path)
    return paths

def XdirectionZigPath(dims,Nx):
    paths = []
    xmin = dims[0]
    xmax = dims[1]
    ymin = dims[2]
    ymax = dims[3]
    zmin = dims[4]
    zmax = dims[5]    
    dx = float(xmax-xmin)/(Nx-1)  # the y step-over
    for n in xrange(0,Nx):
        path = ocl.Path()
        x = xmin+n*dx              # current y-coordinate
        if (n==Nx-1):
            assert( x==xmax)
        elif (n==0):
            assert( x==xmin)
        p1 = ocl.Point(x,ymin,zmax)   # start-point of line
        p2 = ocl.Point(x,ymax,zmax)   # end-point of line
        l = ocl.Line(p1,p2)        # line-object

        path.append( l )           # add the line to the path
        paths.append(path)
    return paths

# run the actual drop-cutter algorithm
def adaptive_path_drop_cutter(surface, cutter, paths,z_h):
    apdc = ocl.AdaptivePathDropCutter()
    apdc.setSTL(surface)
    apdc.setCutter(cutter)
    apdc.setSampling(0.04)      # maximum sampling or "step-forward" distance
                                # should be set so that we don't loose any detail of the STL model
                                # i.e. this number should be similar or smaller than the smallest triangle
    apdc.setMinSampling(0.01) # minimum sampling or step-forward distance
                              # the algorithm subdivides "steep" portions of the toolpath
                              # until we reach this limit.
    apdc.setZ(z_h)
    print apdc.getZ()                            
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
    if debug  == 1: 
        print filename
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


def write_gcode_file(filename,sourcefile, z_h, count, toolpath):
    global ncout    
    modelname = os.path.basename(sourcefile)
    ncout = open(filename,'w')    

    
    comment( "TPath Version      : {0}".format(version))    
    comment( "EuroCAM            : {0}".format(ec_version)) 
    comment( "OpenCAMLib version : {0}".format(ocl.version()))
    comment( "Generated on date {0}".format(time.strftime("%c")))
    if gcmodel == 1:    
        comment( "STL surface file : {0}".format(modelname))

    if gcmachine == 1:    
        comment( "Machine Name  : {0}".format(machine))

    if gctool == 1:
        comment( "Tool name     : {0}".format(t_name))
        comment( "Tool shape    : {0}".format(t_shape))
        comment( "Tool diameter : {0:.4}".format(diameter))

    if gcworkp == 1:
        comment( "WorkPiece dimension ")
        comment( "xmin = {0:12.4f} xmax = {1:12.4f}".format(dims[0], dims[1]))    
        comment( "ymin = {0:12.4f} ymax = {1:12.4f}".format(dims[2], dims[3]))
        comment( "zmin = {0:12.4f} zmax = {1:12.4f}".format(dims[4], dims[5]))        

    if gctoolp == 1:
        comment( "Strategy      : {0}".format("strat"))
        comment( "Direction     : {0} ".format("None")) 
        comment( "Slice N. {0} of {1}".format(count,slices))    
        comment( "Slice height  : {0:.4}".format(z_h))

    ncout.write(preamble+"\n")
    
    if gcverbose == 1:
        comment( " End of preamble ")    

    #TODO modify this behaviuor
    for path in toolpath:
        pen_up()
        first_pt = path[0]
        xy_rapid_to( first_pt.x, first_pt.y)
        pen_down(first_pt.z)
        for p in path[1:]:
            line_to(p.x,p.y,p.z)
        if gcverbose == 1:        
            comment("end of path")

    if gcverbose == 1:
        comment( " Start postamble ") 
    # write postamble        
    ncout.write(postamble+"\n")
    # close the file
    ncout.close()

def line_to(x,y,z):
    f_line = "G1 X{:.4f} Y{:.4f} Z{:.4f} F{:.0f}\n".format(x, y, z, feedrate)
    ncout.write(f_line)
    
def xy_line_to(x,y):
    f_line = "G1 X{:.4f} Y{:.4f}\n".format(x, y)
    ncout.write(f_line)
    
# (endpoint, radius, center, cw?)
def xy_arc_to( x,y, r, cx,cy, cw ):
    if (cw):
        f_line = "G2 X% 8.5f Y% 8.5f R% 8.5f" % (x, y, r)
    else:
        f_line = "G3 X% 8.5f Y% 8.5f R% 8.5f" % (x, y, r)
    # FIXME: optional IJK format arcs
    
def xy_rapid_to(x,y):
    f_line = "G0 X{:.4f} Y{:.4f}\n".format(x, y)
    ncout.write(f_line)

def pen_up():
    f_line = "G0 Z {:.4f}\n".format(safe_height)
    ncout.write(f_line)

def pen_down(z=0):
    #f_line = "G0 Z {:.4f}\n".format(z)
    #filewrite(f_line)
    comment("plunge pass")
    plunge(z)

def plunge(z):
    f_line =  "G1 Z {:.4f} F{:.0f}\n".format(z, plungerate)
    ncout.write(f_line)
    
def comment(s=""):
    s1 = s.replace("(", "<")
    s2 = s1.replace(")",">")
    f_line = "( {} )\n".format(s2)
    ncout.write(f_line)

       
if __name__ == "__main__":
      
      trace()
