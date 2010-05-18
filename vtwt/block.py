import sys

from twisted.internet.defer import inlineCallbacks, gatherResults
from twisted.plugin import IPlugin
from twisted.python import usage
from zope.interface import implements

from jersey import log
from vtwt import cli


class BlockOptions(cli.Options):

    def parseArgs(self, *names):
        if not names:
            raise usage.error("No one to block ;(")
        self["blockees"] = names


class Blocker(cli.Command):

    def execute(self):
        return gatherResults(map(self._block, self.config["blockees"]))

    @inlineCallbacks
    def _block(self, user):
        print "blocking: {0}".format(user)
        yield self.vtwt.block(user)
        print "{0} blocked {1}".format(self.config["user"], user)



class BlockLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Block the given user"
    name = "block"
    shortcut = "B"
    options = BlockOptions
    command = Blocker


loader = BlockLoader()

