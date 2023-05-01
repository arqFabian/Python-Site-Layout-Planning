import bpy, bmesh
import numpy as np
from mathutils import Vector
from os import system

# cleaning the console for a fresh start on the execution

cls = lambda: system('cls')

cls()  # this function call will clear the console

# load files

blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research"

scores_coordinates_sorted = np.load(blender_file_path + '/scores_coordinates_sorted.npy', allow_pickle=True)
print("sorted score values successfully loaded")

NUMBER_SOLUTIONS_TO_PLOT = 10  # number of spheres to be created to represent the ranking


# sphere visualization function

def sphere_creation(sorted_values_input, number_to_plot):
    available_positions, overall_score, activated_f1, activated_f2, activated_f3, f1_values, f2_values, f3_values, \
    available_coordinates = list(zip(*sorted_values_input))
    ranking_collection_name = "Ranking_collection"

    # substitute the z coordinate in avaliable coordinates
    for sublist in available_coordinates:
        sublist[2] = 15  # replace the z coordinate for a known height so that the spheres appear on top of everything

    # reduce the number of spheres to the desired number you want to plot
    coordinate = available_coordinates[:number_to_plot]

    # check if the "Sphere Material" already exists, otherwise create it
    sphere_material = bpy.data.materials.get("Sphere Material")
    if not sphere_material:
        sphere_material = bpy.data.materials.new(name="Sphere Material")
        sphere_material.diffuse_color = (1, 0, 0, 0)

    # check if the collection exists, otherwise create it
    ranking_collection = bpy.data.collections.get(ranking_collection_name)
    if ranking_collection:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in ranking_collection.objects:
            obj.select_set(True)
        bpy.ops.object.delete()

    else:
        ranking_collection = bpy.data.collections.new(ranking_collection_name)
        bpy.context.scene.collection.children.link(ranking_collection)

    # set ranking_collection as the active collection
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[
        ranking_collection_name]

    # loop through the coordinates and create a sphere at each location
    for i, coord in enumerate(coordinate):
        # create a new sphere mesh and object
        bpy.ops.mesh.primitive_uv_sphere_add(location=coord)
        sphere = bpy.context.object

        # set the scale and add a material to the sphere

        j = 1 - (i / number_to_plot)
        sphere.scale = Vector((j, j, j))
        sphere.data.materials.append(sphere_material)

        # set the name of the sphere using the counter value
        sphere.name = "Ranking_" + str(i + 1)

        # link the new tree object to the tree collection
        if sphere.name not in ranking_collection.objects:
            ranking_collection.objects.link(sphere)

        # ranking_collection.objects.link(sphere)

    print("spheres created")

    return


sphere_creation(scores_coordinates_sorted, NUMBER_SOLUTIONS_TO_PLOT)
