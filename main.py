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
import rtree
import random

from os import system
from scipy.optimize import minimize
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D
from mathutils import Vector
import plotly.graph_objects as go


#constants
D_GRID_UNIT_SIZE = 1
sites = ["L1_experiment","test-site-1", "T0-West2"] # list of the sites, in this form since we are manipulating several terrains from a single file
SITE = str(sites[0]) # the number represents the chosen name from the list "sites"
LAND = "AreaSelection" # name of the chosen land mesh reprensenting the area inside the site to be used.
                        # The LAND should be decided based on legislation and area of interest but for now it must be a rectangular shape
BUILDING = "building16x16" # name of the building mesh for wich we are calculating
LEVEL = "level_location" #name of the plane_mesh located at the desired level of implantation of building

K_FACTOR = 5 # Penalization value "k" applied during the activation formula
T0_INFLECTION_VALUE = 0.5 # inflection value "t0" applied during the activation formula. It must be from 0 to 1

WEIGHTS = [0.5, 0.3, 0.2]
# weights applied to each function (f1,f2,f3) respectively. They should add up to 1 because of the normalization.
# This values determined how we rank the different functions for deciding the final score.
# They are applied to the activated values (after using sigmoid function)
NUMBER_SOLUTIONS_TO_PLOT = 5

#paths
SLP_APP_PATH = 'C:/Users/arqfa/PycharmProjects/site_layout' # path to the site_layout app directory.
sys.path.append(SLP_APP_PATH)

#cleaning the console for a fresh start on the execution

cls = lambda: system('cls')

cls() #this function call will clear the console

#hello message

print (f"Starting Site Layout Planning Optimization application for {SITE}")

# defining the paths for the project
#
# path of the blender file we are using.
blender_file_path = bpy.path.abspath("//")  # This will update when using on different blender files.
print (blender_file_path)

# importing the blender_mesh module for measuring and intersection

from blender_mesh import site_analysis

D_GRID_UNIT_SIZE, land_x_dimension, land_y_dimension, building_x_dimension, building_y_dimension, \
building_z_dimension, z_level, top_grid_vtx, vtx_intersection = site_analysis(D_GRID_UNIT_SIZE,
                                                                              SITE, LAND, BUILDING, LEVEL, blender_file_path)


print("the site and building variables have been calculated")


# Volume calculation module

from volume_calculation import z_coordinate_extraction, volume_formula

z_coord_intersection = z_coordinate_extraction(vtx_intersection)
z_coord_land = z_coordinate_extraction(top_grid_vtx)

site_volumes = volume_formula(land_x_dimension, land_y_dimension, D_GRID_UNIT_SIZE, z_coord_intersection, z_level)
print("The volumes per segment of grid have been calculated. There are " + str(len(site_volumes)))

# Tree detection module

site_trees = np.load(blender_file_path + 'site_trees.npy')


# fitness function module transformation

from fitness_functions import available_positions_function, f1_earthwork_vol_function, f2_earthwork_costs_function, \
    f3_deforestation_function, activation_function, temp_overall_score_function, scores_coordinates_sorting_function

# available positions for the building
available_positions = available_positions_function(top_grid_vtx, land_x_dimension, land_y_dimension, building_x_dimension, building_y_dimension)

print(f"there are {str(len(available_positions))} available positions on the grid from the original {str(len(top_grid_vtx))}")

# f1 - Earthwork volumes calculations function
f1_earthwork_vol = f1_earthwork_vol_function(available_positions, site_volumes)

# f2 - Earthwork costs calculations
f2_earthwork_costs = f2_earthwork_costs_function(available_positions, site_volumes)

# f3 - Deforestation Value calculations
f3_deforestation_value = f3_deforestation_function(available_positions, site_trees)

# list with the original values
original_values = list(zip(f1_earthwork_vol, f2_earthwork_costs, f3_deforestation_value))

print(f"fitness functions calculated successfully for {str(len(available_positions))} values")


# Activation Function + final normalization

activated_f1 = activation_function(f1_earthwork_vol, K_FACTOR, T0_INFLECTION_VALUE)
activated_f2 = activation_function(f2_earthwork_costs, K_FACTOR, T0_INFLECTION_VALUE)
activated_f3 = activation_function(f3_deforestation_value, K_FACTOR, T0_INFLECTION_VALUE)

activated_values = list(zip(activated_f1, activated_f2, activated_f3))
print(f"activated fitness functions calculated successfully for {str(len(activated_f1))} values")




# optimization and sorting of solutions

overall_score = temp_overall_score_function(activated_values, WEIGHTS)

scores_coordinates_sorted = scores_coordinates_sorting_function(NUMBER_SOLUTIONS_TO_PLOT, activated_values,
                                                                original_values, available_positions, top_grid_vtx,
                                                                overall_score, z_level)


if scores_coordinates_sorted is not None:

    np.save(blender_file_path + '/scores_coordinates_sorted',
            scores_coordinates_sorted)  # This file can be deleted once the data has been joined
    print("score coordinates values successfully saved as scores_coordinates_sorted.npy")

else:
    print('score_coordinates_sorted not saved')




