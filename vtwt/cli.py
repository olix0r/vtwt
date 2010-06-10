import os, sys

from twisted.internet import reactor
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.python.filepath import FilePath

from jersey import cli, log

from vtwt import util
from vtwt.svc import VtwtService


class Options(cli.Options):
    pass


class Command(cli.Command):

    def __init__(self, config):
        cli.Command.__init__(self, config)

        svc = VtwtService(config.parent["user"], config.parent["password"])
        svc.setServiceParent(self)
        self.vtwt = svc


    def failWhale(self, error):
        return util.failWhale(error, self.config["COLUMNS"])



class CommandFactory(cli.CommandFactory):
    pass



class VtwtOptions(cli.PluggableOptions):

    defaultSubCommand = "watch"

    optFlags = [
            ["debug", "D", "Turn debugging messages on",]
        ]

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
        if self["debug"]:
            self.logLevel = log.TRACE  # Allow all log messages.
        else:
            self.logLevel = log.ERROR+1  # Ignore ~all log messages.

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

        self["COLUMNS"] = int(os.getenv("COLUMNS", 80))


    def readConfigFile(self, configFile):
        fileNS = dict()
        execfile(configFile.path, fileNS)
        for configKey in fileNS.iterkeys():
            k = configKey.replace("_", "-")
            if k in self and self[k] is None:
                self[k] = fileNS[configKey]



class VtwtCommander(cli.PluggableCommandRunner):

    def preApplication(self):
        # twittytwister.txml raises a weird Exception.  Suppress it.
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


