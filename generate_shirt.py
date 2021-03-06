# Takes 1 command line arguments
#   1) string; path to CSV point file

# Generates files in the /models/ directory
#   1) an OBJ file called shirt.obj
#   2) a Maya Binary file called shirt.mb

import sys
#sys.path.insert(0, "/Applications/Autodesk/maya2015/Maya.app/Contents/Frameworks/Python.framework/Versions/Current/lib/python2.7/site-packages")
import maya.standalone
maya.standalone.initialize()
import maya.cmds as cmds
import maya.mel as mel
import csv
import os
import getpass

OSX_RENDER_DIR = "/Users/" + str(getpass.getuser()) + "/Documents/maya/projects/default/images/"
OSX_MB_DIR = "/Users/" + str(getpass.getuser()) + "/Documents/maya/projects/default/"
UBUNTU_RENDER_DIR = "/home/" + str(getpass.getuser()) + "/maya/projects/default/images/"
UBUNTU_MB_DIR = "/home/" + str(getpass.getuser()) + "/maya/projects/default/"

# System specific paths
RENDER_DEFAULT_DIRECTORY = OSX_RENDER_DIR
MB_DEFAULT_DIRECTORY = OSX_MB_DIR

SUBDIVISIONS = 3
OUT_NAME = "shirt"

# Read from CSV file, store in points
def read_csv():
    """Opens CSV file and stores each points (tuple) in a list"""
    points = []
    with open(sys.argv[1], "rU") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 3:
                print("Points in CSV file are greater than 3 dimensions")
                sys.exit(0)
            # If set of points is 2 dimensional, autogenerate the 3rd dimension
            elif len(row) == 2:
                row.append(['0'])
            points.append(tuple(map(float, row)))
    return points

# Create polygon called shirt based on points
def generate(pts):
    """Takes in a list of tuples (set of 3D points) and generates a polygon model"""
    cmds.polyCreateFacet(name="shirt", p=points)
    cmds.polyTriangulate()
    cmds.polyQuad(angle=90)
    cmds.polySubdivideFacet(dv=SUBDIVISIONS)
    cmds.polyTriangulate()
    
    # Center shirt on origin
    centerX = cmds.objectCenter("shirt", x = True, gl = True)
    centerY = cmds.objectCenter("shirt", y = True, gl = True)
    centerZ = cmds.objectCenter("shirt", z = True, gl = True)
    cmds.move(-centerX, -centerY, -centerZ, "shirt", absolute=True)
    
# Exports file as a Maya Binary
def export_mb(name):
    cmds.file(rename = name + ".mb")
    cmds.file(save = True, type = "mayaBinary")
    os.system("cp " + MB_DEFAULT_DIRECTORY + name + ".mb " + os.path.dirname(os.path.realpath(__file__)) + "/models/" + name + ".mb")

# Exports file as an OBJ
def export_obj(name):
    cmds.loadPlugin('objExport')
    obj_path = os.path.dirname(os.path.realpath(__file__)) + "/models/" + name + ".obj"
    mel.eval('file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1" -type "OBJexport" -pr -ea "%s";' % obj_path)

# Main Program
points = read_csv()
generate(points)
export_obj(OUT_NAME)
export_mb(OUT_NAME)
