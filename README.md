# EuroCAM
It would be a pratical and fast replacement of pycam for linux and maybe other OS.

The hard work is done by OpenCAMLib from https://github.com/aewallin/opencamlib.

The program is still in Alpha stage but the main core is almost done.

### CONFIGURATION:

At the first start up the program will create an setting directory depending on the value of the localini variable in ec_glb.py:

- if 1 it will be created as a subdirectory of the current dir (./EuroCAM)
- otherwise it will be created in the user directory under ~/.config (~./config/EuroCAM)

In this directory there are three file:

- eurocam.ini    => Hold the settings of the interface plus some setting like preferred unit preferred paths and so on
- tooltable.ini  => Hold the tools list data
- machtable.ini  => Hold the machines list data
- wptable.ini    => Hold the workpieces data

(in this directory there will be also modeldata.ini and taskdata.ini holding the corresponding values)

In the main directory there are two file:

- machtable_model.ini
- tooltable_model.ini

that are more populated with values to test the UI.

if you copy them as machtable.ini or tooltable.ini after the default files are automatically created you will have some more values to test the ui, of course you can write them by hand, but if you use *inches* you have to verify the values (it is not clear to me how the Qt interface handle the decimal separator)


### USING:
To use it you have to specify at least one:
- Machine
- Tool
- WorkPiece

1) First step is to go in menu file and choose "Open Drawing", it will open the
 file and set the basename of the generated ngc files.
 By default they are created in ngc subdir of the place where you launched the program.
 They have a filename composed by the name of the model file loaded plus the slice and with 
the extension .ng soo if you have loade a file named penguin.stl the and set 3 slices 
 the program will generate three files (penguin-0p8.ngc, penguin-1p6.ngc and 
 penguin-2p4.ngc)

2) go to the *Processes Tab* to choose the milling operation you want set the 
 desidered parameters and click on the "calculate" button if the "g-code" checkbox
 is checked the program start to generate the files else it will generate a ini file
 containing the istructions to generate the g-code (The option is here for future
 testing or for testing the program without generating the files, (to skip the
 time consuming operations)

3) wait a while and see if they are in the ngc directory.


The ngc file uses the information setted in the machine for the preamble and the
postamble so you can set different init operation per different machines.

You can also edit the ngc files generated and modify according your needs.

For now only the Slice strategy works, it assume that the overlap of the passes
in X or Y direction are the diameter of the tool minus the overlap percentage
calculate with this formula diameter-(diameter*overlap/100), if you set 25%
it will be diameter -(diameter*0,25)  

For the feedarate when the program is complete it will have a table containting
 the maximal suggested feedrate for each material (it is your choice what values
 are used ) but i will speed up the tuning operations of the gcode. 

FOR NOW the feedrate is set using the maximun feedrate of the machine obtained

- For the X and Y axis using the formula min(x-feedrate,y-feederate) and 
  corrected by the factor in the spinbox for XY feed.

- For the Z feedrate it is assumed the Z plungerate in the 
 machine settings corrected by the factor in the plungerate spinbox.
 
Both values are percentage so if you put in the box 90 you will obtain the 
max feedrate multiplied per 1.90 if you input -10 you will obtain the max feedrate
 multiplied by 0.90.  

For now only the zig passess work either in X or in Y direction.   

#### TOOLS:

Input SpinBox have a these limit:


Values    | for metric | for inches
--------- | ---------- |------------- 
precision | 0.001 (3 decimals) | 0.0001 (4 decimals)
Tool Diameter and Shaft diameter | 0 to 25 mm | 0 to 1 inch
Cutter Length and Overall Length | 0 to 100 mm |  0 to 5 inch 
Radius       | 0 to 25 mm         | 0 to 1 inch 
Angle        | 0 to 180 degree |  0 to 180 degree               
Number of flutes | 12  | 12


The only check done is that the cutting length of the tool can't be greater than the overall length of the tool

If you need to modify some of these limits, let me know and i modify them in the program. 


#### WORKPIECES:


You can set a upper and lower limits of the pieces, these are take in place to calculate the tollpaths as the start an stop axis movement, so you can set the model anywere in the workpiece setting them.

Is left to you how to use your machine, so you can enter the limits of the worlpiece as 

X: 0 min 10 max

Y: 0 min 15 max

Z: 0 min 4 max

and then fix your larger workpiece on the machinable area and the program will calculate the toolpaths relative to this limits, eventually calcultat the toolpath only for a particular area of the model.

For now there is no visualization of the model limits (work in progress, ready soon), in future there will be (similar at what happen in pycam) a visualization of the model with superimposted the workpiece limits so you can take more visually your decision.


Input SpinBox have these limits:

Values    | for metric | for inches
--------- | ---------- |------------- 
precision | 0.001 (3 decimals) | 0.0001 (4 decimals)
Dimensions | 0 to 2000 mm | 0 to 80 inch

I thinks it is enough for the actual hobby machines, feel free to ask for a different sizes 

#### PROCESSES (PATH CALCULATION):

During the calculations come sata are used to avoid some mistakes:

- The feedrate can't be greater than the machine feedrate
- the step down can't be greater than the cutting length of the tool
- The stepover is calculated starting to the tool diameter and applying the desidered overlap


Good work and beware of flying chips.



 
