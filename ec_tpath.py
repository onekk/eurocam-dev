# Eurocam Toolpath Generation Program
# (c) Dormeletti Carlo 2015 
# some routines are based on code by Anders Wallin (c) 2014 

import time
import os
import math
import ocl                   # https://github.com/aewallin/opencamlib
import camvtk_mod as camvtk  # ocl helper library for VTK version > 5
import ConfigParser

import ec_visu as ECV

version = "0.3.5 Alpha"

def trace():
    global c_cut, debug, diameter, dims, dircut, ec_version, feedrate,\
           gcdecimal, gcmachine, gcmodel,  gctool, gctoolp, gcverbose, gcworkp,\
           machine, plungerate, postamble, preamble, safe_height, show_path,\
           slices, strat, t_name, t_shape, wpdims      
     
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
        #c_length = float(config.get("Tool","len"))
        length = float(config.get("Tool","ovl"))        
        #flutes = int(config.get("Tool", "flu"))
        c_cut =  int(config.get("Tool", "cc"))
        #t_note = config.get("Tool","opt")    
        t_shape = config.get("Tool","sna") 
        
        # WorkPiece data

        wpxmin = float(config.get("WorkPiece", "xmin"))
        wpxmax = float(config.get("WorkPiece", "xmax"))
        wpymin = float(config.get("WorkPiece", "ymin"))    
        wpymax = float(config.get("WorkPiece", "ymax"))
        wpzmin = float(config.get("WorkPiece", "zmin"))
        wpzmax = float(config.get("WorkPiece", "zmax"))

        wpdims = (wpxmin, wpxmax, wpymin, wpymax, wpzmin, wpzmax)

        # Machine data
        machine = config.get("Machine","mach_name") 
        preamble = config.get("Machine","preamble")  
        postamble = config.get("Machine","postamble")


        # Path construction data

        overlap = float(config.get("Path", "xyovl"))
        strat = config.get("Path", "strat") 
        dircut = config.get("Path", "dir") 
        slices = int(config.get("Path", "slices"))
        action = config.get("Path", "action")
        feedrate = float(config.get("Path", "feedrate"))
        plungerate = float(config.get("Path", "plungerate")) 
        safe_height = float(config.get("Path", "safe_height"))
        basename = config.get("Path", "basename")
        stlfile = config.get("Path", "stlfile")

        if c_cut == 1:
            xmin = wpxmin
            xmax = wpxmax
            ymin = wpymin
            ymax = wpxmax
        else: # we have to enter the piece from a side and not plunge in it.
            e_f = diameter + (diameter * 0.10) # add a factor to stay safe
            if dircut in ('X', 'Xb'):
                xmin = wpxmin 
                xmax = wpxmax
                ymin = wpymin - e_f
                ymax = wpxmax + e_f                
            elif dircut in ('Y', 'Yb'):    
                xmin = wpxmin - e_f
                xmax = wpxmax + e_f
                ymin = wpymin
                ymax = wpymax
                
        zmin = wpzmin
        zmax = wpzmax

        dims = [xmin, xmax, ymin, ymax, zmin, zmax]

        print dims
        print wpdims

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
        return


    # For the "sha" field the conversion is the following:
    #
    # 0 = "cylinder" CylCutter(diameter, length)
    # 1 = "sphere"   BallCutter(diameter, length)
    # 2 = "toroid"   BullCutter(diameter, corner_radius, length)
    # 3 = "cone"     ConeCutter(diameter, half angle in radians, length)

    if shape == 0:
        cutter = ocl.CylCutter(diameter, length)
    elif shape == 1:    
        cutter = ocl.BallCutter(diameter, length)
    elif shape == 2: 
        cutter = ocl.BullCutter(diameter, radius, length)
    elif shape == 3: 
        # The angle is the half angle of the cone (90 deg in radians is pi/2)
        # becoming pi/2 * 1/2 = pi/4
        # the conversion between radians and degree is degree * pi/180 so the
        # formula (radius *pi)/360
        rangle = (radius * math.pi)/360  
        cutter = ocl.ConeCutter(diameter, rangle, length)
    elif shape == 4: 
        cutter = cutter.offsetCutter(diameter)

    t_before = time.time()

    ydim = ymax - ymin
    xdim = xmax - xmin
        
    if dircut in ('Y','Yb'):
        n_pass = ydim/overlap        
    elif dircut in ('X','Xb'):
        n_pass = xdim/overlap
    else:
        pass

    if strat in ('T'):
        Np = 6
    else:
        Np = int(math.ceil(n_pass)) #number of lines in the y-direction        

    print "number of passes ", Np

    if dircut == "Y":
        paths = YdirectionZigPath(dims,Np)
    elif dircut == "X":
        paths = XdirectionZigPath(dims,Np)
    elif dircut == "Yb":
        paths = YdirZigZagPath(dims,Np)
    elif dircut == "Xb":
        paths = XdirZigZagPath(dims,Np)
    else:
        print "No valid direction of cut"

    if debug > 0:
        t_path = time.time() - t_before        
        print "Tempo di calcolo del path prima di APDC = > ", t_path

    t_before = time.time()
    
    # now project onto the STL surface
    surface = STLSurfaceSource(stlfile)    

    (raw_toolpath, n_raw) = adaptive_path_drop_cutter(surface,cutter,paths,zmin)

    if debug > 0:
        t1 = time.time() - t_before
        print "Tempo di calcolo di APDC {0} N punti {1}".format(t1,n_raw)

    # filter raw toolpath to reduce size
    tolerance = 0.001
    (fil_tps, n_filtered) = filterCLPaths(raw_toolpath, tolerance)

    if debug  > 0: 
        print " Punti dopo filtro = ",n_filtered

    toolpaths = fil_tps
    count = 0
    for z_h in zslices:    
        toolpaths = sliceCLPaths(fil_tps,tolerance,z_h)
        if action == "ngc":
            count = count + 1
            ep = time.strftime("%y%j%H%M")
            filename = "".join((basename,"-",ep,"-s",str(count),"o",str(slices),".ngc"))

            if debug > 0:
                print "Generating filename = ", os.path.basename(filename)

            write_gcode_file(filename, stlfile,z_h, count, toolpaths)
        else:
            pass

        if show_path == 1:
            ECV.vtk_visualize_toolpath(stlfile, 1, (filename, wpdims))
            #ECV.vtk_visualize_toolpath(stlfile, 0, (toolpaths, safe_height, zmax))
            pass


