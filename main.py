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
import matplotlib.pyplot as plt
import trimesh
from os import system
from scipy.optimize import minimize
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D


#constants
D = 1
sites = ["T1-West2", "Landscape_002.002"]
SITE = str(sites[1]) #"T1-West2"  # "Landscape_002"
LAND = "AreaSelection8x4"
BUILDING = "building4x4"
#building_name = "building4x4"
LEVEL = "level_location"

#paths
SLP_APP_PATH = 'C:/Users/arqfa/PycharmProjects/site_layout' # path to the site_layout app directory.
sys.path.append(SLP_APP_PATH)

# Dummy list for trees can be deleted once the tree detection module  have
# been calculated
site_trees = [0, 1, 0.5, 0, 0.25] * 500

#cleaning the console for a fresh start on the execution

cls = lambda: system('cls')

cls() #this function call will clear the console


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'{name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Site Layout Planning Optimization')

print ("!!!!" + SITE)
# defining the paths for the project

# path of the blender file we are using.
blender_file_path = bpy.path.abspath("//")  # This will update when using on different blender files.
print (blender_file_path)


# importing the blender_mesh module for measuring and intersection

from blender_mesh import site_analysis




D, dx_rows, dy_cols, bx_rows, by_cols, bz_height, z_level, top_grid_vtx, vtx_intersection = site_analysis(D, SITE, LAND, BUILDING, LEVEL, blender_file_path, SLP_APP_PATH)
# print(d, dx_rows, dy_cols, bx_rows, by_cols, bz_height)
print("the site and building variables have been calculated")

# Volume calculation module

from volume_calculation import z_coordinate_extraction, volume_formula

z_coord_intersection = z_coordinate_extraction(vtx_intersection)
z_coord_land = z_coordinate_extraction(top_grid_vtx)

# print(str(len(z_coord_intersection)) + str(z_coord_intersection[0:5]))
# print(str(len(z_coord_land)) + str(z_coord_land[0:5]))

site_volumes = volume_formula(dx_rows, dy_cols, D, z_coord_intersection, z_level)

print("##############")
print("The volumes per segment of grid have been calculated. There are " + str(len(site_volumes)))

# fitness function module

from fitness_functions import available_positions_function, f1_earthwork_vol_function, f2_earthwork_costs_function, \
    f3_deforestation_function, activation_function, temp_optimization_sorting

# available positions
available_positions = available_positions_function(top_grid_vtx, dx_rows, dy_cols, bx_rows, by_cols)
print("there are " + str(len(available_positions)) + " available positions on the grid from the original " + str(
    len(top_grid_vtx)))

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

activated_values = list(zip(activated_f1, activated_f2, activated_f3))
print("activated fitness functions calculated successfully for " + str(len(activated_f1)) + " values")


# optimization and sorting of solutions
weights = [0.5, 0.3, 0.2]
n_solutions = 5
score_values_sorted, score_values = temp_optimization_sorting(n_solutions, activated_values, available_positions,weights)
print("candidates sorted")
if score_values is not None:
    np.save(blender_file_path + '/score_values',
            score_values)  # This file can be deleted once the data has been joined
    print("score values successfully saved")
    np.save(blender_file_path + '/score_values_sorted',
            score_values_sorted)  # This file can be deleted once the data has been joined
    print("sorted score values successfully saved")

else:
    print('score values not saved')