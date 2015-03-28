# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 19:34:26 2015

@author: carlo-m
"""
import ocl
import datetime
import camvtk_mod as camvtk
import ec_ngc_parser as pgc
   
def vtk_visualize_toolpath(stlfile,visu,data):
   
    myscreen = camvtk.VTKScreen()
    stl = camvtk.STLSurf(stlfile)
    myscreen.addActor(stl)
    stl.SetSurface() #
    #stl.SetWireframe()
    stl.SetColor(camvtk.cyan)
    myscreen.camera.SetPosition(15, 13, 7)
    myscreen.camera.SetFocalPoint(5, 5, 0)

    myscreen.camera.Zoom(0.5)

    if visu == 0: # the data are toolpaths
        toolpath_trace(myscreen, data)
    elif visu == 1:
        show_wp(myscreen,data[1])
        ret,toolpath = pgc.make_tpath(data[0]) 
        if ret == "OK":        
            gcodeview(myscreen,toolpath)
        elif ret == "KO":
            print toolpath        
  
    else:
        pass
        
    t = camvtk.Text()
    t.SetPos( (myscreen.width-200, myscreen.height-100) )
    date_text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    t.SetText( "EuroCAM \n " + date_text + "\n Using OpenCAMLib \n" )
    myscreen.addActor(t)
    
    myscreen.render()
    myscreen.iren.Start()

def gcodeview(myscreen,data):

    XYrapidColor = camvtk.green
    feedColor = camvtk.yellow

    pos = ocl.Point(0,0,0) 
   
    first_pt = data[0][1]
    #print first_pt
    myscreen.addActor( camvtk.Sphere(center=(first_pt[0],first_pt[1],first_pt[2]) , radius=0.1, color=camvtk.green) )
    pos = ocl.Point(first_pt[0],first_pt[1],first_pt[2])     

    for point in data[1:]:
        pcs = point[1]
        pos1 = ocl.Point(pcs[0],pcs[1],pcs[2])
        #print pos1.x,pos1.y,pos1.z
        if point[0] == 'r':
            myscreen.addActor( camvtk.Line(p1=( pos.x,pos.y,pos.z),p2=(pos1.x,pos1.y,pos1.z),color=XYrapidColor) )
        else:    
            myscreen.addActor( camvtk.Line(p1=( pos.x,pos.y,pos.z),p2=(pos1.x,pos1.y,pos1.z),color=feedColor) )
        pos = ocl.Point(pos1.x,pos1.y,pos1.z) 

    # END retract up to rapid_height
    myscreen.addActor( camvtk.Sphere(center=(pos.x,pos.y,pos.z) , radius=0.1, color=camvtk.red) )

    camvtk.drawArrows(myscreen,center=(-0.5,-0.5,-0.5)) # XYZ coordinate arrows

def show_wp(scr,dims):
    mdCol = camvtk.pink
    p1 = ocl.Point(dims[0], dims[2], dims[4]) # A
    p2 = ocl.Point(dims[1], dims[2], dims[4]) # B
    scr.addActor( camvtk.Line(p1=(p1.x,p1.y,p1.z),p2=(p2.x,p2.y,p2.z),color=mdCol))
    p1 = ocl.Point(dims[1], dims[2], dims[4]) # B        
    p2 = ocl.Point(dims[1], dims[2], dims[5]) # C
    scr.addActor( camvtk.Line(p1=(p1.x,p1.y,p1.z),p2=(p2.x,p2.y,p2.z),color=mdCol))    
    p1 = ocl.Point(dims[1], dims[2], dims[5]) # C        
    p2 = ocl.Point(dims[0], dims[2], dims[5]) # D
    scr.addActor( camvtk.Line(p1=(p1.x,p1.y,p1.z),p2=(p2.x,p2.y,p2.z),color=mdCol))    
    p1 = ocl.Point(dims[0], dims[2], dims[5]) # D        
    p2 = ocl.Point(dims[0], dims[3], dims[5]) # E
    scr.addActor( camvtk.Line(p1=(p1.x,p1.y,p1.z),p2=(p2.x,p2.y,p2.z),color=mdCol))    
    p1 = ocl.Point(dims[0], dims[3], dims[5]) # E        
    p2 = ocl.Point(dims[1], dims[3], dims[5]) # F
    scr.addActor( camvtk.Line(p1=(p1.x,p1.y,p1.z),p2=(p2.x,p2.y,p2.z),color=mdCol))    
    p1 = ocl.Point(dims[1], dims[3], dims[5]) # F        
    p2 = ocl.Point(dims[1], dims[3], dims[4]) # G
    scr.addActor( camvtk.Line(p1=(p1.x,p1.y,p1.z),p2=(p2.x,p2.y,p2.z),color=mdCol))    
    p1 = ocl.Point(dims[1], dims[3], dims[4]) # G        
    p2 = ocl.Point(dims[0], dims[3], dims[4]) # H
    scr.addActor( camvtk.Line(p1=(p1.x,p1.y,p1.z),p2=(p2.x,p2.y,p2.z),color=mdCol))    
    p1 = ocl.Point(dims[0], dims[3], dims[4]) # H        
    p2 = ocl.Point(dims[0], dims[2], dims[4]) # A
    scr.addActor( camvtk.Line(p1=(p1.x,p1.y,p1.z),p2=(p2.x,p2.y,p2.z),color=mdCol))    
    p1 = ocl.Point(dims[0], dims[2], dims[4]) # A
    p2 = ocl.Point(dims[0], dims[2], dims[5]) # D
    scr.addActor( camvtk.Line(p1=(p1.x,p1.y,p1.z),p2=(p2.x,p2.y,p2.z),color=mdCol))    
    p1 = ocl.Point(dims[0], dims[3], dims[5]) # E
    p2 = ocl.Point(dims[0], dims[3], dims[4]) # H
    scr.addActor( camvtk.Line(p1=(p1.x,p1.y,p1.z),p2=(p2.x,p2.y,p2.z),color=mdCol))        
    p1 = ocl.Point(dims[1], dims[2], dims[5]) # C
    p2 = ocl.Point(dims[1], dims[3], dims[5]) # F
    scr.addActor( camvtk.Line(p1=(p1.x,p1.y,p1.z),p2=(p2.x,p2.y,p2.z),color=mdCol))    
    p1 = ocl.Point(dims[1], dims[2], dims[4]) # B
    p2 = ocl.Point(dims[1], dims[3], dims[4]) # G
    scr.addActor( camvtk.Line(p1=(p1.x,p1.y,p1.z),p2=(p2.x,p2.y,p2.z),color=mdCol))           


def toolpath_trace(myscreen, data):
    toolpaths,rapid_height,feed_height = data
    rapidColor = camvtk.pink
    XYrapidColor = camvtk.green
    plungeColor = camvtk.red
    feedColor = camvtk.yellow
    # zig path algorithm:
    # 1) lift to clearance height
    # 2) XY rapid to start of path
    # 3) plunge to correct z-depth
    # 4) feed along path until end    
    pos = ocl.Point(0,0,0) # keep track of the current position of the tool
    first = True
    # this is working for the zig paths
    
    for path in toolpaths:
        first_pt = path[0]
        if (first == True): # green sphere at path start
            myscreen.addActor( camvtk.Sphere(center=(first_pt.x,first_pt.y,rapid_height) , radius=0.1, color=camvtk.green) )
            # at start of program, assume we have already a rapid move here
            pos = ocl.Point(first_pt.x,first_pt.y,first_pt.z) 
            first = False
        else: # not the very first move
            # retract up to rapid_height
            myscreen.addActor( camvtk.Line(p1=( pos.x,pos.y,pos.z),p2=(pos.x,pos.y,feed_height),color=plungeColor) )
            myscreen.addActor( camvtk.Line(p1=( pos.x,pos.y,feed_height),p2=(pos.x,pos.y,rapid_height),color=rapidColor) )
            # XY rapid into position
            myscreen.addActor( camvtk.Line(p1=( pos.x,pos.y,rapid_height),p2=( first_pt.x,first_pt.y,rapid_height),color=XYrapidColor) )
            pos = ocl.Point(first_pt.x,first_pt.y,first_pt.z)

        # rapid down to the feed_height
        myscreen.addActor( camvtk.Line(p1=( pos.x,pos.y,rapid_height),p2=(pos.x,pos.y,feed_height),color=rapidColor) )
        # feed down to CL
        myscreen.addActor( camvtk.Line(p1=( pos.x,pos.y,feed_height),p2=(pos.x,pos.y,pos.z),color=plungeColor) )

        # feed along the path
        for p in path[1:]:
            myscreen.addActor( camvtk.Line(p1=( pos.x,pos.y,pos.z),p2=(p.x,p.y,p.z),color=feedColor) )
            pos = ocl.Point(p.x,p.y,p.z)

    # END retract up to rapid_height
    myscreen.addActor( camvtk.Line(p1=( pos.x,pos.y,pos.z),p2=(pos.x,pos.y,feed_height),color=plungeColor) )
    myscreen.addActor( camvtk.Line(p1=( pos.x,pos.y,feed_height),p2=(pos.x,pos.y,rapid_height),color=rapidColor) )
    myscreen.addActor( camvtk.Sphere(center=(pos.x,pos.y,rapid_height) , radius=0.1, color=camvtk.red) )

    camvtk.drawArrows(myscreen,center=(-0.5,-0.5,-0.5)) # XYZ coordinate arrows
    


