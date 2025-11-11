from PyQt6.QtCore import QRect


def generate_60_60_60(x, y, standard_pallet_width, border_rect, gutter):
    pallet_width_px = standard_pallet_width
    pallet_height_px = border_rect.height() // 21 - (gutter * 2)

    pallet_rects = [QRect(x,
                          y,
                          pallet_width_px,
                          pallet_height_px),
                    QRect(x + pallet_width_px + gutter,
                          y,
                          pallet_width_px,
                          pallet_height_px),
                    QRect(x + 2 * (pallet_width_px + gutter),
                          y,
                          pallet_width_px,
                          pallet_height_px)]

    new_brush_offset = pallet_height_px + gutter
    return pallet_rects, new_brush_offset


def generate_120_120_120(x, y, standard_pallet_width, border_rect, gutter):
    pallet_width_px = standard_pallet_width
    pallet_height_px = border_rect.height() // 11 - (gutter * 2)

    pallet_rects = [QRect(x,
                          y,
                          pallet_width_px,
                          pallet_height_px),
                    QRect(x + pallet_width_px + gutter,
                          y,
                          pallet_width_px,
                          pallet_height_px),
                    QRect(x + 2 * (pallet_width_px + gutter),
                          y,
                          pallet_width_px,
                          pallet_height_px)]

    new_brush_offset = pallet_height_px + gutter
    return pallet_rects, new_brush_offset


def generate_120_120(x, y, _, border_rect, gutter):
    pallet_width_px = (border_rect.width() - gutter * 3) // 2
    pallet_height_px = int(round(border_rect.height() / 16.1)) - (gutter * 2)
    pallet_last_width_px = border_rect.width() - pallet_width_px - gutter * 3

    pallet_rects = [QRect(x,
                          y,
                          pallet_width_px,
                          pallet_height_px),
                    QRect(x + pallet_width_px + gutter,
                          y,
                          pallet_last_width_px,
                          pallet_height_px)]

    new_brush_offset = pallet_height_px + gutter
    return pallet_rects, new_brush_offset


def generate_120_120_60_60(x, y, standard_pallet_width, border_rect, gutter):
    pallet_width_px = standard_pallet_width
    p120_height_px = border_rect.height() // 11 - (gutter * 2)
    p60_height_px = (p120_height_px - gutter) // 2
    p60_last_height_px = p120_height_px - p60_height_px - gutter

    pallet_rects = [QRect(x,
                          y,
                          pallet_width_px,
                          p120_height_px),
                    QRect(x + pallet_width_px + gutter,
                          y,
                          pallet_width_px,
                          p120_height_px),
                    QRect(x + 2 * (pallet_width_px + gutter),
                          y,
                          pallet_width_px,
                          p60_height_px),
                    QRect(x + 2 * (pallet_width_px + gutter),
                          y + p60_height_px + gutter,
                          pallet_width_px,
                          p60_last_height_px)]

    new_brush_offset = p120_height_px + gutter
    return pallet_rects, new_brush_offset


def generate_17080_17080_120_60(x, y, standard_pallet_width, border_rect, gutter):
    pallet_width_px = standard_pallet_width
    p170_height_px = int(round(border_rect.height() / 7.45)) - (gutter * 2)
    p120_height_px = border_rect.height() // 11 - (gutter * 2)
    p60_height_px = p170_height_px - p120_height_px - gutter

    pallet_rects = [QRect(x,
                          y,
                          pallet_width_px,
                          p170_height_px),
                    QRect(x + pallet_width_px + gutter,
                          y,
                          pallet_width_px,
                          p170_height_px),
                    QRect(x + 2 * (pallet_width_px + gutter),
                          y,
                          pallet_width_px,
                          p120_height_px),
                    QRect(x + 2 * (pallet_width_px + gutter),
                          y + p120_height_px + gutter,
                          pallet_width_px,
                          p60_height_px)]

    new_brush_offset = p170_height_px + gutter
    return pallet_rects, new_brush_offset


def generate_17080_120_120_60_60(x, y, standard_pallet_width, border_rect, gutter):
    pallet_width_px = standard_pallet_width
    p170_height_px = int(round(border_rect.height() / 7.45)) - (gutter * 2)
    p120_height_px = border_rect.height() // 11 - (gutter * 2)
    p60_height_px = p170_height_px - p120_height_px - gutter

    pallet_rects = [QRect(x,
                          y,
                          pallet_width_px,
                          p170_height_px),
                    QRect(x + pallet_width_px + gutter,
                          y,
                          pallet_width_px,
                          p120_height_px),
                    QRect(x + 2 * (pallet_width_px + gutter),
                          y,
                          pallet_width_px,
                          p120_height_px),
                    QRect(x + pallet_width_px + gutter,
                          y + p120_height_px + gutter,
                          pallet_width_px,
                          p60_height_px),
                    QRect(x + 2 * (pallet_width_px + gutter),
                          y + p120_height_px + gutter,
                          pallet_width_px,
                          p60_height_px)]

    new_brush_offset = p170_height_px + gutter
    return pallet_rects, new_brush_offset


