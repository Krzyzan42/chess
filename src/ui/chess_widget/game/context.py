from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from . import (
        ChessController,
    )
    from ui import (
        BoardPainter,
        BoardParams,
        BoardSelection,
        PromotionSelect
    )
    from PySide6.QtGui import QPixmap

class Context:
    controller :'ChessController'
    board_ui :'BoardPainter'
    params :'BoardParams'
    selection :'BoardSelection'
    pixmaps :'dict[Any, QPixmap]'
    promotion_select :'PromotionSelect'