"""
main.py
-------
Assignment 2 - CSC3206 Artificial Intelligence
Entry point for the House Visit Tour (Uniform-Cost Search).

Runs the UCS search over the Assignment 1 route data and displays the result.
If matplotlib / networkx are installed, the full output is shown and the result
table and state-space graph are saved into outputs/. If they are not installed,
a set of instructions is printed to install the required packages.
"""

import os
import sys

from route_data import ROUTES, LOCATIONS, MEMBERS
from ucs_search import ucs_search

def main():
    # Run from the folder containing this file so that route data imports and
    # the generated outputs/ folder do not depend on where the command is run.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    result = ucs_search()
    if result is None:
        print("No tour found that visits every residence.")
        return 1

    try:
        from visualization import display_results, draw_graph
    except ImportError as exc:
        print(f"\n[Note] Graphs were skipped ({exc.name} is not installed).")
        print("       To generate the result table and state-space graph, run:")
        print("           pip install -r requirements.txt")
        return 0

    display_results(result)
    draw_graph(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
