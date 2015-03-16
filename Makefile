# Makefile for eurocam
# copyright 2015 Dormeletti Carlo
# License MIT
# use TAB for identing

trans:
	pyside-lupdate eurocam.pro


ui:
	pyside-uic eurocam.ui -o eurocam_ui.py
	
clean:
	rm *.pyc 

