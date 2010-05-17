from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from zope.interface import implements

from twittytwister.twitter import Twitter

from jersey import cli


class FollowOptions(cli.Options):

    def parseArgs(self, name):
        self["friend"] = name


class Follower(cli.Command):

    @inlineCallbacks
    def execute(self):
        twt = Twitter(self.config.parent["user"], self.config.parent["password"])
        try:
            yield twt.follow_user(self.config["friend"], self._befriended)
        except Exception, e:
            log.error(repr(e))


    def _befriended(self, user):
        print "Following: {0.screen_name}".format(user)



class FollowLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Follow the given user"
    name = "follow"
    shortcut = "f"
    options = FollowOptions
    command = Follower


loader = FollowLoader()

