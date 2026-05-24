"""
kenya-agui — First East African AG-UI implementation

AG-UI Protocol: https://github.com/ag-ui-protocol/ag-ui
"""
from .server import KenyaAGUIServer, AGUIEmitter, AGUIEvent

__version__ = "0.1.0"
__all__ = ["KenyaAGUIServer", "AGUIEmitter", "AGUIEvent"]
