#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
author: Carlo Dormeletti
website: http://github.com/...
last edited: February 2015
"""

import sys
import os
import errno
import time
import math
from PySide import QtCore
from PySide.QtGui import *
from subprocess import call

#----- Eurocam modules
import ec_glb as glb 
from eurocam_ui import Ui_MainWindow
import ec_logic as EC_L
import ec_ui_act as EC_UA
import visvis as vv
plot = vv.use('pyside')
import ec_mview as ECM
stime = time.time()


class MainWindow(QMainWindow, Ui_MainWindow):
   
    def __init__(self, parent=None):
        # maybe a spash screen goes here?
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)    

        # Binding for menu and close action

        self.actionOpen_Drawing.triggered.connect(self.Open_Drawing)
        self.actionAbout_EuroCAM.triggered.connect(self.About_EuroCAM)
        self.actionExit.triggered.connect(self.close) 

        # Binding for Tool Tab 

        self.ToolNewPB.clicked.connect(self.toolNew)
        self.ToolModPB.clicked.connect(self.toolMod)
        self.ToolDelPB.clicked.connect(self.toolDel)
        self.TTConf.clicked.connect(self.toolConf)
        self.TGCBCc.activated.connect(self.TGCBCc_State)
        self.TGCBTyp.activated.connect(self.TGCBTyp_State)
        self.connect(self.ToolCB, QtCore.SIGNAL('activated(QString)'), self.tool_chosen)

        # Binfindg for Machine Tab

        self.MachNewPB.clicked.connect(self.machNew)
        self.MachModPB.clicked.connect(self.machMod)        
        self.MachDelPB.clicked.connect(self.machDel)
        self.MachConfPB.clicked.connect(self.machConf)        
        self.connect(self.MachCB, QtCore.SIGNAL('activated(QString)'), self.mach_chosen)
        self.MGCoCB.activated.connect(self.mcoord_State)

        # Binding for Workpiece Tab

        self.connect(self.WPCB, QtCore.SIGNAL('activated(QString)'), self.wp_chosen)
        self.WPNewPB.clicked.connect(self.wpNew)
        self.WPModPB.clicked.connect(self.wpMod)        
        self.WPDelPB.clicked.connect(self.wpDel)
        self.WPConfPB.clicked.connect(self.wpConf)     

        #Binding for Process Tab

        self.connect(self.PCMachCB, QtCore.SIGNAL('activated(QString)'), self.pc_mach_chosen)
        self.connect(self.PCToolCB, QtCore.SIGNAL('activated(QString)'), self.pc_tool_chosen)
        self.connect(self.PCWPCB, QtCore.SIGNAL('activated(QString)'), self.pc_wp_chosen)        
        self.PCPBCal.clicked.connect(self.pc_calc_task)
        self.PCPBGenG.clicked.connect(self.pc_genG) 
        self.PCPBCt.clicked.connect(self.pc_createTask)        

        # don't needed for now here for reference
        #self.PCSBXYovl.valueChanged.connect(self.pc_SBXYovl_uV)    
        #self.PCSBSdc.valueChanged.connect(self.pc_SB_uV)    
        #self.PCSBOvl.valueChanged.connect(self.pc_Ovl_uV)    
        
        self.connect(self.MainTab,QtCore.SIGNAL('currentChanged(int)'),self.MainTabchosen)        


        self.StartAction()

    def StartAction(self):
        self.Log.append(" EuroCAM")
        
        self.Log.append(" Inifile = {0}".format(glb.inifile))


        ####################################################################
        #                                                                  #
        # To make the translation work the content have to be put here     #
        #                                                                  #
        ####################################################################
       
        self.toolcyl = self.tr("Cylindrical")
        self.toolsph = self.tr("Spherical (Ball)")        
        self.tooltor = self.tr("Toroidal (Bull)") 
        self.toolcon = self.tr("Conical (V shape)") 

        glb.shape = (self.toolcyl, self.toolsph, self.tooltor, self.toolcon)
         
        glb.yes = self.tr("Yes")            
        glb.no = self.tr("No") 
       
        glb.radius = self.tr("Radius")
        glb.CorRad = self.tr("Corner Radius")   
        glb.Angle = self.tr("Angle")   
        glb.degree = self.tr(" deg")
        
        self.mm = " mm"
        self.inch = self.tr(" inch")

        glb.tool_plu = self.tr("Tools")
        glb.mach_plu = self.tr("Machines")
        glb.wp_plu = self.tr("Work Pieces")
        
        glb.tool_sin = self.tr("Tool")
        glb.mach_sin = self.tr("Machine")
        glb.wp_sin = self.tr("Work Piece")
         
        self.posco = self.tr("Positive Coordinates")
        self.negco = self.tr("Negative Coordinates")

        glb.coord = (self.posco,self.negco)
        

        ####################################################################        
        #                                                                  # 
        # QMessageBox string are put here to make them correctly translate # 
        #                                                                  #
        ####################################################################

        # Exit Dialog        
        self.msg_01t = self.tr("<b>Exit Dialog</b>")
        self.msg_01m = self.tr("Are you sure you want to exit?")

        # About EuroCAM Box
        self.msg_02t = self.tr("About EuroCAM")
        self.msg_02m = self.tr("<p align =  center><b>EuroCAM</b>  \
            <br> version {} <br> copyright Carlo Dormeletti 2015 </p><hr>\
            <p align = left> It generates G-Code ready to be sent to a CNC \
            machine.<br></p><p>It uses the great OpenCAMlib by Anders \
            Wallins <br><b> https://github.com/aewallin/opencamlib\</b><br></p>\
            ").format(glb.version)        

        self.msg_03t = self.tr("This data are correct, do you want to write them? ")
        self.msg_04m = self.tr("Are you sure you wan to delete this {0}? ")
        self.msg_05m = self.tr("Only one {0} left, you can't cancel all {1}.")
        self.msg_06t = self.tr("Insert {0} Name")
        self.msg_06m = self.tr("Spaces will be substitude with underscore (_)")        
        self.msg_07m = self.tr("The name <b>'{0}'</b>  is present.<br> <br> \
                       Please choose another name.")
        self.msg_08m = self.tr("At least one path direction has to be checked")                
        self.msg_09m = self.tr("At least one path has to be checked")  
        self.msg_10m = self.tr("You have to load a model to generate a path")
        self.msg_11m = self.tr("Cutter length cannot be great than overall length")
        self.msg_12m = self.tr("You have to select a <b> Path Strategy </b> to \
                        generate a toolpath") 
        self.msg_13m = self.tr("{0} Exist. It will be overwritten.")                        

        self.msg_14m = self.tr("The ini file will be created in {0}")
        self.msg_15m = self.tr("The tools table will be created in {0}")
        self.msg_16m = self.tr("The machines table will be created in {0}")
        self.msg_17m = self.tr("The workpieces table will be created in {0}")

        self.msg_i01 = self.tr("Warning")
                        
        ####################################################################

        # check the esistence of the ini files and crete them if necessary 
        if glb.inifile is None:
            if glb.localini == 1:
                self.create_inifile("./EuroCAM")
            else:
                self.create_inifile("~/.config/EuroCAM")
 
        self.readSettings()                  
        EC_L.setUnit(self)

        # set the unit label
        if int(glb.unit) == 0 :
            glb.dunit = self.tr("Unit = mm")
        else:
            glb.dunit = self.tr("Unit = Inch")     

        # check the presence of the tool table file and create it if necessary

        if glb.f_tooltable is None:
            if glb.localini == 1:
                self.create_toolfile("./EuroCAM")
            else:
                self.create_toolfile("~/.config/EuroCAM")

        EC_L.readTooltable(self)
        self.Log.append("ToolTable Initizialization")

        # check the presence of the machine file and create it if necessary
            
        if glb.f_machtable is None:            
            if glb.localini == 1:
                self.create_machfile("./EuroCAM")
            else:
                self.create_machfile("~/.config/EuroCAM")

        EC_L.readMachtable(self)
        self.Log.append("MachTable Initizialization")

        # check the presence of the machine file and create it if necessary

        if glb.f_wptable is None:
            if glb.localini == 1:
                self.create_wpfile("./EuroCAM")
            else:
                self.create_wpfile("~/.config/EuroCAM")

        EC_L.readWPtable(self)
        self.Log.append("WPTable Initizialization")
        
        EC_UA.initUI(self)
        self.Log.append("UI initialisation")

        EC_UA.writeTooldata(self,self.ToolCB.currentText())
        EC_UA.writeMachdata(self,self.MachCB.currentText())
        EC_UA.writeWPdata(self,self.WPCB.currentText())

        # populate and pre initialize the Process Tab
        EC_UA.popPCdata(self)

        self.pc_step_data()
        self.pc_feed_data()
        self.RightTB.setCurrentIndex(0) # select the Image ToolBox

        glb.basename = os.path.join(os.path.dirname(__file__), 'ngc',glb.basename)

        self.IL_2.setText("Basename Set")
        self.IL_2.setToolTip("Basename = <b>{0}</b>".format(glb.basename))  

        EC_UA.initGV(self)
        if self.MainTab.currentIndex() == 2:
            EC_UA.toolPaint(self)            

        #self.PLOT = QWidget()  
        #self.RightTB.addItem(self.PLOT, "Vis Vis")        
        # Make figure using "self" as a parent
        #Figure = plot.GetFigureClass()
        #self.fig = Figure(self.PLOT)
        #Figure._SetPosition(self.fig,0,0,350,350)
       

    def create_inifile(self,path):
        msgtxt = self.msg_14m.format(path)
        self.myYesDiag(self.msg_i01,msgtxt,"",QMessageBox.Information)        
        self.create_path_and_inifile(path,glb.inif_name)        
        glb.inifile = glb.ini_search_paths(glb.inif_name)        
        self.writeSettings()


    def create_toolfile(self,path):
        msgtxt = self.msg_15m.format(path)
        self.myYesDiag(self.msg_i01,msgtxt,"",QMessageBox.Information)   
        self.create_path_and_inifile(path,glb.toolf_name)
        glb.f_tooltable = glb.ini_search_paths(glb.toolf_name)
        EC_L.writeTooltable(self) 
        

    def create_machfile(self,path):
        msgtxt = self.msg_16m.format(path)
        self.myYesDiag(self.msg_i01,msgtxt,"",QMessageBox.Information)
        self.create_path_and_inifile(path,glb.machf_name) 
        glb.f_machtable = glb.ini_search_paths(glb.machf_name)
        EC_L.writeMachtable(self)


    def create_wpfile(self,path):
        msgtxt = self.msg_17m.format(path)
        self.myYesDiag(self.msg_i01,msgtxt,"",QMessageBox.Information)
        self.create_path_and_inifile(path,glb.wp_name)               
        glb.f_wptable = glb.ini_search_paths(glb.wp_name)        
        EC_L.writeWPtable(self) 

######### inifile actions

    def readSettings(self):
        settings = QtCore.QSettings(glb.inifile, QtCore.QSettings.IniFormat)    
        pos = settings.value("pos", QtCore.QPoint(200, 200))
        size = settings.value("size", QtCore.QSize(400, 400))
        self.resize(size)
        self.move(pos)
        settings.beginGroup("Preferences")
        glb.unit = settings.value("unit")
        settings.endGroup()       

    def writeSettings(self):
        settings = QtCore.QSettings(glb.inifile, QtCore.QSettings.IniFormat)    
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())
        settings.beginGroup("Preferences")
        settings.setValue("unit", glb.unit)
        #settings.setValue("other","prova")
        settings.endGroup()

######### 


    def MainTabchosen(self,value):
        if value == 2:
            EC_UA.toolPaint(self)
        else:
            print "Tab number = ",value
            EC_UA.clearGV(self)
       
    def About_EuroCAM(self):
        QMessageBox.about(self,self.msg_02t,self.msg_02m) 
        
    def maybeSave(self):
        if glb.ModelMod is True:
            ret = QMessageBox.warning(self, "Application",
                    "The document has been modified.\nDo you want to save "
                    "your changes?",
                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            if ret == QMessageBox.Save:
                return self.save()
            elif ret == QMessageBox.Cancel:
                return False
        return True

    def Open_Drawing(self):
        fileName, filtr = QFileDialog.getOpenFileName(self)
        if fileName:
            glb.model[0] = fileName
            # assign the basename model as the fileName without the extension
            # and put it in
            ngcdir = os.path.join(os.path.dirname(__file__), 'ngc')
            basename = os.path.splitext(os.path.basename(fileName))[0]
            glb.basename =  os.path.join(ngcdir,basename)
            self.model_info(fileName)           
            glb.M_Load = True
            EC_UA.popPCdata(self)            
            self.PCPBCal.setVisible(True)
        else:
            return
    
    def model_info(self,filename):
        self.IL_1.setText("Model Loaded")
        self.IL_1.setToolTip("Model name = <b>{0}</b>".format(filename))
        self.IL_2.setText("Basename Set")
        self.IL_2.setToolTip("Basename = <b>{0}</b>".format(glb.basename))        
        self.MdTName.setText("<b>{0}</b>".format(filename))
        self.surf = vv.meshRead(filename)
        md = ECM.ModelWindow()
        md.Plot(self.surf)
        dimx,dimy,dimz = md.getBB()
        print dimx, dimy, dimz
        self.MdTmX.setText("{0:6.3f}".format(dimx.min))        
        self.MdTmY.setText("{0:6.3f}".format(dimy.min))
        self.MdTmZ.setText("{0:6.3f}".format(dimz.min))         
        self.MdTMX.setText("{0:6.3f}".format(dimx.max))        
        self.MdTMY.setText("{0:6.3f}".format(dimy.max))
        self.MdTMZ.setText("{0:6.3f}".format(dimz.max))

        
    def askBasename(self):
        ans = self.askGname("Messaggio"," NGC File ")
        if ans == "KO":
            return
        else:
            glb.basename = ans


    def save(self):
        self.statusbar.showMessage("save selected")


    # event : QCloseEvent
    def closeEvent(self, event):
        msgBox = QMessageBox()
        msgBox.setText(self.msg_01t)
        msgBox.setInformativeText(self.msg_01m)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msgBox.setDefaultButton(QMessageBox.Yes)
        msgBox.setIcon(QMessageBox.Question)
        ret = msgBox.exec_()
        event.ignore()
        if ret == QMessageBox.Yes:
            self.Log.append("Writing Settings") 
            self.writeSettings()
            event.accept()
        elif ret == QMessageBox.Cancel:
            event.ignore()


    def create_path_and_inifile(self,path,inifile):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        try:
            inifile = os.path.join(path,inifile)
            print inifile                       
            with open(inifile,'w') as file:
                file.close()
        except IOError as e:
            msgtit = "Warning"
            msgtxt = "Unable to create file {0} in {1}".format(inifile,path)
            icon = QMessageBox.Information                
            self.myYesDiag(msgtit,msgtxt,icon)


    def dataModDiag(self,ctst,msginfo):
        mtxt = "<table border='1' width = '300'>"
        tln0 = "<tr><td> {0} </td><td align='right'>{1:.3}</td><td align='right'>{2:.3}</td></tr>"
        tln1 = "<tr><td> {0} </td><td align='right'>{1}</td><td align='right'>{2}</td></tr>"
        tln2 = "<tr><td> {0} </td><td>{1}</td><td>{2}</td></tr>"
        if ctst == 0: # Tool Data
            for i,v in enumerate(glb.datahead):
                if i in (0,4,5):
                    mtxt = mtxt + tln1.format(v,glb.oldata[i],glb.newdata[i]) 
                elif i == 6:
                    mtxt = mtxt + tln2.format(v,glb.oldata[i],glb.newdata[i]) 
                else:
                    mtxt = mtxt + tln0.format(v,glb.oldata[i],glb.newdata[i])                     
        elif ctst == 1: # Machine data
            for i,v in enumerate(glb.datahead):
                #if glb.debug:
                #    print "I V old New =>>",i,v,glb.oldata[i],glb.newdata[i]
                if i in (0,1,2,3,4,5):
                    mtxt = mtxt + tln0.format(v,glb.oldata[i],glb.newdata[i]) 
                elif i in (7,8,9):
                    mtxt = mtxt + tln2.format(v,glb.oldata[i],glb.newdata[i]) 
                else:
                    mtxt = mtxt + tln1.format(v,glb.oldata[i],glb.newdata[i]) 
        elif ctst == 2: # WP data
            for i,v in enumerate(glb.datahead):
                if glb.debug:
                    print "I V old New =>>",i,v,glb.oldata[i],glb.newdata[i]
                if i in (0,1,2,3,4,5):
                    mtxt = mtxt + tln0.format(v,glb.oldata[i],glb.newdata[i]) 
                elif i == 7:
                    mtxt = mtxt + tln2.format(v,glb.oldata[i],glb.newdata[i]) 
                else:
                    mtxt = mtxt + tln1.format(v,glb.oldata[i],glb.newdata[i]) 
     
        mtxt = mtxt + "</table>"       

        ret = self.myYesDiag("",mtxt, msginfo,QMessageBox.Question)
             
        if ret == "OK":
            return "OK"
        elif ret == "KO":
            return "KO" 
   

    def showdataDiag(self,ctst,msginfo):
        retrun
        mtxt = "<table border='1' width = '300'>"
        tln0 = "<tr><td> {0} </td><td align='right'>{1:.3}</td></tr>"
        tln1 = "<tr><td> {0} </td><td align='right'>{1}</td></tr>"
        tln2 = "<tr><td> {0} </td><td>{1}</td></tr>"
        if ctst == 0: # Path Data
            for i,v in enumerate(glb.showhead):
                print i,v
                if i in (2,3,4,5):
                    mtxt = mtxt + tln0.format(v,glb.showdata[i]) 
                elif i in (0,1):
                    mtxt = mtxt + tln2.format(v,glb.showdata[i]) 
                else:
                    mtxt = mtxt + tln1.format(v,glb.showdata[i])                     
        elif ctst == 1: # no data for now
            for i,v in enumerate(glb.datahead):
                #if glb.debug:
                #    print "I V old New =>>",i,v,glb.oldata[i],glb.newdata[i]
                if i in (): #decimal data
                    mtxt = mtxt + tln0.format(v,glb.showdata[i]) 
                elif i in (): # string data
                    mtxt = mtxt + tln2.format(v,glb.showdata[i]) 
                else: # integer data
                    mtxt = mtxt + tln1.format(v,glb.showdata[i]) 
     
        mtxt = mtxt + "</table>"       

        ret = self.myYesDiag("",mtxt, msginfo,QMessageBox.Question)
             
        if ret == "OK":
            pass
        elif ret == "KO":
            return "KO" 
   

    def myYesDiag(self,msgtit,msgtxt,msginfo = "" ,icon = QMessageBox.Warning ):
        msgBox = QMessageBox()
        msgBox.setText(msgtxt)
        msgBox.setInformativeText(msginfo)
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel )
        msgBox.setDefaultButton(QMessageBox.Yes)
        msgBox.setIcon(icon)
        ret = msgBox.exec_()
        if ret == QMessageBox.Yes:
            return "OK"
        elif ret == QMessageBox.Cancel:
            return "KO" 
        return "KO" 


    def askMoTname(self,O_data,O_type):
        msg = self.msg_06t.format(O_type)
        text, ok = QInputDialog.getText(self, msg,self.msg_06m)
        
        O_name = text.replace (" ", "_")
    
        if O_name in O_data:
            msgtxt = self.msg_07m.format(O_name)
            self.myYesDiag("",msgtxt,QMessageBox.Warning)
            return "KO"
        else:
            return O_name

    def askGname(self,msg,type):
        msg = self.msg_06t.format(type)
        text, ok = QInputDialog.getText(self, msg,self.msg_06m)
        O_name = text.replace (" ", "_")
        return O_name

    ################################################
    #                                              #
    # Tools Tab related actions                    #
    #                                              #
    ################################################


    def tool_chosen(self, text):
        EC_UA.writeTooldata(self,text)


    def toolNew(self):
        ans = self.askMoTname(glb.Tools,glb.tool_sin)
        if ans == "KO":
            return
        else:
            glb.mot_name = ans
            glb.NewTool = True
            glb.EditTool = True
            EC_UA.greyToolB(self,False)            
            EC_UA.clearToolUI(self)
            glb.oldata = [0,0.0,0.0,0.0,0.0,0.0,0,0,""]


    def toolMod(self):
        glb.EditTool = True
        EC_UA.greyToolB(self,False)
        ttype = int(self.TGCBTyp.currentIndex())
        EC_UA.toolConstraint(self,ttype)
        EC_UA.toolMask(self,False)
        glb.oldata = EC_UA.readTool(self)
        glb.mod_mot_name = self.ToolCB.currentText()
        


    def toolDel(self):
        if self.ToolCB.count() < 2: #2
            msgtxt = self.msg_05m.format(glb.tool_sin,glb.tool_plu)
            self.myYesDiag("",msgtxt,QMessageBox.Warning) 
            return
        else:    
            glb.mod_mot_name = self.ToolCB.currentText()
            glb.oldata = glb.Tools[glb.mod_mot_name]
            glb.newdata = [0,0.0,0.0,0.0,0,0,0,0,""]
            
            glb.datahead= (self.TGLTyp.text(), self.TGLDia.text(), 
                   self.TGLRad.text(), self.TGLLen.text(), self.TGLOvl.text(),
                   self.TGLShd.text(), self.TGLFlu.text(), self.TGLCc.text(), 
                   self.TGLnote.text())
            
            ans = self.dataModDiag(0,self.msg_04m.format(glb.tool_sin))               
            if ans == "OK":
                del glb.Tools[glb.mod_mot_name]
                self.toolUpdate()
            else:
                pass

      
    def toolConf(self):
        glb.newdata = EC_UA.readTool(self)
        if glb.newdata[3] > glb.newdata[4]:
            msgtxt = self.msg_11m
            self.myYesDiag("",msgtxt,QMessageBox.Warning)                             
            return        
        EC_UA.toolMask(self,True)
        glb.EditTool = False

        glb.datahead = (self.TGLTyp.text(), self.TGLDia.text(), 
               self.TGLRad.text(), self.TGLLen.text(), self.TGLOvl.text(), 
               self.TGLShd.text(), self.TGLFlu.text(), self.TGLCc.text(),
               self.TGLnote.text())
               
        ans = self.dataModDiag(0,self.msg_03t)               
        if ans == "OK":
            if glb.NewTool is False:
                glb.Tools[glb.mod_mot_name] = glb.newdata
                self.toolUpdate()
            else:
                glb.Tools[glb.mot_name] = glb.newdata
                self.toolUpdate()
        else:
            pass

        glb.NewTool = False
        EC_UA.greyToolB(self,True)


    def toolUpdate(self):
        EC_L.updateTool(self)                
        EC_UA.popToolUI(self)
        EC_UA.writeTooldata(self,self.ToolCB.currentText())
        self.Log.append("Re Populating UI Tooltable")

    def TGCBCc_State(self,value):
       key = self.ToolCB.currentText() # the name of the tool
       tooldata = glb.Tools[key]
       
       if glb.EditTool is False:            
           self.TGCBCc.setCurrentIndex(int(tooldata[5]))               
       else:
           pass

    def TGCBTyp_State(self,value):
       key = self.ToolCB.currentText() # the name of the tool
       tooldata = glb.Tools[key]
       
       if glb.EditTool is False:            
           self.TGCBTyp.setCurrentIndex(int(tooldata[0]))               
       else:
           ttype = int(self.TGCBTyp.currentIndex())
           EC_UA.toolConstraint(self,ttype)
           EC_UA.toolMask(self,False)

           
    ################################################
    #                                              #
    # Machine Tab related actions                  #
    #                                              #
    ################################################


    def mach_chosen(self, text):
        EC_UA.writeMachdata(self,self.MachCB.currentText())


    def mcoord_State(self,value):
        key = self.MachCB.currentText() # the name of the tool
        machdata = glb.Machs[key]        
        if glb.EditMach is False:
            self.MGCoCB.setCurrentIndex(int(machdata[6]))               
        else:
            pass

    
    def machNew(self):
        ans = self.askMoTname(glb.Machs,glb.mach_sin)
        if ans == "KO":
            return
        else:
            glb.mot_name = ans
            glb.NewMach = True
            glb.EditMach = True
            EC_UA.greyMachB(self,False)
            EC_UA.clearMachUI(self)
            # Set the Machine mask readable 
            EC_UA.machMask(self,False)
            glb.oldata = [0.0,0.0,0.0,0.0,0.0,0.0,0,"","",""]


    def machMod(self):
        glb.EditMach = True
        EC_UA.greyMachB(self,False)
        EC_UA.machMask(self,False)
        glb.oldata = EC_UA.readMach(self)
        glb.mod_mot_name = self.MachCB.currentText()
        
        
    def machDel(self):
        if self.MachCB.count() < 2:
            msgtxt = self.msg_05m.format(glb.mach_sin,glb.mach_plu)
            self.myYesDiag("",msgtxt,QMessageBox.Warning) 
            return
        else:    
            glb.mod_mot_name = self.MachCB.currentText()
            glb.oldata = glb.Machs[glb.mod_mot_name]
            glb.newdata = [0.0,0.0,0.0,0.0,0.0,0.0,0,"","",""]
            
            glb.datahead = (self.MGLTX.text(), self.MGLTY.text(), self.MGLTZ.text(),
                        self.MGLFX.text(), self.MGLFY.text(), self.MGLFZ.text(),
                        self.MGLCo.text(), self.MGLnote.text(),
                        self.MGLpre.text(), self.MGLpost.text() )
            
            ans = self.dataModDiag(0,self.msg_04m.format(glb.mach_sin))               
            if ans == "OK":
                del glb.Machs[glb.mod_mot_name]
                self.machUpdate()
            else:
                pass


    def machConf(self):
        glb.newdata = EC_UA.readMach(self)
        EC_UA.machMask(self,True)
        glb.EditMach = False
        glb.datahead = (self.MGLTX.text(), self.MGLTY.text(), self.MGLTZ.text(),
                        self.MGLFX.text(), self.MGLFY.text(), self.MGLFZ.text(),
                        self.MGLCo.text(), self.MGLnote.text(),
                        self.MGLpre.text(), self.MGLpost.text() )
               
        ans = self.dataModDiag(1,self.msg_03t)               
        if ans == "OK":
            if glb.NewMach is False:
                glb.Machs[glb.mod_mot_name] = glb.newdata
                self.machUpdate()
            else:
                glb.Machs[glb.mot_name] = glb.newdata
                self.machUpdate()
        else:
            pass

        glb.NewMach = False
        EC_UA.greyMachB(self,True)


    def machUpdate(self):
        EC_L.updateMach(self)                
        EC_UA.popMachUI(self)
        EC_UA.writeMachdata(self,self.MachCB.currentText())
        self.Log.append("Re Populating UI Machines table")


    ################################################
    #                                              #
    # Workpiece Tab related actions                #
    #                                              #
    ################################################

    def wp_chosen(self, text):
        print "wpc chosen  = ",text
        EC_UA.writeWPdata(self,self.WPCB.currentText())

    def wpNew(self):
        ans = self.askMoTname(glb.WorkPCs,glb.wp_sin)
        if ans == "KO":
            return
        else:
            glb.mot_name = ans
            glb.NewWP = True
            glb.EditWP = True
            EC_UA.greyWPB(self,False)
            EC_UA.clearWPUI(self)
            # Set the WP mask readable 
            EC_UA.wpMask(self,False)
            glb.oldata = [0.0,0.0,0.0,0.0,0.0,0.0,0,""]        
        
    def wpMod(self):    
        glb.EditWP = True
        EC_UA.greyWPB(self,False)
        EC_UA.wpMask(self,False)
        glb.oldata = EC_UA.readWP(self)
        glb.mod_mot_name = self.WPCB.currentText()        
        
    def wpDel(self):     
        print "self.WPDelPB.clicked"
        # TODO Check the working
        if self.WPCB.count() < 2:
            msgtxt = self.msg_05m.format(glb.wp_sin,glb.wp_plu)
            self.myYesDiag("",msgtxt,QMessageBox.Warning) 
            return
        else:    
            glb.mod_mot_name = self.WPCB.currentText()
            glb.oldata = glb.WorkPCs[glb.mod_mot_name]
            glb.newdata = [0.0,0.0,0.0,0.0,0.0,0.0,0,""]

            glb.datahead = ("{0} lower".format(self.WPGLDX.text()),
                            "{0} upper".format(self.WPGLDX.text()),
                            "{0} lower".format(self.WPGLDY.text()),
                            "{0} upper".format(self.WPGLDY.text()),
                            "{0} lower".format(self.WPGLDZ.text()),
                            "{0} upper".format(self.WPGLDZ.text()),
                            self.WPGLMat.text(),
                            self.WPGLNote.text() ) 
                            
            ans = self.dataModDiag(2,self.msg_04m.format(glb.wp_sin))               
            if ans == "OK":
                del glb.WorkPCs[glb.mod_mot_name]
                self.wpUpdate()
            else:
                pass        
        
    def wpConf(self):
        glb.newdata = EC_UA.readWP(self)
        EC_UA.wpMask(self,True)
        glb.EditWP = False
        print glb.newdata
        glb.datahead = ("{0} lower".format(self.WPGLDX.text()),
                        "{0} upper".format(self.WPGLDX.text()),
                        "{0} lower".format(self.WPGLDY.text()),
                        "{0} upper".format(self.WPGLDY.text()),
                        "{0} lower".format(self.WPGLDZ.text()),
                        "{0} upper".format(self.WPGLDZ.text()),
                        self.WPGLMat.text(),
                        self.WPGLNote.text() )
               
        ans = self.dataModDiag(2,self.msg_03t)
        if ans == "OK":
            if glb.NewWP is False:
                print "Modifica WP"
                print "Prima ", glb.WorkPCs[glb.mod_mot_name]
                glb.WorkPCs[glb.mod_mot_name] = glb.newdata
                print "Dopo ", glb.WorkPCs[glb.mod_mot_name]                
                self.wpUpdate()
            else:
                print "Nuovo WP"                
                glb.WorkPCs[glb.mot_name] = glb.newdata
                self.wpUpdate()
        else:
            pass

        glb.NewWP = False
        EC_UA.greyWPB(self,True)        


    def wpUpdate(self):
        EC_L.updateWP(self)                
        EC_UA.popWPUI(self)
        EC_UA.writeWPdata(self,self.WPCB.currentText())
        self.Log.append("Re Populating UI WorkPieces table")



    ################################################
    #                                              #
    # Processes Tab related actions                #
    #                                              #
    ################################################

 
    def pc_mach_chosen(self,value):
        glb.machdata = glb.Machs[value]        
        self.pc_feed_data()          
        # Deactivate the buttons because some parameters are changed
        self.PCPBCt.setVisible(False)
        self.PCPBGenG.setVisible(False)       
 

    def pc_tool_chosen(self,value):
        glb.t_data = glb.Tools[value]              
        self.pc_step_data()          
        # Deactivate the buttons because some parameters are changed
        self.PCPBCt.setVisible(False)
        self.PCPBGenG.setVisible(False)       


    def pc_wp_chosen(self,value):
        glb.wpdata = glb.WorkPCs[value]
        # TODO insert the correction for feed and step based on material
        # properties?
        #self.pc_feed_data() 
        #self.pc_step_data()                        
        # Deactivate the buttons because some parameters are changed
        self.PCPBCt.setVisible(False)
        self.PCPBGenG.setVisible(False)       


    def pc_createTask(self):
        p_fname = "./pathfile.ini"
        EC_L.writePathfile(self,p_fname,"tsk")            


    def pc_genG(self):
        # the filename has to be "pathgen.ini" because it is hardcoded
        # in ec_tpath.py as the input file
        p_fname = "./pathgen.ini"
        EC_L.writePathfile(self,p_fname,"ngc")
        # call the external program to generate Gcode    
        call(["python","ec_tpath.py"]) #if in same directory, else get abs path 
    

    def pc_calc_task(self):
        self.Log.append("Collecting task data")
        # Deactivate the controls 
        self.PCPBCt.setVisible(False)
        self.PCPBGenG.setVisible(False)
        #self.pc_coll_data()
        # Run the data check and the preliminary calculations        
        ret = self.pc_calc_data()
        if ret == "KO":
            pass
        else:
            pass 
            # do something
        
    def pc_step_data(self):
        diameter = float(glb.t_data[1]) 
        self.PCTTd.setText("{0:.4} {1}".format(diameter,glb.tunit))
        # Step down increment is obtained from the rules of thumb:
        # diameter/2 
        # TODO consider the material data
        # and then tuned by the spinbox controls
        preset = float(diameter/2)
        self.PCSBXYovl.setValue(preset)
        self.PCSBZsd.setValue(preset)    

    def pc_feed_data(self):
        # XY feed is the minimun between X and Y feedrate
        # TODO consider the material data    
        xyfeed = min(float(glb.machdata[3]),float(glb.machdata[4]))
        self.PCSBXYfc.setValue(xyfeed)
        zfeed = float(glb.machdata[5])
        self.PCSBZfc.setValue(zfeed)
          
    def pc_calc_data(self):
        # TODO consider the material data
        m_name = self.PCMachCB.currentText()             
        t_name = self.PCToolCB.currentText()
        wp_h = float(glb.wpdata[5])-float(glb.wpdata[4])  # height = zmax-zmin     
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
            self.myYesDiag("",msgtxt,QMessageBox.Warning)
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
        z_steps.append(wp_h)
        c_ht = wp_h - zpc
        
        while c_ht > 0:
            z_steps.append(c_ht)
            z_pass = z_pass + 1
            c_ht = c_ht - zpc
            c_ht = int((c_ht * 10000) + 0.5) / 10000.0
            
        z_steps.append(0)     

        glb.z_steps = z_steps        
        
        safe_height = 10 

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
        self.PCPBCt.setVisible(True)
        self.PCPBGenG.setVisible(True)

    
##########################################
#                                        #
# Main Loop                              #
#                                        #
##########################################

def main():
    if glb.debug > 4:
        print "main init"
        print __file__
        print os.path.join(os.path.dirname(__file__), '..')
        print os.path.dirname(os.path.realpath(__file__))
        print os.path.abspath(os.path.dirname(__file__))    
        
    locale = QtCore.QLocale.system().name()
    translator = QtCore.QTranslator()
    #translator.load("qt_" + locale, QtCore.QLibraryInfo.location(QtCore.QLibraryInfo.TranslationsPath))
    r = EC_L.search_paths(locale + ".qm") 
    translator.load(r)
   
    app = QApplication(sys.argv)
    app.installTranslator(translator)

    frame = MainWindow()
    frame.show()    
    app.exec_()
"""
def main():
    app = QApplication(sys.argv)
    pixmap = QPixmap(":/splash.png")
    splash = QSplashScreen(pixmap)
    splash.show()
    app.processEvents()
    ...
    window = QMainWindow()
    window.show()
    splash.finish(&window)
    return app.exec_()

"""

if __name__ == '__main__':
    main()

