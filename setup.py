#!/usr/bin/env python

from distutils import core

def infoFromModule(path):
    ns = {}
    execfile(path, ns)
    return dict(
            name= ns["version"].package,
            version= ns["version"].short(),
            )


core.setup(
        packages = ["vtwt",],
        scripts = ["bin/vtwt",],
        **infoFromModule("vtwt/_version.py")
    )


