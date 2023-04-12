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

# defining the paths for the project

# path of the blender file we are using.
blender_file_path = bpy.path.abspath("//")  # This will update when using on different blender files.
print (blender_file_path)
# path to the site_layout app directory.
slp_app_path = 'C:/Users/arqfa/PycharmProjects/site_layout'
sys.path.append(slp_app_path)

# importing the blender_mesh module for measuring and intersection


from blender_mesh import site_analysis

building_name = "building4x4"
d = 1
site = "T1-West2"  # "Landscape_002"
land = "AreaSelection8x4"
building = "building4x4"
level = "level_location"
site_trees = [0, 1, 0.5, 0, 0.25] * 500  # Dummy list for trees can be deleted once the tree detection module  have
# been calculated

d, dx_rows, dy_cols, bx_rows, by_cols, bz_height = site_analysis(d, site, land, building, level, blender_file_path)
# print(d, dx_rows, dy_cols, bx_rows, by_cols, bz_height)
print("the site and building variables have been calculated")

# Volume calculation module

from Volume_calculation import z_coordinate_extraction, volume_formula

vtx_origin = np.load(blender_file_path + 'top_grid_vtx.npy')
print("origin vertex loaded")
# load intersection vertex
vtx_intersection = np.load(blender_file_path + 'vtx_intersection.npy')
print("Intersection data loaded")
# load level z location for volume calculations
z_level = np.load(blender_file_path + 'z_level.npy')
print("Required level of platform loaded")
print(z_level)
z_coord_intersection = z_coordinate_extraction(vtx_intersection)
z_coord_land = z_coordinate_extraction(vtx_origin)

# print(str(len(z_coord_intersection)) + str(z_coord_intersection[0:5]))
# print(str(len(z_coord_land)) + str(z_coord_land[0:5]))

site_volumes = volume_formula(dx_rows, dy_cols, d, z_coord_intersection, z_level)

print("##############")
print("The volumes per segment of grid have been calculated. There are " + str(len(site_volumes)))

# fitness function module

from fitness_functions import available_positions_function, f1_earthwork_vol_function, f2_earthwork_costs_function, \
    f3_deforestation_function, activation_function

# available positions
available_positions = available_positions_function(vtx_origin, dx_rows, dy_cols, bx_rows, by_cols)
print("there are " + str(len(available_positions)) + " available positions on the grid from the original " + str(
    len(vtx_origin)))

# f1 - Earthwork volumes calculations function
f1_earthwork_vol = f1_earthwork_vol_function(available_positions, site_volumes)
# f2 - Earthwork costs calculations
f2_earthwork_costs = f2_earthwork_costs_function(available_positions, site_volumes)
# f3 - Deforestation Value calculations

f3_deforestation_value = f3_deforestation_function(available_positions, site_trees)

print("fitness functions calculated successfully for " + str(len(available_positions)) + " values")
# Activation Function + final normalization
k_factor = 10
t0_point_value = 0.5

activated_f1 = activation_function(f1_earthwork_vol, k_factor, t0_point_value)
activated_f2 = activation_function(f2_earthwork_costs, k_factor, t0_point_value)
activated_f3 = activation_function(f3_deforestation_value, k_factor, t0_point_value)

print("activated fitness functions calculated successfully for " + str(len(activated_f1)) + " values")

# hello 4
