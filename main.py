# This script was created to run a Site Design Analysis experiment
# using accepted earthwork analysis formulas based in prismoidal
# analysis to calculate accurately volumes of earth.

# imports necessary
import bpy, bmesh
import os
import sys
import glob
import csv
import math
import numpy as np
import subprocess
from os import system


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'{name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Site Layout Planning Optimization')

#defining the paths for the project

#path of the blender file we are using.
blend_file_path = bpy.path.abspath("//") #This will update when using on different blender files.
#path to the site_layout app directory.
slp_app_path = 'C:/Users/arqfa/PycharmProjects/site_layout'
sys.path.append(slp_app_path)

#importing the blender_mesh module for measuring and intersection

from blender_mesh import site_analysis

building_name = "building4x4"
d = 1
site = "T1-West2"
land = "AreaSelection8x4"
building = "building4x4"
level = "level_location"

d, dx_rows, dy_cols, bx_rows, by_cols, bz_height = site_analysis(d, site, land, building, level)
print(d, dx_rows, dy_cols, bx_rows, by_cols, bz_height)

from Volume_calculation import*

vtx_origin = np.load('/Users/arqfa/OneDrive/Desktop/Research/top_grid_vtx.npy')
print("origin vertex loaded")
# load intersection vertex
vtx_intersection = np.load('/Users/arqfa/OneDrive/Desktop/Research/vtx_intersection.npy')
print("Intersection data loaded")
# load level z location for volume calculations
z_level = np.load('/Users/arqfa/OneDrive/Desktop/Research/z_level.npy')
print("Required level of platform loaded")
print(z_level)
z_coord_intersection = z_coordinate_extraction(vtx_intersection)
z_coord_land = z_coordinate_extraction(vtx_origin)

#print(str(len(z_coord_intersection)) + str(z_coord_intersection[0:5]))
#print(str(len(z_coord_land)) + str(z_coord_land[0:5]))

site_volumes = volume_formula(dx_rows, dy_cols, D, z_coord_intersection, z_level)

print("##############")
#print("the volumes per segment of grid are: " + str(site_volumes))
print("the volumes per segment of grid have been calculated. There are " + str(len(site_volumes)))
