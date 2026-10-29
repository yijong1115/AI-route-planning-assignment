# CSC3206 Artificial Intelligence — Assignment 2

**House Visit Tour solved with Uniform-Cost Search (UCS)**

Starting from Sunway University (`S`), find the cheapest order in which to visit the
houses of all five group members (`A`–`E`), visiting each exactly once. Route costs are
the weighted costs collected in Assignment 1 from Google Maps.

**Result:** `S → D → C → E → A → B` at a total weighted cost of **1.4200**,
using routes `R7 → R29 → R26 → R32 → R12`, found in 60 state expansions.
Verified optimal against all 120 possible tours by exhaustive enumeration.

---

## 1. Requirements

- **Python 3.9 or newer** (developed and tested on Python 3.11)
- Two third-party packages, listed in `requirements.txt`:
  - `matplotlib` — draws the result table and saves the PNGs
  - `networkx` — builds the state-space graph

Check your Python version first:

```bash
python --version
```

On some systems the command is `python3` instead of `python`. Use whichever
reports 3.9+, and substitute it in every command below.

---

## 2. Setup

From inside the project folder:

```bash
pip install -r requirements.txt
```

<details>
<summary>Optional: use a virtual environment (keeps these packages out of your system Python)</summary>

Windows (PowerShell):

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

</details>

---

## 3. Running the program

### 3.1 Main entry point — run this first

```bash
python main.py
```

This runs the UCS search and prints the full result, then writes two images into
an `outputs/` folder (created automatically if it does not exist).

Expected output:

```
=======================================================
UNIFORM-COST SEARCH (UCS) - HOUSE VISIT TOUR RESULT
=======================================================

Best Route:
  S -> D -> C -> E -> A -> B

Selected Route Numbers:
  R7 -> R29 -> R26 -> R32 -> R12

Segment Breakdown:
  From  To    Route   Mode              Cost
  ------------------------------------------------
  S     D     R7      Drive             0.0145
  D     C     R29     Drive             0.0145
  C     E     R26     Drive             0.4622
  E     A     R32     Drive             0.6061
  A     B     R12     Drive             0.3227

Total Weighted Cost: 1.4200
Total Residences Visited: 5
States Expanded: 60
States Generated: 172
=======================================================
Result table image saved to: ...\outputs\ucs_result_table.png
State-space graph image saved to: ...\outputs\state_space_graph.png
```

Generated files:

| File | Contents |
|---|---|
| `outputs/ucs_result_table.png` | Leg-by-leg breakdown table with the totals in the title |
| `outputs/state_space_graph.png` | State-space graph with the tour highlighted in green. Nodes sit in tour order, so the optimal path is the outer ring; grey chords are connections that exist but were not taken. Green labels give the route ID and the cost of the direction actually travelled, matching the table above. |

`main.py` changes its own working directory to the folder containing the script,
so `outputs/` always lands next to the code no matter where you launch it from.

### 3.2 Verification — proves the answer is optimal

```bash
python brute_force_check.py
```

Enumerates all 5! = 120 possible visiting orders, costs each one, ranks them, and
compares the cheapest against the UCS result. It reuses none of the search logic,
so the two results are genuinely independent.

Expected output ends with:

```
  Brute force : S -> D -> C -> E -> A -> B   cost 1.4200
  UCS         : S -> D -> C -> E -> A -> B   cost 1.4200

  Identical path : True
  Identical cost : True
...
VERIFIED: UCS returned the true global optimum.
```

The script exits with code `0` on a match and `1` on a mismatch.

### 3.3 Running individual modules

Each module can also be run on its own:

```bash
python ucs_search.py
```

Runs only the search and prints a plain-text summary. **Requires no third-party
packages** — useful for checking the algorithm on a machine without matplotlib.

```bash
python visualization.py
```

Runs the search and regenerates both PNGs, same as `main.py`.

---

## 4. What each file does

| File | Role |
|---|---|
| `route_data.py` | The Assignment 1 dataset. No logic — just `LOCATIONS`, `MEMBERS` and `ROUTES`. |
| `ucs_search.py` | The Uniform-Cost Search implementation. Returns the path, route IDs, cost and search statistics. |
| `visualization.py` | Prints the result summary and saves the result table and state-space graph as PNGs. |
| `main.py` | Entry point. Wires the search to the visualisation and degrades gracefully if the plotting packages are missing. |
| `brute_force_check.py` | Independent exhaustive verification of optimality. |
| `requirements.txt` | The two third-party dependencies. |

### The data format

`ROUTES` is an adjacency list — the key is the origin, the value is every route
leading out of it:

```python
"S": [
    {"to": "A", "route": "R1", "mode": "Drive",            "cost": 0.3777},
    {"to": "A", "route": "R2", "mode": "Public Transport", "cost": 0.6797},
    ...
]
```

| Field | Meaning |
|---|---|
| `to` | Destination node |
| `route` | Route ID `R1`–`R35`, matching the Assignment 1 report |
| `mode` | `Drive`, `Walk`, or `Public Transport` |
| `cost` | Weighted cost combining distance, time and mode (lower is better) |

Note that the graph contains **parallel edges** — several routes may connect the
same pair of locations by different transport modes — and is **directed and
asymmetric** (`A→B` costs 0.3227 but `B→A` costs 0.2507).

---

## 5. Troubleshooting

**`ModuleNotFoundError: No module named 'matplotlib'` (or `'networkx'`)**

The dependencies are not installed, or are installed for a different Python.
Run `pip install -r requirements.txt`. If that does not help, install into the
exact interpreter you are running with:

```bash
python -m pip install -r requirements.txt
```

Note that `main.py` catches this case and prints an instruction rather than
crashing, so a missing package will not stop the search from producing its answer.

**`python: command not found`**

Try `python3` instead, or install Python from <https://www.python.org/downloads/>.
On Windows, make sure "Add Python to PATH" was ticked during installation.

**No `outputs/` folder appears**

The folder is created only when the plotting packages are available. Check the
terminal for the `[Note] Graphs were skipped` message, which names the missing
package.

**The graph image looks different from the report**

It should not — `visualization.py` fixes the layout random seed to 42 so the
figure is reproducible. If it differs, check your `networkx` version.

**Nothing prints / the search returns nothing**

`ucs_search()` returns `None` only if no tour visiting all five houses exists.
With the shipped `route_data.py` this cannot happen; the graph is fully connected
(the brute-force check confirms all 120 orderings are feasible). If you have
edited the route data, check that every member is reachable.
