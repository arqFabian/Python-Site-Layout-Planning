
# importing the blender_mesh module for measuring and intersection

from blender_mesh import site_analysis

d, dx_rows, dy_cols, bx_rows, by_cols, bz_height = site_analysis(d, site, land, building, level)
#print(d, dx_rows, dy_cols, bx_rows, by_cols, bz_height)
print("the site and building variables have been calculated")

# Volume calculation module

from Volume_calculation import *

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

# print(str(len(z_coord_intersection)) + str(z_coord_intersection[0:5]))
# print(str(len(z_coord_land)) + str(z_coord_land[0:5]))

site_volumes = volume_formula(dx_rows, dy_cols, D, z_coord_intersection, z_level)

print("##############")
# print("the volumes per segment of grid are: " + str(site_volumes))
print("the volumes per segment of grid have been calculated. There are " + str(len(site_volumes)))

# fitness function module

from fitness_functions import*

# available positions
available_positions = available_positions_function(vtx_origin, dx_rows, dy_cols, bx_rows, by_cols)
print("there are " + str(len(available_positions)) + " available positions on the grid from the original " + str(len(vtx_origin)) )

# f1 - Earthwork volumes calculations function
f1_earthwork_vol = f1_earthwork_vol_function(available_positions, site_volumes)
# f2 - Earthwork costs calculations
f2_earthwork_costs = f2_earthwork_costs_function(available_positions, site_volumes)
# f3 - Deforestation Value calculations
f3_deforestation_value = f3_deforestation_function(available_positions, site_trees)

print("fitness functions calculated successfully for " + str(len(activated_f1)) + " values")
# Activation Function + final normalization
k_factor = 10
t0_point_value = 0.5

activated_f1 = activation_function(f1_earthwork_vol, k_factor, t0_point_value)
activated_f2 = activation_function(f2_earthwork_costs, k_factor, t0_point_value)
activated_f3 = activation_function(f3_deforestation_value, k_factor, t0_point_value)

print("activated fitness functions calculated successfully for " + str(len(activated_f1)) + " values")

