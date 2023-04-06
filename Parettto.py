"""
import numpy as np
from scipy.optimize import minimize

def pareto_optimization(objective_functions, bounds, weights):
    def objective(x):
        return np.sum([w * f(x) for w, f in zip(weights, objective_functions)], axis=0)

    def constraint(x):
        return np.sum(x) - 1.0

    initial_guess = np.random.uniform(bounds[:, 0], bounds[:, 1])
    result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints={'type': 'eq', 'fun': constraint})

    return result.x, result.fun

# Example usage:
def f1(x):
    return x[0]**2

def f2(x):
    return (x[0]-2)**2

def f3(x):
    return (x[0]+1)**2

bounds = np.array([[-5.0, 5.0]])

# Define the weights for the objective functions
weights = [5.0, 1.0, 2.0]

x, f = pareto_optimization([f1, f2, f3], bounds, weights)

print("Optimal x: ", x)
print("Optimal objective values: ", f)
"""
import numpy as np
from scipy.optimize import minimize

def pareto_optimization(objective_functions, bounds, weights):
    def g1(x):
        return 1.0 - abs(f1(x))

    def g3(x):
        return 1.0 - abs(f3(x))

    def objective(x):
        s = s_func(g3(x))
        return weights[0] * g1(x) + weights[1] * f2(x) + weights[2] * s

    def constraint(x):
        return np.sum(x) - 1.0

    def s_func(x):
        return x + 100

    results = []
    for i in range(5):
        initial_guess = np.random.uniform(bounds[:, 0], bounds[:, 1])
        result = minimize(objective, initial_guess, method='SLSQP', bounds=bounds, constraints={'type': 'eq', 'fun': constraint})
        results.append(result.x)

    return results

# Example usage:
def f1(x):
    return x[0] - 1

def f2(x):
    return x[0]**2

def f3(x):
    return -x[0] - 1

bounds = np.array([[-5.0, 5.0]])

# Define the weights for the objective functions
weights = [1.0, 3.0, 1.0]

results = pareto_optimization([f1, f2, f3], bounds, weights)

for i, x in enumerate(results):
    print(f"Candidate {i+1}:")
    print("Optimal x: ", x)
    print("Optimal objective values: ", [g1(x), f2(x), s_func(g3(x))])