# create a simple "Zig" pattern where we cut only in one direction.
# the first line is at ymin, the last line is at ymax

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
    dx = float(xmax-xmin)/(Nx-1)  # the x step-over
    for n in xrange(0,Nx):
        path = ocl.Path()
        x = xmin+n*dx             # current x-coordinate
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


def YdirZigZagPath(dims,Ny):
    paths = []
    xmin = dims[0]
    xmax = dims[1]
    ymin = dims[2]
    ymax = dims[3]
    zmin = dims[4]
    zmax = dims[5]
    dy = float(ymax-ymin)/(Ny-1)  # the y step-over
    z = 0
    for n in xrange(0,Ny):
        path = ocl.Path()
        y = ymin+n*dy # current y-coordinate
        if (n==Ny-1):
            assert( y==ymax)
        elif (n==0):
            assert( y==ymin)
        p1 = ocl.Point(xmin,y,zmin)   # start-point of line
        p2 = ocl.Point(xmax,y,zmin)   # end-point of line
        if z == 0:    
            #print "Z0 ZZY ", z, p1, p2
            l = ocl.Line(p1,p2)        # line-object
            z = 1
        else:
           #print "Z>0 ZZY", z, p2, p1
           l = ocl.Line(p2,p1)
           z = 0
        path.append( l )           # add the line to the path
           
        paths.append(path)
    return paths

def XdirZigZagPath(dims,Np):
    paths = []
    xmin = dims[0]
    xmax = dims[1]
    ymin = dims[2]
    ymax = dims[3]
    zmin = dims[4]
    zmax = dims[5]
    dx = float(xmax-xmin)/(Np-1)  # the x step-over
    z = 0
    for n in xrange(0,Np):
        path = ocl.Path()
        x = xmin+n*dx # current y-coordinate
        if (n==Np-1):
            assert( x==xmax)
        elif (n==0):
            assert( x==xmin)
        p1 = ocl.Point(x,ymin,zmin)   # start-point of line
        p2 = ocl.Point(x,ymax,zmin)   # end-point of line
        if z == 0:    
            #print "Z0 ZZY ", z, p1, p2
            l = ocl.Line(p1,p2)        # line-object
            z = 1
        else:
           #print "Z>0 ZZY", z, p2, p1
           l = ocl.Line(p2,p1)
           z = 0
        path.append( l )           # add the line to the path
           
        paths.append(path)
    return paths

