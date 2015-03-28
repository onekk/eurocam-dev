# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 19:29:17 2015

@author: carlo-m
"""
import re
import sys
import os.path


def scan_gcode(filename):
    #print filename
    # Iterate through g-code file
    lcnt = 0
    unit = "none"
    command = []
    fin = open(filename, 'r')    
    for line in fin:
        lcnt += 1 
        # Strip comments/spaces/tabs/new line and capitalize. Comment MSG not supported.
        block = re.sub('\s|\(.*?\)','',line).upper() 
        #block = re.sub('\\\\','',block) # Strip \ block delete character
        #block = re.sub('%','',block) # Strip % program start/stop character
        
        if len(block) == 0 :  # Ignore empty blocks
            #print "Skipping: " + line.strip()
            pass
        else :  
            
            g_cmd = re.findall(r'[^0-9\.\-]+',block) # Extract block command characters
            g_num = re.findall(r'[0-9\.\-]+',block) # Extract block numbers
            
            # G-code block error checks
            # if len(g_cmd) != len(g_num) : print block; raise Exception('Invalid block. Unbalanced word and values.')
            if 'N' in g_cmd :
                if g_cmd[0]!='N':
                    msg =  'Line  {0}: line number must be first command in line.'.format(lcnt)
                    return ("KO", unit, msg)
                if g_cmd.count('N') > 1:
                    msg = 'Line {0}: More than one line number in block.'.format(lcnt)
                    return ("KO" ,unit, msg)
                g_cmd = g_cmd[1:]  # Remove line number word
                g_num = g_num[1:]
                   
            for cmd,num in zip(g_cmd,g_num) :
                command.append((cmd,num))
    
    motions = []            
    for cmd in command:
        if cmd[0] == 'F':
           pass
        elif cmd[0] == 'G':
           if cmd[1] in ('00','01','02','03','1','0','2','3','90','91'):
               motions.append(cmd)
           elif cmd[1] == 21:
               unit = "mm"
           elif cmd[1] ==20:
               unit = "inch"
        else:
            motions.append(cmd)   
              
    print "motions  {0} \n \n".format(len(motions))
    return ("OK",unit,motions)

def out_point(motions):
    points = []
    cnt = 0
    flag = 1
    while flag > 0:
        if cnt >= len(motions):
            return points
        #print cnt, len(motions)    
        mot = motions[cnt]
        #print "motion = ", mot,cnt
        mtyp = ''
        if mot[0] == 'G':
            if mot[1] in ('00','0'):
                mtyp = "r"
            if mot[1] in ('01','1'):
                mtyp = "n"
            if mot[1] in ('02','2'):
                mtyp = "cwa"
            if mot[1] in ('03','3'):
                mtyp = "ccwa"                
            if mot[1] in ('90','91'):
                mtyp = "cc"
        else:
            mtyp = "no motion"
        #print "Motion = ", mtyp    
        if mtyp in ("r","n","cwa","ccwa") : #linear motions we expect a coordinate
            block = 0
            idx = cnt
            x = "n"
            y = "n"
            z = "n"            
            while block == 0:
                #print "Coordinates in while = ",x,y,z                 
                idx = idx + 1
                if idx > len(motions):
                    points.append((mtyp ,(x,y,z)))
                    return points                      
                mot = motions[idx]
                #print "mot after check block ", idx, mot
                if mot[0] in ('X','Y','Z'):
                    #print "mot is motion" 
                    if mot[0] is 'X':
                        x = mot[1]
                    if mot[0] is 'Y':
                        y = mot[1]
                    if mot[0] is 'Z':
                        z = mot[1]
                else:
                    #print "mot is no motion"                    
                    block = 1
            points.append((mtyp,(x,y,z)))                    
            cnt = idx + 1

        else:
            print "motion is no lm (idx)", idx
            idx = idx + 1
        cnt = idx    
            
    return points

def clear_points(points):
    pfilt = []
    for point in points:
        if point[1] == ('n','n','n'):
            pass
        else:
            pfilt.append(point)
     
    return pfilt
    
def aggregate_tpath(points):    
    pfilt2 = []
    x = 0.0
    y = 0.0
    z = 0.0
    cnt = 0
    while cnt < len(points):
        if points[cnt][1][0] == 'n':
            xp = x
        else:
            xp = float(points[cnt][1][0])
        if points[cnt][1][1] == 'n':
            yp = y
        else:
            yp = float(points[cnt][1][1])
        if points[cnt][1][2] == 'n':
            zp = z
        else:
            zp = float(points[cnt][1][2])
        x = xp
        y = yp
        z = zp
        pfilt2.append((points[cnt][0],(x,y,z)))
        #print pfilt2
        cnt = cnt + 1
    return pfilt2

def make_tpath(filename):
    ret = scan_gcode(filename)
    if ret[0] == "OK":
        if len(ret[2]) > 1:
            points = out_point(ret[2])
            raw_tp = clear_points(points)
            toolpath = aggregate_tpath(raw_tp)
        else:
             return "KO","Toolpath is wrong"
        return "OK",toolpath
    else:
         return "KO",[]

if __name__ == "__main__":
        
    filename = "test.ngc"
    
    ret,toolpath = make_tpath(filename)
    if ret[0] == "OK":
        print toolpath
    elif ret == "KO":
        print "Errore"
        