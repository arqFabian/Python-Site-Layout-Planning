import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnchoredOffsetbox, AuxTransformBox, TextArea, VPacker, AnnotationBbox
from matplotlib.patheffects import withStroke


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

participant = [1, 2, 3, 4, 5, 6, 7]
blender_answer = [(61, -16, 0), (-21, 11, 0), (62, 28, 0), (9, 21, 0), (10, 21, 0), (58, -2, 0), (-28, -7, 0), (-24, -14, 0), (9,24,0), (28, -27, 0)]
vr_answer = [(6, -45, 0), (31, 20, 0), (36, -15, 0), (36, -13, 0), (34, -36, 0), (6, -44, 0), (31, 20, 0), (31, 20, 0), (9,1,0), (35,-35,0)]

recommended_answer = (35, -35, 0)

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


accuracy_percentage_improvement = accuracy_function(answers, recommended_answer)
print(accuracy_percentage_improvement)


# function to plot the accuracy graph

def accuracy_graph(answer_input, recommended_answer_input):
    title = "Accuracy Graph"

    # Define the center point
    center_point = [(x_center, y_center) for x_center, y_center, z_center in [recommended_answer_input]][0]

    # Define the concentric circles
    circles = list(range(10, 91, 10))

    # Define the points from blender and unity answers
    blender_answers, unity_answers = list(zip(*answer_input))

    # Extract only the x and y coordinates from the blender and unity answers
    blender_points = [(x, y) for x, y, z in blender_answers]
    unity_points = [(x, y) for x, y, z in unity_answers]

    # Create the figure and axis objects
    fig, ax = plt.subplots()

    # Set the aspect ratio to be equal
    ax.set_aspect('equal')

    # Plot the concentric circles with custom colors and radius annotations
    for i, radius in enumerate(circles):

        circle = plt.Circle(center_point, radius, fill=False, color="gray")
        ax.add_artist(circle)
        if i % 2 == 0:  # Skip adding annotation for even index circles
            continue
        # Calculate the coordinates for the annotation
        annotation_x = center_point[0] + radius * 0.8  # Adjust the factor (0.9) as needed
        annotation_y = center_point[1] - radius * 0.65  # Adjust the factor (0.9) as needed
        # Add radius annotation
        ax.text(annotation_x, annotation_y, f'{radius} m', ha='center', va='center', color="gray", fontsize=8)

    # Plot the points from blender and unity answers and add labels
    for i, point in enumerate(blender_points):
        ax.scatter(*point, color='orange', label='Blender Answers' if i == 0 else None, edgecolors='white',
                   linewidths=1)
        ax.annotate('b' + str(i), xy=point, xytext=(2, 2), textcoords='offset points', color='darkgray')

    for i, point in enumerate(unity_points):
        ax.scatter(*point, color='blue', label='VR - Unity Answers' if i == 0 else None, edgecolors='white',
                   linewidths=1)
        ax.annotate('a' + str(i), xy=point, xytext=(2, 2), textcoords='offset points', color='darkgray')


    # Plot the center point as a red cross
    ax.scatter(center_point[0], center_point[1], color='red', marker='x', label='Recommended Position')

    # Set the axis limits and labels
    ax.set_xlim(center_point[0] - max(circles), center_point[0] + max(circles))
    ax.set_ylim(center_point[1] - max(circles), center_point[1] + max(circles))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    # Hide the axis
    #ax.axis('off')

    # Add the legend
    ax.legend(loc='lower left')

    # Add the title
    ax.set_title(title)

    # Add the graphic scale
    scale_length_meters = 50
    xlim = ax.get_xlim()
    scale_length_plot = scale_length_meters
    scale_bar = AuxTransformBox(ax.transData)
    scale_bar.add_artist(plt.Line2D([0, scale_length_plot], [0, 0], color='black', lw=2))
    scale_label = TextArea(f'{scale_length_meters} m', textprops={'color': 'black', 'fontsize': 10})
    scale_anchored_box = AnchoredOffsetbox(loc='lower right', child=VPacker(children=[scale_bar, scale_label]),
                                           pad=0.1, frameon=False, bbox_to_anchor=(1, 0), bbox_transform=ax.transAxes,
                                           borderpad=0.)

    ax.add_artist(scale_anchored_box)

    # Remove the axis
    ax.axis('off')

    # Show the plot
    plt.show()

    return


accuracy_graph(answers, recommended_answer)


def accuracy_bar_chart(available_position_list, y_original_value, y_label, number_of_plotted_solutions):
    # Create a new figure for the column graph
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the column graph for costs
    positions = [i + 1 for i in range(number_of_plotted_solutions)]
    y_values = y_original_value[:number_of_plotted_solutions]
    # ax.bar(positions, y_values)

    # Generate a list of colors for each bar
    num_bars = len(y_values)
    # colors = plt.cm.Set2(np.arange(num_bars))
    colors = plt.cm.Blues(np.linspace(1, 0.2, num_bars))

    ax.bar(positions, y_values, color=colors)

    for i in range(len(positions)):
        ax.text(positions[i], y_values[i] + 0.5, 'P. ' + str(available_position_list[i]), ha='center')

    # Add labels for the axes
    ax.set_xlabel('Ranking')
    ax.set_ylabel(str(y_label))
    ax.set_title(str(y_label) + ' vs Ranking of Position')

    # Add trend line
    z = np.polyfit(positions, y_values, 1)
    p = np.poly1d(z)
    ax.plot(positions, p(positions), "r--")

    # Plot the line graph for y values
    ax.plot(positions, y_values, '-o', label='Y values trend')

    # Add a legend to the graph
    ax.legend()

    return



