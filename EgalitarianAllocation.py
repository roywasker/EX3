import cvxpy
import doctest


def egalitarian_allocation(valuations: list[list[float]]):
    """
           Examples:
               >>> egalitarian_allocation(valuations=[[11,11,22,33,44], [11,22,44,55,66], [11,33,22,11,66]])
               player 0 receives  100.0% of resource 0 and 0.0% of resource 1 and 0.0% of resource 2 and 70.59% of resource 3 and 58.82% of resource 4
               player 1 receives  0.0% of resource 0 and 0.0% of resource 1 and 100.0% of resource 2 and 29.41% of resource 3 and 0.0% of resource 4
               player 2 receives  0.0% of resource 0 and 100.0% of resource 1 and 0.0% of resource 2 and 0.0% of resource 3 and 41.18% of resource 4

               >>> egalitarian_allocation(valuations=[[1,19,80], [20,1,79]])
               player 0 receives  0.0% of resource 0 and 100.0% of resource 1 and 50.31% of resource 2
               player 1 receives  100.0% of resource 0 and 0.0% of resource 1 and 49.69% of resource 2

               >>> egalitarian_allocation(valuations=[[11,25,32,45], [85,43,86,13], [24,58,36,77],[54,62,35,60]])
               player 0 receives  0.0% of resource 0 and 0.0% of resource 1 and 100.0% of resource 2 and 54.79% of resource 3
               player 1 receives  66.65% of resource 0 and 0.0% of resource 1 and 0.0% of resource 2 and 0.0% of resource 3
               player 2 receives  0.0% of resource 0 and 37.66% of resource 1 and 0.0% of resource 2 and 45.21% of resource 3
               player 3 receives  33.35% of resource 0 and 62.34% of resource 1 and 0.0% of resource 2 and 0.0% of resource 3

               >>> egalitarian_allocation(valuations=[[12,56,76,23,56,85,36,44], [21,35,56,85,99,48,68,20]])
               player 0 receives  36.36% of resource 0 and 100.0% of resource 1 and 100.0% of resource 2 and 0.0% of resource 3 and 0.0% of resource 4 and 100.0% of resource 5 and 0.0% of resource 6 and 100.0% of resource 7
               player 1 receives  63.64% of resource 0 and 0.0% of resource 1 and 0.0% of resource 2 and 100.0% of resource 3 and 100.0% of resource 4 and 0.0% of resource 5 and 100.0% of resource 6 and 0.0% of resource 7
           """

    # Declare the variables and utility
    num_of_players = len(valuations)
    num_of_resources = len(valuations[0])
    variables = []
    utility_for_player = []

    # Calculation of the utility for all player
    for i in range(num_of_players):
        utility = 0
        for j in range(num_of_resources):
            variables.append(cvxpy.Variable(num_of_players))  # fractions of all the resources by number of player
            utility += variables[j][i] * valuations[i][j]  # Calculation of the utility for player i
        utility_for_player.append(utility)  # insert  utility for player i to utility list

    min_utility = cvxpy.Variable()

    # list all the constraints for the maximize function
    fixed_constraints = \
        [variables[i][j] >= 0 for i in range(num_of_resources) for j in range(num_of_players)] + \
        [variables[i][j] <= 1 for i in range(num_of_resources) for j in range(num_of_players)] + \
        [utility_for_player[i] >= min_utility for i in range(num_of_players)] + \
        [sum(variables[i]) == 1 for i in range(num_of_resources)]

    # solve the equation
    prob = cvxpy.Problem(cvxpy.Maximize(min_utility), constraints=fixed_constraints)
    prob.solve(solver=cvxpy.ECOS)

    # print the result
    for i in range(num_of_players):
        print(f"player {i} receives ", end=" ")
        for j in range(num_of_resources):
            if j == 0:
                print(f"{abs(round(variables[j][i].value * 100, 2))}% of resource {j}", end="")
            else:
                print(f" and {abs(round(variables[j][i].value * 100, 2))}% of resource {j}", end="")
        print()


if __name__ == "__main__":
    doctest.testmod()
