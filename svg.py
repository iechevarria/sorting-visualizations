from itertools import chain

from matplotlib import cm

from macaroni import get_double_macaroni_connection_svg


def unnest_svg_list(svg_list):
    return "\n".join(list(chain(*svg_list)))


def get_color_dict(end_state):
    num_vals = len(end_state)

    cmap = cm.get_cmap("magma_r")
    return {
        val: tuple(int(v * 255) for v in cmap(0.075 + 0.8 * idx / (num_vals - 1)))[:3]
        for idx, val in enumerate(end_state)
    }


def get_color(colors, val):
    r, g, b = colors[val]
    return f"rgba({r},{g},{b},1.0)"


def get_swaps_and_straights(history):
    # pad history at the beginning and end to make my life easier
    padded_history = history.copy()
    padded_history.insert(0, padded_history[0])
    padded_history.append(padded_history[-1])

    # transform the padded history into something a little more useful
    movements = {
        val: [(arr.index(val), i) for i, arr in enumerate(padded_history)]
        for val in padded_history[0]
    }
    swaps = {
        val: (
            [((None, None), movement[0])]
            + [(a, b) for a, b in zip(movement, movement[1:]) if a[0] != b[0]]
            + [(movement[-1], (None, None))]
        )
        for val, movement in movements.items()
    }
    straights = {
        val: [(a[1], b[0]) for a, b in zip(swap, swap[1:]) if a[1] != b[0]]
        for val, swap in swaps.items()
    }

    return swaps, straights


def transform_coords(coords, spacing, line_width, line_height, y_offset):
    p1, p2 = coords
    x1, y1 = p1
    x2, y2 = p2

    xt1 = x1 * spacing + (x1 + 0.5) * line_width
    yt1 = y1 * line_height + y_offset
    xt2 = x2 * spacing + (x2 + 0.5) * line_width
    yt2 = y2 * line_height + y_offset

    return xt1, yt1, xt2, yt2


def make_straight_path(val, coords, color_dict, transform_kwargs):
    x1, y1, x2, y2 = transform_coords(coords, **transform_kwargs)
    stroke_color = get_color(color_dict, val)
    stroke_width = transform_kwargs["line_width"]

    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"'
        f'stroke="{stroke_color}" stroke-linecap="round"'
        f'stroke-width="{stroke_width}" />'
    )


def make_swap_path(
    val, coords, color_dict, transform_kwargs, min_curve_radius, curve_radius_delta
):
    x1, y1, x2, y2 = transform_coords(coords, **transform_kwargs)
    stroke_color = get_color(color_dict, val)

    distance = abs(coords[0][0] - coords[1][0])
    curve_radius = min_curve_radius + curve_radius_delta / distance
    stroke_width = transform_kwargs["line_width"]

    return get_double_macaroni_connection_svg(
        x1,
        y1,
        x2,
        y2,
        curve_radius,
        stroke_width=stroke_width,
        stroke_color=stroke_color,
    )


def make_swap_paths(swaps, mode, color_dict, transform_kwargs, curve_kwargs):
    a, b = (0, 1) if mode == "over" else (1, 0)
    return unnest_svg_list(
        [
            [
                make_swap_path(val, coord, color_dict, transform_kwargs, **curve_kwargs)
                for coord in coords[1:-1]
                if coord[a][0] < coord[b][0]
            ]
            for val, coords in swaps.items()
        ]
    )


def generate(
    history,
    filename,
    spacing=2,
    line_width=6,
    line_height=24,
    min_curve_radius_denominator=5,
):

    # set up some params
    y_offset = line_width / 2
    transform_kwargs = {
        "spacing": spacing,
        "line_width": line_width,
        "line_height": line_height,
        "y_offset": y_offset,
    }

    # compute curve stuff
    min_curve_radius = (line_height - line_width) / min_curve_radius_denominator
    curve_kwargs = {
        "min_curve_radius": min_curve_radius,
        "curve_radius_delta": line_height - line_width - spacing - min_curve_radius,
    }

    colors = get_color_dict(history[-1])
    swaps, straights = get_swaps_and_straights(history)

    # actually make the svgs
    straight_paths = unnest_svg_list(
        [
            [
                make_straight_path(val, coord, colors, transform_kwargs)
                for coord in coords
            ]
            for val, coords in straights.items()
        ]
    )
    swap_kwargs = {
        "swaps": swaps,
        "color_dict": colors,
        "transform_kwargs": transform_kwargs,
        "curve_kwargs": curve_kwargs,
    }
    under_swap_paths = make_swap_paths(mode="under", **swap_kwargs)
    over_swap_paths = make_swap_paths(mode="over", **swap_kwargs)

    # compute svg dimensions
    num_vals = len(history[0])
    total_width = (num_vals) * spacing + num_vals * line_width
    total_height = (len(history) + 1) * line_height + 2 * y_offset

    with open(f"{filename}.svg", "w+") as text_file:
        text_file.write(
            f"""
                <svg width="{total_width}" height="{total_height}">
                {straight_paths + under_swap_paths + over_swap_paths}
                </svg>
            """
        )
