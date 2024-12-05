__version__ = "0.3.2"

# ruff: noqa: E402

# needed to avoid
# RuntimeError: Working outside of application context.
import eventlet
eventlet.monkey_patch()

# load the environment variables for this setup from .env file
from dotenv import load_dotenv
load_dotenv()
load_dotenv(".env")
load_dotenv(".env.local")

# "silence" lower-level modules
import logging
for module in [ "pymongo.connection", "pymongo.serverSelection", "pymongo.command", "pymongo.topology" ]:
  module_logger = logging.getLogger(module)
  module_logger.setLevel(logging.WARN)
