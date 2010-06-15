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
   _{lines}__
|\\/{space} x \\
}}   {body}   |
|/\\{lines}__-/"""

_whalePaddingLen = 6

def failWhale(error, columns=80):
    if isinstance(error, WebError):
        emsg = "{0.status} {0.message}".format(error)
    else:
        emsg = str(error)

    width = columns - _whalePaddingLen
    lines = []
    for line in emsg.splitlines():
        lines.extend(greedyWrap(line, width))
    lineLength = max(map(len, lines))

    msg = "{0}|\n|{0}".format((_whalePaddingLen/2)*" ").join(
                map(lambda l: "{0:{1}}".format(l, lineLength),
                    lines))

    return _whaleFmt.format(
            space = " "*lineLength,
            lines = "_"*lineLength,
            length = lineLength,
            body = msg)

