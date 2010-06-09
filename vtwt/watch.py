import os, sys, time

from twisted.application.internet import TimerService
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.plugin import IPlugin
from twisted.python.text import greedyWrap
from zope.interface import implements

from jersey import log
from vtwt import cli, whale


class WatchOptions(cli.Options):

    optParameters = [
            ["limit", "L", None,
                "The maximum number of messages to be displayed at once.", int],
            ["interval", "i", None, "Time between requests", int],
        ]

    optFlags = [
            ["long", "l", "Display in long format."],
        ]


    def parseArgs(self, watchee="home"):
        self["watchee"] = watchee

    def postOptions(self):
        log.debug("Going to watch {0[watchee]} ")


class Watcher(cli.Command):

    def execute(self):
        log.trace("Executing watcher.")

        self._lastPrintedId = None
        if self.config["interval"]:
            svc = TimerService(self.config["interval"], self.showTimeline)
            svc.setServiceParent(self)

            # Since this runs ~forever, just return a Deferred that doesn't call
            # back.  A swift SIGINT will kill it.
            d = Deferred()

        else:
            # Print it once and exit
            d = self.showTimeline()

        return d


    @inlineCallbacks
    def showTimeline(self):
        try:
            log.debug(("Requesting {0.config[watchee]} timeline since "
                       "{0._lastPrintedId}").format(self))
            watchee = self.config["watchee"]
            params = dict()

            if self._lastPrintedId:
                params["since_id"] = self._lastPrintedId

            if watchee == "home":
                messages = yield self.vtwt.getHomeTimeline(params)
            else:
                messages = yield self.vtwt.getUserTimeline(watchee, params)

            messages = self._limitMessages(messages, self.config["limit"])
            if messages:
                self._printMessages(messages)

        except whale.Error, we:
            print >>sys.stderr, whale.fail(int(we.status))

        except Exception, e:
            from traceback import print_exc
            print >>sys.stderr, "ERROR: {0!r}".format(e)
            print >>sys.stderr, print_exc()


    @staticmethod
    def _limitMessages(messages, limit=None):
        if limit and limit < len(messages):
            log.trace("Limiting messages: {0}".format(", ".join(
                    m.id for m in messages[:-limit])))
            del messages[:-limit]
        return messages


    def _printMessages(self, messages):
        screenNameWidth = max(len(msg.user.screen_name) for msg in messages)
        for msg in messages:
            self._printMessage(msg, screenNameWidth)

        if messages and self.config["interval"] and not self.config["long"]:
            self._printTimestamp()


    def _printMessage(self, msg, screenNameWidth=14):
        if self.config["long"]:
            fmt = "--- {0.user.screen_name:{2}} {0.created_at} [{0.id}]\n" \
                  "    {1}"
            paddingLen = 4

        else:
            fmt = "{0.user.screen_name:{2}}  {1}"
            paddingLen = screenNameWidth + 2

        width = self.config.parent["COLUMNS"] - paddingLen

        log.trace("Formatting {0} at {1} characters.".format(
                "long message" if self.config["long"] else "message",
                width))
        joiner = "\n" + (" " * paddingLen)
        text = joiner.join(greedyWrap(msg.text, width))
        try:
            print fmt.format(msg, text, screenNameWidth)
        except UnicodeEncodeError, uee:
            # Ignore messages with Unicode errors.  Sahri Charlie.
            log.warn("Unicode error printing message {0.id}".format(msg))
        else:
            self._lastPrintedId = msg.id


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

