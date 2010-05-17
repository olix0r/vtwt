from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from zope.interface import implements

from twittytwister.twitter import Twitter

from jersey import cli, log


class FollowersOptions(cli.Options):
    optFlags = [
            ["long", "l", "Print more user information."],
        ]


class Followers(cli.Command):

    @inlineCallbacks
    def execute(self):
        twt = Twitter(self.config.parent["user"], self.config.parent["password"])
        followers = []
        try:
            yield twt.list_followers(followers.append)
            self._printFollowers(followers)

        except:
            log.err()


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

