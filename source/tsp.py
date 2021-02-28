#!/usr/bin/python

# Code from
# https://www.gurobi.com/documentation/8.1/examples/tsp_py.html


# Copyright 2019, Gurobi Optimization, LLC

# Solve a traveling salesman problem on a randomly generated set of
# points using lazy constraints.   The base MIP model only includes
# 'degree-2' constraints, requiring each node to have exactly
# two incident edges.  Solutions to this model may contain subtours -
# tours that don't visit every city.  The lazy constraint callback
# adds new constraints to cut them off.

import itertools
import gurobipy as grb
import numpy as np


# Callback - use lazy constraints to eliminate sub-tours
def opt_tsp_model(dist_matrix):
    n = len(dist_matrix)

    def subtourelim(model, where):
        if where == grb.GRB.Callback.MIPSOL:
            # make a list of edges selected in the solution
            vals = model.cbGetSolution(model._vars)
            selected = grb.tuplelist(
                (i, j) for i, j in model._vars.keys() if vals[i, j] > 0.5
            )
            # find the shortest cycle in the selected edge list
            tour = subtour(selected)
            if len(tour) < n:
                # add subtour elimination constraint for every pair of cities in tour
                model.cbLazy(
                    grb.quicksum(
                        model._vars[i, j] for i, j in itertools.combinations(tour, 2)
                    )
                    <= len(tour) - 1
                )

    # Given a tuplelist of edges, find the shortest subtour

    def subtour(edges):
        unvisited = list(range(n))
        cycle = range(n + 1)  # initial length has 1 more city
        while unvisited:  # true if list is non-empty
            thiscycle = []
            neighbors = unvisited
            while neighbors:
                current = neighbors[0]
                thiscycle.append(current)
                unvisited.remove(current)
                neighbors = [j for i, j in edges.select(current, "*") if j in unvisited]
            if len(cycle) > len(thiscycle):
                cycle = thiscycle
        return cycle

    def tsp_compute(dist_matrix: np.ndarray):
        # Dictionary of Euclidean distance between each pair of points
        n = len(dist_matrix)
        dist = {
            (i, j): dist_matrix[i, j]
            for i in range(dist_matrix.shape[0])
            for j in range(i)
        }

        m = grb.Model()

        # Create variables

        vars = m.addVars(dist.keys(), obj=dist, vtype=grb.GRB.BINARY, name="e")
        for i, j in vars.keys():
            vars[j, i] = vars[i, j]  # edge in opposite direction

        # You could use Python looping constructs and m.addVar() to create
        # these decision variables instead.  The following would be equivalent
        # to the preceding m.addVars() call...
        #
        # vars = tupledict()
        # for i,j in dist.keys():
        #   vars[i,j] = m.addVar(obj=dist[i,j], vtype=GRB.BINARY,
        #                        name='e[%d,%d]'%(i,j))

        # Add degree-2 constraint

        m.addConstrs(vars.sum(i, "*") == 2 for i in range(n))

        # Using Python looping constructs, the preceding would be...
        #
        # for i in range(n):
        #   m.addConstr(sum(vars[i,j] for j in range(n)) == 2)

        # Optimize model

        m._vars = vars
        m.Params.lazyConstraints = 1
        m.optimize(subtourelim)

        vals = m.getAttr("x", vars)
        selected = grb.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)

        tour = subtour(selected)
        assert len(tour) == n

        print("")
        print("Optimal tour: %s" % str(tour))
        print("Optimal cost: %g" % m.objVal)
        print("")
        return tour

    return tsp_compute(dist_matrix)


def calc_dist_matrix(points):
    n = len(points)
    dist_matrix = np.zeros([n, n])
    for i in range(n):
        for j in range(i, n):
            dij = (points[i] - points[j]) ** 2
            dij = dij.sum() ** 0.5
            dij = np.abs(points[i] - points[j]).sum()
            dist_matrix[i, j] = dij
            dist_matrix[j, i] = dij
    return dist_matrix
