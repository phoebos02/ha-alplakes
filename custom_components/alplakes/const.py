DOMAIN = "alplakes"

DEFAULT_LAKE = "zurich"
DEFAULT_LATITUDE = 47.255
DEFAULT_LONGITUDE = 8.688
DEFAULT_DEPTH = 0.1
DEFAULT_SCAN_INTERVAL = 10
DEFAULT_LOCATION_NAME = "Männedorf"

BASE_URL = "https://alplakes-api.eawag.ch/simulations/point"
ONE_D_BASE_URL = "https://alplakes-api.eawag.ch/simulations/1d/point"

# Default/fallback model. Individual lakes may override this below.
DEFAULT_MODEL = "delft3d-flow"
ONE_D_MODEL = "simstrat"

THREE_D_MODEL_BY_LAKE = {
    "ageri": "delft3d-flow",
    "annecy": "delft3d-flow",
    "biel": "delft3d-flow",
    "bourget": "delft3d-flow",
    "caldonazzo": "delft3d-flow",
    "garda": "delft3d-flow",
    "geneva": "delft3d-flow",
    "greifensee": "delft3d-flow",
    "hallwil": "delft3d-flow",
    "joux": "delft3d-flow",
    "lucerne": "mitgcm",
    "lugano": "delft3d-flow",
    "murten": "delft3d-flow",
    "neuchatel": "mitgcm",
    "stmoritz": "delft3d-flow",
    "zug": "mitgcm",
    "zurich": "delft3d-flow",
}

ONE_D_SIMSTRAT_LAKES = (
    "aegeri",
    "ammersee",
    "amsoldingersee",
    "annecy",
    "arendsee",
    "attersee",
    "baldegg",
    "bannwaldsee",
    "barchetsee",
    "barone",
    "bichelsee",
    "biel",
    "bled",
    "bourget",
    "brenet",
    "bret",
    "bretaye",
    "brienz",
    "burgaschisee",
    "burgseeli",
    "cadagno",
    "caldonazzo",
    "champfer",
    "chavonnes",
    "chiemsee",
    "chlimoossee",
    "como",
    "dittligsee",
    "egelsee",
    "eibsee",
    "faaker",
    "fuschlsee",
    "garda",
    "geistsee",
    "geneva",
    "gerzensee",
    "grabensee",
    "greifensee",
    "grosseralpsee",
    "gruntensee",
    "gruyere",
    "hallwil",
    "hasenseeost",
    "hasenseewest",
    "hauptwilerweiher",
    "hopfensee",
    "hugiweiher",
    "husemersee",
    "huttnersee",
    "huttwilersee",
    "inkwilersee",
    "irrsee",
    "iseo",
    "joux",
    "klontalersee",
    "kochelsee",
    "konigsee",
    "lauerz",
    "lenkerseeli",
    "lioson",
    "lobsigensee",
    "lowerconstance",
    "lowerlugano",
    "lowerzurich",
    "lucernealpnachersee",
    "lucernegersauerandtreibbecken",
    "lucernekreuztrichterandvitznauerbecken",
    "lucerneurnersee",
    "lungern",
    "lutzelsee",
    "maggiore",
    "marwilermoos",
    "mattsee",
    "mauensee",
    "mettmenhaslisee",
    "millstaetter",
    "mondsee",
    "moossee",
    "murten",
    "neuchatel",
    "niedersonthofener",
    "nussbommersee",
    "obererbommerweiher",
    "oberesbanzlauiseeli",
    "obertrumer",
    "oeschinensee",
    "ossiacher",
    "pfaffikon",
    "poschiavo",
    "riegsee",
    "rotsee",
    "sarnen",
    "sassolo",
    "schliersee",
    "seehamer",
    "seeweidsee",
    "sempach",
    "sihlsee",
    "sils",
    "silvaplana",
    "simssee",
    "soppensee",
    "staffelsee",
    "starnberger",
    "steinsee",
    "stmoritz",
    "stockseewli",
    "superiore",
    "tachinger",
    "tegernsee",
    "thun",
    "tome",
    "traunsee",
    "turlersee",
    "uebeschisee",
    "untererchatzensee",
    "upperconstance",
    "upperlugano",
    "upperlugano_python_enkf",
    "upperzurich",
    "vagoweiher",
    "walchensee",
    "walensee",
    "wallersee",
    "weissensee",
    "wilemersee",
    "wistererweiher",
    "wolfgangsee",
    "worthsee",
    "worthersee",
    "zeller",
    "zug",
)

# User-facing IDs that must be translated before calling the AlpLakes API.
LAKE_API_ID_BY_LAKE = {
    "aegeri": "ageri",
    "brunnen": "lucerne",
    "pfaffikersee": "pfaffikon",
}

ONE_D_LAKE_IDS = frozenset(ONE_D_SIMSTRAT_LAKES) - frozenset(THREE_D_MODEL_BY_LAKE)
VALID_LAKES = sorted(
    set(THREE_D_MODEL_BY_LAKE)
    | set(ONE_D_SIMSTRAT_LAKES)
    | set(LAKE_API_ID_BY_LAKE)
)

MODEL_BY_LAKE = {
    **THREE_D_MODEL_BY_LAKE,
    **{lake: ONE_D_MODEL for lake in ONE_D_LAKE_IDS},
}

MODEL_NAME_BY_MODEL = {
    "delft3d-flow": "Delft3D-FLOW",
    "mitgcm": "MITgcm",
    "simstrat": "Simstrat",
}

# Backward-compatible alias for older code importing MODEL.
MODEL = DEFAULT_MODEL
