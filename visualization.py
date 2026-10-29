"""
visualization.py
-----------------
Assignment 2 - CSC3206 Artificial Intelligence
Role: Output and Visualization (Teoh Chia Sin)

Displays the UCS result produced by ucs_search.ucs_search():
    {
        "path": (str, ...),          # e.g. ("S","D","C","E","A","B")
        "routes": (str, ...),        # e.g. ("R7","R29","R26","R32","R12")
        "cost": float,
        "states_expanded": int,
        "states_generated": int,
    }

Provides:
    1. display_results(result)  -> printed summary + segment table + saved PNG table
    2. draw_graph(result)       -> state-space graph with optimal path highlighted (PNG)

Run directly (python visualization.py) to execute the real search and
generate both output files in outputs/.
"""

import math
import os

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from route_data import ROUTES, LOCATIONS

OUTPUT_DIR = "outputs"


# ---------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------
def _lookup_edge(from_loc, to_loc, route_id):
    """Find the specific edge dict used, matching by route id (e.g. 'R7')."""
    for edge in ROUTES.get(from_loc, []):
        if edge["to"] == to_loc and edge["route"] == route_id:
            return edge
    return None


def _segments(result):
    """Build a list of segment dicts (from, to, route, mode, cost) from a result."""
    path = result["path"]
    routes = result["routes"]
    segments = []
    for i, route_id in enumerate(routes):
        src, dst = path[i], path[i + 1]
        edge = _lookup_edge(src, dst, route_id)
        segments.append({
            "from": src,
            "to": dst,
            "route": route_id,
            "mode": edge["mode"] if edge else "?",
            "cost": edge["cost"] if edge else float("nan"),
        })
    return segments


# ---------------------------------------------------------------------
# 1. TEXTUAL / TABLE RESULT DISPLAY
# ---------------------------------------------------------------------
def display_results(result):
    segments = _segments(result)

    print("=" * 55)
    print("UNIFORM-COST SEARCH (UCS) - HOUSE VISIT TOUR RESULT")
    print("=" * 55)

    print("\nBest Route:")
    print("  " + " -> ".join(result["path"]))

    print("\nSelected Route Numbers:")
    print("  " + " -> ".join(result["routes"]))

    print("\nSegment Breakdown:")
    header = f"  {'From':<6}{'To':<6}{'Route':<8}{'Mode':<18}{'Cost':<10}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for s in segments:
        print(f"  {s['from']:<6}{s['to']:<6}{s['route']:<8}{s['mode']:<18}{s['cost']:<10.4f}")

    print("\nTotal Weighted Cost: {:.4f}".format(result["cost"]))
    print("Total Residences Visited: {}".format(len(result["path"]) - 1))
    print("States Expanded: {}".format(result["states_expanded"]))
    print("States Generated: {}".format(result["states_generated"]))
    print("=" * 55)

    _save_results_table_image(result, segments)


def _save_results_table_image(result, segments):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    rows = [[s["from"], s["to"], s["route"], s["mode"], f"{s['cost']:.4f}"] for s in segments]
    col_labels = ["From", "To", "Route", "Mode", "Cost"]

    fig, ax = plt.subplots(figsize=(6.5, 0.6 * (len(rows) + 2)))
    ax.axis("off")

    table = ax.table(cellText=rows, colLabels=col_labels, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.5)

    plt.title(
        f"UCS Result Summary\nPath: {' -> '.join(result['path'])}\n"
        f"Total Cost: {result['cost']:.4f}  |  "
        f"Expanded: {result['states_expanded']}  |  "
        f"Generated: {result['states_generated']}",
        fontsize=11, pad=12
    )

    out_path = os.path.join(OUTPUT_DIR, "ucs_result_table.png")
    plt.savefig(out_path, bbox_inches="tight", dpi=200)
    plt.close(fig)
    print(f"Result table image saved to: {os.path.abspath(out_path)}")


