import sys

from twisted.internet.defer import inlineCallbacks
from twisted.plugin import IPlugin
from zope.interface import implements

from jersey import log
from vtwt import cli


class FollowOptions(cli.Options):

    def parseArgs(self, *names):
        if not names:
            raise usage.error("No one to follow ;(")
        self["friends"] = names


class Follower(cli.Command):

    @inlineCallbacks
    def execute(self):
        users = []
        for friend in self.config["friends"]:
            try:
                user = yield self.vtwt.follow(friend)
                self._printFollowee(user)

            except Exception, e:
                print >>sys.stderr, repr(e)


    def _printFollowee(self, user):
        print "{u.screen_name}".format(c=self.config, u=user)



class FollowLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Follow the given user"
    name = "follow"
    shortcut = "f"
    options = FollowOptions
    command = Follower


loader = FollowLoader()

