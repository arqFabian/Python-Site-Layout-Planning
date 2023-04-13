# This script uses trimesh as the main tool for processing the intersections.
# The lists are imported from blender and in here are reformatted as numpy arrays.
# The meshes are in GLB format as per recommended by trimesh on their website.

"""
Fragment of code that identifies the intersection point between the site
and rays with origin on a grid stationed above the bounds of the site.
The scripts works outside the frame of blender.
"""

import trimesh
import rtree
import numpy as np

blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research/"
# mesh
#import mesh representing the site from blender
mesh = trimesh.load(blender_file_path + 'terrain.glb', force='mesh')
#load data from blender grid origin
data = np.load(blender_file_path + 'top_grid_vtx.npy')
def intersection_trimesh (top_grid_vtx_input, blender_file_path_input):
    # mesh
    # import mesh representing the site from blender
    mesh = trimesh.load(blender_file_path_input + '/terrain.glb', force='mesh')
    # create some rays and find the intersection "rays - site"
    # load data from blender grid origin
    top_data = top_grid_vtx_input

    if mesh and top_data is not None:
        ray_origins = np.array(top_data)
        # print(ray_origins)
        # ray_directions pointing down
        ray_directions = np.array([[0, 0, -1]] * int(len(ray_origins)))

        # run trimesh to find the intersection between the rays and site
        locations, index_ray, index_tri = mesh.ray.intersects_location(

            ray_origins=ray_origins,
            ray_directions=ray_directions)

        # sorting the intersections based on the index of the rays to follow the order of the grid

        locations = np.array(locations)

        index_ray = np.array(index_ray)
        inds = index_ray.argsort()
        vtx_intersection = locations[inds]
        # print("this is the sorted list: " + str(sortedIntersections))
        print("Number of intersections: " + str(len(vtx_intersection)))
        # add a condition that verifies if the number of intersections is similar to the number of rays if not report an error

        # saving the intersections as "vtx_intersection.npy" file
        np.save(blender_file_path_input + '/vtx_intersection', vtx_intersection)

    else:
        print("mesh and data not found")
    return vtx_intersection

vtx_intersection = intersection_trimesh(data,blender_file_path)



"""# create some rays and find the intersection "rays - site"

ray_origins = np.array(data)
#print(ray_origins)
# ray_directions pointing down
ray_directions = np.array([[0, 0, -1]] * int(len(ray_origins)))

# run trimesh to find the intersection between the rays and site
locations, index_ray, index_tri = mesh.ray.intersects_location(

    ray_origins=ray_origins,
    ray_directions=ray_directions)

# sorting the intersections based on the index of the rays to follow the order of the grid

locations = np.array(locations)

index_ray = np.array(index_ray)
inds = index_ray.argsort()
vtx_intersection = locations[inds]
# print("this is the sorted list: " + str(sortedIntersections))
print("Number of intersections: " + str(len(vtx_intersection)))
# add a condition that verifies if the number of intersections is similar to the number of rays if not report an error


# saving the intersections as "vtx_intersection.npy" file
np.save(blender_file_path + '/vtx_intersection', vtx_intersection)"""

