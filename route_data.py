"""Route data collected in Assignment 1 (Google Maps, 17 June 2026)."""

LOCATIONS = {
    "S": "Sunway University",
    "A": "Gan Yi Jong",
    "B": "Chew Khai Shuen",
    "C": "Teoh Chia Sin",
    "D": "Jeremy Tey Jie Ming",
    "E": "Lee How Seet",
}

MEMBERS = frozenset({"A", "B", "C", "D", "E"})

ROUTES = {
    "S": [
        {"to": "A", "route": "R1", "mode": "Drive", "cost": 0.3777},
        {"to": "A", "route": "R2", "mode": "Public Transport", "cost": 0.6797},
        {"to": "B", "route": "R3", "mode": "Drive", "cost": 0.5346},
        {"to": "B", "route": "R4", "mode": "Public Transport", "cost": 0.8065},
        {"to": "C", "route": "R5", "mode": "Walk", "cost": 0.0173},
        {"to": "C", "route": "R6", "mode": "Drive", "cost": 0.0013},
        {"to": "D", "route": "R7", "mode": "Drive", "cost": 0.0145},
        {"to": "D", "route": "R8", "mode": "Walk", "cost": 0.0173},
        {"to": "E", "route": "R9", "mode": "Drive", "cost": 0.4949},
        {"to": "E", "route": "R10", "mode": "Drive", "cost": 0.5838},
        {"to": "E", "route": "R11", "mode": "Public Transport", "cost": 0.6338},
    ],
    "A": [
        {"to": "B", "route": "R12", "mode": "Drive", "cost": 0.3227},
        {"to": "C", "route": "R13", "mode": "Drive", "cost": 0.3654},
        {"to": "C", "route": "R14", "mode": "Public Transport", "cost": 0.6754},
        {"to": "D", "route": "R15", "mode": "Drive", "cost": 0.3549},
        {"to": "E", "route": "R16", "mode": "Drive", "cost": 0.7894},
        {"to": "E", "route": "R17", "mode": "Drive", "cost": 0.6752},
    ],
    "B": [
        {"to": "A", "route": "R18", "mode": "Drive", "cost": 0.2507},
        {"to": "C", "route": "R19", "mode": "Drive", "cost": 0.5405},
        {"to": "D", "route": "R20", "mode": "Drive", "cost": 0.5376},
        {"to": "E", "route": "R21", "mode": "Drive", "cost": 0.7500},
    ],
    "C": [
        {"to": "A", "route": "R22", "mode": "Drive", "cost": 0.3280},
        {"to": "B", "route": "R23", "mode": "Drive", "cost": 0.5028},
        {"to": "D", "route": "R24", "mode": "Drive", "cost": 0.0181},
        {"to": "D", "route": "R25", "mode": "Walk", "cost": 0.0328},
        {"to": "E", "route": "R26", "mode": "Drive", "cost": 0.4622},
    ],
    "D": [
        {"to": "A", "route": "R27", "mode": "Drive", "cost": 0.3471},
        {"to": "B", "route": "R28", "mode": "Drive", "cost": 0.5376},
        {"to": "C", "route": "R29", "mode": "Drive", "cost": 0.0145},
        {"to": "C", "route": "R30", "mode": "Walk", "cost": 0.0328},
        {"to": "E", "route": "R31", "mode": "Drive", "cost": 0.4994},
    ],
    "E": [
        {"to": "A", "route": "R32", "mode": "Drive", "cost": 0.6061},
        {"to": "B", "route": "R33", "mode": "Drive", "cost": 0.7270},
        {"to": "C", "route": "R34", "mode": "Drive", "cost": 0.4671},
        {"to": "D", "route": "R35", "mode": "Drive", "cost": 0.4617},
    ],
}
