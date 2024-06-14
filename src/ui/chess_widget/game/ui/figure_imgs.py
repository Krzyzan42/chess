from chess import (
    PAWN,
    KNIGHT,
    BISHOP,
    ROOK,
    QUEEN,
    KING,
    WHITE,
    BLACK
)
from PySide6.QtGui import QPixmap

resource_path = 'resources/'

def get_figure_pixmaps():
    return {
        (PAWN, WHITE): QPixmap(resource_path + 'white_pawn.png'),
        (KNIGHT, WHITE): QPixmap(resource_path + 'white_knight.png'),
        (BISHOP, WHITE): QPixmap(resource_path + 'white_bishop.png'),
        (ROOK, WHITE): QPixmap(resource_path + 'white_rook.png'),
        (QUEEN, WHITE): QPixmap(resource_path + 'white_queen.png'),
        (KING, WHITE): QPixmap(resource_path + 'white_king.png'),

        (PAWN, BLACK): QPixmap(resource_path + 'black_pawn.png'),
        (KNIGHT, BLACK): QPixmap(resource_path + 'black_knight.png'),
        (BISHOP, BLACK): QPixmap(resource_path + 'black_bishop.png'),
        (ROOK, BLACK): QPixmap(resource_path + 'black_rook.png'),
        (QUEEN, BLACK): QPixmap(resource_path + 'black_queen.png'),
        (KING, BLACK): QPixmap(resource_path + 'black_king.png'),

    }