from pallet_rect_class import PalletRect
import constants

color = constants.PALLET_COLORS


def gen_60_60_60(x, y, _, gutter, dimensions):
    p60_width = dimensions["standard_width"]
    p60_height = dimensions["v-60-height"]

    pallet_rects = [PalletRect(x, y, p60_width, p60_height, color=color["60"]),
                    PalletRect(x + p60_width + gutter, y, p60_width, p60_height, color=color["60"]),
                    PalletRect(x + 2 * (p60_width + gutter), y, p60_width, p60_height, color=color["60"])]

    brush_offset = p60_height + gutter
    return pallet_rects, brush_offset


def gen_120_120_120(x, y, _, gutter, dimensions):
    p120_width = dimensions["standard_width"]
    p120_height = dimensions["v-120-height"]

    pallet_rects = [PalletRect(x, y, p120_width, p120_height, color=color["120"]),
                    PalletRect(x + p120_width + gutter, y, p120_width, p120_height, color=color["120"]),
                    PalletRect(x + 2 * (p120_width + gutter), y, p120_width, p120_height, color=color["120"])]

    brush_offset = p120_height + gutter
    return pallet_rects, brush_offset


def gen_120_120(x, y, border_rect, gutter, dimensions):
    p120_width = dimensions["h-120-width"]
    p120_height = dimensions["h-120-height"]
    p120_last_width = border_rect.width() - p120_width - gutter * 3

    pallet_rects = [PalletRect(x, y, p120_width, p120_height, color=color["120"]),
                    PalletRect(x + p120_width + gutter, y, p120_last_width, p120_height, color=color["120"])]

    brush_offset = p120_height + gutter
    return pallet_rects, brush_offset


def gen_120_120_60_60(x, y, _, gutter, dimensions):
    p120_width = dimensions["standard_width"]
    p120_height = dimensions["v-120-height"]
    p60_height = (p120_height - gutter) // 2
    p60_last_height = p120_height - p60_height - gutter

    pallet_rects = [PalletRect(x, y, p120_width, p120_height, color=color["120"]),
                    PalletRect(x + p120_width + gutter, y, p120_width, p120_height, color=color["120"]),
                    PalletRect(x + 2 * (p120_width + gutter), y, p120_width, p60_height, color=color["60"]),
                    PalletRect(x + 2 * (p120_width + gutter), y + p60_height + gutter, p120_width, p60_last_height, color=color["60"])]

    brush_offset = p120_height + gutter
    return pallet_rects, brush_offset


def gen_17080_17080_120_60(x, y, _, gutter, dimensions):
    pallet_width = dimensions["standard_width"]
    p170_height = dimensions["v-17080-height"]
    p120_height = dimensions["v-120-height"]
    p60_height = p170_height - p120_height - gutter

    pallet_rects = [PalletRect(x, y, pallet_width, p170_height, color=color["17080"]),
                    PalletRect(x + pallet_width + gutter, y, pallet_width, p170_height, color=color["17080"]),
                    PalletRect(x + 2 * (pallet_width + gutter), y, pallet_width, p120_height, color=color["120"]),
                    PalletRect(x + 2 * (pallet_width + gutter), y + p120_height + gutter, pallet_width, p60_height, color=color["60"])]

    brush_offset = p170_height + gutter
    return pallet_rects, brush_offset


def gen_17080_120_120_60_60(x, y, _, gutter, dimensions):
    pallet_width = dimensions["standard_width"]
    p170_height = dimensions["v-17080-height"]
    p120_height = dimensions["v-120-height"]
    p60_height = p170_height - p120_height - gutter

    pallet_rects = [PalletRect(x, y, pallet_width, p170_height, color=color["17080"]),
                    PalletRect(x + pallet_width + gutter, y, pallet_width, p120_height, color=color["120"]),
                    PalletRect(x + 2 * (pallet_width + gutter), y, pallet_width, p120_height, color=color["120"]),
                    PalletRect(x + pallet_width + gutter, y + p120_height + gutter, pallet_width, p60_height, color=color["60"]),
                    PalletRect(x + 2 * (pallet_width + gutter), y + p120_height + gutter, pallet_width, p60_height, color=color["60"])]

    brush_offset = p170_height + gutter
    return pallet_rects, brush_offset


def gen_120_60_60_60_60(x, y, _, gutter, dimensions):
    pallet_width = dimensions["standard_width"]
    p120_height = dimensions["v-120-height"]
    p60_height = (p120_height - gutter) // 2
    p60_last_height = p120_height - p60_height - gutter

    pallet_rects = [PalletRect(x, y, pallet_width, p120_height, color=color["120"]),
                    PalletRect(x + pallet_width + gutter, y, pallet_width, p60_height, color=color["60"]),
                    PalletRect(x + 2 * (pallet_width + gutter), y, pallet_width, p60_height, color=color["60"]),
                    PalletRect(x + pallet_width + gutter, y + p60_height + gutter, pallet_width, p60_last_height, color=color["60"]),
                    PalletRect(x + 2 * (pallet_width + gutter), y + p60_height + gutter, pallet_width, p60_last_height, color=color["60"])]

    brush_offset = p120_height + gutter
    return pallet_rects, brush_offset


