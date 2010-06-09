import os, sys

from twisted.internet.defer import inlineCallbacks
from twisted.plugin import IPlugin
from zope.interface import implements

from jersey import log
from vtwt import cli, whale


class UnFollowOptions(cli.Options):

    def parseArgs(self, *names):
        if not names:
            raise usage.error("No one to unfollow ;(")
        self["losers"] = names


class UnFollower(cli.Command):

    @inlineCallbacks
    def execute(self):
        users = []
        for loser in self.config["losers"]:
            try:
                user = yield self.vtwt.unfollow(loser)

            except Exception, e:
                print >>sys.stderr, whale.fail(e)

            else:
                self._printLoser(loser)


    def _printLoser(self, user):
        print "{u}".format(c=self.config, u=user)




class UnFollowLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Un-follow the given user"
    name = "unfollow"
    shortcut = "u"
    options = UnFollowOptions
    command = UnFollower


loader = UnFollowLoader()

