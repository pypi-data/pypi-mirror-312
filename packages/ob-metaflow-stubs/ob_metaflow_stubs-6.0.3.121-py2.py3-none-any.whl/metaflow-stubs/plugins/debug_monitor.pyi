######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.33.1+obcheckpoint(0.1.4);ob(v1)                                                   #
# Generated on 2024-12-02T17:17:46.406555                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.monitor


class DebugMonitor(metaflow.monitor.NullMonitor, metaclass=type):
    @classmethod
    def get_worker(cls):
        ...
    ...

class DebugMonitorSidecar(object, metaclass=type):
    def __init__(self):
        ...
    def process_message(self, msg):
        ...
    ...

