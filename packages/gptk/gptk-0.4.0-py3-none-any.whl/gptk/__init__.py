'''J.T. Hartzfeld's Personal Library
    This is a collection of generally useful snippets and bits that make
    their way into most of my projects.
'''
import os
from pathlib import Path
from auto_all import start_all, end_all


start_all()

from propertyplus import *

try:
    from .encoding import *
except ImportError:
    from gptk.encoding import *

try:
    from .singletons import *
except ImportError:
    from gptk.singletons import *

try:
    from .enums import *
except ImportError:
    from gptk.enums import *

end_all()
