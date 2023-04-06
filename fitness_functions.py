import math
import numpy as np

# verts = np.load('/Users/arqfa/OneDrive/Desktop/Research/site_volumes.npy')
verts = list(range(500))  # Dummy list to test the tracking of avalibale positions.
# verts = list(string.ascii_lowercase)
# print (verts)

dx_rows = 8
dy_cols = 4
bx_rows = 2
by_cols = 2
D = 1  # module size


def available_positions_function(list_of_vertex, distance_x, distance_y, building_x, building_y):
    dx = distance_x
    dy = distance_y
    bx = building_x
    by = building_y
    available_positions_on_site = []
    for i in range((dy - by + 1)): # i -> is the number of rows on the site
        j_min = (by * dx / 2) + bx + (dx + bx / 2) * i
        j_max = j_min + dx - bx
        for j in range(int(j_min), int(j_max) + 1):
            x = verts[j]
            available_positions_on_site.append(x)
    print("Available positions calculated.")
    return available_positions_on_site


available_positions = available_positions_function(verts, dx_rows, dy_cols, bx_rows, by_cols)
print("there are " + str(len(available_positions)) + " available positions on the grid")

"""
Dummy lists
This lists need to be replaced with their equivalent from the actual data.
Specifically "Volumes" and "Trees"
"""

volumes = np.load('/Users/arqfa/OneDrive/Desktop/Research/site_volumes.npy')
# volumes =list(range(-10,200)) #substitute this volume list for the actual calculations
# volumes = [-1]*8+[2]*8+[-3]*8+[-4]*8
Trees = [0, 1, 0.5, 0, 0.25] * 8
print(("there are ") + str(len(volumes)) + (" independent volumes on the grid of the site"))
# print (volumes)

""""""
# fitness functions
""""""
# f1 - Earthwork volumes calculations
f1_earthwork_vol = []

for i in range(len(available_positions)):  # determine the number of available position to calculate f1
    max_j = (by_cols / D)
    partials_f1 = []
    for j in range(
            int(max_j)):  # determine the number of rows to add up equivalent to the number of rows of the building projection
        # determines the partial intervals of sums that add up to the building projection
        min_k = j * (dx_rows / D) + i
        max_k = min_k + (bx_rows / D)

        # F1 - Earthwork volumes
        function1 = (math.fsum(volumes[int(min_k):int(max_k)]))  # Formula for fitness function f1_earthwork_volumes
        partials_f1.append(function1)

    """
    #optional checkpoint of the iterations
    print("the partials for f1, f2, f3 respectively are: ")
    print(partials_f1)
    """

    # Formula to sum the partials representing the sum of the values per row under the building projection
    y = abs(math.fsum(partials_f1[0:int(max_j)]))

    # Creation of the lists with the values per position for the fitness function prior to the normalization
    f1_earthwork_vol.append(y)
# print(("These are the results for the ") + (str(len(f1_earthwork_vol))) +(" possible positions"))
# print("For f1-earthwork volumes: ")
# print(f1_earthwork_vol)
""""""
# f2 - Earthwork costs calculations
""""""
Unit_price = 660
f2_earthwork_costs = []

for i in range(len(available_positions)):  # determine the number of available position to calculate f1
    max_j = (by_cols / D)
    partials_f2 = []
    for j in range(
            int(max_j)):  # determine the number of rows to add up equivalent to the number of rows of the building projection
        # determines the partial intervals of sums that add up to the building projection
        min_k = j * (dx_rows / D) + i
        max_k = min_k + (bx_rows / D)

        # F2 - Earthwork Costs
        function2 = abs(math.fsum(volumes[int(min_k):int(max_k)]))
        partials_f2.append(function2)
    """
    #optional checkpoint of the iterations
    print("the partials for f2 respectively are: ")
    print(partials_f2)
    """

    # Formula to sum the partials representing the sum of the values per row under the building projection

    y = (math.fsum(partials_f2[0:int(max_j)])) * int(Unit_price)

    # Creation of the lists with the values per position for the fitness function prior to the normalization
    f2_earthwork_costs.append(y)
# print(("These are the results for the ") + (str(len(f1_earthwork_vol))) +(" possible positions"))
# print("For f2-earthwork costs: ")
# print(f2_earthwork_costs)
""""""
# f3 - Deforestation Value calculations
""""""
f3_deforestation_value = []

for i in range(len(available_positions)):  # determine the number of available position to calculate f1
    max_j = (by_cols / D)

    partials_f3 = []
    for j in range(
            int(max_j)):  # determine the number of rows to add up equivalent to the number of rows of the building projection
        # determines the partial intervals of sums that add up to the building projection
        min_k = j * (dx_rows / D) + i
        max_k = min_k + (bx_rows / D)

        # F3 - Deforestation Value
        function3 = math.fsum(Trees[int(min_k):int(max_k)])
        partials_f3.append(function3)

    """
    #optional checkpoint of the iterations
    print("the partials f3 respectively are: ")
    print(partials_f3)
    """

    # Formula to sum the partials representing the sum of the values per row under the building projection
    y = (math.fsum(partials_f3[0:int(max_j)]))

    # Creation of the lists with the values per position for the fitness function prior to the normalization
    f3_deforestation_value.append(y)
