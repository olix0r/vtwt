from twisted.plugin import IPlugin
from zope.interface import implements

from jersey import log
from vtwt import cli, whale


class FollowersOptions(cli.Options):
    optFlags = [
            ["long", "l", "Print more user information."],
        ]


class Followers(cli.Command):

    @inlineCallbacks
    def execute(self):
        try:
            followers = yield self.vtwt.getFollowers()

        except whale.Error, we:
            print >>sys.stderr, whale.fail(int(we.status))
            raise SystemError(1)

        except Exception, e:
            print >>sys.stderr, repr(e)

        self._printFollowers(followers)


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

