import sys

from twisted.internet.defer import inlineCallbacks, gatherResults
from twisted.plugin import IPlugin
from twisted.python import usage
from zope.interface import implements

from jersey import log
from vtwt import cli, whale


class UnBlockOptions(cli.Options):

    def parseArgs(self, *names):
        if not names:
            raise usage.error("No one to unblock ;(")
        self["unblockees"] = names


class UnBlocker(cli.Command):

    @inlineCallbacks
    def execute(self):
        for unblockee in self.config["unblockees"]:
            try:
                yield self._unblock(unblockee)

            except whale.Error, we:
                print >>sys.stderr, whale.fail(int(we.status))

            except Exception, e:
                print >>sys.stderr, repr(e)


    @inlineCallbacks
    def _unblock(self, user):
        yield self.vtwt.unblock(user)
        print "{0}".format(user)



class UnBlockLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Un-block the given user"
    name = "unblock"
    shortcut = "B"
    options = UnBlockOptions
    command = UnBlocker


loader = UnBlockLoader()

