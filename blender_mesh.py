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
from os import system


# start of process def export():
def site_analysis(grid_size, full_site, land_extents_for_analysis, building_for_analysis, level_for_implantation,
                  blender_path):
    # determine the variables from the inputs

    d = grid_size
    site = bpy.data.objects.get(full_site)  # the full site chosen for analysis and intersection
    land = bpy.data.objects.get(
        land_extents_for_analysis)  # land is the rectangular plane representing the area on the site that allows for the building construction, it projects the extents of the grid its dimensions must be integers.
    building = bpy.data.objects.get(building_for_analysis)  # chosen building to be tested for site layout planning
    level = bpy.data.objects.get(
        level_for_implantation)  # a rectangular plane whose z coordinate determines the level of the platform where the building will be constructed.
    height_of_grid = 10
    print("Terrain selected: " + str(full_site))
    print("Land selected: " + str(land_extents_for_analysis))
    print("building selected: " + str(building_for_analysis))
    print("level selected: " + str(level_for_implantation))
    print("Grid size: " + str(grid_size) + " m")

    # measuring the land and creating top grid and saving the vertex on the top grid
    if land != None:
        print("found the mesh")
        print("land mesh is located at ", land.location.x, ", ", land.location.y, ", ", land.location.z)
        print("with bounding box ", land.dimensions.x, ", ", land.dimensions.y, ", ", land.dimensions.z)

        # Setting variables

        dx_rows = int(land.dimensions.x)
        dy_cols = int(land.dimensions.y)
        h = int(site.dimensions.z) + height_of_grid

        vtx = []
        for i in range(dx_rows + 1):
            for j in range(dy_cols + 1):
                vtx.append([i * land.dimensions.x / dx_rows + land.location.x - land.dimensions.x / 2.0,
                            j * land.dimensions.y / dy_cols + land.location.y - land.dimensions.y / 2.0,
                            land.dimensions.z + h])

        faces = []
        for i in range(dx_rows):
            for j in range(dy_cols):
                faces.append([i * (dy_cols + 1) + j, (i + 1) * (dy_cols + 1) + j, (i + 1) * (dy_cols + 1) + j + 1])
                faces.append([i * (dy_cols + 1) + j, (i + 1) * (dy_cols + 1) + j + 1, i * (dy_cols + 1) + j + 1])

        mesh = bpy.data.meshes.new("top_mesh")
        mesh.from_pydata(vtx, [], faces)
        obj = bpy.data.objects.new("top_grid_of_analysis", mesh)
        bpy.context.scene.collection.objects.link(obj)
        print("Top Grid created as: top_grid_of_analysis")

        # saving the list of vertex of the "Top Grid" to be used on the mesh_intersection file with trimesh.
        vtx_position = [x for l in vtx for x in l]
        vtx_id = len(vtx)
        top_grid_vtx = np.array_split(vtx_position, vtx_id)
        # np.save('/Users/arqfa/OneDrive/Desktop/Research/top_grid_vtx', top_grid_vtx)
        np.save(blender_path + 'top_grid_vtx', top_grid_vtx)
        print("ray origins for intersection exported as 'top_grid_vtx'")

        # Delete "top_grid_of_analysis" since it won't be used anymore
        obj = bpy.data.objects.get("top_grid_of_analysis")
        if obj != None:
            # Remove the object from the scene
            bpy.data.objects.remove(obj)
        else:
            print("Object with the name 'top_grid_of_analysis' not found")
    else:
        print("mesh not found")

    # This section establishes the new level location base on the height (z value) position of a plane
    if level != None:
        z_level = float(level.location.z)
        print(z_level)
        np.save(blender_path + 'z_level',
                z_level)  # This file can be deleted once the data has been joined
    else:
        print("level location '" + str(level_for_implantation) + "' not found")

    # This section analizes dimensions of the new building
    if building is not None:
        bx_rows = int(building.dimensions.x)
        by_cols = int(building.dimensions.y)
        bz_height = int(building.dimensions.z)
        print("The building has the following dimensions (x,y,z):  ", building.dimensions.x, ", ",
              building.dimensions.y,
              ", ", building.dimensions.z)
    else:
        print("The building " + str(building_for_analysis) + "not found")

    # Exporting the terrain for intersection

    if site is not None:
        # the name of the "site" that is being exported was defined at the beginning of the script
        bpy.context.view_layer.objects.active = site
        site.select_set(True)
        # Duplicate mesh
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'},
                                      TRANSFORM_OT_translate={"value": (0, 0, 0), "orient_axis_ortho": 'X',
                                                              "orient_type": 'GLOBAL',
                                                              "orient_matrix": ((0, 0, 0), (0, 0, 0), (0, 0, 0)),
                                                              "orient_matrix_type": 'GLOBAL',
                                                              "constraint_axis": (False, False, False), "mirror": False,
                                                              "use_proportional_edit": False,
                                                              "proportional_edit_falloff": 'SMOOTH',
                                                              "proportional_size": 1,
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

        # To counter the error of "trimesh" that read the mesh rotated (and fails the intersection) we rotate on the
        # x direction , 90 degrees, solving the no intersection error
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL',
                                 orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                                 constraint_axis=(True, False, False), mirror=False, use_proportional_edit=False,
                                 proportional_edit_falloff='SMOOTH', proportional_size=1,
                                 use_proportional_connected=False,
                                 use_proportional_projected=False, snap=False, snap_elements={'INCREMENT'},
                                 use_snap_project=False, snap_target='CLOSEST', use_snap_self=True, use_snap_edit=True,
                                 use_snap_nonedit=True, use_snap_selectable=False)

        # export the rotated mesh to same data
        # blend_file_path = bpy.data.filepath
        # directory = os.path.dirname(blend_file_path)
        directory = os.path.dirname(blender_path)
        target_file = os.path.join(directory, 'terrain.glb')
        bpy.ops.export_scene.gltf(filepath=target_file, check_existing=True, export_format='GLB', use_selection=True)
        print("terrain mesh exported successfully as 'terrain.glb' for the site: " + str(full_site))
        # delete dummy object
        bpy.ops.object.delete()

    else:
        print("site not found")

    # to calculate the intersection between the GRID and the terrain, run the file mesh_intersection.py that uses
    # trimesh to launch rays from the grid vertex and determines the intersection with the site.

    command = ['/Users/arqfa/PycharmProjects/pythonProject/venv/Scripts/python',
               '/Users/arqfa/PycharmProjects/site_layout/mesh_intersection.py']
    print(f'Running \"{" ".join(command)}\"')
    subprocess.call(command, shell=True)
    # load trimesh intersection lists.
    # the vertexes of the intersection are on the list "vtx_intersection.npy" that comes straight from the uploaded file
    try:
        vtx_intersection = np.load('/Users/arqfa/OneDrive/Desktop/Research/vtx_intersection.npy')
        print("Intersection data loaded back into blender")
    except:
        print("Error loading vtx_intersection.npy")

        # exit function if there was an error loading the file
        return

    # continue with the rest of the code to visualize the intersection mesh
    faces = []
    for i in range(dx_rows):
        for j in range(dy_cols):
            faces.append([i * (dy_cols + 1) + j, (i + 1) * (dy_cols + 1) + j, (i + 1) * (dy_cols + 1) + j + 1])
            faces.append([i * (dy_cols + 1) + j, (i + 1) * (dy_cols + 1) + j + 1, i * (dy_cols + 1) + j + 1])
    mesh = bpy.data.meshes.new("Top_intersection")
    mesh.from_pydata(vtx_intersection, [], faces)
    obj = bpy.data.objects.new("mesh_intersection", mesh)
    bpy.context.scene.collection.objects.link(obj)
    print("!!!!Visualization of intersection mesh completed as 'mesh intersection' for the site: " + str(full_site))

    return d, dx_rows, dy_cols, bx_rows, by_cols, bz_height
    # return {'dx': dx_rows, 'dy': dy_cols, 'bx': bx_rows}#d, dx_rows, dy_cols, bx_rows, by_cols, bz_height
