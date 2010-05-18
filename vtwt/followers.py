from twisted.plugin import IPlugin
from zope.interface import implements

from jersey import log
from vtwt import cli


class FollowersOptions(cli.Options):
    optFlags = [
            ["long", "l", "Print more user information."],
        ]


class Followers(cli.Command):

    def execute(self):
        return self.vtwt.getFollowers().addCallback(self._printFollowers)


    def _printFollowers(self, followers):
        for follower in followers:
            self._printFollower(follower)

    def _printFollower(self, follower):
        if self.config["long"]:
            followerFmt = "{0.screen_name} ({0.name})"
        else:
            followerFmt = "{0.screen_name}"

        print followerFmt.format(follower)



class FollowersLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "List followers"
    name = "followers"
    shortcut = None
    options = FollowersOptions
    command = Followers


loader = FollowersLoader()

