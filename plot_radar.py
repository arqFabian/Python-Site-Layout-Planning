
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D


blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research"

available_positions = np.load(blender_file_path + '/available_positions.npy')
print("available positions successfully loaded")
score_values_sorted = np.load(blender_file_path + '/score_values_sorted.npy')  # This file can be deleted once the data has been joined
print("sorted score values successfully loaded")
def radar_plot (sorted_values_input, number_of_plotted_solutions):
    n = number_of_plotted_solutions
    position_id, scores, f1, f2, f3 = list(zip(*sorted_values_input))
    activated_functions = list(zip(f1,f2,f3))
    categories = ['f1 Earthwork values', 'f2 earthwork costs', 'f3 deforestation values']
    fig = go.Figure()
    for i in range(n):
        fig.add_trace(go.Scatterpolar(
            r=activated_functions[i],
            theta=categories,
            fill='toself',
            name='Position' + str(position_id[i])
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

"""categories = ['processing cost', 'mechanical properties', 'chemical stability',
              'thermal stability', 'device integration']

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=[1, 5, 2, 2, 3],
    theta=categories,
    fill='toself',
    name='Product A'
))
fig.add_trace(go.Scatterpolar(
    r=[4, 3, 2.5, 1, 2],
    theta=categories,
    fill='toself',
    name='Product B'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5]
        )),
    showlegend=False
)

fig.show()"""

number_solutions = 5

#slp_plot = radar_plot(score_values_sorted, number_solutions)





def scatter_graph_3D_1 (sorted_values_input, number_of_plotted_solutions):
    n = number_of_plotted_solutions
    position_id, scores, f1, f2, f3 = list(zip(*sorted_values_input))
    #categories = ['f1 Earthwork values', 'f2 earthwork costs', 'f3 deforestation values']


    # Assuming you have three lists of values representing the Pareto front for each fitness function
    x = f1[:n]
    y = f2[:n]
    z = f3[:n]

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(x, y, z)

    ax.set_xlabel('f1 Earthwork values')
    ax.set_ylabel('f2 earthwork costs')
    ax.set_zlabel('f3 deforestation values')

    plt.show()


def scatter_graph_3D_2(sorted_values_input, number_of_plotted_solutions):
    position_id, scores, f1, f2, f3 = list(zip(*sorted_values_input))
    categories = ['f1 Earthwork values', 'f2 earthwork costs', 'f3 deforestation values']

    # Assuming you have three lists of values representing the Pareto front for each fitness function
    x = f1
    y = f2
    z = f3

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    for i in range(number_of_plotted_solutions):
        ax.scatter(x[i], y[i], z[i], color='b')
        ax.text(x[i], y[i], z[i], position_id[i], color='r', fontsize=8)

    ax.set_xlabel('f1 Earthwork values')
    ax.set_ylabel('f2 earthwork costs')
    ax.set_zlabel('f3 deforestation values')

    plt.show()


def scatter_graph_3D_3(sorted_values_input, number_of_plotted_solutions):
    n = number_of_plotted_solutions
    position_id, scores, f1, f2, f3 = list(zip(*sorted_values_input))
    categories = ['f1 Earthwork values', 'f2 earthwork costs', 'f3 deforestation values']

    # Assuming you have three lists of values representing the Pareto front for each fitness function
    x = f1[:n]
    y = f2[:n]
    z = f3[:n]

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(x, y, z)

    # Add labels for the axes
    ax.set_xlabel(categories[0])
    ax.set_ylabel(categories[1])
    ax.set_zlabel(categories[2])

    # Add table
    table_data = [position_id, f1, f2, f3]
    col_labels = ['Position', categories[0], categories[1], categories[2]]
    table = ax.table(cellText=table_data, colLabels=col_labels, loc='bottom')

    # Adjust table properties
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.5)

    plt.show()

def scatter_graph_3D_4(sorted_values_input, number_of_plotted_solutions):
    n = number_of_plotted_solutions
    position_id, scores, f1, f2, f3 = list(zip(*sorted_values_input))
    categories = ['f1 Earthwork values', 'f2 earthwork costs', 'f3 deforestation values']

    # Assuming you have three lists of values representing the Pareto front for each fitness function
    x = f1[:n]
    y = f2[:n]
    z = f3[:n]

    print (x)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Add labels for the axes
    ax.set_xlabel(categories[0])
    ax.set_ylabel(categories[1])
    ax.set_zlabel(categories[2])

    # Add table
    table_data = [list(position_id)[:n], list(x), list(y), list(z)]
    col_labels = ['Position', categories[0], categories[1], categories[2]]
    table = ax.table(cellText=table_data, colLabels=col_labels, loc='bottom')

    # Adjust table properties
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.5)

    plt.show()

def scatter_graph_3D(sorted_values_input, number_of_plotted_solutions):
    n = number_of_plotted_solutions
    position_id, scores, f1, f2, f3 = list(zip(*sorted_values_input))
    categories = ['f1 Earthwork values', 'f2 earthwork costs', 'f3 deforestation values']

    # Assuming you have three lists of values representing the Pareto front for each fitness function
    x = f1[:n]
    y = f2[:n]
    z = f3[:n]

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter(x, y, z)

    # Add labels for the axes
    ax.set_xlabel(categories[0])
    ax.set_ylabel(categories[1])
    ax.set_zlabel(categories[2])

    # Transpose the table data so that each list is a column
    table_data = list(zip(position_id, f1, f2, f3))

    # Add table
    col_labels = ['Position', categories[0], categories[1], categories[2]]
    table = ax.table(cellText=table_data, colLabels=col_labels, loc='bottom')

    # Adjust table properties
    table.auto_set_font_size(False)
    table.set_fontsize(6)
    table.scale(1, 1.5)

    plt.show()

scatter_plot = scatter_graph_3D(score_values_sorted,number_solutions)

scatter_plot = scatter_graph_3D(score_values_sorted,number_solutions)

