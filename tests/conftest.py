import sys
from pathlib import Path
# import pytest

pytest_plugins = "pytest_homeassistant_custom_component"

# Add the project root directory to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

# @pytest.fixture(autouse=True)
# def enable_custom_integrations(enable_custom_integrations):
#    """Enable loading of custom integrations."""
#    yield
