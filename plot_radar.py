import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D

NUMBER_SOLUTIONS_TO_PLOT = 10

blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research"

scores_coordinates_sorted = np.load(blender_file_path + '/scores_coordinates_sorted.npy', allow_pickle=True)
print("sorted score values successfully loaded")


# Radar graph

def radar_plot(sorted_values_input, number_of_plotted_solutions):
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

    print('Plot Successful')

    return

slp_plot = radar_plot(scores_coordinates_sorted, NUMBER_SOLUTIONS_TO_PLOT)


def radar_plot_single(sorted_values_input):
    available_positions, overall_score, activated_f1, activated_f2, activated_f3, f1_values, f2_values, f3_values, \
    available_coordinates = list(zip(*sorted_values_input))
    activated_functions = list(zip(activated_f1, activated_f2, activated_f3))
    categories = ['f1 Earthwork values', 'f2 earthwork costs', 'f3 deforestation values']
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=activated_functions[0],
        theta=categories,
        fill='toself',
        name='Position' + str(available_positions[0])
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

    print('Plot Successful')

    return


#radar_plot_single(scores_coordinates_sorted[0],1)
#for i in range(int(NUMBER_SOLUTIONS_TO_PLOT)):
    #scores = scores_coordinates_sorted[i]
   # print (scores)
    #n = 1
    #radar_plot(scores)



# column graph
# This function only works from inside scatter graph

def column_graph_plot(available_position_list, y_original_value, y_label, number_of_plotted_solutions):
    # Create a new figure for the column graph
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the column graph for costs
    positions = [i + 1 for i in range(number_of_plotted_solutions)]
    y_values = y_original_value[:number_of_plotted_solutions]
    #ax.bar(positions, y_values)

    # Generate a list of colors for each bar
    num_bars = len(y_values)
    #colors = plt.cm.Set2(np.arange(num_bars))
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


# scatter graph

def scatter_graph_3D(sorted_values_input, number_of_plotted_solutions):
    n = number_of_plotted_solutions
    available_positions, overall_score, activated_f1, activated_f2, activated_f3, f1_values, f2_values, f3_values, \
    available_coordinates = list(zip(*sorted_values_input))
    categories = ['Score', 'f1 Earthwork values', 'f2 earthwork costs', 'f3 deforestation values']

    # Assuming you have three lists of values representing the Pareto front for each fitness function
    x = activated_f1[:n]
    y = activated_f2[:n]
    z = activated_f3[:n]

    # Create column graphs
    column_graph_plot(available_positions, f1_values, str(categories[1]), n)  # Earthwork volume column graph
    column_graph_plot(available_positions, f2_values, str(categories[2]), n)  # Earthwork cost column graph
    column_graph_plot(available_positions, f3_values, str(categories[3]), n)  # Deforestation value column graph

    # Create the scatter plot figure
    fig = plt.figure(figsize=(14, 9))  # Adjust figure size here
    gs = fig.add_gridspec(nrows=1, ncols=2, width_ratios=[1, 1])

    ax = fig.add_subplot(gs[0, 0], projection='3d')
    ax.scatter(x, y, z)

    # Add labels for the axes
    ax.set_xlabel(categories[1])
    ax.set_ylabel(categories[2])
    ax.set_zlabel(categories[3])

    # Add labels for each dot
    for i in range(n):
        ax.text(x[i], y[i], z[i], 'P. ' + str(available_positions[i]))

    # Transpose the table data so that each list is a column
    table_data = list(
        zip(available_positions[:n], overall_score[:n], activated_f1[:n], activated_f2[:n], activated_f3[:n]))

    # Add table
    col_labels = ['Position', categories[0], categories[1], categories[2], categories[3]]
    table = fig.add_subplot(gs[0, 1]).table(cellText=table_data, colLabels=col_labels, loc='center')

    # Adjust table properties
    table.auto_set_font_size(False)
    table.set_fontsize(8)

    # Adjust subplot parameters to fit the graph and the table
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.3)

    plt.show()

    return


scatter_plot = scatter_graph_3D(scores_coordinates_sorted, NUMBER_SOLUTIONS_TO_PLOT)
