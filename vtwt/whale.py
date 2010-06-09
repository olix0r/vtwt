
from twisted.web.error import Error

_WHALE_FMT = """\
   ________
|\\/      X \\
 }}  {0: 3}    >
|/\\_______-/
"""

def fail(code):
    return _WHALE_FMT.format(code)
