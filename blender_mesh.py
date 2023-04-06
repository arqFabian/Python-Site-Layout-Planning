# This script was created to run a Site Design Analysis experiment
# using accepted earthwork analysis formulas based in prismoidal
# analysis to calculate accurately volumes of earth.

import bpy, bmesh
import os
import sys
import glob
import csv
import math
import numpy as np
import subprocess

# cleaning segment
from os import system

cls = lambda: system('cls')

cls()  # this function call will clear the console

# start of process def export():
def site_analysis (grid_size, full_site, land_extents_for_analysis, building_for_analysis, level_for_implantation):
    d = grid_size
    site = full_site #the full site chosen for analysis and intersection
    land = land_extents_for_analysis
    # land is the rectangular plane representing the area on the site that allows
    # for the building construction, it projects the extents of the grid its dimensions must be integers.
    building = building_for_analysis #chosen building to be tested for site layout planning
    level = level_for_implantation # a rectangular plane whose z coordinate determines the level
    # of the platform where the building will be constructed.

    print("Site Analysis in process")
    scene = bpy.data.scenes['Scene']
    # T1- terrain of West2- option
    land = bpy.data.objects.get("AreaSelection8x4")  # chosen area of the site
    level = bpy.data.objects.get("level_location")  # cut plane where the new level location would be.
    Site = "T1-West2"
    # Site = "2.Landscape.001-Orig.001"
    # T3- Lake - Option
    # land = bpy.data.objects.get("Plane.002")
    # Site = "T3-Lake"
    print("Terrain selected: " + str(Site))

####
if land != None:
    print("found the mesh")
else:
    print("mesh not found")

print("land mesh is located at ", land.location.x, ", ", land.location.y, ", ", land.location.z)
print("with bounding box ", land.dimensions.x, ", ", land.dimensions.y, ", ", land.dimensions.z)

# Setting variables

dx_rows = int(land.dimensions.x);
dy_cols = int(land.dimensions.y);
D = 1  # distance between vertices

vtx = []
for i in range(dx_rows + 1):
    for j in range(dy_cols + 1):
        vtx.append([i * land.dimensions.x / dx_rows + land.location.x - land.dimensions.x / 2.0,
                    j * land.dimensions.y / dy_cols + land.location.y - land.dimensions.y / 2.0,
                    land.dimensions.z + 5])

faces = []
for i in range(dx_rows):
    for j in range(dy_cols):
        faces.append([i * (dy_cols + 1) + j, (i + 1) * (dy_cols + 1) + j, (i + 1) * (dy_cols + 1) + j + 1])
        faces.append([i * (dy_cols + 1) + j, (i + 1) * (dy_cols + 1) + j + 1, i * (dy_cols + 1) + j + 1])

mesh = bpy.data.meshes.new("top_grid")
mesh.from_pydata(vtx, [], faces)
obj = bpy.data.objects.new("Plane_Top", mesh)
bpy.context.scene.collection.objects.link(obj)
print("Top Grid created as: Plane_Top")

# Exporting the vtx list for trimesh
# Save

o = [x for l in vtx for x in l]
v = len(vtx)
origin = np.array_split(o, v)
np.save('/Users/arqfa/OneDrive/Desktop/Research/origin', origin)
print("ray origins for intersection exported as 'origin.npy'")

############
# This section establishes the new level location base on the height (z value) position of a plane
z_level = float(level.location.z);
print(z_level)
np.save('/Users/arqfa/OneDrive/Desktop/Research/z_level',
        z_level)  # This file can be deleted once the data has been joined

# Exporting the terrain for intersection

# the name of the "site" that is being exported was defined at the beginning of the script
bpy.data.objects[Site].select_set(True)

# Duplicate mesh
bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'},
                              TRANSFORM_OT_translate={"value": (0, 0, 0), "orient_axis_ortho": 'X',
                                                      "orient_type": 'GLOBAL',
                                                      "orient_matrix": ((0, 0, 0), (0, 0, 0), (0, 0, 0)),
                                                      "orient_matrix_type": 'GLOBAL',
                                                      "constraint_axis": (False, False, False), "mirror": False,
                                                      "use_proportional_edit": False,
                                                      "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1,
                                                      "use_proportional_connected": False,
                                                      "use_proportional_projected": False, "snap": False,
                                                      "snap_elements": {'INCREMENT'}, "use_snap_project": False,
                                                      "snap_target": 'CLOSEST', "use_snap_self": True,
                                                      "use_snap_edit": True, "use_snap_nonedit": True,
                                                      "use_snap_selectable": False, "snap_point": (0, 0, 0),
                                                      "snap_align": False, "snap_normal": (0, 0, 0),
                                                      "gpencil_strokes": False, "cursor_transform": False,
                                                      "texture_space": False, "remove_on_cancel": False,
                                                      "view2d_edge_pan": False, "release_confirm": False,
                                                      "use_accurate": False, "use_automerge_and_split": False})

# To counter the error of "trimesh" that read the mesh rotated (and fails the intersection)
# we rotate on the x direction , 90 degrees, solving the no intersection error
bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL',
                         orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                         constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False,
                         proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False,
                         use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'},
                         use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True,
                         use_snap_nonedit=True, use_snap_selectable=False)
print("object duplicated succesfully")

# export rotated mesh to same data
blend_file_path = bpy.data.filepath
directory = os.path.dirname(blend_file_path)
target_file = os.path.join(directory, 'terrain.glb')
bpy.ops.export_scene.gltf(filepath=target_file, check_existing=True, export_format='GLB', use_selection=True)
print("terrain mesh exported: " + str(Site) + " selected")
# delete dummy object
bpy.ops.object.delete()

print("Duplicate dummy deleted")
# bpy.ops.object.delete(use_global=False, confirm=False)

# Run trimesh on an external script
command = ['/Users/arqfa/PycharmProjects/pythonProject/venv/Scripts/python',
           '/Users/arqfa/OneDrive/Desktop/Research/Intersection.py']
print(f'Running \"{" ".join(command)}\"')
subprocess.call(command, shell=True)

# load trimesh intersection lists.
# the vertexes of the intersection are on the list "vtx_intersection" that comes straight from the uploaded file
vtx_intersection = np.load('/Users/arqfa/OneDrive/Desktop/Research/intersection.npy')
print("Intersection data loaded back into blender")

# Visualize intersection mesh

faces = []
for i in range(dx_rows):
    for j in range(dy_cols):
        faces.append([i * (dy_cols + 1) + j, (i + 1) * (dy_cols + 1) + j, (i + 1) * (dy_cols + 1) + j + 1])
        faces.append([i * (dy_cols + 1) + j, (i + 1) * (dy_cols + 1) + j + 1, i * (dy_cols + 1) + j + 1])
mesh = bpy.data.meshes.new("Top_intersection")
mesh.from_pydata(vtx_intersection, [], faces)
obj = bpy.data.objects.new("Plane_int", mesh)
bpy.context.scene.collection.objects.link(obj)
print("!!!!Visualization of intersection mesh completed for terrain: " + str(Site))

# Delete top plane
# Get the object with the name "Plane_Top"
obj = bpy.data.objects.get("Plane_Top")

# Check if the object exists
if obj is not None:
    # Remove the object from the scene
    bpy.data.objects.remove(obj)
else:
    # Object with the name "Sphere" not found
    print("Object with the name 'Sphere' not found")

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
# print (vtx_intersection)


