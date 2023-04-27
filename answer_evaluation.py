import math
import numpy as np
import matplotlib.pyplot as plt
import random

blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research"

site_information = np.load(blender_file_path + '/site_information.npy')
print("site information loaded")
# D, dx_rows, dy_cols, bx_rows, by_cols, bz_height, z_level = site_information

D = int(site_information[0])
dx_rows = int(site_information[1])
dy_cols = int(site_information[2])
bx_rows = int(site_information[3])
by_cols = int(site_information[4])
bz_height = int(site_information[5])
z_level = int(site_information[6])

blender_answer = [(-2, -3, 0), (-17, -5, 0), (2, 3, 4), (-5, 6, 7), (8, 9, 10), (-11, 12, 13)]
vr_answer = [(-1, 25, 0), (3, 20, 0), (4, 15, 0), (5, 10, 0), (10, -6, 8), (5, -10, 0)]

recommended_answer = (0, 18, 0)

answers = list(zip(blender_answer, vr_answer))


# function to calculate the difference on the distance between answers in relation to the recommended answer

def accuracy_function(answer_input, recommended_answer_input):
    blender, unity = list(zip(*answer_input))
    x2, y2, z2 = recommended_answer_input

    distance_blender = []
    distance_unity = []
    for i in blender:
        # define the coordinates of the two points
        x1, y1, z1 = i

        # calculate the distance using the distance formula
        distance = round((math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)), 3)
        distance_blender.append(distance)
    print(distance_blender)
    for i in unity:
        x1, y1, z1 = i

        # calculate the distance using the distance formula
        distance = round((math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)), 3)
        distance_unity.append(distance)
    print(distance_unity)

    accuracy_improvement = []
    for i in range(len(distance_blender)):
        improvement = round((float(distance_blender[i]) - float(distance_unity[i])) * 100 / float(distance_blender[i]),
                            3)
        accuracy_improvement.append(improvement)

    return accuracy_improvement


print(accuracy_function(answers, recommended_answer))


# function to plot the accuracy graph

def accuracy_graph(answer_input, recommended_answer_input):
    title = "Accuracy Graph"

    # Define the center point
    center_point = [(x_center, y_center) for x_center, y_center, z_center in [recommended_answer_input]][0]

    # Define the concentric circles
    circles = [5, 10, 15, 20, 25, 30]

    # Define the points from blender and unity answers
    blender_answers, unity_answers = list(zip(*answer_input))

    # Extract only the x and y coordinates from the blender and unity answers
    blender_points = [(x, y) for x, y, z in blender_answers]
    unity_points = [(x, y) for x, y, z in unity_answers]

    # Create the figure and axis objects
    # Create the figure and axis objects
    fig, ax = plt.subplots()

    # Plot the concentric circles
    for radius in circles:
        circle = plt.Circle(center_point, radius, fill=False)
        ax.add_artist(circle)

    # Plot the points from blender and unity answers and add labels
    for i, point in enumerate(blender_points):
        ax.scatter(*point, color='orange', label='Blender Answers' if i == 0 else None)
        ax.annotate('b' + str(i), xy=point, xytext=(3, 3), textcoords='offset points')

    for i, point in enumerate(unity_points):
        ax.scatter(*point, color='blue', label='Unity Answers' if i == 0 else None)
        ax.annotate('a' + str(i), xy=point, xytext=(3, 3), textcoords='offset points')

    # Plot the center point
    ax.scatter(*center_point, color='red', label='Recommended Position')

    # Set the axis limits and labels
    ax.set_xlim(center_point[0] - max(circles), center_point[0] + max(circles))
    ax.set_ylim(center_point[1] - max(circles), center_point[1] + max(circles))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    # Add the legend
    ax.legend()

    # Add the title
    ax.set_title(title)

    # Show the plot
    plt.show()

    return


accuracy_graph(answers, recommended_answer)
