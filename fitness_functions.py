import math
import numpy as np
import random

K_FACTOR = 5  # Penalization value "k" applied during the activation formula
T0_INFLECTION_VALUE = 0.5  # inflection value "t0" applied during the activation formula. It must be from 0 to 1

WEIGHTS = [0.5, 0.3, 0.2]
NUMBER_SOLUTIONS_TO_PLOT = 5

# blender_file_path = "/Users/arqfa/OneDrive/Desktop/Research"
blender_file_path = "/Users/arqfa/OneDrive - Kyushu University/ResearchBigData/VR-research/BlenderFiles"

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

print(site_information)

top_grid_vtx = np.load(blender_file_path + '/top_grid_vtx.npy')
print("origin vertex loaded")

site_volumes = np.load(blender_file_path + '/site_volumes.npy')
print(f"For site volume the max value is {max(site_volumes)} and the min value is {min(site_volumes)}")

#print("there are " + str(len(site_volumes)) + " independent volumes on the grid of the site")
# print (volumes)
# site_trees = [0, 1, 0.5, 0, 0.25] * 1000
site_trees = np.load(blender_file_path + '/site_trees.npy')
print("tree information loaded")


# print(site_volumes)

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


available_positions = available_positions_function(top_grid_vtx, dx_rows, dy_cols, bx_rows, by_cols)
print("there are " + str(len(available_positions)) + " available positions on the grid")


# fitness functions


# f1 - Earthwork volumes calculations function
def f1_earthwork_vol_function(available_position_list, volume_list):
    positions = available_position_list
    volume = volume_list
    f1 = []

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

        rounded_vol_sum = round(vol_sum, 3)


        # Creation of the lists with the values per position for the fitness function prior to the normalization
        f1.append(rounded_vol_sum)

    print(f"the max value for f1 is {max(f1)} and the min value is {min(f1)}")

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

        costs_sum = ((math.fsum(partials_f2[0:int(j_max)])) + (bx_rows * by_cols * 2.5)) * int(unit_price)

        # Round the results to two decimals since they represent JPY currency.
        rounded_costs_sum = round(costs_sum, 2)

        # Creation of the lists with the values per position for the fitness function prior to the normalization
        f2.append(rounded_costs_sum)

    print("f2_earthwork_costs calculated")
    print(f"the max value for f2 is {max(f2)} and the min value is {min(f2)}")

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
        for j in range(int(j_max)):  # determine the number of rows to add up equivalent to the
            # number of rows of the building projection
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


    print("f3_deforestation_value calculated")
    print(f"the max value for f2 is {max(f3)} and the min value is {min(f3)}")

    return f3


f3_deforestation_value = f3_deforestation_function(available_positions, site_trees)


# Normalization of the results. This function was incorporated as part of the activation function

def normalization_of_functions(input_list):

    list_max = max(input_list)
    # list_min = 0  # optimizing for zero
    list_min = min(input_list)  # optimizing for the lowest value
    print(f"max original for {str(max(input_list))}")
    print(f"min original {str(min(input_list))}")
    normalized_result = []
    for value in input_list:
        normalization = (list_max - value) / (list_max - list_min)
        rounded_normalization = round(normalization, 3)
        normalized_result.append(rounded_normalization)
    # print("max normalized " + str(max(normalized_result)))
    return normalized_result


# f1_normalized = normalization_of_functions(f1_earthwork_vol)
# f2_normalized = normalization_of_functions(f2_earthwork_costs)
# f3_normalized = normalization_of_functions(f3_deforestation_value)

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
    #max_list = max(activated_list) # the highest value becomes the ideal scenario

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
original_values = list(zip(f1_earthwork_vol, f2_earthwork_costs, f3_deforestation_value))

# List with the normalized values
activated_values = list(zip(activated_f1, activated_f2, activated_f3))


# Review the combination of scores

# function to Calculate overall score

def temp_overall_score_function(activated_values_list, weights_input):
    # multiply the values per the weight_input, so they can be summed up, and we can obtain a overall score
    # This function can be replaced once the pareto optimization has been sorted since it will deliver this step

    overall_score = [round(sum(w * a for w, a in zip(weights_input, vals)), 3) for vals in activated_values_list]
    print("overall scores calculated")
    return overall_score


overall_score = temp_overall_score_function(activated_values, WEIGHTS)

# function to add


def scores_coordinates_sorting_function(number_of_solutions, activated_values_list, original_values_list,
                                        available_positions_list, vtx_coordinates_list, overall_score_list,
                                        level_for_implantation):
    # separate the values per function from activated_values_list using zip
    activated_f1, activated_f2, activated_f3 = zip(*activated_values_list)

    # separate the original values per function from the combined original_values_list using zip
    f1_values, f2_values, f3_values = zip(*original_values_list)

    # replace the height of the locations per level_for_implantation value
    for sublist in vtx_coordinates_list:
        sublist[2] = level_for_implantation

    available_coordinates = []
    for i in range(len(available_positions_list)):
        location = available_positions_list[i]

        coordinates = vtx_coordinates_list[int(location)]
        available_coordinates.append(coordinates)
    print(f'there are {str(len(available_coordinates))} available coordinates')

    scores = list(
        zip(available_positions_list, overall_score_list, activated_f1, activated_f2, activated_f3, f1_values,
            f2_values,
            f3_values, available_coordinates))
    print('Scores for the available positions calculated successfully')
    scores_sorted = sorted(scores, key=lambda x: x[1], reverse=True)
    print(f'{str(len(scores_sorted))} scores sorted successfully')

    scores_coordinates_sorted = []
    for tup in scores_sorted:
        tup_list = list(tup)
        for i, item in enumerate(tup_list):
            if isinstance(item, np.ndarray):
                tup_list[i] = item.tolist()
        scores_coordinates_sorted.append(tuple(tup_list))

    # preview of chosen candidates
    for i in range(int(number_of_solutions)):
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
        print("coordinates", candidate[8])

    # save
    scores_coordinates_sorted = np.array(scores_coordinates_sorted, dtype=object)
    np.savetxt(blender_file_path + '/scores_coordinates_sorted.txt', scores_coordinates_sorted, delimiter=',', fmt='%s')

    print("sorted score values successfully saved as scores_coordinates_sorted.txt ")

    # isolate the available coordinates from scores_coordinates_sorted
    coordinates_unity = [tup[8] for tup in scores_coordinates_sorted]
    # save the list of coordinates as coordinates_unity.txt
    np.savetxt(blender_file_path + '/coordinates_unity.txt', coordinates_unity, delimiter=',', fmt='%s')

    # Remove the available_coordinates from scores_coordinates_sorted
    scores_sorted_without_coordinates = [(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]) for tup in
                                         scores_coordinates_sorted]
    # Save the sorted scores without coordinates to a text file
    np.savetxt(blender_file_path + '/sorted_scores_unity.txt', scores_sorted_without_coordinates, delimiter=',',
               fmt='%s')

    return scores_coordinates_sorted


scores_coordinates_sorted = scores_coordinates_sorting_function(NUMBER_SOLUTIONS_TO_PLOT, activated_values,
                                                                original_values, available_positions, top_grid_vtx,
                                                                overall_score, z_level)

#np.save(blender_file_path + '/scores_coordinates_sorted.npy',
#        scores_coordinates_sorted)  # This file can be deleted once the data has been joined


