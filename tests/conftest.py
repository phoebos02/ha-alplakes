import sys
from pathlib import Path
import pytest
from pytest_socket import enable_socket, socket_allow_hosts

pytest_plugins = "pytest_homeassistant_custom_component"

# Add the project root directory to the Python path
project_root = str(Path(__file__).parent.parent)
sys.path.insert(0, project_root)

# @pytest.fixture(autouse=True)
# def enable_custom_integrations(enable_custom_integrations):
#    """Enable loading of custom integrations."""
#    yield

@pytest.hookimpl(trylast=True)
def pytest_runtest_setup():
    """Re-enable sockets and allow specific hosts before each test."""
    enable_socket()
    socket_allow_hosts(["127.0.0.1", "152.88.10.20"], allow_unix_socket=True)
