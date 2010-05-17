from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from zope.interface import implements

from twittytwister.twitter import Twitter

from jersey import cli


class UnFollowOptions(cli.Options):

    def parseArgs(self, name):
        self["friend"] = name


class UnFollower(cli.Command):

    @inlineCallbacks
    def execute(self):
        twt = Twitter(self.config.parent["user"], self.config.parent["password"])
        try:
            yield twt.unfollow_user(self.config["friend"], self._befriended)
        except Exception, e:
            log.error(repr(e))


    def _befriended(self, user):
        print "Un-following: {0.screen_name}".format(user)



class UnFollowLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Un-follow the given user"
    name = "unfollow"
    shortcut = "u"
    options = UnFollowOptions
    command = UnFollower


loader = UnFollowLoader()

