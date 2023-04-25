import math
import numpy as np


"""dx_rows = 20
dy_cols = 20
bx_rows = 4
by_cols = 4
D = 1  # module size"""
K_FACTOR = 10 # Penalization value "k" applied during the activation formula
T0_INFLECTION_VALUE = 0.5 # inflection value "t0" applied during the activation formula. It must be from 0 to 1

WEIGHTS = [0.5, 0.3, 0.2]
NUMBER_SOLUTIONS_TO_PLOT = 2

blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research"

vtx_origin = np.load(blender_file_path + '/top_grid_vtx.npy')
print("origin vertex loaded")

site_volumes = np.load(blender_file_path + '/site_volumes.npy')

site_information = np.load(blender_file_path + '/site_information.npy')
D, dx_rows, dy_cols, bx_rows, by_cols, bz_height, z_level = zip(*site_information)

# volumes =list(range(-10,200)) #substitute this volume list for the actual calculations
# volumes = [-1]*8+[2]*8+[-3]*8+[-4]*8
site_trees = [0, 1, 0.5, 0, 0.25] * 100
print("there are " + str(len(site_volumes)) + " independent volumes on the grid of the site")
# print (volumes)

print(site_volumes)

def available_positions_function(list_of_vertex, distance_x, distance_y, building_x, building_y):
    # verts = list_of_vertex
    verts = list(range(len(list_of_vertex)))
    dx = distance_x
    dy = distance_y
    bx = building_x
    by = building_y
    available_positions_on_site = []
    for i in range((dy - by + 1)):  # i -> is the number of rows on the site
        j_min = (by * dx / 2) + bx + (dx + bx / 2) * i
        j_max = j_min + dx - bx
        for j in range(int(j_min), int(j_max) + 1):
            x = verts[j]
            available_positions_on_site.append(x)
    print("Available positions calculated.")
    return available_positions_on_site


available_positions = available_positions_function(vtx_origin, dx_rows, dy_cols, bx_rows, by_cols)
print("there are " + str(len(available_positions)) + " available positions on the grid")

"""
Dummy lists
This lists need to be replaced with their equivalent from the actual data.
Specifically "Volumes" and "Trees"
"""


# fitness functions


# f1 - Earthwork volumes calculations function
def f1_earthwork_vol_function(available_position_list, volume_list):
    positions = available_position_list
    volume = volume_list
    f1 = []
    ##f1_2 = []

    for i in range(len(positions)):  # determine the number of available position to calculate f1
        j_max = (by_cols / D)
        partials_f1 = []
        for j in range(
                int(j_max)):  # determine the number of rows to add up equivalent to the number of rows of the building projection
            # determines the partial intervals of sums that add up to the building projection
            k_min = j * (dx_rows / D) + i
            k_max = k_min + (bx_rows / D)

            # F1 - Earthwork volumes
            function1 = (math.fsum(volume[int(k_min):int(k_max)]))  # Formula for fitness function f1_earthwork_volumes
            partials_f1.append(function1)

        # Formula to sum the partials representing the sum of the values per row under the building projection
        vol_sum = abs(math.fsum(partials_f1[0:int(j_max)]))
        ##vol_sum2 = math.fsum(partials_f1[0:int(j_max)])



        rounded_vol_sum = round(vol_sum, 3)
        ##rounded_vol_sum2 = round(vol_sum2,3)

        # Creation of the lists with the values per position for the fitness function prior to the normalization
        f1.append(rounded_vol_sum)
        ##f1_2.append(rounded_vol_sum2)

    ##print(f1)
    ##print(f1_2)

    return f1


f1_earthwork_vol = f1_earthwork_vol_function(available_positions, site_volumes)


# print("These are the results for the " + (str(len(f1_earthwork_vol))) + " possible positions")
# print("For f1-earthwork volumes (m3): ")
# print(f1_earthwork_vol[:5])


# f2 - Earthwork costs calculations

def f2_earthwork_costs_function(available_position_list, volume_list):
    positions = available_position_list
    volume = volume_list
    unit_price = 660  # official cost in JPY for earthwork in JAPAN for 2022 in Fukuoka
    f2 = []
    for i in range(len(positions)):  # determine the number of available position to calculate f1
        j_max = (by_cols / D)
        partials_f2 = []
        for j in range(
                int(j_max)):  # determine the number of rows to add up equivalent to the number of rows of the building projection
            # determines the partial intervals of sums that add up to the building projection
            k_min = j * (dx_rows / D) + i
            k_max = k_min + (bx_rows / D)

            # F2 - Earthwork Costs
            function2 = abs(math.fsum(volume[int(k_min):int(k_max)]))
            partials_f2.append(function2)

        # Formula to sum the partials representing the sum of the values per row under the building projection

        costs_sum = (math.fsum(partials_f2[0:int(j_max)])) * int(unit_price)

        # Round the results to two decimals since they represent JPY currency.
        rounded_costs_sum = round(costs_sum, 2)

        # Creation of the lists with the values per position for the fitness function prior to the normalization
        f2.append(rounded_costs_sum)

    ## print("These are the results for the " + (str(len(available_positions))) + " possible positions")
    ## print("For f2-earthwork costs: ")
    ## print(f2_earthwork_costs)

    return f2


