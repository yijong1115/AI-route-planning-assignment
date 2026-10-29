"""
brute_force_check.py
--------------------
Assignment 2 - CSC3206 Artificial Intelligence
Independent verification of the Uniform-Cost Search result (Section 9.1).

Purpose
-------
UCS is *theoretically* guaranteed to return the optimal tour. This script checks
that guarantee *empirically*, without reusing any of the search logic, so the two
results are genuinely independent.

Method
------
Because the tour must start at S and visit each of the five residences exactly
once, every possible tour corresponds to one ordering (permutation) of
{A, B, C, D, E}. There are 5! = 120 such orderings. For each ordering:

    1. Walk the legs S -> first -> second -> ... -> last.
    2. For each leg, take the cheapest available route between those two
       locations (parallel routes such as drive/walk are all considered).
    3. Sum the weighted costs to get that ordering's total.

Taking the minimum over all 120 orderings gives the true global optimum by
exhaustive enumeration. If UCS agrees with it, the UCS result is confirmed
optimal rather than merely plausible.
"""

import os
import sys
from itertools import permutations

from route_data import ROUTES, MEMBERS, LOCATIONS
from ucs_search import ucs_search

SEPARATOR = "=" * 62


def cheapest_leg(origin, destination):
    """Return the cheapest route dict from origin to destination, or None."""
    options = [e for e in ROUTES.get(origin, []) if e["to"] == destination]
    if not options:
        return None
    return min(options, key=lambda e: e["cost"])


def tour_cost(order, start="S"):
    """Total cost of visiting `order` from `start`, or None if unreachable.

    Returns (total_cost, [route_ids]).
    """
    total = 0.0
    routes = []
    current = start
    for destination in order:
        edge = cheapest_leg(current, destination)
        if edge is None:
            return None, None          # this ordering is not possible
        total += edge["cost"]
        routes.append(edge["route"])
        current = destination
    return total, routes


def brute_force(start="S"):
    """Evaluate every ordering. Returns a list of (cost, order, routes), sorted."""
    results = []
    for order in permutations(sorted(MEMBERS)):
        cost, routes = tour_cost(order, start)
        if cost is not None:
            results.append((cost, order, routes))
    results.sort(key=lambda item: item[0])
    return results


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    all_orders = list(permutations(sorted(MEMBERS)))
    results = brute_force()

    print(SEPARATOR)
    print("BRUTE-FORCE VERIFICATION OF THE UCS RESULT")
    print(SEPARATOR)
    print(f"\nOrderings enumerated : {len(all_orders)}  (5! = 120)")
    print(f"Feasible orderings   : {len(results)}")

    print("\nFive cheapest tours found by exhaustive enumeration:")
    header = f"  {'Rank':<6}{'Tour':<30}{'Cost':<10}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for rank, (cost, order, _routes) in enumerate(results[:5], start=1):
        tour = " -> ".join(("S",) + order)
        print(f"  {rank:<6}{tour:<30}{cost:<10.4f}")

    best_cost, best_order, best_routes = results[0]
    best_path = ("S",) + best_order

    # ---- the independent UCS result -------------------------------------
    ucs = ucs_search()

    print("\n" + SEPARATOR)
    print("COMPARISON")
    print(SEPARATOR)
    print(f"\n  Brute force : {' -> '.join(best_path)}   cost {best_cost:.4f}")
    print(f"  UCS         : {' -> '.join(ucs['path'])}   cost {ucs['cost']:.4f}")

    same_path = tuple(ucs["path"]) == best_path
    same_cost = abs(ucs["cost"] - best_cost) < 1e-9

    print(f"\n  Identical path : {same_path}")
    print(f"  Identical cost : {same_cost}")

    print("\n  Optimal visiting order:")
    for step, node in enumerate(best_path):
        tag = "start" if step == 0 else f"stop {step}"
        print(f"    {tag:<8} {node} - {LOCATIONS.get(node, node)}")
    print(f"\n  Routes used: {' -> '.join(best_routes)}")

    print("\n" + SEPARATOR)
    if same_path and same_cost:
        print("VERIFIED: UCS returned the true global optimum.")
        print(SEPARATOR)
        return 0

    print("MISMATCH: the UCS result does not match the exhaustive optimum.")
    print(SEPARATOR)
    return 1


if __name__ == "__main__":
    sys.exit(main())
