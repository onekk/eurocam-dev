# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 16:10:37 2015

@author: carlo-m
"""

import os
import sys


sversion = "0.4"
version = sversion + ".5 Alpha"

debug = 3 # comment out to deactivate debug output

localini = 1
# 0 create the ini file in ./EuroCAM
# 1 create the ini file in ]~/.config/EuroCAM
  
#TODO check if work in windows and macs too
def ini_search_paths(file_name):
    paths = map(
        lambda path: os.path.join(path, file_name),
        (
            '~/.config/EuroCAM/',
            './EuroCAM/'
        ),
    )
    for path in paths:
        if os.path.isfile(path):
            return path

# These variable are defined here to be used in all the modules.
# Some of them are translated in the main loop 
inif_name = "eurocam.ini"
toolf_name = "tooltable.ini"
machf_name = "machtable.ini"
wp_name = "wptable.ini" 

inifile = ini_search_paths(inif_name)
f_tooltable = ini_search_paths(toolf_name)
f_machtable = ini_search_paths(machf_name)
f_wptable = ini_search_paths(wp_name)

model =  [None,None,None] # filename,other data   
Tools = {"Tool1" : [1,0.0,0.0,0.0,0.0,0.0,0,0,""], "Tool2" : [0,1.0,0.0,0.0,0.0,0.0,0,0,""]}
Tooldata = ["sha","dia","rad","len","ovl","shd","flu","cc","opt"]
## explanation:
# sha = shape
# dia = diameter
# rad = radius
# len = length
# flu = number of flutes
# cc  = (boolean?) center cut or some other info 
# opt = optional could be used for other info 

Machs = {"eShapeoko" : [10.00,10.00,10.00,100.00,100.00,100.00,1,"note","p","po"]}
Machdata = ["mtx","mty","mtz","mfx","mfy","mfz","cot","opt","pre","post"]
WorkPCs = {"WP1" : [0,15,0,15,0,4,0,""]}
WorkPcdata = ["xmin","xmax","ymin","ymax","zmin","zmax","mat","note"]
PCData = []
# 0 = m_name, 1 = t_name, 2 = feedrate, 3 = plungerate, 4 = safe_height
# 5 = strat, 6 = dircut,  7 = xyovl,  8 = z_steps   


#######################

# Variable used to modify the Labels 

Radius = ""
CorRad = ""
Angle = ""


# Flag

EditTool = False # Used to signal at the  
NewTool = False  #

EditMach = False
NewMach = False

EditWP = False
NewWP = False

M_Load = False

#### Variables in alphabetical order, downcase names 

## B
basename = "eurocam"

## C

coord = () # tuple MGCoCB items

## D
datahead = ()
# debug       # see upper
degree = ""   # for translate degree unit, hold "deg" in En_US  
dunit = ""    # Displayed unit message in the top label

## F

feedrate = [] # xy,z values of feedrate used for Process calculation

# f_machtable # see upper 
# f_tooltable # see upper
# f_wptable # see upper

## G
gcodec = []   # Hold the preferences for the G-Code file generation

## I

# inifile     # see upper
# inif_name   # see upper


## L

# localini   # see upper

## M

# machf_name  # see upper 
mach_plu = "" # Hold the Machine plural 
mach_sin = "" # Hold the Machine Singular
machdata = [] # machine data selected in the PC Tab (used for toolpath gen.)
# model       # see upper 
m_name = ""
mod_mot_name = ""
mot_name = ""

## N
newdata = []
no = ""       # Hold the "No" value displayed in some combobox 

## O
oldata = []

## P
pathfile = ""
plungerate = 0

## S 
shape = ()    # tuple TGTyp items
showdata = []
showhead = []
stime = "" 
spunit = ""   # Speed unit mm/min or IPS (Inch per second)
#sversion     # see upper
## T
# toolf_name  # see upper
t_data = []   # tooldata selected in the PC Tab (used for toolpath gen.)
t_name = ""
tool_plu = "" # Hold the Tool plural
tool_sin = "" # Hold Tool singular
tunit = ""    # Tool unit mm or inches(maybe other dimensions?)

## U
unit = 0      # Overall unit value  0 = mm or 1 = inches

## V

# version    # see upper

## Z
z_steps = []

## W
# wp_fname   # see upper
wpdata = []  # WP data selected in the PC Tab (used for toolpath gen.)
wpdim = [] # hold the Wp data adjusetd with offset in the display window and
           # ready to be sent to the toolpath generator  
wp_plu = ""  # Hold the Workpiece plural
wp_sin = ""  # Hold the Workpiece singular
## Y
yes = ""      # Hold the "Yes" value displayed in some combobox

## X
xyfeedrate = 0 

