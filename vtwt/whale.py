
from twisted.web.error import Error

_WHALE_FMT = """\
   __{lines}___
|\\/ {spaces}  X \\
}}    {msg}    >
|/\\_{lines}___-/
"""

def fail(error):
    if isinstance(error, Error):
        msg = "{0.status}: {0.message}".format(error)
    else:
        msg = repr(error)

    return _WHALE_FMT.format(
            spaces=" "*len(msg),
            lines="_"*len(msg),
            msg=msg)


