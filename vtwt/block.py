import sys

from twisted.internet.defer import inlineCallbacks, gatherResults
from twisted.plugin import IPlugin
from twisted.python import usage
from zope.interface import implements

from jersey import log
from vtwt import cli, whale


class BlockOptions(cli.Options):

    def parseArgs(self, *names):
        if not names:
            raise usage.error("No one to block ;(")
        self["blockees"] = names


class Blocker(cli.Command):

    @inlineCallbacks
    def execute(self):
        for blockee in self.config["blockees"]:
            try:
                yield self._block(blockee)

            except whale.Error, we:
                print >>sys.stderr, whale.fail(int(we.status))
                raise SystemExit(1)

            except Exception, e:
                print >>sys.stderr, repr(e)


    @inlineCallbacks
    def _block(self, user):
        yield self.vtwt.block(user)
        print "{0}".format(user)



class BlockLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Block the given user"
    name = "block"
    shortcut = "B"
    options = BlockOptions
    command = Blocker


loader = BlockLoader()

