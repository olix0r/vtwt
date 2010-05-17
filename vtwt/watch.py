import os, sys, time

from twisted.application.internet import TimerService
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.internet.error import DNSLookupError
from twisted.plugin import IPlugin
from zope.interface import implements

from jersey import cli, log

from twittytwister.twitter import Twitter

from vtwt.util import decodeText


class WatchOptions(cli.Options):

    optParameters = [
            ["limit", "l", None,
                "The maximum number of messages to be displayed at once.", int],
            ["interval", "i", None, "Time between requests", int],
        ]

    def parseArgs(self, *keywords):
        self["keywords"] = keywords


class Watcher(cli.Command):

    def execute(self):
        self.twt = Twitter(self.config.parent["user"], self.config.parent["password"])
        self._maxId = None

        if not self.config["keywords"]:
            func = self.showHome
        
        else:
            raise RuntimeError("Oops.")

        if self.config["interval"]:
            svc = TimerService(self.config["interval"], func)
            svc.setServiceParent(self)

            # Since this runs ~forever, just return a Deferred that doesn't call
            # back.  A swift SIGINT will kill it.
            d = Deferred()

        else:
            d = func()

        return d


    @inlineCallbacks
    def showHome(self):
        params = dict()
        if self._maxId:
            params["since_id"] = self._maxId
        self._msgBuffer = []
        try:
            yield self.twt.home_timeline(self.cb_gotMsg, params)
        except Exception, e:
            print >>sys.stderr, str(e)
        else:
            self._printMessages(self._msgBuffer)


    def cb_gotMsg(self, msg):
        msg.text = decodeText(msg.text)
        self._msgBuffer.insert(0, msg)


    def _printMessages(self, messages):
        limit = self.config["limit"] or len(messages)
        for msg in messages[:limit]:
            self._printMessage(msg)

        if messages and self.config["interval"]:
            print "# {0}".format(time.ctime())


    def _printMessage(self, msg):
        print "{0.user.screen_name:14}  {0.text}".format(msg)
        if self._maxId is None or self._maxId < msg.id:
            self._maxId = msg.id



class WatchLoader(cli.CommandFactory):
    implements(IPlugin)

    description = "Watch the twitter"
    name = "watch"
    shortcut = "w"
    options = WatchOptions
    command = Watcher


loader = WatchLoader()

