# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 17:51:47 2015

@author: carlo-m
"""
import ec_glb as glb
import PySide.QtGui as QtGui
import PySide.QtCore as QtCore


def init_ui(self):
     # Clear the upper labels
    for obj in (self.IL_1 , self.IL_2 , self.IL_3 , self.IL_4 , self.IL_5):
        obj.setText("")

    # Set the units in the QEditText Boxes
    set_ui_unit(self)

    clear_model_tab(self)
    tool_ui_populate(self)
    mach_ui_populate(self)
    wp_ui_populate(self)
    init_processes_ui(self)
    init_gcode_ui(self)


def set_ui_unit(self):
    # set the Unit in the Tool Tab
    for obj in (self.TGSPRad , self.TGSPDia, self.TGSPOvl, self.TGSPShd,
                     self.TGSPLen):
        obj.setSuffix(glb.tunit)
    # set the Unit in the Machine Tab (Machine Dimensions)
    for obj in (self.MGSPTX, self.MGSPTY, self.MGSPTZ):
        obj.setSuffix(glb.tunit)
    # set the Unit in the Machine Tab (Machine feedrate)
    for obj in (self.MGSPFX, self.MGSPFY, self.MGSPFZ):
        obj.setSuffix(glb.spunit)
    # set the Unit in the Model Tab
    for obj in (self.MdLdimx, self.MdLdimy, self.MdLdimz):
        obj.setText(glb.tunit)

    self.IL_5.setText(glb.dunit)

################### GV actions

def clear_graphics_win(self):
        self.scene.clear()
        pass

def init_graphics_win(self):
    self.scene = QtGui.QGraphicsScene()
    self.scene.setSceneRect(0, 0, 378, 398)
    self.brush1 = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    self.brush1.setStyle(QtCore.Qt.SolidPattern)
    self.pen1 =  QtGui.QPen(QtCore.Qt.green, 3, QtCore.Qt.DashDotLine,
                     QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin)
    #self.GV.setForegroundBrush()
    self.GV.setBackgroundBrush(self.brush1)
    self.GV.setScene(self.scene)

def tool_paint(self):
    self.RightTB.setCurrentIndex(0) # Image Tab
    rect1 = self.scene.addRect(150,100,40,80)
    #rect1.fill()
    #text = self.scene.addText('hello')
    #text.setDefaultTextColor(QtGui.QColor(QtCore.Qt.red))

################### Model UI


def clear_model_tab(self):
    for obj in (self.MdTmX, self.MdTmY, self.MdTmZ,
                    self.MdTMX, self.MdTMY, self.MdTMZ,
                    self.MdTdimx, self.MdTdimy, self.MdTdimz):
        obj.setText("")
        obj.setReadOnly(True)
        obj.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)

def write_model_data(self,dims):
        dimx,dimy,dimz = dims
        if glb.unit == 0 :
            dimformat="{0:10.3f}"
        elif glb.unit == 1:
            dimformat = "{0:10.4f}"
        else:
            dimformat = "{0:6.3f}"

        self.MdTmX.setText(dimformat.format(dimx.min))
        self.MdTmY.setText(dimformat.format(dimy.min))
        self.MdTmZ.setText(dimformat.format(dimz.min))
        self.MdTMX.setText(dimformat.format(dimx.max))
        self.MdTMY.setText(dimformat.format(dimy.max))
        self.MdTMZ.setText(dimformat.format(dimz.max))
        self.MdTdimx.setText(dimformat.format(dimx.max-dimx.min))
        self.MdTdimy.setText(dimformat.format(dimy.max-dimy.min))
        self.MdTdimz.setText(dimformat.format(dimz.max-dimz.min))

################## Tool UI

def init_tool_comboboxes(self):
    self.ToolCB.clear()
    self.ToolCB.addItems(sorted(glb.Tools.keys()))
    self.PCToolCB.clear()
    self.PCToolCB.addItems(sorted(glb.Tools.keys()))


def init_tool_shape_comboboxes(self):
    # populate the Tool Shape ComboBox
    self.TGCBTyp.clear()
    self.TGCBTyp.addItems(glb.shape)
    self.TGCBTyp.setInsertPolicy(QtGui.QComboBox.InsertPolicy.NoInsert)


def init_centercut_combobox(self):
    # populate the Center Cut ComboBox
    self.TGCBCc.clear()
    self.TGCBCc.addItems([glb.no,glb.yes])
    self.TGCBCc.setInsertPolicy(QtGui.QComboBox.InsertPolicy.NoInsert)


def write_tool_data(self,key):
    # http://www.anderswallin.net/2011/08/opencamlib-cutter-shapes/
    #0 = CylCutter(diameter, length)
    #1 = BallCutter(diameter, length)
    #2 = BullCutter(diameter, corner_radius, length)
    #3 = ConeCutter(diameter, angle, length)
    #
    data = glb.Tools[key]
    ttype = int(data[0])

    set_tool_limits(self,ttype)

    self.TGCBTyp.setCurrentIndex(ttype)
    self.TGSPDia.setValue(float(data[1]))
    self.TGSPRad.setValue(float(data[2]))
    self.TGSPLen.setValue(float(data[3]))
    self.TGSPOvl.setValue(float(data[4]))
    self.TGSPShd.setValue(float(data[5]))
    self.TGSPFlu.setValue(int(data[6]))
    self.TGCBCc.setCurrentIndex(int(data[7]))
    self.TGTnote.setText(str(data[8]))


def clear_tool_ui(self):
    for obj in (self.TGSPDia, self.TGSPRad, self.TGSPLen, self.TGSPOvl,
                self.TGSPShd ):
        obj.setValue(0.0)
    self.TGSPFlu.setValue(0)
    self.TGCBCc.setCurrentIndex(0)
    self.TGTnote.setText("")


def set_tool_limits(self,ttype):
    if ttype in (0,1):
        self.TGLRad.setVisible(False)
        self.TGSPRad.setVisible(False)

    elif ttype == 2:
        self.TGLRad.setVisible(True)
        self.TGLRad.setText(glb.CorRad)
        self.TGSPRad.setVisible(True)
        if glb.unit == 1: # inches
            self.TGSPRad.setRange(0.0000, 1.0000)
            self.TGSPRad.setDecimals(4)
            self.TGSPRad.setSingleStep(0.001)
        else:
            self.TGSPRad.setRange(0.000, 25.000)
            self.TGSPRad.setDecimals(3)
            self.TGSPRad.setSingleStep(0.5)

        self.TGSPRad.setSuffix(glb.tunit)

    elif ttype == 3:
        self.TGLRad.setVisible(True)
        self.TGLRad.setText(glb.Angle)
        self.TGSPRad.setVisible(True)
        self.TGSPRad.setRange(0.0, 180.0)
        self.TGSPRad.setDecimals(1)
        self.TGSPRad.setSingleStep(1.0)

        self.TGSPRad.setSuffix(glb.degree)

    else:
        self.TGLRad.setVisible(True)
        self.TGLRad.setText(glb.Radius)
        self.TGSPRad.setVisible(True)
        if glb.unit == 1: # inches
            self.TGSPRad.setRange(0.0000, 1.0000)
            self.TGSPRad.setDecimals(4)
            self.TGSPRad.setSingleStep(0.001)
        else:
            self.TGSPRad.setRange(0.000, 25.000)
            self.TGSPRad.setDecimals(3)
            self.TGSPRad.setSingleStep(0.5)

        self.TGSPRad.setSuffix(glb.tunit)

    if glb.unit == 1: # inches
        for obj in (self.TGSPDia,self.TGSPShd ):
            obj.setRange(0.0000, 1.0000)
            obj.setDecimals(4)
            obj.setSingleStep(0.001)

        for obj in (self.TGSPLen,self.TGSPOvl):
            obj.setRange(0.0000, 5.0000)
            obj.setDecimals(4)
            obj.setSingleStep(0.001)

    else:
        for obj in (self.TGSPDia,self.TGSPShd ):
            obj.setRange(0.000, 25.000)
            obj.setDecimals(3)
            obj.setSingleStep(0.5)

        for obj in (self.TGSPLen,self.TGSPOvl):
            obj.setRange(0.000, 100.000)
            obj.setDecimals(3)
            obj.setSingleStep(0.5)


def read_tool_data(self):
    """
       Read the tool mask (except for the tool name and return a list
       with this values
       ["sha","dia","rad","len","ovl","shd","flu","cc","opt"]
    """
    data = []
    for i,v in enumerate((self.TGCBTyp, self.TGSPDia,self.TGSPRad, self.TGSPLen,
                  self.TGSPOvl, self.TGSPShd,self.TGSPFlu, self.TGCBCc,
                  self.TGTnote)):
        if i == 0: # Tool Shape
            data.append(v.currentIndex())
        elif i in (1,2,3,4,5,6): # Dia,Rad,Len,Flu
            data.append(v.value())
        elif i == 7: # Cc
            data.append(v.currentIndex())
        elif i == 8: #Notes
            data.append(v.toPlainText())
    return data


def tool_ui_mask(self,mskst):
    for f_object in (self.TGSPDia, self.TGSPRad,self.TGSPLen, self.TGSPOvl,
                     self.TGSPShd, self.TGSPFlu, self.TGTnote ):
        f_object.setReadOnly(mskst)


def tool_ui_populate(self):
    init_tool_shape_comboboxes(self)
    init_centercut_combobox(self)
    init_tool_comboboxes(self)
    tool_ui_visibility(self,True)


def tool_ui_visibility(self,action):
    self.ToolNewPB.setVisible(action)
    self.ToolModPB.setVisible(action)
    self.ToolDelPB.setVisible(action)
    self.ToolCB.setEnabled(action)
    self.TTConf.setVisible(not action)
    self.TTConf.setEnabled(not action)



################### Machine UI

def clear_mach_ui(self):
    for Eobject in (self.MGSPTX, self.MGSPTY, self.MGSPTZ, self.MGSPFX,
                self.MGSPFY, self.MGSPFZ ):
        Eobject.setValue(0.0)

    self.MGCoCB.setCurrentIndex(0)
    self.MGTnote.setText("")
    self.MGTpre.setText("")
    self.MGTpost.setText("")


def mach_ui_populate(self):
    mach_ui_mask(self,True)
    init_machine_coordinate_combobox(self)
    init_machine_names_comboboxes(self)
    set_mach_limits(self)
    mach_ui_visibility(self,True)


def mach_ui_mask(self,mskst):
    for f_object in (self.MGSPTX, self.MGSPTY, self.MGSPTZ, self.MGSPFX,
                     self.MGSPFY, self.MGSPFZ,self.MGTnote, self.MGTpre,
                     self.MGTpost):
        f_object.setReadOnly(mskst)


def init_machine_coordinate_combobox(self):
    # populate the Machine coordinate ComboBox
    self.MGCoCB.clear()
    self.MGCoCB.addItems(glb.coord)
    self.MGCoCB.setInsertPolicy(QtGui.QComboBox.InsertPolicy.NoInsert)


def init_machine_names_comboboxes(self):
    # Populate the Machine Names ComboBox in Machine and Processes TAB
    self.MachCB.clear()
    self.MachCB.addItems(sorted(glb.Machs.keys()))
    self.PCMachCB.clear()
    self.PCMachCB.addItems(sorted(glb.Machs.keys()))


def set_mach_limits(self):
    if glb.unit == 1: # inches
        for f_object in (self.MGSPTX, self.MGSPTY, self.MGSPTZ, self.MGSPFX,
                     self.MGSPFY, self.MGSPFZ ):
            f_object.setRange(0.0000, 100.0000)
            f_object.setDecimals(4)
            f_object.setSingleStep(0.25)
    else:
        for f_object in (self.MGSPTX, self.MGSPTY, self.MGSPTZ, self.MGSPFX,
                     self.MGSPFY, self.MGSPFZ ):
            f_object.setRange(0.000, 2500.000)
            f_object.setDecimals(3)
            f_object.setSingleStep(5.00)


def read_mach_data(self):
    """
       Read the machine mask (except for the machine name and return a list
       ["mtx","mty","mtz","mfx","mfy","mfz","cot","opt"]
    """
    data = []
    for i,v in enumerate((self.MGSPTX, self.MGSPTY, self.MGSPTZ, self.MGSPFX,
                self.MGSPFY, self.MGSPFZ, self.MGCoCB, self.MGTnote,
                self.MGTpre,self.MGTpost)):
        if i in (0,1,2,3,4,5): #
            data.append(v.value())
        elif i == 6: # Cc
            data.append(v.currentIndex())
        elif i in (7,8,9): # Notes , pre ,post
            data.append(v.toPlainText())
    return data


def write_mach_data(self,key):
    data = glb.Machs[key]

    f_object = (self.MGSPTX, self.MGSPTY, self.MGSPTZ, self.MGSPFX,
                self.MGSPFY, self.MGSPFZ )
    f_field = (0,1,2,3,4,5)
    for Eobject,idx in zip(f_object,f_field):
        Eobject.setValue(float(data[idx]))

    self.MGCoCB.setCurrentIndex(int(data[6]))
    self.MGTnote.setText(str(data[7]))
    self.MGTpre.setText(str(data[8]))
    self.MGTpost.setText(str(data[9]))

def mach_ui_visibility(self,action):
    self.MachNewPB.setVisible(action)
    self.MachModPB.setVisible(action)
    self.MachDelPB.setVisible(action)
    self.MachCB.setEnabled(action)
    self.MachConfPB.setVisible(not action)
    self.MachConfPB.setEnabled(not action)


################### Workpiece UI


def clear_wp_ui(self):
    for obj in (self.WPGSBLDX, self.WPGSBUDX, self.WPGSBLDY, self.WPGSBUDY,
                    self.WPGSBLDZ,self.WPGSBUDZ):
        obj.setValue(0.0)

    self.WPGCBMat.setCurrentIndex(0)
    self.WPGTNote.setText("")


def write_wp_data(self,key):
    glb.wpdata = glb.WorkPCs[key]

    for idx,obj in enumerate((self.WPGSBLDX, self.WPGSBUDX, self.WPGSBLDY,
                                  self.WPGSBUDY, self.WPGSBLDZ,self.WPGSBUDZ)):
        obj.setValue(float(glb.wpdata[idx]))

    self.WPGCBMat.setCurrentIndex(int(glb.wpdata[6]))
    self.WPGTNote.setText(glb.wpdata[7])

def wp_ui_mask(self,mskst):
    for f_object in (self.WPGSBLDX, self.WPGSBLDY, self.WPGSBLDZ, self.WPGSBUDX,
                     self.WPGSBUDY, self.WPGSBUDZ, self.WPGTNote):
        f_object.setReadOnly(mskst)

def init_wp_comboboxes(self):
    # populate the Workpiece ComboBox
    self.WPCB.clear()
    self.WPCB.addItems(sorted(glb.WorkPCs.keys()))
    self.PCWPCB.clear()
    self.PCWPCB.addItems(sorted(glb.WorkPCs.keys()))

def wp_ui_visibility(self,action):
    self.WPNewPB.setVisible(action)
    self.WPModPB.setVisible(action)
    self.WPDelPB.setVisible(action)
    self.WPCB.setEnabled(action)
    self.WPConfPB.setVisible(not action)
    self.WPConfPB.setEnabled(not action)


def wp_ui_populate(self):
    wp_ui_mask(self,True)
    init_wp_comboboxes(self)
    set_mach_limits(self)
    wp_ui_visibility(self,True)


def read_wp_data(self):
    """
       Read the WP mask (except for the WP name and return a list
       ["xmin","xmax","ymin","ymax","zmin","zmax","mat","note"]
    """
    data = []
    for i,v in enumerate((self.WPGSBLDX, self.WPGSBUDX, self.WPGSBLDY,
                          self.WPGSBUDY, self.WPGSBLDZ, self.WPGSBUDZ,
                          self.WPGCBMat,self.WPGTNote)):
        if i in (0,1,2,3,4,5): #
            data.append(v.value())
        elif i == 6: # Material
            data.append(v.currentIndex())
        elif i == 7: # Notes
            data.append(v.toPlainText())
    return data


def set_mach_limits(self):

    if glb.unit == 1: # inches
        for obj in (self.WPGSBLDX, self.WPGSBUDX, self.WPGSBLDY, self.WPGSBUDY,
                    self.WPGSBLDZ, self.WPGSBUDZ):
            obj.setRange(0.0000, 80.0000)
            obj.setDecimals(4)
            obj.setSingleStep(0.001)
            obj.setSuffix(glb.tunit)

    else:
        for obj in (self.WPGSBLDX, self.WPGSBUDX, self.WPGSBLDY, self.WPGSBUDY,
                    self.WPGSBLDZ, self.WPGSBUDZ):
            obj.setRange(-2000.000, 2000.000)
            obj.setDecimals(3)
            obj.setSingleStep(0.5)
            obj.setSuffix(glb.tunit)

################### Processes UI

def init_processes_ui(self):
    self.PCPDRB1.setEnabled(True)
    self.PCPDRB2.setEnabled(True)
    self.PCPDRB3.setEnabled(False)
    self.PCPDRB4.setEnabled(False)
    self.PCSTRB1.setEnabled(True)
    self.PCSTRB2.setEnabled(False)
    self.PCSTRB3.setEnabled(False)
    self.PCSTRB4.setEnabled(False)
    self.PCL01.setVisible(False)
    self.PCSB01.setVisible(False)
    self.PCPBGenG.setVisible(False)
    self.PCPBCt.setVisible(False)
    self.PCPBCal.setVisible(False)
    self.PCSTRB1.setChecked(True) # Check the SR Strategy
    self.PCPDRB1.setChecked(True) # Check the X direction
    self.PCTTd.setReadOnly(True)  # it has no meaning to modify it in thr PC UI
    set_processes_limits(self)

def set_processes_limits(self):
    if glb.unit == 1: # inches
        for obj in (self.PCSBXYovl,self.PCSBZsd):
            obj.setRange(0.0000, 1.0000)
            obj.setDecimals(4)
            obj.setSingleStep(0.001)
            obj.setSuffix(glb.tunit)

        for obj in (self.PCSBXYfc,self.PCSBZfc):
            obj.setRange(0.0000, 20.0000)
            obj.setDecimals(4)
            obj.setSingleStep(0.001)
            obj.setSuffix(glb.spunit)

    else:
        for obj in (self.PCSBXYovl,self.PCSBZsd):
            obj.setRange(0.000, 25.000)
            obj.setDecimals(3)
            obj.setSingleStep(0.05)
            obj.setSuffix(glb.tunit)

        for obj in (self.PCSBXYfc,self.PCSBZfc):
            obj.setRange(0.000, 1600.000)
            obj.setDecimals(3)
            obj.setSingleStep(0.5)
            obj.setSuffix(glb.spunit)

def processes_data_populate(self):
        m_name = self.PCMachCB.currentText()
        glb.machdata = glb.Machs[m_name]
        t_name = self.PCToolCB.currentText()
        glb.t_data = glb.Tools[t_name]
        #TODO the WPiece data
        w_name = self.PCWPCB.currentText()
        glb.wpdata = glb.WorkPCs[w_name]


################### G-Code  UI

def init_gcode_ui(self):
    # disable the checkbox
    gcode_ui_visibility(self,False)

    for obj in (self.GCPB1, self.GCPB2, self.GCPB3 ):
        obj.setVisible(False)

def gcode_ui_visibility(self,action):
    for obj in (self.GCmodel, self.GCmachine, self.GCtool, self.GCwp,
                self.GCtp, self.GCverbose, self.GCview, self.GCSBd):
        obj.setEnabled(action)

###################