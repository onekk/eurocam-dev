# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 16:22:33 2015

use some code from 
simple parallel finish toolpath example
Anders Wallin 2014-02-23

@author: Carlo Dormeletti
"""


import os
import time
import math
import ConfigParser

import ec_ngc_fw  as ngc_fw # G-code output is produced by this module
import ec_glb as glb 


def search_paths(file_name):
    paths = map(
        lambda path: os.path.join(path, file_name),
        (
            './src/',
            './i18n/'
        ),
    )
    for path in paths:
        if os.path.isfile(path):
            return path

def setUnit(self):
    if int(glb.unit) == 0 :
        glb.tunit = self.mm
        glb.spunit = " mm/min"
    else:
        glb.tunit = self.inch
        glb.spunit = " IPS"

############## Tools Logic

def readTooltable(self):
    config = ConfigParser.SafeConfigParser()
    config.read(glb.f_tooltable)
    if config.sections() is not []:
        glb.Tools={}
        tdata = []
        for name in config.sections():
            for data in glb.Tooldata:
                tdata.append(config.get(name, data))
            if glb.debug > 3:    
                print tdata
             
            glb.Tools[str(name)] = tdata
            tdata = []
    else:
        print "file vuoto"
            
def writeTooltable(self):
    config = ConfigParser.SafeConfigParser()

    for k,v in glb.Tools.iteritems():
        config.add_section(k)
        for i,d in enumerate(glb.Tooldata):
            if glb.debug > 3:
                print k,d,str(v[i])
            config.set(k,d,str(v[i]))
    with open(glb.f_tooltable, 'wb') as configfile:
        config.write(configfile)    

def updateTool(self):
    writeTooltable(self)
    self.Log.append("Re Writing ToolTable")            
    readTooltable(self)
    self.Log.append("Re Read ToolTable")

############## Machine Logic

def readMachtable(self):
    config = ConfigParser.SafeConfigParser()
    config.read(glb.f_machtable)
    if config.sections() is not []:
        glb.Machs={}
        mdata = []
        for name in config.sections():
            for data in glb.Machdata:
                mdata.append(config.get(name, data))
      
            glb.Machs[str(name)] = mdata
            mdata = []
    else:
        print "file vuoto"

def writeMachtable(self):
    config = ConfigParser.SafeConfigParser()
    for k,v in glb.Machs.iteritems():
        config.add_section(k)
        for i,d in enumerate(glb.Machdata):
            config.set(k,d,str(v[i]))
    with open(glb.f_machtable, 'wb') as configfile:
        config.write(configfile)    
  
def updateMach(self):
    writeMachtable(self)
    self.Log.append("Re Writing MachTable")            
    readMachtable(self)
    self.Log.append("Re Read MachTable")


############## Workpiece Logic

def readWPtable(self):
    config = ConfigParser.SafeConfigParser()
    config.read(glb.f_wptable)
    if config.sections() is not []:
        glb.WorkPCs={}
        wpdata = []
        for name in config.sections():
            for data in glb.WorkPcdata:
                wpdata.append(config.get(name, data))
      
            glb.WorkPCs[str(name)] = wpdata
            wpdata = []
    else:
        print "file vuoto"

def writeWPtable(self):
    config = ConfigParser.SafeConfigParser()
    for k,v in glb.WorkPCs.iteritems():
        config.add_section(k)
        for i,d in enumerate(glb.WorkPcdata):
            config.set(k,d,str(v[i]))
    with open(glb.f_wptable, 'wb') as configfile:
        config.write(configfile)    
  
def updateWP(self):
    print glb.WorkPCs
    writeWPtable(self)
    self.Log.append("Re Writing WPTable")            
    readWPtable(self)
    self.Log.append("Re Read WPTable")

############## Path generation 


def writePathfile(self,p_fname,action):

    if os.path.exists(p_fname):
        msgtxt = self.msg_13m.format(p_fname)
        ret = self.myYesDiag("",msgtxt)
        if ret == "OK":
            pass
        else:
            return

    m_name =  glb.PCData[0]       
    t_name = glb.PCData[1]
    feedrate = glb.PCData[2]
    plungerate = glb.PCData[3]
    safe_height = glb.PCData[4]
    strat = glb.PCData[5]
    dircut = glb.PCData[6]
    xyovl =  glb.PCData[7] 
    z_steps = glb.PCData[8]           
                                  
    config = ConfigParser.SafeConfigParser()
    
    # add a general section to pass some variable or to set the beahviour of
    # the program modifying the pathgen.ini file
    config.add_section('General')
    config.set("General","debug",str(0))       
    config.set("General","ec_version",str(glb.version))
        
    config.add_section('Tool')
    #config.set('Section1', 'an_int', '15')
    config.set("Tool","name", t_name )
    for name,value in zip(glb.Tooldata,glb.t_data):    
        config.set("Tool",name,value)            
    config.set("Tool","sna",glb.shape[int(glb.t_data[0])])    


    config.add_section('WorkPiece')
    # Model data
    config.set("WorkPiece","xmin",str(glb.wpdim[0]))                
    config.set("WorkPiece","xmax",str(glb.wpdim[1]))            
    config.set("WorkPiece","ymin",str(glb.wpdim[2]))            
    config.set("WorkPiece","ymax",str(glb.wpdim[3]))
    config.set("WorkPiece","zmin",str(glb.wpdim[4]))            
    config.set("WorkPiece","zmax",str(glb.wpdim[5]))

                                    

    config.add_section('Machine')
    # Machine data
    config.set("Machine","mach_name",m_name) 
    config.set("Machine","preamble",glb.machdata[8])  
    config.set("Machine","postamble",glb.machdata[9])

    config.add_section('Path')
    # Path construction data

    config.set("Path", "xyovl",str(xyovl))
    config.set("Path", "strat",str(strat))    
    config.set("Path", "dir",dircut) 
    config.set("Path", "slices",str(len(z_steps)))

    for s_index,value in zip(xrange(1,len(z_steps)+1),z_steps):
        config.set("Path","slice-{}".format(s_index),str(value))

    config.set("Path", "action",action)
    config.set("Path", "feedrate",str(feedrate))
    config.set("Path", "plungerate",str(plungerate)) 
    config.set("Path", "safe_height",str(safe_height))    
    config.set("Path", "basename",glb.basename)
    config.set("Path", "stlfile",glb.model[0])        

    config.add_section('G-Code')
    # Control G-Code file output
    if glb.gcodec[0] is True: # GCmodel
        config.set("G-Code", "model","1")
    else:
        config.set("G-Code", "model","0")

    if glb.gcodec[1] is True: # GCmachine
        config.set("G-Code", "machine","1")
    else:
        config.set("G-Code", "machine","0")
        
    if glb.gcodec[2] is True: # GCtool
        config.set("G-Code", "tool","1")
    else:
        config.set("G-Code", "tool","0")
        
    if glb.gcodec[3] is True: # GCwp
        config.set("G-Code", "workp","1")
    else:
        config.set("G-Code", "workp","0")
        
    if glb.gcodec[4] is True: # GCtp
        config.set("G-Code", "toolpath","1")
    else:
        config.set("G-Code", "toolpath","0")        

    if glb.gcodec[5] is True: # GCverbose
        config.set("G-Code", "verbose","1")
    else:
        config.set("G-Code", "verbose","0") 

    if glb.gcodec[6] is True: # GCview
        config.set("G-Code", "view","1")
    else:
        config.set("G-Code", "view","0")

    config.set("G-Code", "decimals", str(glb.gcodec[7]))
               
    with open(p_fname, 'wb') as configfile:
        config.write(configfile)                
            
        # XY feed is the minimun between X and Y feedrate
        # TODO consider the material data    
        xyfeed = min(float(glb.machdata[3]),float(glb.machdata[4]))
        self.PCSBXYfc.setValue(xyfeed)
        zfeed = float(glb.machdata[5])
        self.PCSBZfc.setValue(zfeed)
          
def calc_process(self):
        # TODO consider the material data
        m_name = self.PCMachCB.currentText()             
        t_name = self.PCToolCB.currentText()
        #retrieve the wp coordinates from the display window
        glb.wpdim = self.md.get_wp_dim()
        print glb.wpdim
        #return # FIXME provvisorio        

        zmin = float(glb.wpdim[4])               
        zmax = float(glb.wpdim[5])
        
        wp_h = zmax - zmin  # workpiece height      

        # TODO if wp_h > max H_working emit a warning
    
        # TODO if the tool is not capable of centercut and the workpiece,
        # is small than the model emit a warning

        feedrate = self.PCSBXYfc.value()
        plungerate = self.PCSBZfc.value()
        zpc = self.PCSBZsd.value()
        xyovl = self.PCSBXYovl.value()
        
        # Select strategy for now it only cosmetic as only one strategy is
        # implemented  
        for i,obj in enumerate((self.PCSTRB1, self.PCSTRB2, self.PCSTRB3, self.PCSTRB4)):
            if obj.isChecked():
                if i == 0:
                    strat = "SR"
                    break            
                elif i == 1:
                    strat = "NC"
                    break
        else:
             msgtxt = self.msg_12m
             self.myYesDiag("",msgtxt,"",QMessageBox.Warning)
             return "KO"                    
        # dircut is obtained from the Process Tab (for now only X and Y work)

        for i,obj in enumerate((self.PCPDRB1, self.PCPDRB2, self.PCPDRB3, self.PCPDRB4)):
            if obj.isChecked():
                if i == 0:
                    dircut = "X"
                    break
                elif i == 1:
                    dircut = "Y"
                    break
        else:
            msgtxt = self.msg_08m
            self.myYesDiag("",msgtxt,"",QMessageBox.Warning)
            return "KO"                    

        # maybe shape has to be considered in step down calculations ? 
        # shape = int(glb.t_data[0])
        # TODO check the alghoritmn to obtain the slices
 
        # TODO check a minimal height for the purpose of having the piece
        # fixed on the base, or maybe create a grid of tabs, in the last pass?
        #
        #TODO elaborate the negative coordinate strategy 
        z_steps = []
        z_pass = 1
        # at the height of the piece         
        z_steps.append(zmax)
        c_ht = zmax - zpc
        if glb.debug > 1:
            print "wp_h = {0} zpc = {1}".format(wp_h,zpc)
            print "start loop"
        # FIXME verify for a redundant 0.0 slice
        while z_pass < 100: # set a safety for the number of pass
            print "c_ht = {0}  zmin = {1} zmax = {2}".format( c_ht,zmin,zmax)
           
            z_steps.append(c_ht)
            z_pass = z_pass + 1
            c_ht = c_ht - zpc
            c_ht = round(c_ht,5)
            if c_ht <= zmin:
                print c_ht, zmin
                z_steps.append(zmin)
                break
        else:
            print "error in loop"

        if glb.debug > 1:        
            print "end loop"    
            print z_steps 
     

        glb.z_steps = z_steps        
        
        safe_height = zmax + (zmax + 0.25) # TODO to be set in the UI 

        # put the calculated data in the appropriate places
        glb.PCData = []
        # 0 = m_name, 1 = t_name, 2 = feedrate, 3 = plungerate, 4 = safe_height
        # 5 = strat, 6 = dircut,  7 = xyovl,  8 = z_steps        
        glb.PCData.append(m_name)
        glb.PCData.append(t_name)
        glb.PCData.append(feedrate)
        glb.PCData.append(plungerate)
        glb.PCData.append(safe_height)
        glb.PCData.append(strat)
        glb.PCData.append(dircut)
        glb.PCData.append(xyovl) 
        glb.PCData.append(z_steps)
         
        # All the validation are OK make the button visible
        #self.PCPBCt.setVisible(True) # TODO activate when the Tab is done  
        self.PCPBGenG.setVisible(True)            