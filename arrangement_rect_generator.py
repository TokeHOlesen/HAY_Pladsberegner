from PyQt6.QtGui import QColor
from PyQt6.QtCore import QRect
import constants

colors = constants.PALLET_COLORS


class PalletRect(QRect):
    """A child class of QRect, which adds a .color property. Requires a color= keyword argument."""
    def __init__(self, *args, color) -> None:
        super().__init__(*args)
        self.color: QColor = QColor(color)


def gen_60_60_60(x, y, _, gutter, dimensions) -> tuple[list[PalletRect], int]:
    p60_width: int = dimensions["standard_width"]
    p60_height: int = dimensions["v-60-height"]

    pallet_rects: list[PalletRect] = [PalletRect(x, y, p60_width, p60_height, color=colors["60"]),
                                      PalletRect(x + p60_width + gutter, y, p60_width, p60_height, color=colors["60"]),
                                      PalletRect(x + 2 * (p60_width + gutter), y, p60_width, p60_height,
                                                 color=colors["60"])]

    brush_offset: int = p60_height + gutter
    return pallet_rects, brush_offset


def gen_120_120_120(x, y, _, gutter, dimensions) -> tuple[list[PalletRect], int]:
    p120_width: int = dimensions["standard_width"]
    p120_height: int = dimensions["v-120-height"]

    pallet_rects: list[PalletRect] = [PalletRect(x, y, p120_width, p120_height, color=colors["120"]),
                                      PalletRect(x + p120_width + gutter, y, p120_width, p120_height,
                                                 color=colors["120"]),
                                      PalletRect(x + 2 * (p120_width + gutter), y, p120_width, p120_height,
                                                 color=colors["120"])]

    brush_offset: int = p120_height + gutter
    return pallet_rects, brush_offset


def gen_120_120(x, y, border_rect, gutter, dimensions) -> tuple[list[PalletRect], int]:
    p120_width: int = dimensions["h-120-width"]
    p120_height: int = dimensions["h-120-height"]
    p120_adj_width: int = border_rect.width() - p120_width - gutter * 3

    pallet_rects: list[PalletRect] = [PalletRect(x, y, p120_width, p120_height, color=colors["120"]),
                                      PalletRect(x + p120_width + gutter, y, p120_adj_width, p120_height,
                                                 color=colors["120"])]

    brush_offset: int = p120_height + gutter
    return pallet_rects, brush_offset


def gen_120_120_60_60(x, y, _, gutter, dimensions) -> tuple[list[PalletRect], int]:
    p120_width: int = dimensions["standard_width"]
    p120_height: int = dimensions["v-120-height"]
    p60_height: int = (p120_height - gutter) // 2
    p60_adj_height: int = p120_height - p60_height - gutter

    pallet_rects: list[PalletRect] = [PalletRect(x, y, p120_width, p120_height, color=colors["120"]),
                                      PalletRect(x + p120_width + gutter, y, p120_width, p120_height,
                                                 color=colors["120"]),
                                      PalletRect(x + 2 * (p120_width + gutter), y, p120_width, p60_height,
                                                 color=colors["60"]),
                                      PalletRect(x + 2 * (p120_width + gutter), y + p60_height + gutter, p120_width,
                                                 p60_adj_height,
                                                 color=colors["60"])]

    brush_offset: int = p120_height + gutter
    return pallet_rects, brush_offset


def gen_17080_17080_120_60(x, y, _, gutter, dimensions) -> tuple[list[PalletRect], int]:
    pallet_width: int = dimensions["standard_width"]
    p170_height: int = dimensions["v-17080-height"]
    p120_height: int = dimensions["v-120-height"]
    p60_height: int = p170_height - p120_height - gutter

    pallet_rects: list[PalletRect] = [PalletRect(x, y, pallet_width, p170_height, color=colors["17080"]),
                                      PalletRect(x + pallet_width + gutter, y, pallet_width, p170_height,
                                                 color=colors["17080"]),
                                      PalletRect(x + 2 * (pallet_width + gutter), y, pallet_width, p120_height,
                                                 color=colors["120"]),
                                      PalletRect(x + 2 * (pallet_width + gutter), y + p120_height + gutter,
                                                 pallet_width, p60_height,
                                                 color=colors["60"])]

    brush_offset: int = p170_height + gutter
    return pallet_rects, brush_offset


