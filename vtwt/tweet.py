from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from zope.interface import implements

from jersey import cli, log

from twittytwister.twitter import Twitter


class TweetOptions(cli.Options):

    def parseArgs(self, *tokens):
        if not tokens:
            raise cli.UsageError("Nothing to tweet.")
        self["tweet"] = " ".join(tokens)


class Tweeter(cli.Command):

    @inlineCallbacks
    def execute(self):
        twt = Twitter(self.config.parent["user"], self.config.parent["password"])
        
        text = self.config["tweet"]
        msg = yield twt.update(text)
        print "@{0} {1}".format(self.config.parent["user"], text)



class TweetLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Tweet something"
    name = "tweet"
    shortcut = "t"
    options = TweetOptions
    command = Tweeter


loader = TweetLoader()

