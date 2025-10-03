import os, sys

# Ensure project root is on sys.path so 'lib' is importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Alias legacy imports to the new module locations
from lib import helpers as _helpers
sys.modules['helpers'] = _helpers

from lib import cli as _cli
sys.modules['cli'] = _cli
sys.modules['main'] = _helpers