def adaptive_path_drop_cutter(surface, cutter, paths,z_h):
    apdc = ocl.AdaptivePathDropCutter()
    apdc.setSTL(surface)
    apdc.setCutter(cutter)
    apdc.setSampling(0.04)   # maximum sampling or "step-forward" distance
                             # should be set so that we don't loose any 
                             # detail of the STL model i.e. this number 
                             # should be similar or smaller than the
                             # smallest triangle
    apdc.setMinSampling(0.01)  # minimum sampling or step-forward distance
                               # the algorithm subdivides "steep" portions of 
                               # the toolpath until we reach this limit.
    apdc.setZ(z_h)
    if debug > 0:
        print "Apdc zmin = {0:.4f}".format(apdc.getZ())                            
    cl_paths=[]
    n_points=0
    for path in paths:
        apdc.setPath( path )
        apdc.run()
        cl_points = apdc.getCLPoints()
        n_points = n_points + len( cl_points )
        cl_paths.append( apdc.getCLPoints() )
    return (cl_paths, n_points)


def STLSurfaceSource(filename):
    ''' STLSurfaceSource(filename) 

   this could be any source of triangles as long as it produces an 
   ocl.STLSurf() we can work with
   
    '''
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


def filterCLPaths(cl_paths, tolerance=0.001):
    ''' filterCLPaths(cl_paths, tolerance=0.001)
    
    to reduce the G-code size we filter here. (this is not strictly required
    and could be omitted)
    we could potentially detect G2/G3 arcs here, if there was a filter for that.
    idea:
    if a path in the raw toolpath has three points (p1,p2,p3)
    and point p2 lies within tolerance of the straight line p1-p3
    then we simplify the path to (p1,p3)
    '''
    cl_filtered_paths = []
    n_filtered=0
    for cl_path in cl_paths:
        cl_filtered = filter_path(cl_path,tolerance)

        n_filtered = n_filtered + len(cl_filtered)
        cl_filtered_paths.append(cl_filtered)
    return (cl_filtered_paths, n_filtered)


