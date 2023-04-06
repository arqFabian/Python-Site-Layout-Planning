# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# imports necessary
import trimesh
import numpy as np
import plotly.graph_objects as go
import math


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'{name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Site Layout Planning Optimization')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import blender_mesh
from blender_mesh import*

d = 1
site = "T1-West2"
land = "AreaSelection8x4"
building = ""
level =
slp_result = site_analysis(d, site, land, building, level)
built = site_analysis()
land = bpy.data.objects.get("AreaSelection8x4")# chosen area of the site
level = bpy.data.objects.get("level_location") #cut plane where the new level location would be.
Site = "T1-West2"
#Site = "2.Landscape.001-Orig.001"
#T3- Lake - Option
#land = bpy.data.objects.get("Plane.002")
#Site = "T3-Lake"
D = 1 #distance between vertices
print ("Terrain selected: " + str(Site))