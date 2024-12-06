import sys
import warnings

warnings.warn(
    "The '${PACKAGE_NAME}' package is deprecated. Please use '${REDIRECT_TO}' instead.",
    DeprecationWarning,
    stacklevel=2
)

# Import everything from robotframework-pabot
try:
    from robotframework_pabot import *
except ImportError:
    sys.exit("Please install robotframework-pabot package")
