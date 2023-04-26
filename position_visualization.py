import bpy, bmesh
import numpy as np
from mathutils import Vector

blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research"

scores_coordinates_sorted = np.load(blender_file_path + '/scores_coordinates_sorted.npy', allow_pickle=True)
print("sorted score values successfully loaded")

NUMBER_SOLUTIONS_TO_PLOT = 10

def sphere_creation(sorted_values_input, number_to_plot):
    available_positions, overall_score, activated_f1, activated_f2, activated_f3, f1_values, f2_values, f3_values,\
    available_coordinates = list(zip(*sorted_values_input))

    for sublist in available_coordinates:
        sublist[2] = 15
    # create a new material and set its properties
    mat = bpy.data.materials.new(name="Sphere Material")
    mat.diffuse_color = (1, 0, 0, 0)

    coords = available_coordinates[:number_to_plot]
    print (coords)
    # loop through the coordinates and create a sphere at each location
    for i, coord in enumerate(coords):
        # create a new sphere mesh and object
        bpy.ops.mesh.primitive_uv_sphere_add(location=coord)
        sphere = bpy.context.object

        # set the scale and add a material to the sphere
        j = 1 - (i/number_to_plot)
        sphere.scale = Vector((j, j, j))
        sphere.data.materials.append(mat)

        # set the name of the sphere using the counter value
        sphere.name = "Ranking_" + str(i + 1)

    print("spheres created")

    return


sphere_creation(scores_coordinates_sorted, NUMBER_SOLUTIONS_TO_PLOT)