def generate_120_60_60_60_60(x, y, standard_pallet_width, border_rect, gutter):
    pallet_width_px = standard_pallet_width
    p120_height_px = border_rect.height() // 11 - (gutter * 2)
    p60_height_px = (p120_height_px - gutter) // 2
    p60_last_height_px = p120_height_px - p60_height_px - gutter

    pallet_rects = [QRect(x,
                          y,
                          pallet_width_px,
                          p120_height_px),
                    QRect(x + pallet_width_px + gutter,
                          y,
                          pallet_width_px,
                          p60_height_px),
                    QRect(x + 2 * (pallet_width_px + gutter),
                          y,
                          pallet_width_px,
                          p60_height_px),
                    QRect(x + pallet_width_px + gutter,
                          y + p60_height_px + gutter,
                          pallet_width_px,
                          p60_last_height_px),
                    QRect(x + 2 * (pallet_width_px + gutter),
                          y + p60_height_px + gutter,
                          pallet_width_px,
                          p60_last_height_px)]

    new_brush_offset = p120_height_px + gutter
    return pallet_rects, new_brush_offset


def generate_145_145_145(x, y, standard_pallet_width, border_rect, gutter):
    pallet_width_px = standard_pallet_width
    pallet_height_px = border_rect.height() // 9 - (gutter * 2)

    pallet_rects = [QRect(x,
                          y,
                          pallet_width_px,
                          pallet_height_px),
                    QRect(x + pallet_width_px + gutter,
                          y,
                          pallet_width_px,
                          pallet_height_px),
                    QRect(x + 2 * (pallet_width_px + gutter),
                          y,
                          pallet_width_px,
                          pallet_height_px)]

    new_brush_offset = pallet_height_px + gutter
    return pallet_rects, new_brush_offset


def generate_17080_17080_17080(x, y, standard_pallet_width, border_rect, gutter):
    pallet_width_px = standard_pallet_width
    pallet_height_px = int(round(border_rect.height() / 7.45)) - (gutter * 2)

    pallet_rects = [QRect(x,
                          y,
                          pallet_width_px,
                          pallet_height_px),
                    QRect(x + pallet_width_px + gutter,
                          y,
                          pallet_width_px,
                          pallet_height_px),
                    QRect(x + 2 * (pallet_width_px + gutter),
                          y,
                          pallet_width_px,
                          pallet_height_px)]

    new_brush_offset = pallet_height_px + gutter
    return pallet_rects, new_brush_offset


def generate_17090_145_145(x, y, _, border_rect, gutter):
    p17090_width_px = int(round((border_rect.width() - gutter * 2) / 2.7))
    p145_width_px = border_rect.width() - p17090_width_px - gutter * 3
    p17090_height_px = int(round(border_rect.height() / 7.45)) - (gutter * 2)
    p145_height_px = border_rect.height() // 15 - (gutter * 2)

    pallet_rects = [QRect(x,
                          y,
                          p17090_width_px,
                          p17090_height_px),
                    QRect(x + p17090_width_px + gutter,
                          y,
                          p145_width_px,
                          p145_height_px),
                    QRect(x + p17090_width_px + gutter,
                          y + p145_height_px + gutter,
                          p145_width_px,
                          p145_height_px)]

    new_brush_offset = p17090_height_px + gutter
    return pallet_rects, new_brush_offset


def generate_17090_17090_130_130_130(x, y, _, border_rect, gutter):
    p17090_width_px = int(round((border_rect.width() - gutter * 2) / 2.7))
    p130_width_px = border_rect.width() - p17090_width_px - gutter * 3
    p17090_height_px = int(round(border_rect.height() / 7.45)) - (gutter * 2)
    p130_height_px = int(round((p17090_height_px * 2 - gutter) / 3))
    p130_last_height_px = (p17090_height_px * 2 + gutter) - (p130_height_px + gutter) * 2

    pallet_rects = [QRect(x,
                          y,
                          p17090_width_px,
                          p17090_height_px),
                    QRect(x,
                          y + p17090_height_px + gutter,
                          p17090_width_px,
                          p17090_height_px),
                    QRect(x + p17090_width_px + gutter,
                          y,
                          p130_width_px,
                          p130_height_px),
                    QRect(x + p17090_width_px + gutter,
                          y + p130_height_px + gutter,
                          p130_width_px,
                          p130_height_px),
                    QRect(x + p17090_width_px + gutter,
                          y + (p130_height_px + gutter) * 2,
                          p130_width_px,
                          p130_last_height_px)]

    new_brush_offset = (p17090_height_px + gutter) * 2
    return pallet_rects, new_brush_offset


