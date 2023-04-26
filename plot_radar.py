
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D

NUMBER_SOLUTIONS_TO_PLOT = 1

blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research"

scores_coordinates_sorted = np.load(blender_file_path + '/scores_coordinates_sorted.npy', allow_pickle=True)
print("sorted score values successfully loaded")

#Radar graph

def radar_plot (sorted_values_input, number_of_plotted_solutions):
    n = number_of_plotted_solutions
    available_positions, overall_score, activated_f1, activated_f2, activated_f3, f1_values, f2_values, f3_values, \
    available_coordinates = list(zip(*sorted_values_input))
    activated_functions = list(zip(activated_f1, activated_f2, activated_f3))
    categories = ['f1 Earthwork values', 'f2 earthwork costs', 'f3 deforestation values']
    fig = go.Figure()
    for i in range(n):
        fig.add_trace(go.Scatterpolar(
            r=activated_functions[i],
            theta=categories,
            fill='toself',
            name='Position' + str(available_positions[i])
        ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=False
    )

    fig.show()

    print ('Plot Successful')

slp_plot = radar_plot(scores_coordinates_sorted, NUMBER_SOLUTIONS_TO_PLOT)


#scatter graph

def scatter_graph_3D(sorted_values_input, number_of_plotted_solutions):
    n = number_of_plotted_solutions
    available_positions, overall_score, activated_f1, activated_f2, activated_f3, f1_values, f2_values, f3_values, \
    available_coordinates = list(zip(*sorted_values_input))
    categories = ['f1 Earthwork values', 'f2 earthwork costs', 'f3 deforestation values']

    # Assuming you have three lists of values representing the Pareto front for each fitness function
    x = activated_f1[:n]
    y = activated_f2[:n]
    z = activated_f3[:n]

    fig = plt.figure(figsize=(10, 6))  # Adjust figure size here
    ax = fig.add_subplot(projection='3d')

    ax.scatter(x, y, z)

    # Add labels for the axes
    ax.set_xlabel(categories[0])
    ax.set_ylabel(categories[1])
    ax.set_zlabel(categories[2])

    # Transpose the table data so that each list is a column
    table_data = list(zip(available_positions[:n], activated_f1[:n], activated_f2[:n], activated_f3[:n]))

    # Add table
    col_labels = ['Position', categories[0], categories[1], categories[2]]
    table = ax.table(cellText=table_data, colLabels=col_labels, loc='bottom')

    # Adjust table properties
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.5)

    plt.show()

    return

scatter_plot = scatter_graph_3D(scores_coordinates_sorted, NUMBER_SOLUTIONS_TO_PLOT)


