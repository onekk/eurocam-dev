#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
author: Carlo Dormeletti
website: http://github.com//onekk
last edited: February 2015


"""

import sys
import os
import errno
import time
import math
import random
from subprocess import Popen

# Pyside import
from PySide import __version__ as PS_Ver
import PySide.QtCore as core
import PySide.QtGui as gui

# Eurocam modules

import ec_glb as glb
from eurocam_ui import Ui_MainWindow
import ec_logic as EC_L
import ec_ui_act as EC_UA
import visvis as vv
plot = vv.use('pyside')

import ec_mview as ECM

stime = time.time()

class MainWindow(gui.QMainWindow, Ui_MainWindow):
    '''
    Main window class
    '''
    def __init__(self, parent=None):


        # maybe a spash screen goes here?
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("EuroCAM - {0}".format(glb.sversion))

        # Binding for menu and close action
        self.actionOpen_Drawing.triggered.connect(self.open_drawing)
        self.actionAbout_EuroCAM.triggered.connect(self.about_eurocam)
        self.actionExit.triggered.connect(self.close)
        self.actionShow_display_window.triggered.connect(self.model_load)
        self.actionHelp.triggered.connect(self.help_text)
        self.menuInch.triggered.connect(self.unit_change)
        self.actionGCF.triggered.connect(self.set_gbasename)
        self.actionAbout_Qt.triggered.connect(self.about_Qt)
        # Binding for Tool Tab
        self.ToolNewPB.clicked.connect(self.tool_new)
        self.ToolModPB.clicked.connect(self.tool_mod)
        self.ToolDelPB.clicked.connect(self.tool_del)
        self.TTConf.clicked.connect(self.tool_conf)
        self.TGCBCc.activated.connect(self.tool_cb_state)
        self.TGCBTyp.activated.connect(self.tool_type_state)
        self.connect(self.ToolCB, core.SIGNAL('activated(QString)'),
                     self.tool_chosen)
        # Binfindg for Machine Tab
        self.MachNewPB.clicked.connect(self.mach_new)
        self.MachModPB.clicked.connect(self.mach_mod)
        self.MachDelPB.clicked.connect(self.mach_del)
        self.MachConfPB.clicked.connect(self.mach_conf)
        self.connect(self.MachCB, core.SIGNAL('activated(QString)'),
                     self.mach_chosen)
        self.MGCoCB.activated.connect(self.mach_coord_state)
        # Binding for Workpiece Tab
        self.connect(self.WPCB, core.SIGNAL('activated(QString)'),
                     self.wp_chosen)
        self.WPNewPB.clicked.connect(self.wp_new)
        self.WPModPB.clicked.connect(self.wp_mod)
        self.WPDelPB.clicked.connect(self.wp_del)
        self.WPConfPB.clicked.connect(self.wp_conf)
        # Binding for Process Tab
        self.connect(self.PCMachCB, core.SIGNAL('activated(QString)'),
                     self.pc_mach_chosen)
        self.connect(self.PCToolCB, core.SIGNAL('activated(QString)'),
                     self.pc_tool_chosen)
        self.connect(self.PCWPCB, core.SIGNAL('activated(QString)'),
                     self.pc_wp_chosen)
        self.PCPBCal.clicked.connect(self.pc_calc_task)
        self.PCPBGenG.clicked.connect(self.pc_gen_g)
        #self.PCPBCt.clicked.connect(self.pc_create_task)

        # Binding for the G-Code Tab
        self.GCPB1.clicked.connect(self.gen_ngc)
        self.GCPB2.clicked.connect(self.save_ngc_pref)

        self.md = None # create a void reference for the model display
                       #  window otherwise the new window is destroyed

        self.connect(self.MainTab, core.SIGNAL('currentChanged(int)'),
                     self.main_tab_chosen)

        self.start_action()

    def start_action(self):
        '''
        start_action()

        Contain the main variabel assignement for the translation

        '''
        self.Log.append(" EuroCAM")

        self.Log.append(" Inifile = {0}".format(glb.inifile))

        # To make the translation work the content have to be put here

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

        self.mm = " mm" # no need to translate
        self.inch = self.tr(" inch")

        glb.tool_plu = self.tr("Tools")
        glb.mach_plu = self.tr("Machines")
        glb.wp_plu = self.tr("Work Pieces")

        glb.tool_sin = self.tr("Tool")
        glb.mach_sin = self.tr("Machine")
        glb.wp_sin = self.tr("Work Piece")

        self.posco = self.tr("Positive Coordinates")
        self.negco = self.tr("Negative Coordinates")

        glb.coord = (self.posco, self.negco)

        # QMessageBox string are put here to make them correctly translate

        # Exit Dialog
        self.msg_01t = self.tr("<b>Exit Dialog</b>")
        self.msg_01m = self.tr("Are you sure you want to exit?")

        self.msg_02m = self.tr("<p> There is no help file yet, please report\
            this error at <br> <b> https://github.com/onekk/eurocam </b></p>")
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
        self.msg_18m = self.tr("You have to load a model to show a display window")
        self.msg_19m = self.tr("<b>EuroCAm</b> has launched the toolpath generator \
            program with PID number {0} ")

        # About EuroCAM message
        self.msg_a01t = self.tr("About EuroCAM")
        self.msg_a01m = self.tr("<p align = left><b>EuroCAM</b> version \
            <b>{0}</b> <br> copyright Carlo Dormeletti 2015 </p><hr>\
            <p> It generates G-Code ready to be sent to a CNC machine.<br></p>\
            <p align = left>For Issues and request about this program use the\
            Issues function at: <br> <br>\
            <b> https://github.com/onekk/eurocam </b></p>").format(glb.version)

        # About Qt message
        self.msg_a02t = self.tr("About Qt")
        self.msg_a02m = self.tr("<p><b>EuroCAM</b> version <b>{0}</b><br>\
             is Using : <br><br> <b>Pyside</b> version = <b>{1}</b> Compiled \
             using <br><b>Qt</b> version = <b>{2[0]}.{2[1]}.{2[2]}</b> <br>\
             <br> Running on <b> Qt</b> version = <b>{3}</b> </p> \
             <p> To obtain his features it use : <br>\
             - the visvis library for the display window see at:<br> \
             <b> https://code.google.com/p/visvis </b> <br> <br>\
             - the great OpenCAMlib Library by Anders Wallins <br>\
             see <b> https://github.com/aewallin/opencamlib</b><br><br> The \
             exact version of OpenCamlib could be seen in the top comment of \
             the generated G-Code files </p> \
             ").format(glb.version, PS_Ver, core.__version_info__,
                       core.qVersion())

        self.msg_i01 = self.tr("Warning")

        # check the esistence of the ini files and crete them if necessary
        if glb.inifile is None:
            if glb.localini == 1:
                self.create_inifile("./EuroCAM")
            else:
                self.create_inifile("~/.config/EuroCAM")

        self.read_ini_settings()
        EC_L.set_unit(self)

        # set the unit label
        if int(glb.unit) == 0:
            glb.dunit = self.tr("Unit = mm")
        else:
            glb.dunit = self.tr("Unit = Inch")

        # read the tables if they exist, if not create them and then read them        
        
        EC_L.check_tool_table(self)
        self.Log.append("ToolTable Initizialization")

        EC_L.check_mach_table(self)
        self.Log.append("MachTable Initizialization")

        EC_L.check_wp_table(self)
        self.Log.append("WPTable Initizialization")

        EC_UA.init_ui(self)
        self.Log.append("UI initialisation")

        EC_UA.write_tool_data(self, self.ToolCB.currentText())
        EC_UA.write_mach_data(self, self.MachCB.currentText())
        EC_UA.write_wp_data(self, self.WPCB.currentText())

        # populate and pre initialize the Process Tab
        EC_UA.processes_data_populate(self)

        self.pc_step_data()
        self.pc_feed_data()
        self.RightTB.setCurrentIndex(0) # select the Image ToolBox

        glb.basename = os.path.join(os.path.dirname(__file__), 'ngc',
                                    glb.basename)

        self.IL_2.setText("Basename Set")
        self.IL_2.setToolTip("Basename = <b>{0}</b>".format(glb.basename))

        EC_UA.init_graphics_win(self)
        if self.MainTab.currentIndex() == 2:
            EC_UA.tool_paint(self)

        self.MainTab.removeTab(6) # self.TaskTab TODO delete when the task tab is finished
        self.MainTab.setCurrentIndex(0)
        self.RightTB.setCurrentIndex(1) # Show the Text TAB

        self.show()

    def create_inifile(self, path):
        '''
        If there is no inifile create one
        '''
        msgtxt = self.msg_14m.format(path)
        self.my_diag(self.msg_i01, msgtxt, "", gui.QMessageBox.Information)
        self.create_path_and_inifile(path, glb.inif_name)
        glb.inifile = glb.ini_search_paths(glb.inif_name)
        self.write_ini_settings()

    def read_ini_settings(self):
        '''
        read inifile
        '''
        settings = core.QSettings(glb.inifile, core.QSettings.IniFormat)
        pos = settings.value("pos", core.QPoint(200, 200))
        size = settings.value("size", core.QSize(400, 400))
        self.resize(size)
        self.move(pos)
        settings.beginGroup("Preferences")
        glb.unit = settings.value("unit")
        settings.endGroup()

    def write_ini_settings(self):
        '''
        write inifile
        '''
        settings = core.QSettings(glb.inifile, core.QSettings.IniFormat)
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())
        settings.beginGroup("Preferences")
        settings.setValue("unit", glb.unit)
        #settings.setValue("other","prova")
        settings.endGroup()


    ######################################
    #                                    #
    # Menu actions                       #
    #                                    #
    ######################################

    def open_drawing(self):
        '''
        open drawing file and call the necessary actions
        '''
        filters = []
        filters.append("*.stl")
        filters.append("*.*")

        dialog = gui.QFileDialog()
        dialog.setNameFilters(filters)


        if dialog.exec_():
            f_names = dialog.selectedFiles()
        else:
            return

        if len(f_names) > 0:
            f_name = f_names[0]
            glb.model[0] = f_name
            # assign the basename model as the fileName without the extension
            # and put it in
            ngcdir = os.path.join(os.path.dirname(__file__), 'ngc')
            basename = os.path.splitext(os.path.basename(f_name))[0]
            glb.basename = os.path.join(ngcdir, basename)
            self.model_info(f_name)

            EC_UA.processes_data_populate(self)
            self.PCPBCal.setVisible(True)
        else:
            return

    def about_eurocam(self):
        '''
        qhow the dialog holding the information about program
        '''
        gui.QMessageBox.about(self, self.msg_a01t, self.msg_a01m)

    def model_load(self):
        '''
        Create the model display window and load the model in it
        '''
        if glb.M_Load == True:
            # visualize a splash window during the model loading.
            pixmap = QPixmap("./splash.png")
            splash = QSplashScreen(pixmap)
            splash.setWindowFlags(core.Qt.WindowStaysOnTopHint)
            splash.show()
            # Loading some items
            #app.processEvents()
            splash.showMessage("Eurocam .. Loading model")

            f_name = glb.model[0]
            self.md = ECM.ModelWindow()
            self.md.load_data(f_name)

            splash.finish()

        else:
            self.my_diag(self.msg_i01, self.msg_18m, "",
                         gui.QMessageBox.Information)

    def help_text(self):
        '''
        Show the Help text
        '''
        self.RightTB.setCurrentIndex(1) # select the Text ToolBox
        locale = core.QLocale.system().name()
        helpfile = EC_L.search_paths("eurocam_help-" + locale +".txt")
        if helpfile:
            self.TWid.setSource(helpfile)
        elif EC_L.search_paths("eurocam_help.txt"):
            self.TWid.setSource(EC_L.search_paths("eurocam_help.txt"))
        else:
            self.TWid.setHtml(self.msg_02m)

    def unit_change(self):
        '''
        Change the unit in the UI
        '''
        # FIXME add the action
        if self.menuInch.isChecked() == True:
            print "eurocam:MW: unit inches"
        else:
            print "unit mm"

    def set_gbasename(self):
        self.ask_basename()
        self.IL_2.setText("Basename Set")
        self.IL_2.setToolTip("Basename = <b>{0}</b>".format(glb.basename))

    def about_Qt(self):
        gui.QMessageBox.about(self, self.msg_a02t, self.msg_a02m)

    def closeEvent(self, event):
        '''
        called by Exit menu item trough self.close()
        and triggered also pressing the close button on the titlebar
        event : QCloseEvent
        '''
        msgBox = gui.QMessageBox()
        msgBox.setText(self.msg_01t)
        msgBox.setInformativeText(self.msg_01m)
        msgBox.setStandardButtons(gui.QMessageBox.Yes | gui.QMessageBox.Cancel)
        msgBox.setDefaultButton(gui.QMessageBox.Yes)
        msgBox.setIcon(gui.QMessageBox.Question)
        ret = msgBox.exec_()
        event.ignore()
        if ret == gui.QMessageBox.Yes:
            self.Log.append("Writing Settings")
            self.write_ini_settings()
            # in case something go wrong with the creation of the model we
            # can close the window
            try:
                self.md.close()
            except:
                event.accept()
            event.accept()
        elif ret == gui.QMessageBox.Cancel:
            event.ignore()

    # Miscellaneous actions


    def ask_basename(self):
        ans = self.ask_gname("Messaggio", " NGC File ")
        if ans == "KO":
            return
        else:
            glb.basename = ans

    def main_tab_chosen(self, value):
        if value == 2:
            EC_UA.tool_paint(self)
        elif value == 3:
            text = self.WPCB.currentText()
            self.change_wp(text)
        elif value == 4:
            text = self.PCWPCB.currentText()
            self.change_wp(text)
        else:
            if glb.debug[0] == 1:
                print "Tab number = ", value
            EC_UA.clear_graphics_win(self)

    def model_info(self, filename):
        self.IL_1.setText("Model Loaded")
        self.IL_1.setToolTip("Model name = <b>{0}</b>".format(filename))
        self.IL_2.setText("Basename Set")
        self.IL_2.setToolTip("Basename = <b>{0}</b>".format(glb.basename))
        self.MdTName.setText("<b>{0}</b>".format(filename))

        self.load_model()

    def load_model(self):
        filename = glb.model[0]
        self.md = ECM.ModelWindow()
        self.md.load_data(filename)
        glb.M_Load = True
        dims = self.md.getBB("md")
        EC_UA.write_model_data(self, dims)

    def change_wp(self, value):
        EC_UA.write_wp_data(self, value)
        if glb.debug[4] == 1:
            print glb.wpdata

        if glb.M_Load == True:
            self.wp_plot()

    def wp_plot(self):
        xmin = float(glb.wpdata[0])
        xmax = float(glb.wpdata[1])
        ymin = float(glb.wpdata[2])
        ymax = float(glb.wpdata[3])
        zmin = float(glb.wpdata[4])
        zmax = float(glb.wpdata[5])
        if int(glb.unit) == 0:
            dunit = "mm"
        else:
            dunit = "inch"
        self.md.wp_create(xmin, xmax, ymin, ymax, zmin, zmax, dunit)

    def save(self):
        self.statusbar.showMessage("save selected")

    def create_path_and_inifile(self, path, inifile):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        try:
            inifile = os.path.join(path, inifile)
            if glb.debug[0] == 1:
                print inifile
            with open(inifile, 'w') as ofile:
                ofile.close()
        except IOError as e:
            msgtit = "Warning"
            msgtxt = "Unable to create file {0} in {1}".format(inifile, path)
            self.my_diag(msgtit, msgtxt, "", gui.QMessageBox.Information)


    # Dialog used in the interface    #


    def data_mod_diag(self, ctst, msginfo):
        mtxt = "<table border='1' width = '300'>"
        tln0 = "<tr><td> {0} </td><td align='right'>{1:.3}</td><td align='right'>{2:.3}</td></tr>"
        tln1 = "<tr><td> {0} </td><td align='right'>{1}</td><td align='right'>{2}</td></tr>"
        tln2 = "<tr><td> {0} </td><td>{1}</td><td>{2}</td></tr>"
        if ctst == 0: # Tool Data
            for i, v in enumerate(glb.datahead):
                if glb.debug[4] == 1:
                    print i, v
                if i in (1, 3, 4, 5): # float
                    mtxt = mtxt + tln0.format(v, glb.oldata[i], glb.newdata[i])
                elif i in (0, 2, 6, 7): # integer
                    mtxt = mtxt + tln1.format(v, glb.oldata[i], glb.newdata[i])
                else: # text no special formatting
                    mtxt = mtxt + tln2.format(v, glb.oldata[i], glb.newdata[i])
        elif ctst == 1: # Machine data
            for i, v in enumerate(glb.datahead):
                if glb.debug[4] == 1:
                    print "I V old New =>>", i, v, glb.oldata[i], glb.newdata[i]
                if i in (0, 1, 2, 3, 4, 5): # float
                    mtxt = mtxt + tln0.format(v, glb.oldata[i], glb.newdata[i])
                elif i == 6: # integer
                    mtxt = mtxt + tln1.format(v, glb.oldata[i], glb.newdata[i])
                else: # text no special formatting
                    mtxt = mtxt + tln2.format(v, glb.oldata[i], glb.newdata[i])
        elif ctst == 2: # WP data
            for i, v in enumerate(glb.datahead):
                if glb.debug[4] == 1:
                    print "I V old New =>>", i, v, glb.oldata[i], glb.newdata[i]
                if i in (0, 1, 2, 3, 4, 5):  # float
                    mtxt = mtxt + tln0.format(v, glb.oldata[i], glb.newdata[i])
                elif i == 6: # integer
                    mtxt = mtxt + tln1.format(v, glb.oldata[i], glb.newdata[i])
                else: # text no special formatting
                    mtxt = mtxt + tln2.format(v, glb.oldata[i], glb.newdata[i])

        mtxt = mtxt + "</table>"

        ret = self.my_diag("", mtxt, msginfo, gui.QMessageBox.Question)

        if ret == "OK":
            return "OK"
        elif ret == "KO":
            return "KO"


    def my_diag(self, msgtit, msgtxt, msginfo="",
                icon=gui.QMessageBox.Information):
        msgctit = "EuroCAm - {0}".format(msgtit)            
        msgBox = gui.QMessageBox(self,msgctit,msgtxt)
        msgBox.setInformativeText(msginfo)
        msgBox.setStandardButtons(gui.QMessageBox.Yes | gui.QMessageBox.Cancel)
        msgBox.setDefaultButton(gui.QMessageBox.Yes)
        msgBox.setIcon(icon)
        ret = msgBox.exec_()
        if ret == gui.QMessageBox.Yes:
            return "OK"
        elif ret == gui.QMessageBox.Cancel:
            return "KO"
        return "KO"


    def ask_name(self, O_data, O_type):
        msg = self.msg_06t.format(O_type)
        text, ok = gui.QInputDialog.getText(self, msg, self.msg_06m)

        O_name = text.replace(" ", "_")

        if O_name in O_data:
            msgtxt = self.msg_07m.format(O_name)
            self.my_diag("", msgtxt, "", gui.QMessageBox.Warning)
            return "KO"
        else:
            return O_name

    def ask_gname(self, msg, g_type):
        msg = self.msg_06t.format(g_type)
        text, ok = gui.QInputDialog.getText(self, msg, self.msg_06m)
        O_name = text.replace(" ", "_")
        return O_name


    # Tools Tab related actions


    def tool_chosen(self, text):
        EC_UA.write_tool_data(self, text)


    def tool_new(self):
        ans = self.ask_name(glb.Tools, glb.tool_sin)
        if ans == "KO":
            return
        else:
            glb.mot_name = ans
            glb.NewTool = True
            glb.EditTool = True
            EC_UA.tool_ui_visibility(self, False)
            EC_UA.clear_tool_ui(self)
            glb.oldata = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, ""]


    def tool_mod(self):
        glb.EditTool = True
        EC_UA.tool_ui_visibility(self, False)
        ttype = int(self.TGCBTyp.currentIndex())
        EC_UA.set_tool_limits(self, ttype)
        EC_UA.tool_ui_mask(self, False)
        glb.oldata = EC_UA.read_tool_data(self)
        glb.mod_mot_name = self.ToolCB.currentText()



    def tool_del(self):
        if self.ToolCB.count() < 2: #2
            msgtxt = self.msg_05m.format(glb.tool_sin, glb.tool_plu)
            self.my_diag("", msgtxt, "", gui.QMessageBox.Warning)
            return
        else:
            glb.mod_mot_name = self.ToolCB.currentText()
            glb.oldata = glb.Tools[glb.mod_mot_name]
            glb.newdata = [0, 0.0, 0.0, 0.0, 0, 0, 0, 0, ""]

            glb.datahead = (self.TGLTyp.text(), self.TGLDia.text(),
                            self.TGLRad.text(), self.TGLLen.text(),
                            self.TGLOvl.text(), self.TGLShd.text(),
                            self.TGLFlu.text(), self.TGLCc.text(),
                            self.TGLnote.text())

            ans = self.data_mod_diag(0, self.msg_04m.format(glb.tool_sin))
            if ans == "OK":
                del glb.Tools[glb.mod_mot_name]
                self.tool_update()
            else:
                pass


    def tool_conf(self):
        glb.newdata = EC_UA.read_tool_data(self)
        if glb.newdata[3] > glb.newdata[4]:
            self.my_diag("", self.msg_11m, "", gui.QMessageBox.Warning)
            return
        EC_UA.tool_ui_mask(self, True)
        glb.EditTool = False

        glb.datahead = (self.TGLTyp.text(), self.TGLDia.text(),
                        self.TGLRad.text(), self.TGLLen.text(),
                        self.TGLOvl.text(), self.TGLShd.text(),
                        self.TGLFlu.text(), self.TGLCc.text(),
                        self.TGLnote.text())

        ans = self.data_mod_diag(0, self.msg_03t)
        if ans == "OK":
            if glb.NewTool is False:
                glb.Tools[glb.mod_mot_name] = glb.newdata
                self.tool_update()
            else:
                glb.Tools[glb.mot_name] = glb.newdata
                self.tool_update()
        else:
            pass

        glb.NewTool = False
        EC_UA.tool_ui_visibility(self, True)


    def tool_update(self):
        EC_L.update_tool_table(self)
        EC_UA.tool_ui_populate(self)
        EC_UA.write_tool_data(self, self.ToolCB.currentText())
        self.Log.append("Re Populating UI Tooltable")

    def tool_cb_state(self, value):
        key = self.ToolCB.currentText() # the name of the tool
        tooldata = glb.Tools[key]

        if glb.EditTool is False:
            self.TGCBCc.setCurrentIndex(int(tooldata[5]))
        else:
            pass

    def tool_type_state(self, value):
        key = self.ToolCB.currentText() # the name of the tool
        tooldata = glb.Tools[key]

        if glb.EditTool is False:
            self.TGCBTyp.setCurrentIndex(int(tooldata[0]))
        else:
            ttype = int(self.TGCBTyp.currentIndex())
            EC_UA.set_tool_limits(self, ttype)
            EC_UA.tool_ui_mask(self, False)


    ################################################
    #                                              #
    # Machine Tab related actions                  #
    #                                              #
    ################################################


    def mach_chosen(self, text):
        EC_UA.write_mach_data(self, self.MachCB.currentText())


    def mach_coord_state(self, value):
        key = self.MachCB.currentText() # the name of the tool
        machdata = glb.Machs[key]
        if glb.EditMach is False:
            self.MGCoCB.setCurrentIndex(int(machdata[6]))
        else:
            pass


    def mach_new(self):
        ans = self.ask_name(glb.Machs, glb.mach_sin)
        if ans == "KO":
            return
        else:
            glb.mot_name = ans
            glb.NewMach = True
            glb.EditMach = True
            EC_UA.mach_ui_visibility(self, False)
            EC_UA.clear_mach_ui(self)
            # Set the Machine mask readable
            EC_UA.mach_ui_mask(self, False)
            glb.oldata = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, "", "", ""]


    def mach_mod(self):
        glb.EditMach = True
        EC_UA.mach_ui_visibility(self, False)
        EC_UA.mach_ui_mask(self, False)
        glb.oldata = EC_UA.read_mach_data(self)
        glb.mod_mot_name = self.MachCB.currentText()


    def mach_del(self):
        if self.MachCB.count() < 2:
            msgtxt = self.msg_05m.format(glb.mach_sin, glb.mach_plu)
            self.my_diag("", msgtxt, "", gui.QMessageBox.Warning)
            return
        else:
            glb.mod_mot_name = self.MachCB.currentText()
            glb.oldata = glb.Machs[glb.mod_mot_name]
            glb.newdata = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, "", "", ""]

            glb.datahead = (self.MGLTX.text(), self.MGLTY.text(),
                            self.MGLTZ.text(), self.MGLFX.text(),
                            self.MGLFY.text(), self.MGLFZ.text(),
                            self.MGLCo.text(), self.MGLnote.text(),
                            self.MGLpre.text(), self.MGLpost.text())

            ans = self.data_mod_diag(0, self.msg_04m.format(glb.mach_sin))
            if ans == "OK":
                del glb.Machs[glb.mod_mot_name]
                self.mach_update()
            else:
                pass


    def mach_conf(self):
        glb.newdata = EC_UA.read_mach_data(self)
        EC_UA.mach_ui_mask(self, True)
        glb.EditMach = False
        glb.datahead = (self.MGLTX.text(), self.MGLTY.text(), self.MGLTZ.text(),
                        self.MGLFX.text(), self.MGLFY.text(), self.MGLFZ.text(),
                        self.MGLCo.text(), self.MGLnote.text(),
                        self.MGLpre.text(), self.MGLpost.text())

        ans = self.data_mod_diag(1, self.msg_03t)
        if ans == "OK":
            if glb.NewMach is False:
                glb.Machs[glb.mod_mot_name] = glb.newdata
                self.mach_update()
            else:
                glb.Machs[glb.mot_name] = glb.newdata
                self.mach_update()
        else:
            pass

        glb.NewMach = False
        EC_UA.mach_ui_visibility(self, True)


    def mach_update(self):
        EC_L.update_mach_table(self)
        EC_UA.mach_ui_populate(self)
        EC_UA.write_mach_data(self, self.MachCB.currentText())
        self.Log.append("Re Populating UI Machines table")


    ################################################
    #                                              #
    # Workpiece Tab related actions                #
    #                                              #
    ################################################

    def wp_chosen(self, value):
        self.PCWPCB.setCurrentIndex(self.WPCB.currentIndex())
        self.change_wp(value)


    def wp_new(self):
        ans = self.ask_name(glb.WorkPCs, glb.wp_sin)
        if ans == "KO":
            return
        else:
            glb.mot_name = ans
            glb.NewWP = True
            glb.EditWP = True
            EC_UA.wp_ui_visibility(self, False)
            EC_UA.clear_wp_ui(self)
            # Set the WP mask readable
            EC_UA.wp_ui_mask(self, False)
            glb.oldata = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, ""]

    def wp_mod(self):
        glb.EditWP = True
        EC_UA.wp_ui_visibility(self, False)
        EC_UA.wp_ui_mask(self, False)
        glb.oldata = EC_UA.read_wp_data(self)
        glb.mod_mot_name = self.WPCB.currentText()

    def wp_del(self):
        if self.WPCB.count() < 2:
            msgtxt = self.msg_05m.format(glb.wp_sin, glb.wp_plu)
            self.my_diag("", msgtxt, "", QMessageBox.Warning)
            return
        else:
            glb.mod_mot_name = self.WPCB.currentText()
            glb.oldata = glb.WorkPCs[glb.mod_mot_name]
            glb.newdata = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, ""]

            glb.datahead = ("{0} lower".format(self.WPGLDX.text()),
                            "{0} upper".format(self.WPGLDX.text()),
                            "{0} lower".format(self.WPGLDY.text()),
                            "{0} upper".format(self.WPGLDY.text()),
                            "{0} lower".format(self.WPGLDZ.text()),
                            "{0} upper".format(self.WPGLDZ.text()),
                            self.WPGLMat.text(),
                            self.WPGLNote.text())

            ans = self.data_mod_diag(2, self.msg_04m.format(glb.wp_sin))
            if ans == "OK":
                del glb.WorkPCs[glb.mod_mot_name]
                self.wp_update()
            else:
                pass

    def wp_conf(self):
        glb.newdata = EC_UA.read_wp_data(self)
        EC_UA.wp_ui_mask(self, True)
        glb.EditWP = False
        if glb.debug[4] == 1:
            print glb.newdata
        glb.datahead = ("{0} lower".format(self.WPGLDX.text()),
                        "{0} upper".format(self.WPGLDX.text()),
                        "{0} lower".format(self.WPGLDY.text()),
                        "{0} upper".format(self.WPGLDY.text()),
                        "{0} lower".format(self.WPGLDZ.text()),
                        "{0} upper".format(self.WPGLDZ.text()),
                        self.WPGLMat.text(),
                        self.WPGLNote.text())

        ans = self.data_mod_diag(2, self.msg_03t)
        if ans == "OK":
            if glb.NewWP is False:
                if glb.debug[4] == 1:
                    print "Prima ", glb.WorkPCs[glb.mod_mot_name]
                glb.WorkPCs[glb.mod_mot_name] = glb.newdata
                if glb.debug[4] == 1:
                    print "Dopo ", glb.WorkPCs[glb.mod_mot_name]
                self.wp_update()
            else:
                glb.WorkPCs[glb.mot_name] = glb.newdata
                self.wp_update()
        else:
            pass

        glb.NewWP = False
        EC_UA.wp_ui_visibility(self, True)


    def wp_update(self):
        EC_L.update_wp_table(self)
        EC_UA.wp_ui_populate(self)
        EC_UA.write_wp_data(self, self.WPCB.currentText())
        self.Log.append("Re Populating UI WorkPieces table")


    ################################################
    #                                              #
    # Processes Tab related actions                #
    #                                              #
    ################################################

    def pc_buttons(self, action):
        self.PCPBCt.setVisible(action)
        self.PCPBGenG.setVisible(action)
        self.GCPB1.setVisible(action)
        self.GCPB2.setVisible(action)

    def pc_mach_chosen(self, value):
        # Set the same machine in the Machine Tab
        self.MachCB.setCurrentIndex(self.PCMachCB.currentIndex())
        EC_UA.write_mach_data(self, self.MachCB.currentText())
        # Do the other actions
        glb.machdata = glb.Machs[value]
        self.pc_feed_data()
        # Deactivate the buttons because some parameters are changed
        self.pc_buttons(False)


    def pc_tool_chosen(self, value):
        # Set the same tool in the Tools Tab
        self.ToolCB.setCurrentIndex(self.PCToolCB.currentIndex())
        EC_UA.write_tool_data(self, self.ToolCB.currentText())
        # Do the other actions
        glb.t_data = glb.Tools[value]
        self.pc_step_data()
        # Deactivate the buttons because some parameters are changed
        self.pc_buttons(False)


    def pc_wp_chosen(self, value):
        # Set the same WP in the WP Tab
        self.WPCB.setCurrentIndex(self.PCWPCB.currentIndex())
        self.change_wp(value)
        # Do the other actions
        # TODO insert the correction for feed and step based on material
        # properties?
        #self.pc_feed_data()
        #self.pc_step_data()
        # Deactivate the buttons because some parameters are changed
        self.pc_buttons(False)


    def pc_create_task(self):
        # TODO the action for create Task
        self.MainTab.setCurrentIndex(6)


    def pc_gen_g(self):
        self.MainTab.setCurrentIndex(5)
        EC_UA.gcode_ui_visibility(self, True)
        self.GCPB1.setVisible(True)
        #self.GCPB2.setVisible(True)


    def pc_calc_task(self):
        # Run the data check and the preliminary calculations
        ret = self.pc_calc_data()

        if ret == "KO":
            # or do something
            pass
        else:
            pass
            # or do something

    def pc_step_data(self):
        diameter = float(glb.t_data[1])
        c_length = float(glb.t_data[3])
        self.PCTTd.setText("{0:.4} {1}".format(diameter, glb.tunit))
        # Step down increment is obtained from the rules of thumb:
        # diameter/2
        # TODO consider the material data
        # and then tuned by the spinbox controls
        preset = float(diameter/2)
        self.PCSBXYovl.setValue(preset)
        self.PCSBXYovl.setRange(0.000, diameter)
        self.PCSBZsd.setValue(preset)
        self.PCSBZsd.setRange(0.000, c_length)

    def pc_feed_data(self):
        # XY feed is the minimun between X and Y feedrate
        # TODO consider the material data
        xyfeed = min(float(glb.machdata[3]), float(glb.machdata[4]))
        self.PCSBXYfc.setValue(xyfeed)
        zfeed = float(glb.machdata[5])
        self.PCSBZfc.setValue(zfeed)

    def pc_calc_data(self):
        EC_L.calc_process(self)


    ################################################
    #                                              #
    # G-Code Tab related actions                   #
    #                                              #
    ################################################


    def gen_ngc(self):
        self.read_gcodetab_checkboxes()
        # the filename has to be "pathgen.ini" because it is hardcoded
        # in ec_tpath.py as the input file
        p_fname = "./pathgen.ini"
        ans = EC_L.write_pathfile(self, p_fname, "ngc")
        if ans == "OK":
            # call the ec_tpath.py to generate Gcode in non blocking mode
            # and emit a message with PID number of the process
            pid = Popen(["python2", "ec_tpath.py"]).pid
            msgtxt = self.msg_19m.format(pid)
            self.my_diag("", msgtxt, "", gui.QMessageBox.Information)
        else:
            return

    def read_gcodetab_checkboxes(self):
        # Read the checkboxes and set the variables to generate the G-Code
        glb.gcodec = []
        for obj in (self.GCmodel, self.GCmachine, self.GCtool, self.GCwp,
                    self.GCtp, self.GCverbose, self.GCview):
            glb.gcodec.append(obj.isChecked())
        # retrieve the content of the decimal SB self.GCdecimals
        glb.gcodec.append(self.GCSBd.value())

        if glb.debug[2] == 1:
            print glb.gcodec

    def save_ngc_pref(self):
        # TODO add the proper actions
        print "Save NGC pressed"

    ################################################
    #                                              #
    # Task (self.TaskTab) related actions          #
    #                                              #
    ################################################

        # TODO add the Task creations

    def create_task(self):

        p_fname = "./pathfile.ini"
        EC_L.write_pathfile(self, p_fname, "tsk")


##########################################
#                                        #
# Main Loop                              #
#                                        #
##########################################

def main():
    if glb.debug[0] == 1:
        print "main init"
        print __file__
        print os.path.join(os.path.dirname(__file__), '..')
        print os.path.dirname(os.path.realpath(__file__))
        print os.path.abspath(os.path.dirname(__file__))

    locale = core.QLocale.system().name()
    translator = core.QTranslator()
    #translator.load("qt_" + locale, core.QLibraryInfo.location(core.QLibraryInfo.TranslationsPath))
    lang_file = EC_L.search_paths(locale + ".qm")
    translator.load(lang_file)

    app = gui.QApplication(sys.argv)
    app.installTranslator(translator)
    # init the splash screen
    pixmap = gui.QPixmap("./splash.png")
    splash = gui.QSplashScreen(pixmap)
    splash.setWindowFlags(core.Qt.WindowStaysOnTopHint)    
    splash.show()
    app.processEvents()
    # Loading some items
    splash.showMessage("Eurocam .. Loading modules")

    app.processEvents()
    # end of the splah init

    frame = MainWindow()
    #frame.show() # is done in the program

    splash.finish(frame)

    app.exec_()

if __name__ == '__main__':
    main()
