# EuroCAM
It would be a pratical and fast replacement of pycam for linux and maybe other OS.

The hard work is done by OpenCAMLib from https://github.com/aewallin/opencamlib.

The program is still in Alpha stage but the main core is almost done.

see in the i18n directory the help file, it can be visualized also through the help menu

I'm using and developing eurocam on debian jessie

Chances are that you have most of the library needed in the package manager of your favourite distribution, these are the basical requirements.

 - Pyside: the python binding to the qt4 library, usually it is installable from the distro package manager.

- visvis is a graphics library with python binding that is easily embeddable in qt4 (it is the only graphics library that i have made to work with qt4 even if in a separate window). If it is not found in your distro is usually installable with "pip install visvis" and doing that generally pull in all his the desired dependencies notable numpy and some other scientific libraries.

- vtk version 6.1,  in debian is present as  "vtk6" package name and the corresponding python-vk6 bindings
 
- openCAMLib from "https://github.com/aewallin/opencamlib" use the instruction on github to produce a debian package and install it

- eurocam use a modified version of the camvtk, modified to work with vtk version > 5  

For any issue please use the issues button on the github page and I try to help you as best i can 

Good working

Carlo D.