def gen_17080_120_120_60_60(x, y, _, gutter, dimensions) -> tuple[list[PalletRect], int]:
    pallet_width: int = dimensions["standard_width"]
    p170_height: int = dimensions["v-17080-height"]
    p120_height: int = dimensions["v-120-height"]
    p60_height: int = p170_height - p120_height - gutter

    pallet_rects: list[PalletRect] = [PalletRect(x, y, pallet_width, p170_height, color=colors["17080"]),
                                      PalletRect(x + pallet_width + gutter, y, pallet_width, p120_height,
                                                 color=colors["120"]),
                                      PalletRect(x + 2 * (pallet_width + gutter), y, pallet_width, p120_height,
                                                 color=colors["120"]),
                                      PalletRect(x + pallet_width + gutter, y + p120_height + gutter, pallet_width,
                                                 p60_height,
                                                 color=colors["60"]),
                                      PalletRect(x + 2 * (pallet_width + gutter), y + p120_height + gutter,
                                                 pallet_width, p60_height,
                                                 color=colors["60"])]

    brush_offset: int = p170_height + gutter
    return pallet_rects, brush_offset


def gen_120_60_60_60_60(x, y, _, gutter, dimensions) -> tuple[list[PalletRect], int]:
    pallet_width: int = dimensions["standard_width"]
    p120_height: int = dimensions["v-120-height"]
    p60_height: int = (p120_height - gutter) // 2
    p60_adj_height: int = p120_height - p60_height - gutter

    pallet_rects: list[PalletRect] = [PalletRect(x, y, pallet_width, p120_height, color=colors["120"]),
                                      PalletRect(x + pallet_width + gutter, y, pallet_width, p60_height,
                                                 color=colors["60"]),
                                      PalletRect(x + 2 * (pallet_width + gutter), y, pallet_width, p60_height,
                                                 color=colors["60"]),
                                      PalletRect(x + pallet_width + gutter, y + p60_height + gutter, pallet_width,
                                                 p60_adj_height,
                                                 color=colors["60"]),
                                      PalletRect(x + 2 * (pallet_width + gutter), y + p60_height + gutter, pallet_width,
                                                 p60_adj_height,
                                                 color=colors["60"])]

    brush_offset: int = p120_height + gutter
    return pallet_rects, brush_offset


def gen_145_145_145(x, y, _, gutter, dimensions) -> tuple[list[PalletRect], int]:
    p145_width: int = dimensions["standard_width"]
    p145_height: int = dimensions["v-145-height"]

    pallet_rects: list[PalletRect] = [PalletRect(x, y, p145_width, p145_height, color=colors["145"]),
                                      PalletRect(x + p145_width + gutter, y, p145_width, p145_height,
                                                 color=colors["145"]),
                                      PalletRect(x + 2 * (p145_width + gutter), y, p145_width, p145_height,
                                                 color=colors["145"])]

    brush_offset: int = p145_height + gutter
    return pallet_rects, brush_offset


def gen_17080_17080_17080(x, y, _, gutter, dimensions) -> tuple[list[PalletRect], int]:
    p17080_width: int = dimensions["standard_width"]
    p17080_height: int = dimensions["v-17080-height"]

    pallet_rects: list[PalletRect] = [PalletRect(x, y, p17080_width, p17080_height, color=colors["17080"]),
                                      PalletRect(x + p17080_width + gutter, y, p17080_width, p17080_height,
                                                 color=colors["17080"]),
                                      PalletRect(x + 2 * (p17080_width + gutter), y, p17080_width, p17080_height,
                                                 color=colors["17080"])]

    brush_offset: int = p17080_height + gutter
    return pallet_rects, brush_offset


def gen_17090_145_145(x, y, border_rect, gutter, dimensions) -> tuple[list[PalletRect], int]:
    p17090_width: int = dimensions["v-17090-width"]
    p17090_height: int = dimensions["v-17080-height"]
    p145_width: int = border_rect.width() - p17090_width - gutter * 3
    p145_height: int = dimensions["h-145-height"]

    pallet_rects: list[PalletRect] = [PalletRect(x, y, p17090_width, p17090_height, color=colors["17090"]),
                                      PalletRect(x + p17090_width + gutter, y, p145_width, p145_height,
                                                 color=colors["145"]),
                                      PalletRect(x + p17090_width + gutter, y + p145_height + gutter, p145_width,
                                                 p145_height,
                                                 color=colors["145"])]

    brush_offset: int = p17090_height + gutter
    return pallet_rects, brush_offset


def gen_17090_17090_130_130_130(x, y, border_rect, gutter, dimensions) -> tuple[list[PalletRect], int]:
    p17090_width: int = dimensions["v-17090-width"]
    p17090_height: int = dimensions["v-17080-height"]
    p130_width: int = border_rect.width() - p17090_width - gutter * 3
    p130_height: int = int(round((p17090_height * 2 - gutter) / 3))
    p130_adj_height: int = (p17090_height * 2 + gutter) - (p130_height + gutter) * 2

    pallet_rects: list[PalletRect] = [PalletRect(x, y, p17090_width, p17090_height, color=colors["17090"]),
                                      PalletRect(x, y + p17090_height + gutter, p17090_width, p17090_height,
                                                 color=colors["17090"]),
                                      PalletRect(x + p17090_width + gutter, y, p130_width, p130_height,
                                                 color=colors["130"]),
                                      PalletRect(x + p17090_width + gutter, y + p130_height + gutter, p130_width,
                                                 p130_height,
                                                 color=colors["130"]),
                                      PalletRect(x + p17090_width + gutter, y + (p130_height + gutter) * 2, p130_width,
                                                 p130_adj_height,
                                                 color=colors["130"])]

    brush_offset: int = (p17090_height + gutter) * 2
    return pallet_rects, brush_offset


