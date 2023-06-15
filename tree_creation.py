# imports necessary
import bpy, bmesh
import numpy as np
import sys
from os import system

# Constants and parameters

# Site and object names

sites = ["L1_experiment", "L2_experiment", "L3_experiment", "test-site-1", "T0-West2"]  # list of the sites, in this form since we are manipulating several terrains from a single file

SITE = str(sites[0])  # the number represents the chosen name from the list "sites" name of the terrain we want to
# create trees

LAND = "AreaSelection"  # name of the chosen land mesh reprensenting the area inside the site to be used.
# The LAND should be decided based on legislation and area of interest but for now it must be a rectangular shape

# Algorithm parameters
GRID_UNIT_SIZE = 1

# tree constants
tree_object = "tree"  # name of the existing tree object
tree_quantity_for_particles = 50

# paths for python scripts
SLP_APP_PATH = 'C:/Users/arqfa/PycharmProjects/site_layout'  # path to the site_layout app directory.
sys.path.append(SLP_APP_PATH)

# defining the paths for the project

blender_file_path = bpy.path.abspath("//")  # path of the blender file, This will update when using on different
print(blender_file_path)

# cleaning the console for a fresh start on the execution
cls = lambda: system('cls')

cls()  # this function call will clear the console

# load vtx intersection list
#vtx_intersection = np.load(blender_file_path + 'vtx_intersection.npy')  # for testing the tree detection function
# and has no influence on the rest of the script
#print('vtx_intersection loaded')

# Dummy list for trees can be deleted once the tree detection module  has been calculated

# random.seed(123)  # set seed value
# site_trees = [random.randint(0, 1) for _ in range(10000)]
# np.save(blender_file_path + '/site_trees.npy',
#        site_trees)  # This file can be deleted once there is a tree creation module


# Start of tree creation
print('Tree creation component')



# creation of top mesh for tree detection
from blender_mesh import land_top_grid_analysis

top_grid_vtx, land_x_dimension, land_y_dimension, height = land_top_grid_analysis(GRID_UNIT_SIZE, SITE, LAND, blender_file_path)


# function to create a particle system from a terrain and a weight map

def create_particle_system(tree_object_input, terrain_object_input, tree_quantity_input):
    #initial message
    print(f"starting the creation of the particle system for {SITE}")

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select the "landscape" object
    terrain = bpy.data.objects[terrain_object_input]
    terrain.select_set(True)

    # Duplicate the selected object
    bpy.ops.object.duplicate()

    # Get the duplicate object
    terrain_duplicate = bpy.context.selected_objects[0]

    # Set the name of the duplicate object
    terrain_duplicate.name = terrain.name + "_vegetation"

    # Deselect all objects
    #bpy.ops.object.select_all(action='DESELECT')

    #terrain_duplicate = bpy.data.objects[terrain_object_input]
    terrain_duplicate.select_set(True)

    particle_systems = terrain_duplicate.particle_systems
    if "tree_particle_system" in particle_systems:
        bpy.ops.object.particle_system_remove()

    # Create a new particle system for the terrain object
    psys = terrain_duplicate.modifiers.new("ParticleSettings", type='PARTICLE_SYSTEM').particle_system

    # rename
    psys.name = "tree_particle_system"

    # Set particle system settings
    psys.settings.count = tree_quantity_input
    psys.settings.type = 'HAIR'
    psys.settings.emit_from = 'VERT'
    psys.settings.use_advanced_hair = True
    psys.settings.rotation_mode = 'GLOB_Z'

    # Set up the tree object as the particle object
    psys.settings.render_type = 'OBJECT'
    psys.settings.instance_object = bpy.data.objects[tree_object_input]
    psys.settings.particle_size = 0.5
    psys.settings.size_random = 0.1

    # Set vertex group for density

    psys_group = terrain_duplicate.particle_systems["tree_particle_system"]
    psys_group.vertex_group_density = "vegetation"

    # hide emitter from view and render
    bpy.context.object.show_instancer_for_viewport = False
    bpy.context.object.show_instancer_for_render = False

    # Update scene to reflect changes
    bpy.context.view_layer.update()

    print("Tree particle system created")
    return


