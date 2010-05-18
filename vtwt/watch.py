import os, sys, time

from twisted.application.internet import TimerService
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.internet.error import DNSLookupError
from twisted.plugin import IPlugin
from twisted.python.text import greedyWrap
from zope.interface import implements

from jersey import log
from vtwt import cli


class WatchOptions(cli.Options):

    optParameters = [
            ["limit", "L", None,
                "The maximum number of messages to be displayed at once.", int],
            ["interval", "i", None, "Time between requests", int],
        ]

    optFlags = [
            ["long", "l", "Display in long format."],
        ]


class Watcher(cli.Command):

    def execute(self):
        log.trace("Executing watcher.")

        self._lastPrintedId = None
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
        params = dict()
        if self._lastPrintedId:
            params = {"since_id": self._lastPrintedId, }
            log.trace("Requesting new messages")
        else:
            log.trace("Requesting all messages")

        try:
            messages = yield self.vtwt.getTimelineUpdates(params)
            self._printMessages(messages)

        except Exception, e:
            from traceback import print_exc
            print >>sys.stderr, print_exc(e)


    @staticmethod
    def _limitMessages(messages, limit=None):
        if limit and limit < len(messages):
            log.trace("Limiting messages: {0}".format(", ".join(
                    m.id for m in messages[:-limit])))
            del messages[:-limit]
        return messages


    def _printMessages(self, messages):
        for msg in self._limitMessages(messages, self.config["limit"]):
            try:
                self._printMessage(msg)
            except UnicodeEncodeError, uee:
                # Ignore messages with Unicode errors.  Sahri Charlie.
                log.warn("Unicode error printing message {0.id}".format(msg))
            else:
                self._lastPrintedId = msg.id

        if messages and self.config["interval"] and not self.config["long"]:
            self._printTimestamp()


    def _printMessage(self, msg):
        log.trace("Formatting {0.id}".format(msg))
        width = os.getenv("COLUMNS", 80)

        if self.config["long"]:
            fmt = "--- {0.user.screen_name:15} {0.created_at} [{0.id}]\n    {1}"
            joiner = "\n    "

        else:
            fmt = "{0.user.screen_name:15} {1}"
            joiner = "\n" + (" "*16)

        text = joiner.join(greedyWrap(msg.text, width))
        print fmt.format(msg, text)


    @staticmethod
    def _printTimestamp():
        print "# {0}".format(time.ctime())




class WatchLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Watch the twitter"
    name = "watch"
    shortcut = "w"
    options = WatchOptions
    command = Watcher


loader = WatchLoader()

