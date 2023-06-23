import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D

NUMBER_SOLUTIONS_TO_PLOT = 5

#blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research"
blender_file_path = "/Users/arqfa/OneDrive - Kyushu University/ResearchBigData/VR-research/BlenderFiles"
#site_data_path = "/Site"
#scores_coordinates_sorted = np.load(blender_file_path + site_data_path + '/scores_coordinates_sorted.npy', allow_pickle=True)
#print("sorted score values successfully loaded")


answer1 = [11, 8, 69, 15, 14, 43, 8, 8, 5, 1, 44, 20, 99, 8, 3, 75, 46]
answer2 = [6, 35, 6, 63, 3, 1, 1, 1, 82, 14, 6]
answer3 = [10, 1, 11, 38, 1, 83, 2, 3, 97, 20, 66]




def answer_checker(answer_input, site_data_path_input, blender_file_path_input):
    scores_coordinates_sorted = np.load(blender_file_path_input + site_data_path_input + '/scores_coordinates_sorted.npy',
                                        allow_pickle=True)
    print("Sorted score values successfully loaded")
    print(f"coordinates for {site_data_path_input}")
    for i in answer_input:
        if i <= len(scores_coordinates_sorted):

            print(scores_coordinates_sorted[i-1][8])
        else:
            print(f"Answer {i} is out of range.")

# Call the answer_checker function with the desired inputs
answer_checker(answer1, "/Site1", blender_file_path)
answer_checker(answer2, "/Site2", blender_file_path)
answer_checker(answer3, "/Site3", blender_file_path)



