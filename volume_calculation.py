import numpy as np


#blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research"
blender_file_path = "/Users/arqfa/OneDrive - Kyushu University/ResearchBigData/VR-research/BlenderFiles"
vtx_origin = np.load(blender_file_path + '/top_grid_vtx.npy')
print("origin vertex loaded")
# load intersection vertex
vtx_intersection = np.load(blender_file_path + '/vtx_intersection.npy')
print("Intersection data loaded")
# load level z location for volume calculations
z_level = np.load(blender_file_path + '/z_level.npy')
print("Intersection data loaded")
print(z_level)

site_information = np.load(blender_file_path + '/site_information.npy')
print("site information loaded")
#D, dx_rows, dy_cols, bx_rows, by_cols, bz_height, z_level = site_information

D = int(site_information[0])
dx_rows = int(site_information[1])
dy_cols = int(site_information[2])
bx_rows = int(site_information[3])
by_cols = int(site_information[4])
bz_height = int(site_information[5])
z_level = int(site_information[6])

###
# This function extract the z coordinate from the vtx intersections.
# the z coordinate is the value use for the volume calculations
###

def z_coordinate_extraction(input_list_vertex):
    coord = []
    for i in range(len(input_list_vertex)):
        j = input_list_vertex[i]
        k = j[2]
        coord.append(k)

    return coord


z_coord_intersection = z_coordinate_extraction(vtx_intersection)
z_coord_land = z_coordinate_extraction(vtx_origin)



#############
# This function takes the
def volume_formula(distance_x, distance_y, d_dist_btw_axes, z_intersection_list, input_z_level):
    level_difference = []
    h = d_dist_btw_axes
    for i in range(len(z_intersection_list)):
        level_difference.append(z_intersection_list[i] - input_z_level)
    # code for area!!!!
    # Trapezoid area formula: A = ((a+b)/2)*h; where:
    # a, b are the z coordinates of two points and "h" is the distance between rows or axes in this case D
    x = int(distance_x)
    y = int(distance_y)
    areas = []
    for i in range(0, int(y / h)):
        i_min = i * (x / h + 1)
        i_max = int(i_min) + (x / h)
        for j in range(int(i_min), int(i_max + 1)):
            a = level_difference[j]
            b = level_difference[int(j + x / h + 1)]
            grid_area = (a + b) / 2
            areas.append(grid_area)
    # print("areas by axis X " + str(len(areas)) + str(areas))

    # !!!!!!code for volume!!!!
    # Prismoid formula : V = (A1+A2)*d/2 ;
    # where d is distance between the areas so in this case it is the value we called D or 1 m
    volumes = []
    for i in range(int(y / h)):
        i_min = i * (x / h + 1)
        i_max = int(i_min) + (x / h)
        for j in range(int(i_min), int(i_max)):
            v = ((areas[j] + areas[(j + 1)]) / 2) * h
            volumes.append(v)
    # print("volumes by axis X: " + str(len(volumes)) + str(volumes))
    return volumes


site_volumes = volume_formula(dx_rows, dy_cols, D, z_coord_intersection, z_level)

#print("!!!!!!!!")
#print("the volumes per segment of grid are: " + str(site_volumes))

np.save(blender_file_path + '/site_volumes',
        site_volumes)  # This file can be deleted once the data has been joined
#print("Volumes exported successfully")


