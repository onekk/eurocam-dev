# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 19:34:26 2015

@author: carlo-m
"""
import ocl
import datetime
import camvtk_mod as camvtk
   
def vtk_visualize_toolpath(stlfile, toolpaths,rapid_height,feed_height):
    myscreen = camvtk.VTKScreen()
    stl = camvtk.STLSurf(stlfile)
    myscreen.addActor(stl)
    stl.SetSurface() #
    #stl.SetWireframe()
    stl.SetColor(camvtk.cyan)
    myscreen.camera.SetPosition(15, 13, 7)
    myscreen.camera.SetFocalPoint(5, 5, 0)

    myscreen.camera.Zoom(0.5)

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


    t = camvtk.Text()
    t.SetPos( (myscreen.width-200, myscreen.height-100) )
    date_text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    t.SetText( "EuroCAM \n " + date_text + "\n Using OpenCAMLib \n" )
    myscreen.addActor(t)
    
    myscreen.render()
    myscreen.iren.Start()