create_particle_system(tree_object, SITE, tree_quantity_for_particles)


# function to make the instances real to be

def make_instances_real(terrain_object_input):
    # initial message
    print(f"starting conversion of particles into instances for {SITE}")

    # data collection
    tree_collection_name = "Tree instances"
    terrain_name = terrain_object_input + '_vegetation'
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

    # set tree collection as the active collection
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[
        tree_collection_name]

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    # Select the "landscape" object
    terrain = bpy.data.objects[terrain_name]
    terrain.select_set(True)

    # Make the instances real
    bpy.ops.object.duplicates_make_real()

    # Add the new objects to the tree collection
    tree_instances = bpy.data.collections[tree_collection_name]
    terrain_source = bpy.data.objects[terrain_name].users_collection[0]
    for obj in bpy.context.selected_objects:
        terrain_source.objects.unlink(obj)
        tree_instances.objects.link(obj)

    # success message
    print(f"conversion of particles into instances for {SITE} successful!!")


make_instances_real(SITE)



# function to detect if there is a tree on the region

def tree_detection_down(top_grid_vtx_input, site_input, top_grid_height_input):
    # initial message
    print(f'starting down ray tracing for {SITE}')

    # List of coordinates to check
    coordinates = top_grid_vtx_input

    if coordinates and site_input:
        # Get the object by name
        #site_obj = bpy.data.objects[site]

        # Hide LAND
        land_object = bpy.data.objects.get(LAND)

        if land_object is not None:
            # Hide the object in the viewport
            land_object.hide_viewport = True

        # Select and hide all objects that start with "terrain_"
        for terrain_obj in bpy.data.objects:
            if terrain_obj.name.startswith(site_input):
                terrain_obj.hide_viewport = True

        # Boolean list to store results
        site_trees_result = []

        # Get the current scene's dependency graph
        depsgraph = bpy.context.evaluated_depsgraph_get()

        # Iterate through coordinates and check for object
        for coord in coordinates:
            # Set up ray cast parameters
            origin = tuple(map(float, coord))
            direction = (0, 0, -1)
            distance = top_grid_height_input

            # Perform ray cast, providing the depsgraph as the first argument
            hit, loc, norm, obj, matrix, _ = bpy.context.scene.ray_cast(depsgraph, origin, direction, distance=distance)

            # If an object is hit, add 1 to the result list, otherwise add 0
            if hit:
                site_trees_result.append(1)
            else:
                site_trees_result.append(0)

        # Unhide all objects that start with "terrain_"
        for terrain_obj in bpy.data.objects:
            if terrain_obj.name.startswith(site_input):
                terrain_obj.hide_viewport = False

        land_object.hide_viewport = False

    else:
        print("")

    print(f"site_trees detection successful!!. There are {str(sum(site_trees_result))} trees under the selected area")

    return site_trees_result


site_trees = tree_detection_down(top_grid_vtx, SITE, height)
np.save(blender_file_path + '/site_trees', site_trees)
print("trees saved")


# function to create trees based on a boolean list
#
# it allows random list instead of particle systems
# This function is optional in case there is a need to create visualization of how many trees were detected
# or in case there is a need to visualize the random list
def insert_trees_from_site_tree_list(vtx_intersection_input, site_trees_list_input, tree_object_name):
    # initial message
    print(f'starting implantation of tree detected according to tree boolean list for {SITE}')

    # get the coordinates and site tree values for the specified number of solutions to plot
    coordinates = vtx_intersection_input
    trees = site_trees_list_input
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

    print(f"Trees created successfully!!. {str(sum(site_trees_list_input))} trees inserted")

    return


#insert_trees_from_site_tree_list(vtx_intersection, site_trees, tree_object)