def generate_130_120_120(x, y, _, border_rect, gutter):
    p130_width_px = (border_rect.width() - gutter * 3) // 2
    p120_width_px = border_rect.width() - p130_width_px - gutter * 3
    p130_height_px = int(round(border_rect.height() / 9.4)) - (gutter * 2)
    p120_height_px = int(round(border_rect.height() / 16.1)) - (gutter * 2)

    pallet_rects = [QRect(x,
                          y,
                          p130_width_px,
                          p130_height_px),
                    QRect(x + p130_width_px + gutter,
                          y,
                          p120_width_px,
                          p120_height_px),
                    QRect(x + p130_width_px + gutter,
                          y + p120_height_px + gutter,
                          p120_width_px,
                          p120_height_px)]

    new_brush_offset = (p120_height_px * 2) + (gutter * 2)
    return pallet_rects, new_brush_offset


def generate_130_130(x, y, _, border_rect, gutter):
    pallet_width_px = (border_rect.width() - gutter * 3) // 2
    pallet_height_px = int(round(border_rect.height() / 9.4)) - (gutter * 2)

    pallet_rects = [QRect(x,
                          y,
                          pallet_width_px,
                          pallet_height_px),
                    QRect(x + pallet_width_px + gutter,
                          y,
                          pallet_width_px,
                          pallet_height_px)]

    new_brush_offset = pallet_height_px + gutter
    return pallet_rects, new_brush_offset


def generate_17080_60(x, y, _, border_rect, gutter):
    p17080_width_px = int(round((border_rect.width() - gutter * 3) / 1.35))
    p60_width_px = border_rect.width() - p17080_width_px - gutter * 3
    pallet_height_px = int(round(border_rect.height() / 16.3)) - (gutter * 2)

    pallet_rects = [QRect(x,
                          y,
                          p17080_width_px,
                          pallet_height_px),
                    QRect(x + p17080_width_px + gutter,
                          y,
                          p60_width_px,
                          pallet_height_px)]

    new_brush_offset = pallet_height_px + gutter
    return pallet_rects, new_brush_offset


def generate_17090_60(x, y, _, border_rect, gutter):
    p17090_width_px = int(round((border_rect.width() - gutter * 3) / 1.35))
    p60_width_px = border_rect.width() - p17090_width_px - gutter * 3
    p17090_height_px = int(round(border_rect.height() / 14.5)) - (gutter * 2)
    p60_height_px = int(round(border_rect.height() / 16.3)) - (gutter * 2)

    pallet_rects = [QRect(x,
                          y,
                          p17090_width_px,
                          p17090_height_px),
                    QRect(x + p17090_width_px + gutter,
                          y,
                          p60_width_px,
                          p60_height_px)]

    new_brush_offset = p17090_height_px + gutter
    return pallet_rects, new_brush_offset


def generate_23090(x, y, _, border_rect, gutter):
    pallet_width_px = border_rect.width() - gutter * 2
    pallet_height_px = int(round(border_rect.height() / 14.5)) - (gutter * 2)

    pallet_rects = [QRect(x,
                          y,
                          pallet_width_px,
                          pallet_height_px)]

    new_brush_offset = pallet_height_px + gutter
    return pallet_rects, new_brush_offset


generate = {
    (60, 60, 60): generate_60_60_60,
    (120, 120, 120): generate_120_120_120,
    (120, 120): generate_120_120,
    (120, 120, 60, 60): generate_120_120_60_60,
    (17080, 17080, 120, 60): generate_17080_17080_120_60,
    (17080, 120, 120, 60, 60): generate_17080_120_120_60_60,
    (120, 60, 60, 60, 60): generate_120_60_60_60_60,
    (145, 145, 145): generate_145_145_145,
    (17080, 17080, 17080): generate_17080_17080_17080,
    (17090, 145, 145): generate_17090_145_145,
    (17090, 17090, 130, 130, 130): generate_17090_17090_130_130_130,
    (130, 120, 120): generate_130_120_120,
    (130, 130): generate_130_130,
    (17080, 60): generate_17080_60,
    (17090, 60): generate_17090_60,
    (23090, ): generate_23090,
}
