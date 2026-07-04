import re


def sanitize_location_name(location_name: str) -> str:
    """Return the normalized location name used for entries and entities."""
    return re.sub(r"\W+", "", location_name.lower())


def normalize_measurement_value(value: float) -> str:
    """Normalize numeric values for stable unique IDs."""
    return f"{float(value):.6f}".rstrip("0").rstrip(".")


def make_measurement_id(
    lake: str,
    location_name: str,
    latitude: float,
    longitude: float,
    depth: float,
) -> str:
    """Build a stable ID for a specific lake measurement point."""
    return "_".join(
        [
            "lake",
            lake,
            sanitize_location_name(location_name),
            normalize_measurement_value(latitude),
            normalize_measurement_value(longitude),
            normalize_measurement_value(depth),
        ]
    )
