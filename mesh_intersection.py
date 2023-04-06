#import mesh representing the site from blender
mesh = trimesh.load('/Users/arqfa/OneDrive/Desktop/Research/terrain.glb', force='mesh')

# create some rays and find the intersection "rays - site"
#load data from blender grid origin
data = np.load('/Users/arqfa/OneDrive/Desktop/Research/origin.npy')
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
sortedIntersections = locations[inds]
#print("this is the sorted list: " + str(sortedIntersections))
print("Number of intersections: " + str(len(sortedIntersections)))
# add a condition that verifies if the number of intersections is similar to the number of rays if not report an error


#saving the intersections as "intersection.npy" file
np.save('/Users/arqfa/OneDrive/Desktop/Research/intersection', sortedIntersections)