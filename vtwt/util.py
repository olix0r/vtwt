
import re
from htmlentitydefs import name2codepoint

# From http://wiki.python.org/moin/EscapingHtml

_HTMLENT_CODEPOINT_RE =  re.compile('&({0}|#\d+);'.format(
        '|'.join(name2codepoint.keys())))

def recodeText(text):
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


