from typing import TYPE_CHECKING, Any
import chess

if TYPE_CHECKING:
    from . import *
    from PySide6.QtGui import QPixmap

class Context:
    board :'chess.Board'
    params :'BoardParams'
    selection :'BoardSelection'
    pixmaps :'dict[Any, QPixmap]'