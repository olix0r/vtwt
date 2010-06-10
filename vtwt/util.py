import re
from htmlentitydefs import name2codepoint

from twisted.python.text import greedyWrap
from twisted.web.error import Error as WebError


# From http://wiki.python.org/moin/EscapingHtml

_HTMLENT_CODEPOINT_RE =  re.compile('&({0}|#\d+);'.format(
        '|'.join(name2codepoint.keys())))

def recodeText(text):
    """Parses things like &amp; and &#8020; into real characters."""
    def _entToUnichr(match):
        ent = match.group(1)
        try:
            if ent.startswith("#"):
                char = unichr(int(ent[1:]))
            else:
                char = unichr(name2codepoint[ent])
        except:
            char = match.group(0)

        return char

    return _HTMLENT_CODEPOINT_RE.sub(_entToUnichr, text)


_whaleFmt = """\
   __{lines}___
|\\/  {spaces} X \\
}}    {body}    |
|/\\__{lines}__-/"""

_whalePaddingLen = 9

def failWhale(error, columns=80):
    if isinstance(error, WebError):
        emsg = "{0.message} {0.code}".format(error)
    else:
        emsg = str(error)

    width = columns - _whalePaddingLen
    lines = []
    for line in emsg.splitlines():
        lines.extend(greedyWrap(line, width))
    lineLength = max(map(len, lines))

    msg = "    |\n|    ".join(
                map(lambda l: "{0:{1}}".format(l, lineLength),
                    lines))

    return _whaleFmt.format(
            spaces = " "*lineLength,
            lines = "_"*lineLength,
            length = lineLength,
            body = msg)