def gen_145_145_145(x, y, _, gutter, dimensions):
    p145_width = dimensions["standard_width"]
    p145_height = dimensions["v-145-height"]

    pallet_rects = [PalletRect(x, y, p145_width, p145_height, color=color["145"]),
                    PalletRect(x + p145_width + gutter, y, p145_width, p145_height, color=color["145"]),
                    PalletRect(x + 2 * (p145_width + gutter), y, p145_width, p145_height, color=color["145"])]

    brush_offset = p145_height + gutter
    return pallet_rects, brush_offset


def gen_17080_17080_17080(x, y, _, gutter, dimensions):
    p17080_width = dimensions["standard_width"]
    p17080_height = dimensions["v-17080-height"]

    pallet_rects = [PalletRect(x, y, p17080_width, p17080_height, color=color["17080"]),
                    PalletRect(x + p17080_width + gutter, y, p17080_width, p17080_height, color=color["17080"]),
                    PalletRect(x + 2 * (p17080_width + gutter), y, p17080_width, p17080_height, color=color["17080"])]

    brush_offset = p17080_height + gutter
    return pallet_rects, brush_offset


def gen_17090_145_145(x, y, border_rect, gutter, dimensions):
    p17090_width = dimensions["v-17090-width"]
    p17090_height = dimensions["v-17080-height"]
    p145_width = border_rect.width() - p17090_width - gutter * 3
    p145_height = dimensions["h-145-height"]

    pallet_rects = [PalletRect(x, y, p17090_width, p17090_height, color=color["17090"]),
                    PalletRect(x + p17090_width + gutter, y, p145_width, p145_height, color=color["145"]),
                    PalletRect(x + p17090_width + gutter, y + p145_height + gutter, p145_width, p145_height, color=color["145"])]

    brush_offset = p17090_height + gutter
    return pallet_rects, brush_offset


def gen_17090_17090_130_130_130(x, y, border_rect, gutter, dimensions):
    p17090_width = dimensions["v-17090-width"]
    p17090_height = dimensions["v-17080-height"]
    p130_width = border_rect.width() - p17090_width - gutter * 3
    p130_height = int(round((p17090_height * 2 - gutter) / 3))
    p130_last_height = (p17090_height * 2 + gutter) - (p130_height + gutter) * 2

    pallet_rects = [PalletRect(x, y, p17090_width, p17090_height, color=color["17090"]),
                    PalletRect(x, y + p17090_height + gutter, p17090_width, p17090_height, color=color["17090"]),
                    PalletRect(x + p17090_width + gutter, y, p130_width, p130_height, color=color["130"]),
                    PalletRect(x + p17090_width + gutter, y + p130_height + gutter, p130_width, p130_height, color=color["130"]),
                    PalletRect(x + p17090_width + gutter, y + (p130_height + gutter) * 2, p130_width, p130_last_height, color=color["130"])]

    brush_offset = (p17090_height + gutter) * 2
    return pallet_rects, brush_offset


def gen_130_120_120(x, y, border_rect, gutter, dimensions):
    p130_width = dimensions["v-130-width"]
    p130_height = dimensions["v-130-height"]
    p120_width = border_rect.width() - p130_width - gutter * 3
    p120_height = dimensions["h-120-height"]

    pallet_rects = [PalletRect(x, y, p130_width, p130_height, color=color["130"]),
                    PalletRect(x + p130_width + gutter, y, p120_width, p120_height, color=color["120"]),
                    PalletRect(x + p130_width + gutter, y + p120_height + gutter, p120_width, p120_height, color=color["120"])]

    brush_offset = (p120_height * 2) + (gutter * 2)
    return pallet_rects, brush_offset


def gen_130_130(x, y, border_rect, gutter, dimensions):
    p130_width = dimensions["v-130-width"]
    p130_height = dimensions["v-130-height"]
    p130_last_width = border_rect.width() - p130_width - gutter * 3

    pallet_rects = [PalletRect(x, y, p130_width, p130_height, color=color["130"]),
                    PalletRect(x + p130_width + gutter, y, p130_last_width, p130_height, color=color["130"])]

    brush_offset = p130_height + gutter
    return pallet_rects, brush_offset


def gen_17080_60(x, y, border_rect, gutter, dimensions):
    p17080_width = dimensions["h-17080-width"]
    p60_width = border_rect.width() - p17080_width - gutter * 3
    pallet_height = dimensions["h-17080-height"]

    pallet_rects = [PalletRect(x, y, p17080_width, pallet_height, color=color["17080"]),
                    PalletRect(x + p17080_width + gutter, y, p60_width, pallet_height, color=color["60"])]

    brush_offset = pallet_height + gutter
    return pallet_rects, brush_offset


def gen_17090_60(x, y, border_rect, gutter, dimensions):
    p17090_width = dimensions["h-17090-width"]
    p17090_height = dimensions["h-17090-height"]
    p60_width = border_rect.width() - p17090_width - gutter * 3
    p60_height = dimensions["h-60-height"]

    pallet_rects = [PalletRect(x, y, p17090_width, p17090_height, color=color["17090"]),
                    PalletRect(x + p17090_width + gutter, y, p60_width, p60_height, color=color["60"])]

    brush_offset = p17090_height + gutter
    return pallet_rects, brush_offset


def gen_23090(x, y, _, gutter, dimensions):
    pallet_width_px = dimensions["h-23090-width"]
    pallet_height_px = dimensions["h-23090-height"]

    pallet_rects = [PalletRect(x, y, pallet_width_px, pallet_height_px, color=color["23090"])]

    brush_offset = pallet_height_px + gutter
    return pallet_rects, brush_offset


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
    (23090, ): gen_23090,
}
