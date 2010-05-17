from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from zope.interface import implements

from twittytwister.twitter import Twitter

from jersey import cli, log


class FollowingOptions(cli.Options):
    optFlags = [
            ["long", "l", "Print more user information."],
        ]


class Following(cli.Command):

    @inlineCallbacks
    def execute(self):
        twt = Twitter(self.config.parent["user"], self.config.parent["password"])
        self._friends = []
        try:
            yield twt.list_friends(self._friends.append)
            self._printFriends(self._friends)

        except Exception, e:
            log.error(str(e))


    def _printFriends(self, friends):
        for friend in friends:
            self._printFriend(friend)

    def _printFriend(self, friend):
        if self.config["long"]:
            fmt = "{0.screen_name} ({0.name})"
        else:
            fmt = "{0.screen_name}"

        print fmt.format(friend)



class FollowingLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "List friends"
    name = "following"
    shortcut = "F"
    options = FollowingOptions
    command = Following


loader = FollowingLoader()