def gen_130_120_120(x, y, border_rect, gutter, dimensions) -> tuple[list[PalletRect], int]:
    p130_width: int = dimensions["v-130-width"]
    p130_height: int = dimensions["v-130-height"]
    p120_width: int = border_rect.width() - p130_width - gutter * 3
    p120_height: int = dimensions["h-120-height"]

    pallet_rects: list[PalletRect] = [PalletRect(x, y, p130_width, p130_height, color=colors["130"]),
                                      PalletRect(x + p130_width + gutter, y, p120_width, p120_height,
                                                 color=colors["120"]),
                                      PalletRect(x + p130_width + gutter, y + p120_height + gutter, p120_width,
                                                 p120_height,
                                                 color=colors["120"])]

    brush_offset: int = (p120_height * 2) + (gutter * 2)
    return pallet_rects, brush_offset


def gen_130_130(x, y, border_rect, gutter, dimensions) -> tuple[list[PalletRect], int]:
    p130_width: int = dimensions["v-130-width"]
    p130_height: int = dimensions["v-130-height"]
    p130_last_width: int = border_rect.width() - p130_width - gutter * 3

    pallet_rects: list[PalletRect] = [PalletRect(x, y, p130_width, p130_height, color=colors["130"]),
                                      PalletRect(x + p130_width + gutter, y, p130_last_width, p130_height,
                                                 color=colors["130"])]

    brush_offset: int = p130_height + gutter
    return pallet_rects, brush_offset


def gen_17080_60(x, y, border_rect, gutter, dimensions) -> tuple[list[PalletRect], int]:
    p17080_width: int = dimensions["h-17080-width"]
    p60_width: int = border_rect.width() - p17080_width - gutter * 3
    pallet_height: int = dimensions["h-17080-height"]

    pallet_rects: list[PalletRect] = [PalletRect(x, y, p17080_width, pallet_height, color=colors["17080"]),
                                      PalletRect(x + p17080_width + gutter, y, p60_width, pallet_height,
                                                 color=colors["60"])]

    brush_offset: int = pallet_height + gutter
    return pallet_rects, brush_offset


def gen_17090_60(x, y, border_rect, gutter, dimensions) -> tuple[list[PalletRect], int]:
    p17090_width: int = dimensions["h-17090-width"]
    p17090_height: int = dimensions["h-17090-height"]
    p60_width: int = border_rect.width() - p17090_width - gutter * 3
    p60_height: int = dimensions["h-60-height"]

    pallet_rects: list[PalletRect] = [PalletRect(x, y, p17090_width, p17090_height, color=colors["17090"]),
                                      PalletRect(x + p17090_width + gutter, y, p60_width, p60_height,
                                                 color=colors["60"])]

    brush_offset: int = p17090_height + gutter
    return pallet_rects, brush_offset


def gen_23090(x, y, _, gutter, dimensions) -> tuple[list[PalletRect], int]:
    p23090_width: int = dimensions["h-23090-width"]
    p23090_height: int = dimensions["h-23090-height"]

    pallet_rects: list[PalletRect] = [PalletRect(x, y, p23090_width, p23090_height, color=colors["23090"])]

    brush_offset: int = p23090_height + gutter
    return pallet_rects, brush_offset


# The key corresponds to the arrangement tuple to be drawn; the value is the corresponding drawing function
generate = {
    (60, 60, 60): gen_60_60_60,
    (120, 120, 120): gen_120_120_120,
    (120, 120): gen_120_120,
    (120, 120, 60, 60): gen_120_120_60_60,
    (17080, 17080, 120, 60): gen_17080_17080_120_60,
    (17080, 120, 120, 60, 60): gen_17080_120_120_60_60,
    (120, 60, 60, 60, 60): gen_120_60_60_60_60,
    (145, 145, 145): gen_145_145_145,
    (17080, 17080, 17080): gen_17080_17080_17080,
    (17090, 145, 145): gen_17090_145_145,
    (17090, 17090, 130, 130, 130): gen_17090_17090_130_130_130,
    (130, 120, 120): gen_130_120_120,
    (130, 130): gen_130_130,
    (17080, 60): gen_17080_60,
    (17090, 60): gen_17090_60,
    (23090,): gen_23090,
}
