#!/usr/bin/env python2.6

import os, sys

from twisted.internet import reactor
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.python.filepath import FilePath

from jersey import cli, log


class VtwtOptions(cli.PluggableOptions):

    defaultSubCommand = "watch"

    optParameters = [
            ["config-file", "c",
                os.path.expanduser("~/.vtwtrc"), "Vtwt config file",],
            ["user", "u", None, "Twitter User",],
            ["password", "p", None, "Twitter Password",],
        ]


    @property
    def commandPackage(self):
        import vtwt
        return vtwt


    def postOptions(self):
        self.logLevel = log.ERROR+1  # IGNORE ~all log messages.

        cf = FilePath(self["config-file"])
        if cf.exists():
            self.readConfigFile(cf)

        if not self["user"]:
            raise cli.UsageError("No user specified.")

        if not self["password"]:
            from getpass import getpass
            self["password"] = getpass(
                    "{0[user}@twitter.com password: ".format(self))
        if not self["password"]:
            raise cli.UsageError("No password specified.")


    def readConfigFile(self, configFile):
        fileNS = {}
        execfile(configFile.path, fileNS)
        for k in fileNS:
            if k in self and self[k] is None:
                self[k] = fileNS[k]



class VtwtCommander(cli.PluggableCommandRunner):

    def preApplication(self):
        import logging
        logging.raiseExceptions = False



def run(args=sys.argv[:]):
    program = os.path.basename(args[0])
    args = args[1:]

    opts = VtwtOptions(program)
    try:
        opts.parseOptions()
        VtwtCommander(program, opts).run()

    except cli.UsageError, ue:
        print >>sys.stderr, str(opts)
        print >>sys.stderr, str(ue)
        raise SystemExit(os.EX_USAGE)

    except SystemExit, ex:
        raise ex

    except Exception, e:
        print >>sys.stderr, str(e)
        raise SystemExit(1)


