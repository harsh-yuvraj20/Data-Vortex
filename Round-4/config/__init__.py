"""Config package initialization."""
try:
    from config.settings import *  # noqa: F401, F403
except ImportError:
    from .settings import *  # noqa: F401, F403
