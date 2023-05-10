"""

print(f"Candidate {i + 1}:")
candidate = scores_coordinates_sorted[i]
print("Position: ", candidate[0])
print("Overall Score: ", candidate[1])
print("function 1: ", candidate[2])
print("function 2: ", candidate[3])
print("function 3: ", candidate[4])
print("value f1: ", candidate[5])
print("value f2: ", candidate[6])
print("value f3: ", candidate[7])
print("coordinates", candidate[8])"""

import numpy as np

#blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research"
#scores_coordinates_sorted = np.loadtxt(blender_file_path + '/scores_coordinates_sorted.txt')
#print(f"coordinates {str(scores_coordinates_sorted[0])}")

import os

blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research"
file_path = os.path.join(blender_file_path, 'scores_coordinates_sorted.txt')

if os.path.isfile(file_path):
    scores_coordinates_sorted = np.loadtxt(file_path, delimiter=',')
    print(f"coordinates: {str(scores_coordinates_sorted[0][2])}")
else:
    print(f"File '{file_path}' does not exist.")




