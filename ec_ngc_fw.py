###########################
#                         #
# simple G-code writer.   #
# Anders Wallin 2012      #
# Carlo Dormeletti 2015   #
#                         #
###########################



def fileopen(filename):
    global ncout
    ncout = open(filename,'w')

def filewrite(line):
    global ncout
    ncout.write(line)

def fileclose():
    global ncout
    ncout.close()

def line_to(x,y,z):
    f_line = "G1 X{:.4f} Y{:.4f} Z{:.4f} F{:.0f}\n".format(x, y, z, feedrate)
    filewrite(f_line)
    
def xy_line_to(x,y):
    f_line = "G1 X{:.4f} Y{:.4f}\n".format(x, y)
    filewrite(f_line)
    
# (endpoint, radius, center, cw?)
def xy_arc_to( x,y, r, cx,cy, cw ):
    if (cw):
        f_line = "G2 X% 8.5f Y% 8.5f R% 8.5f" % (x, y, r)
    else:
        f_line = "G3 X% 8.5f Y% 8.5f R% 8.5f" % (x, y, r)
    # FIXME: optional IJK format arcs
    
def xy_rapid_to(x,y):
    f_line = "G0 X{:.4f} Y{:.4f}\n".format(x, y)
    filewrite(f_line)

def pen_up():
    f_line = "G0 Z {:.4f}\n".format(safe_height)
    filewrite(f_line)

def pen_down(z=0):
    #f_line = "G0 Z {:.4f}\n".format(z)
    #filewrite(f_line)
    comment("plunge pass")
    plunge(z)


def plunge(z):
    f_line =  "G1 Z {:.4f} F{:.0f}\n".format(z, plungerate)
    filewrite(f_line)

def comment(s=""):
    s1 = s.replace("(", "<")
    s2 = s1.replace(")",">")
    f_line = "( {} )\n".format(s2)
    filewrite(f_line)
    
if __name__ == "__main__":
    print "Nothing to see here."
