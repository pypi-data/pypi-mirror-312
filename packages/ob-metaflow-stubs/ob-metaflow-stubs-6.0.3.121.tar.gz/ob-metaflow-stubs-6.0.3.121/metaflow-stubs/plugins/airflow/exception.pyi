######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.12.33.1+obcheckpoint(0.1.4);ob(v1)                                                   #
# Generated on 2024-12-02T17:17:46.437915                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException

class AirflowException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class NotSupportedException(metaflow.exception.MetaflowException, metaclass=type):
    ...

