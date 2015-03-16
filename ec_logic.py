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
    #TODO all the lineas are to be config.set reading the appropriate vars
    # maybe passing it has an argument of the module
    config.add_section('Tool')
    #config.set('Section1', 'an_int', '15')
    config.set("Tool","name", t_name )
    for name,value in zip(glb.Tooldata,glb.t_data):    
        config.set("Tool",name,value)            
    config.set("Tool","sna",glb.shape[int(glb.t_data[0])])    

    config.add_section('Model')
    # Model data
    for name,value in zip(glb.WorkPcdata,glb.wpdata):    
        config.set("Model",name,str(value))                

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
           
    with open(p_fname, 'wb') as configfile:
        config.write(configfile)                
            
            