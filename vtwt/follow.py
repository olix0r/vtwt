from twisted.plugin import IPlugin
from zope.interface import implements

from jersey import log
from vtwt import cli


class FollowOptions(cli.Options):

    def parseArgs(self, name):
        self["friend"] = name


class Follower(cli.Command):

    def execute(self):
        return self.vtwt.follow(self.config["friend"]).addCallback(self._befriended)


    def _befriended(self, user):
        print "{self.config[user]}: {user.screen_name}".format(
            self=self, user=user)



class FollowLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Follow the given user"
    name = "follow"
    shortcut = "f"
    options = FollowOptions
    command = Follower


loader = FollowLoader()

