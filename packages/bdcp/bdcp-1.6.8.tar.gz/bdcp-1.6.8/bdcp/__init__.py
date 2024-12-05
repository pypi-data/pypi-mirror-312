#!/usr/bin/env python
# -*- coding:utf-8 -*-
__version__ = "1.6.8"


from . import connections, offline
Connect = connect = Connection =connections.Connection
offline = offline.Offline
__all__ = [
    "Connect",
    "Connection",
    "connect",
    "offline",
    "__version__",
]