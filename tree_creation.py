# imports necessary
import bpy, bmesh
import numpy as np

from os import system

# path of the blender file we are using.
blender_file_path = bpy.path.abspath("//")  # This will update when using on different blender files.
print(blender_file_path)

# cleaning the console for a fresh start on the execution

cls = lambda: system('cls')

cls()  # this function call will clear the console

# Dummy list for trees can be deleted once the tree detection module  has been calculated

site_trees = np.load(blender_file_path + 'site_trees.npy')
print('site_trees loaded')
vtx_intersection = np.load(blender_file_path + 'vtx_intersection.npy')
print('vtx_intersection loaded')

tree_object = "tree"  # name of the existing tree object


def insert_trees(vtx_intersection_input, site_trees_input, tree_object_name):

    # get the coordinates and site tree values for the specified number of solutions to plot
    coordinates = vtx_intersection_input[:5]
    trees = site_trees_input
    tree_collection_name = "Tree Collection"

    # check if the collection exists, otherwise create it
    tree_collection = bpy.data.collections.get(tree_collection_name)
    if tree_collection:
        bpy.ops.object.select_all(action='DESELECT')
        for obj in tree_collection.objects:
            obj.select_set(True)
        bpy.ops.object.delete()

    if not tree_collection:
        tree_collection = bpy.data.collections.new(tree_collection_name)
        bpy.context.scene.collection.children.link(tree_collection)

    # set ranking_collection as the active collection
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[
        tree_collection_name]

    # loop through the coordinates and insert a tree at each location if the site tree value is 1
    for i, coordinates in enumerate(coordinates):
        if trees[i] == 1:
            # create a new tree object and set its location
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[str(tree_object_name)].select_set(True)
            new_tree = bpy.context.selected_objects[0].copy()
            new_tree.location = coordinates

            # link the new tree object to the tree collection
            tree_collection.objects.link(new_tree)

            # set the name of the tree using the counter value
            new_tree.name = "tree" + str(i + 1)

    print("trees inserted")

    return


insert_trees(vtx_intersection, site_trees, tree_object)


def tree_detection(vtx_intersection_input, tree_object_name):

