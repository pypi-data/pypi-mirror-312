"""Library for creating beautiful and insightful visualizations."""

from importlib.metadata import version

from plastik import colors, lines
from plastik.axes import *  # noqa:F401,F403
from plastik.grid import *  # noqa:F401,F403
from plastik.legends import *  # noqa:F401,F403
from plastik.percentiles import percentiles
from plastik.ridge import *  # noqa:F401,F403

__version__ = version(__package__)
__all__ = ["colors", "lines", "percentiles"]
