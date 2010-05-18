from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from zope.interface import implements

from jersey import log
from vtwt import cli


class TweetOptions(cli.Options):

    def parseArgs(self, *tokens):
        if not tokens:
            raise cli.UsageError("Nothing to tweet.")
        self["tweet"] = " ".join(tokens)


class Tweeter(cli.Command):

    @inlineCallbacks
    def execute(self):
        text = self.config["tweet"]
        try:
            msgId = yield self.vtwt.tweet(text)
            print "{0}\t{1}".format(self.config.parent["user"], text)
        except Exception, e:
            log.error(str(e))



class TweetLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Tweet something"
    name = "tweet"
    shortcut = "t"
    options = TweetOptions
    command = Tweeter


loader = TweetLoader()