# print(("These are the results for the ") + (str(len(f1_earthwork_vol))) +(" possible positions"))
# print("For f3-deforestation value: ")
# print(f3_deforestation_value)

"""print("These are the results for the " + (str(len(f1_earthwork_vol))) + " possible positions")
print("For f1-earthwork volumes: ")
print(f1_earthwork_vol)
print("For f2-earthwork costs: ")
print(f2_earthwork_costs)
print("For f3-deforestation value: ")
print(f3_deforestation_value)"""

""""""
# Normalization of the results
""""""


# N1 - Normalization of the resulst for f1 - earthwork volume calculations
def normalization_of_functions(input_list):
    max_list = max(input_list)
    min_list = 0
    normalization = [(value - max_list) / (min_list - max_list) for value in input_list]
    return normalization


n1_normalize_f1 = normalization_of_functions(f1_earthwork_vol)
n2_normalize_f2 = normalization_of_functions(f2_earthwork_costs)
n3_normalize_f3 = normalization_of_functions(f3_deforestation_value)

print("The following are the scores for the " + (str(len(f1_earthwork_vol))) + " possible positions.")
print("For the normalized f1-earthwork volumes: ")
print(n1_normalize_f1)
print("For the normalized f2-earthwork costs: ")
print(n2_normalize_f2)
print("For the normalized f3-deforestation values: ")
print(n3_normalize_f3)

""""""
# Activation Function + final normalization
""""""


def activation_function(input_value, k, t0):
    return 1 / (1 + math.exp(-k * (input_value - t0)))


def normalized_activation_function(activation_list):
    max_list = 1  # This value is the ideal scenario
    min_list = min(activation_list)
    normalized_list = [(value - min_list) / (max_list - min_list) for value in activation_list]
    return normalized_list


# Activation for normalized n1_normalized_f1
k_penalization_factor = 10
t0_inflection_point = 0.5

activation_n1 = [activation_function(value, k_penalization_factor, t0_inflection_point) for value in n1_normalize_f1]
activation_n2 = [activation_function(value, k_penalization_factor, t0_inflection_point) for value in n2_normalize_f2]
activation_n3 = [activation_function(value, k_penalization_factor, t0_inflection_point) for value in n3_normalize_f3]

normalized_activation_n1 = normalized_activation_function(activation_n1)
normalized_activation_n2 = normalized_activation_function(activation_n2)
normalized_activation_n3 = normalized_activation_function(activation_n3)

print("The following are the scores  after applying the activation function for the " + (
    str(len(f1_earthwork_vol))) + "possible positions.")
print("For the normalized f1-earthwork volumes: ")
# print(activation_n1)
print(normalized_activation_n1)
print("For the normalized f2-earthwork scores: ")
# print(activation_n2)
print(normalized_activation_n2)
print("For the normalized f3-deforestation values: ")
# print(activation_n3)
print(normalized_activation_n3)

""""""


# Selection of top three recomendations

# This section combines the results of the three functions as sublists of a master List that can later be tabulated


def create_nested_list(*lists):
    nested_list = []
    for i in range(len(lists[0])):
        inner_list = []
        for j in range(len(lists)):
            inner_list.append(lists[j][i])
        nested_list.append(inner_list)
    return nested_list


# list with the original values
original_values = create_nested_list(available_positions, f1_earthwork_vol, f2_earthwork_costs, f3_deforestation_value)
# List with the normalized values
normalized_values = create_nested_list(normalized_activation_n1, normalized_activation_n2, normalized_activation_n3)
"""
def sum_of_values (input_list):
    sum = math.fsum(input_list)
    return sum

scores = sum_of_values(normalized_values)
"""
l = []
for i in range(len(normalized_values)):
    j = normalized_values[i]
    k = math.fsum(j)
    l.append(k)

scores_position = create_nested_list(available_positions, l)

print("######################################")
print(
    "List with all the original values per position is as follows with the first value being the vertex id, followed by the results of f1, f2, f3 respectively:")
print(original_values)
print("######################################")
print(
    "List with all the normalized values per position is as follows with the first value being the vertex id, followed by the normalized activation of f1, f2, f3 respectively:")
print(normalized_values)
print("######################################")
print(scores_position)
print("######################################")
# print(scores)

np.save('/Users/arqfa/OneDrive/Desktop/Research/normalized_values',
        normalized_values)  # This file can be deleted once the data has been joined
print("normalized values successfully saved")
np.save('/Users/arqfa/OneDrive/Desktop/Research/available_positions',
        available_positions)  # This file can be deleted once the data has been joined
print("available positions values successfully saved")