def write_gcode_file(filename,sourcefile, z_h, count, toolpath):
    global gcdecimal, dircut
    modelname = os.path.basename(sourcefile)
    ncout = open(filename,'w')    

    #xmin = dims[0]
    #xmax = dims[1]
    #ymin = dims[2]
    #ymax = dims[3]
    #zmin = dims[4]
    #zmax = dims[5] 
    
    dplaces = "".join((":0",str(gcdecimal+5) ,".",str(gcdecimal),"f"))

    wpd1 = "".join(("( xmin = {0", dplaces, "} xmax = {1", dplaces, "} )\n"))    
    wpd2 = "".join(("( ymin = {0", dplaces, "} ymax = {1", dplaces, "} )\n"))
    wpd3 = "".join(("( zmin = {0", dplaces, "} zmax = {1", dplaces, "} )\n"))

    ncout.write(comment("TPath version      : {0}".format(version)))
    ncout.write(comment("EuroCAM version    : {0}".format(ec_version))) 
    ncout.write(comment("OpenCAMLib version : {0}".format(ocl.version())))
    ncout.write(comment("Generated on date {0}".format(time.strftime("%c"))))
    if gcmodel == 1:    
        ncout.write(comment("STL surface file : {0}".format(modelname)))

    if gcmachine == 1:    
        ncout.write(comment("Machine name   : {0}".format(machine)))

    if gctool == 1:
        ncout.write(comment("Tool name      : {0}".format(t_name)))
        ncout.write(comment("Tool shape     : {0}".format(t_shape)))
        ncout.write(comment("Tool diameter  : {0:.4}".format(diameter)))

    if gcworkp == 1:
        ncout.write("( Work Piece dimensions ) \n")
        ncout.write(wpd1.format(wpdims[0], wpdims[1]))    
        ncout.write(wpd2.format(wpdims[2], wpdims[3]))
        ncout.write(wpd3.format(wpdims[4], wpdims[5]))       

    if gctoolp == 1:
        ncout.write(comment("Strategy       : {0}".format(strat)))
        ncout.write(comment("Direction      : {0} ".format(dircut))) 
        ncout.write(comment("Slice N. {0} of {1}".format(count,slices)))    
        ncout.write(comment("Height of pass : {0:.4}".format(z_h)))

    ncout.write(preamble+"\n")
    
    if gcverbose == 1:
        ncout.write("( End of preamble ) \n")

    # the line is formed by four places a point and the number of decimal
    # so it can have 9999.(number of decimals) and 9999 mm almost ten meters

    gcwlrxy =  "".join(("G00 X{0", dplaces, "} Y{1", dplaces, "}\n"))
    gcwlxyz =  "".join(("G01 X{0", dplaces, "} Y{1", dplaces , "} Z{2", dplaces,"}\n"))    
    gcwpz = "".join(("Z{0",dplaces , "}\n"))

    # TODO take in account if the tools is not center cut to move past the wp
    # limits
    # TODO defining an enter strategy on the wp to reduce the wearing of the tool
    npath = 1
    if debug > 0:
        print "Toolpath is composed of {0} path".format(len(toolpath))
        
    if dircut in ("X","Y"):
        # This beahviour assume that the first point is a rapid and to the x,y pos
        # and the plunge down on the z axis at the specified plunge rate
        # so it is taylored on the Zig alghoritms 
        for path in toolpath:
            if gcverbose == 1:        
                ncout.write("( Path {0} start )\n".format(str(npath)))        
            # raise the tool at safe height
            ncout.write("".join(("G00 Z{0",dplaces,"}\n")).format(safe_height))
            # take out of the path the first point        
            first_pt = path[0]
            # move to the first point of the path (rapid move)
            ncout.write(gcwlrxy.format(first_pt.x, first_pt.y))
            if gcverbose == 1:
                ncout.write("( rapid move )\n")
       
            # plunge down in the workpiece (NOTE if it is center cut)        
            ncout.write("G01 F {0:.1f} \n".format(plungerate))
            ncout.write(gcwpz.format(first_pt.z))
            # set the feedrate
            ncout.write("F {0:.1f} \n".format(feedrate))
            for p in path[1:]:
                ncout.write(gcwlxyz.format(p.x, p.y, p.z))
            if gcverbose == 1:        
                ncout.write("( Path {0} end )\n".format(str(npath)))
            if debug > 0:
                print "Path number ",npath
            npath = npath + 1    
        # return to the safe height at the end of the work
        ncout.write("".join(("G00 Z{",dplaces,"}\n")).format(safe_height))

    elif dircut in ("Xb","Yb"):
        # This beahviour is for the ZigZag paths (bidirectional)
        # there is no need to raise the tool to the safe_height after each pass
        # ?? FICME to test
        f_p = 1 # set a flag for the first poin of the first path
        for path in toolpath:
            if gcverbose == 1:        
                ncout.write("( Path {0} start )\n".format(str(npath)))        
            if f_p == 1:    
                # raise the tool at safe height
                ncout.write("".join(("G00 Z{0",dplaces,"}\n")).format(safe_height))
                # take out of the path the first point
                first_pt = path[0]
                # move to the first point of the path (rapid move)
                ncout.write(gcwlrxy.format(first_pt.x, first_pt.y))
    
                if gcverbose == 1:
                    ncout.write("( rapid move )\n")
           
                # plunge down in the workpiece (NOTE if it is center cut)        
                ncout.write("G01 F {0:.1f} \n".format(plungerate))
                ncout.write(gcwpz.format(first_pt.z))                
                f_p = 0 # reset the flag 
            else:
                first_pt = path[0]
                #print "fpz {0} z_h {1}".format(first_pt.z, z_h)
                if first_pt.z > z_h: # slice height is lower than model height
                    ncout.write("".join(("G01 Z{0",dplaces,"}\n")).format(first_pt.z))
                else:                 # raise the tool to the height of the slice 
                    ncout.write("".join(("G01 Z{0",dplaces,"}\n")).format(z_h))                    
                ncout.write("G01 F {0:.1f} \n".format(plungerate))
                # move to the first point of the path
                ncout.write(gcwlxyz.format(first_pt.x, first_pt.y, first_pt.z))
                if gcverbose == 1:
                    ncout.write("( path link move )\n")                
            # set the feedrate
            ncout.write("F {0:.1f} \n".format(feedrate))
            for p in path[1:]:
                ncout.write(gcwlxyz.format(p.x, p.y, p.z))
            if gcverbose == 1:        
                ncout.write("( Path {0} end )\n".format(str(npath)))
            if debug > 0:
                print "Path number ",npath
            npath = npath + 1    
        # return to the safe height at the end of the work
        ncout.write("".join(("G00 Z{",dplaces,"}\n")).format(safe_height))
    else:
        pass
    
    if gcverbose == 1:
         ncout.write("( Start postamble )\n ") 
    # write postamble        
    ncout.write(postamble+"\n")
    # close the file
    ncout.close()
   
# (endpoint, radius, center, cw?)
def xy_arc_to( x,y, r, cx,cy, cw ):
    if (cw):
        f_line = "G2 X% 8.5f Y% 8.5f R% 8.5f" % (x, y, r)
    else:
        f_line = "G3 X% 8.5f Y% 8.5f R% 8.5f" % (x, y, r)
    # FIXME: optional IJK format arcs
    
    
def comment(s=""):
    s1 = s.replace("(", "<")
    s2 = s1.replace(")",">")
    f_line = "( {} )\n".format(s2)
    return f_line

       
if __name__ == "__main__":
      
      trace()
