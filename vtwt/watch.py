import os, sys, time

from twisted.application.internet import TimerService
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.internet.error import DNSLookupError
from twisted.plugin import IPlugin
from zope.interface import implements

from jersey import log
from vtwt import cli


class WatchOptions(cli.Options):

    optParameters = [
            ["limit", "l", None,
                "The maximum number of messages to be displayed at once.", int],
            ["interval", "i", None, "Time between requests", int],
        ]


class Watcher(cli.Command):

    def execute(self):
        if self.config["interval"]:
            svc = TimerService(self.config["interval"], self.showHome)
            svc.setServiceParent(self)

            # Since this runs ~forever, just return a Deferred that doesn't call
            # back.  A swift SIGINT will kill it.
            d = Deferred()

        else:
            # Print it once and exit
            d = self.showHome()

        return d


    @inlineCallbacks
    def showHome(self):
        try:
            messages = yield self.vtwt.getTimelineUpdates()
            self._printMessages(messages)
        except Exception, e:
            print >>sys.stderr, str(e)


    def _printMessages(self, messages):
        limit = self.config["limit"] or len(messages)
        for msg in messages[:limit]:
            self._printMessage(msg)

        if messages and self.config["interval"]:
            print "# {0}".format(time.ctime())


    def _printMessage(self, msg):
        print "{0.user.screen_name:14}  {0.text}".format(msg)



class WatchLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Watch the twitter"
    name = "watch"
    shortcut = "w"
    options = WatchOptions
    command = Watcher


loader = WatchLoader()

