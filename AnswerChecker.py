import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D

NUMBER_SOLUTIONS_TO_PLOT = 5

#blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research"
blender_file_path = "/Users/arqfa/OneDrive - Kyushu University/ResearchBigData/VR-research/BlenderFiles"
site_data_path = "/Site1"
answer = 7
scores_coordinates_sorted = np.load(blender_file_path + site_data_path + '/scores_coordinates_sorted.npy', allow_pickle=True)
print("sorted score values successfully loaded")
print(scores_coordinates_sorted[(int(answer))-1])
