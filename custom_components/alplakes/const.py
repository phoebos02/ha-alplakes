DOMAIN = "alplakes"

# Predefined list of valid lake names
VALID_LAKES = [
    "zurich", "geneva", "biel", "joux", "neuchatel", "thun", "brunnen", "lucerne"
]
# Default configurations
DEFAULT_LAKE = "zurich"
DEFAULT_LATITUDE = 47.36539
DEFAULT_LONGITUDE = 8.54305
DEFAULT_DEPTH = 1.0
DEFAULT_SCAN_INTERVAL = 10

BASE_URL = "https://alplakes-api.eawag.ch/simulations/point"
MODEL = "delft3d-flow" 