f2_earthwork_costs = f2_earthwork_costs_function(available_positions, site_volumes)


# f3 - Deforestation Value calculations

def f3_deforestation_function(available_position_list, tree_list):
    positions = available_position_list
    tree = tree_list
    f3 = []

    for i in range(len(positions)):  # determine the number of available position to calculate f1
        j_max = (by_cols / D)

        f3_partials = []
        for j in range(
                int(j_max)):  # determine the number of rows to add up equivalent to the number of rows of the building projection
            # determines the partial intervals of sums that add up to the building projection
            k_min = j * (dx_rows / D) + i
            k_max = k_min + (bx_rows / D)

            # F3 - Deforestation Value
            function3 = math.fsum(tree[int(k_min):int(k_max)])
            f3_partials.append(function3)

        # Formula to sum the partials representing the sum of the values per row under the building projection
        tree_sum = (math.fsum(f3_partials[0:int(j_max)]))

        # Creation of the lists with the values per position for the fitness function prior to the normalization
        f3.append(tree_sum)

    # print("These are the results for the " + (str(len(available_positions))) + " possible positions")
    # print("For f3-deforestation value: ")
    # print(f3_deforestation_value)

    return f3


f3_deforestation_value = f3_deforestation_function(available_positions, site_trees)


# Normalization of the results. This function was incorporated as part of the activation function

def normalization_of_functions(input_list):
    n_list = input_list  # List to normalize
    list_max = max(n_list)
    print("max original " + str(max(n_list)))
    list_min = 0  # optimizing for zero
    #list_min = min(n_list) # optimizing for the lowest value
    normalized_result = []
    for value in n_list:
        normalization = (list_max - value) / (list_max - list_min)
        rounded_normalization = round(normalization, 3)
        normalized_result.append(rounded_normalization)
    # print("max normalized " + str(max(normalized_result)))
    return normalized_result


f1_normalized = normalization_of_functions(f1_earthwork_vol)
f2_normalized = normalization_of_functions(f2_earthwork_costs)
f3_normalized = normalization_of_functions(f3_deforestation_value)

# Activation Function + final normalization

def activation_function(input_list, k_penalization_factor, t0_inflection_point):
    # Normalization of function, optimizing for zero
    normalized_list = normalization_of_functions(input_list)

    # Application of activation function on normalized list
    k_value = k_penalization_factor  # numerical value representing penalization
    t0_point = t0_inflection_point  # number representing the inflection or tolerance of the sigmoid curve

    activated_list = [1 / (1 + math.exp(-k_value * (value - t0_point))) for value in normalized_list]

    # Once again normalization of activated list because of numerical shift due to k and t0 values.
    min_list = min(activated_list)
    max_list = 1  # This value is the ideal scenario
    #max_list = max(activated_list) #the highest value becomes the ideal scenario
    normalized_activated_list = [(value - min_list) / (max_list - min_list) for value in activated_list]
    normalized_activated_list = [round(value, 3) for value in normalized_activated_list]
    print("max activated " + str(max(normalized_activated_list)))
    return normalized_activated_list


# Activation for normalized n1_normalized_f1


activated_f1 = activation_function(f1_earthwork_vol, K_FACTOR, T0_INFLECTION_VALUE)
activated_f2 = activation_function(f2_earthwork_costs, K_FACTOR, T0_INFLECTION_VALUE)
activated_f3 = activation_function(f3_deforestation_value, K_FACTOR, T0_INFLECTION_VALUE)


# Selection of top three recommendations

# This section combines the results of the three functions as sublist of a master List that can later be tabulated


# list with the original values
original_values = list(zip(available_positions, f1_earthwork_vol, f2_earthwork_costs, f3_deforestation_value))

# List with the normalized values
activated_values = list(zip(activated_f1, activated_f2, activated_f3))

# Review the combination of scores


def temp_optimization_sorting(number_of_solutions, activated_values_list, available_positions_list, weights_input):

    optimization_list = [round(sum(w*a for w, a in zip(weights_input, vals)), 3) for vals in activated_values_list]
    f1, f2, f3 = zip(*activated_values_list)
    scores = list(zip(available_positions_list, optimization_list, f1, f2, f3))
    print('Scores for the available positions calculated successfully')
    scores_sorted = sorted(scores, key=lambda x: x[1], reverse=True)
    print('scores sorted successfully')

    for i in range(int(number_of_solutions)):
        print(f"Candidate {i + 1}:")
        candidate = scores_sorted[i]
        print("Position: ", candidate[0])
        print("Score: ", candidate[1])
        print("function 1: ", candidate[2])
        print("function 2: ", candidate[3])
        print("function 3: ", candidate[4])

    return scores_sorted, scores


score_values_sorted, score_values = temp_optimization_sorting(NUMBER_SOLUTIONS_TO_PLOT, activated_values, available_positions, WEIGHTS)
print("candidates sorted")

np.save(blender_file_path + '/score_values',
        score_values)  # This file can be deleted once the data has been joined
print("score values successfully saved")
np.save(blender_file_path + '/score_values_sorted',
        score_values_sorted)  # This file can be deleted once the data has been joined
print("sorted score values successfully saved")

#table_list = create_nested_list(score_values_list, activated_f1, activated_f2, activated_f3)
#print(table_list[2])


