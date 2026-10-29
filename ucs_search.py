"""Uniform-Cost Search for the house tour problem.

State: (current_location, visited_members). Goal test is applied at
expansion (not generation) so the first goal state popped from the
frontier is guaranteed to carry the minimum cumulative cost.
"""

import heapq
from itertools import count

from route_data import ROUTES, MEMBERS


def ucs_search(start="S", members=MEMBERS):
    counter = count()
    frontier = [(0.0, next(counter), start, frozenset(), (start,), ())]
    best_cost = {}
    states_expanded = 0
    states_generated = 1  # the initial state

    while frontier:
        cost, _, location, visited, path, routes_used = heapq.heappop(frontier)

        state_key = (location, visited)
        if state_key in best_cost and best_cost[state_key] <= cost:
            continue  # stale queue entry, a cheaper path already expanded this state
        best_cost[state_key] = cost
        states_expanded += 1

        if visited == members:
            return {
                "path": path,
                "routes": routes_used,
                "cost": cost,
                "states_expanded": states_expanded,
                "states_generated": states_generated,
            }

        for edge in ROUTES.get(location, []):
            if edge["to"] not in members or edge["to"] in visited:
                continue
            next_visited = visited | {edge["to"]}
            next_cost = cost + edge["cost"]
            states_generated += 1
            heapq.heappush(
                frontier,
                (
                    next_cost,
                    next(counter),
                    edge["to"],
                    next_visited,
                    path + (edge["to"],),
                    routes_used + (edge["route"],),
                ),
            )

    return None


if __name__ == "__main__":
    result = ucs_search()
    print("Best route:", " -> ".join(result["path"]))
    print("Selected route numbers:", " -> ".join(result["routes"]))
    print(f"Total weighted cost: {result['cost']:.4f}")
    print("Total residences visited:", len(MEMBERS))
    print("States expanded:", result["states_expanded"])
    print("States generated:", result["states_generated"])