# ---------------------------------------------------------------------
# 2. GRAPH VISUALIZATION
# ---------------------------------------------------------------------
def draw_graph(result, save_name="state_space_graph.png"):
    """
    Draw the state-space graph and highlight the optimal path in green.

    Background edges are undirected: one per location pair, labelled with the
    cheapest route available between that pair in either direction. The tour
    edges are drawn on top as arrows labelled with the cost of the direction
    UCS actually travelled, which is what the result table reports. Keeping one
    label per pair is what stops the two directions of a pair (e.g. A->B at
    0.3227 and B->A at 0.2507) from overlapping and contradicting the table.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = result["path"]

    # The exact directed cost paid for each traversed segment.
    path_costs = {(s["from"], s["to"]): s["cost"] for s in _segments(result)}
    path_pairs = {frozenset(edge) for edge in path_costs}

    # One undirected edge per pair, keeping the cheaper direction for context.
    G = nx.Graph()
    for src, edges in ROUTES.items():
        for e in edges:
            if not G.has_edge(src, e["to"]) or e["cost"] < G[src][e["to"]]["weight"]:
                G.add_edge(src, e["to"], weight=e["cost"])

    # Lay the nodes out on a circle in tour order, so the tour is the outer
    # ring and every unused connection is a chord inside it. A spring layout
    # here routes tour edges straight through unrelated nodes (E->A crossing B)
    # and piles the labels on top of each other.
    ring = list(path) + [n for n in G.nodes() if n not in path]
    pos = {}
    for i, node in enumerate(ring):
        angle = math.pi / 2 - 2 * math.pi * i / len(ring)
        pos[node] = (math.cos(angle), math.sin(angle))

    background = [(u, v) for u, v in G.edges() if frozenset((u, v)) not in path_pairs]

    plt.figure(figsize=(9, 7.6))

    # Connections not used by the tour, in grey. Left unlabelled on purpose:
    # this graph is near-complete, so 10 extra numbers converging on the centre
    # obscures the result. Their costs are in route_data.py.
    nx.draw_networkx_edges(G, pos, edgelist=background, edge_color="#d0d0d0", width=1.0)

    # The tour itself, drawn on top with its true direction and cost.
    tour = nx.DiGraph()
    tour.add_edges_from(path_costs)
    nx.draw_networkx_edges(
        tour, pos, edge_color="#2e7d32", width=2.8,
        arrowstyle="-|>", arrowsize=18, node_size=900,
    )
    nx.draw_networkx_edge_labels(
        tour, pos,
        edge_labels={
            (s["from"], s["to"]): f"{s['route']}\n{s['cost']:.4f}"
            for s in _segments(result)
        },
        font_size=8, font_color="#2e7d32", font_weight="bold",
        bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": "none"},
    )

    # Nodes last so the arrowheads sit behind them rather than across them.
    node_colors = ["#2e7d32" if n in path else "#90a4ae" for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=900)
    nx.draw_networkx_labels(G, pos, font_color="white", font_weight="bold")

    plt.legend(
        handles=[
            Line2D([0], [0], color="#2e7d32", lw=2.8,
                   label="Tour edge - route taken and the cost of that direction"),
            Line2D([0], [0], color="#d0d0d0", lw=1.4,
                   label="Connection available but not used by the tour"),
        ],
        loc="upper center", bbox_to_anchor=(0.5, 0.02),
        fontsize=8, frameon=False, ncol=2,
    )
    plt.title(
        f"State-Space Graph - Optimal Path: {' -> '.join(path)}"
        f"  (total cost {result['cost']:.4f})",
        fontsize=12,
    )
    plt.margins(0.12)
    plt.axis("off")

    out_path = os.path.join(OUTPUT_DIR, save_name)
    plt.savefig(out_path, bbox_inches="tight", dpi=200)
    plt.close()
    print(f"State-space graph image saved to: {os.path.abspath(out_path)}")


# ---------------------------------------------------------------------
# 3. RUN DIRECTLY
# ---------------------------------------------------------------------
if __name__ == "__main__":
    from ucs_search import ucs_search

    result = ucs_search()
    display_results(result)
    draw_graph(result)