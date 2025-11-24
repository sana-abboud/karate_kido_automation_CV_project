import os

# Base directories
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "../data")

# Template paths
TEMPLATES = {
    "game": os.path.join(DATA_DIR, "game_window/game.png"),
    "character1": os.path.join(DATA_DIR, "characters/karate_kid_template.png"),
    "character2": os.path.join(DATA_DIR, "characters/karate_kid_template2.png"),
    "lantern": "data/lantern/lantern.jpg",
    "wood": [
        os.path.join(DATA_DIR, "wood/left wood.png"),
        os.path.join(DATA_DIR, "wood/right wood.png"),
        os.path.join(DATA_DIR, "wood/left wood2.png"),
        os.path.join(DATA_DIR, "wood/right wood2.png"),
    ],
}

# Thresholds
MATCH_THRESHOLD = 0.68
WOOD_THRESHOLD = 0.8
LANTERN_THRESHOLD = 0.5
GLASS_MIN_AREA = 500