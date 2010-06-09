from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from twisted.python.text import greedyWrap
from zope.interface import implements

from jersey import log
from vtwt import cli, whale


class TweetOptions(cli.Options):

    def parseArgs(self, *tokens):
        self["tweet"] = " ".join(tokens)
        if not tokens:
            raise cli.UsageError("Nothing to tweet.")


class Tweeter(cli.Command):

    @inlineCallbacks
    def execute(self):
        try:
            text = self.config["tweet"]
            msgId = yield self.vtwt.tweet(text)
            wrapped = self._wrapText(text, len(str(msgId)))
            print "{0}  {1}".format(msgId, wrapped)

        except Exception, e:
            print >>sys.stderr, whale.fail(e)



    def _wrapText(self, text, paddingLen):
        width = self.config.parent["COLUMNS"] - paddingLen
        joiner = "\n" + str(" " * paddingLen)
        return joiner.join(greedyWrap(text, width))



class TweetLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Tweet something"
    name = "tweet"
    shortcut = "t"
    options = TweetOptions
    command = Tweeter


loader = TweetLoader()

