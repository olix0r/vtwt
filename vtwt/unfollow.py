from twisted.plugin import IPlugin
from zope.interface import implements

from jersey import log
from vtwt import cli


class UnFollowOptions(cli.Options):

    def parseArgs(self, name):
        self["friend"] = name


class UnFollower(cli.Command):

    def execute(self):
        return self.vtwt.unfollow(self.config["friend"]
                ).addCallback(self._befriended)


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

