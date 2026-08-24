import sys
from pathlib import Path

# Ensure src directory is in sys.path
root_path = Path(__file__).resolve().parent.parent
src_path = root_path / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from adpilot.api.main import app

# Expose app for Vercel Serverless Functions
__all__ = ["app"]
