DOMAIN = "alplakes"

# Lake IDs offered by the integration. Some legacy names are kept for
# compatibility and translated to the correct API lake ID in LAKE_API_ID_BY_LAKE.
VALID_LAKES = [
    "ageri",
    "biel",
    "brunnen",
    "caldonazzo",
    "garda",
    "geneva",
    "greifensee",
    "hallwil",
    "joux",
    "lucerne",
    "lugano",
    "murten",
    "neuchatel",
    "stmoritz",
    "zug",
    "thun",
    "zurich",
]

# Legacy/user-facing IDs that must be translated before calling the AlpLakes API.
LAKE_API_ID_BY_LAKE = {
    "brunnen": "lucerne",
}

DEFAULT_LAKE = "zurich"
DEFAULT_LATITUDE = 47.255
DEFAULT_LONGITUDE = 8.688
DEFAULT_DEPTH = 0.1
DEFAULT_SCAN_INTERVAL = 10
DEFAULT_LOCATION_NAME = "Männedorf"

BASE_URL = "https://alplakes-api.eawag.ch/simulations/point"

# Default/fallback model. Individual lakes may override this below.
DEFAULT_MODEL = "delft3d-flow"

MODEL_BY_LAKE = {
    "lucerne": "mitgcm",
    "neuchatel": "mitgcm",
    "zug": "mitgcm",
    "thun": "simstrat",
}

MODEL_NAME_BY_MODEL = {
    "delft3d-flow": "Delft3D-FLOW",
    "mitgcm": "MITgcm",
    "simstrat": "Simstrat",
}

# Backward-compatible alias for older code importing MODEL.
MODEL = DEFAULT_MODEL
