from itertools import chain

from matplotlib import cm

from macaroni import make_line_svg, make_double_macaroni_connection_svg


def unnest_svg_list(svg_list):
    return "\n".join(list(chain(*svg_list)))


def get_color_dict(sorted_list, cmap="magma_r"):
    num_vals = len(sorted_list)

    cmap = cm.get_cmap("magma_r")
    return {
        val: tuple(int(v * 255) for v in cmap(0.075 + 0.8 * idx / (num_vals - 1)))[:3]
        for idx, val in enumerate(sorted_list)
    }


def get_color(color_dict, val):
    r, g, b = color_dict[val]
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


def indices_to_coords(indices, spacing, line_width, line_height, y_offset):
    """Transforms list indices into svg coordinates"""

    p1, p2 = indices
    x1, y1 = p1
    x2, y2 = p2

    xt1 = x1 * spacing + (x1 + 0.5) * line_width
    yt1 = y1 * line_height + y_offset
    xt2 = x2 * spacing + (x2 + 0.5) * line_width
    yt2 = y2 * line_height + y_offset

    return xt1, yt1, xt2, yt2


def make_straight_path(val, indices, color_dict, transform_kwargs):
    """Creates an svg of a straight path"""

    coords = indices_to_coords(indices, **transform_kwargs)
    stroke_color = get_color(color_dict, val)
    stroke_width = transform_kwargs["line_width"]
    stroke_linecap = "round"

    return make_line_svg(*coords, stroke_width, stroke_color, stroke_linecap)


def make_swap_path(
    val, indices, color_dict, transform_kwargs, min_curve_radius, curve_radius_delta
):
    """Creates an svg of a swap path"""

    x1, y1, x2, y2 = indices_to_coords(indices, **transform_kwargs)
    stroke_color = get_color(color_dict, val)

    distance = abs(indices[0][0] - indices[1][0])
    curve_radius = min_curve_radius + curve_radius_delta / distance
    stroke_width = transform_kwargs["line_width"]

    return make_double_macaroni_connection_svg(
        x1,
        y1,
        x2,
        y2,
        curve_radius,
        stroke_width=stroke_width,
        stroke_color=stroke_color,
    )


def make_straight_paths(straights, color_dict, transform_kwargs):
    return unnest_svg_list(
        [
            [
                make_straight_path(val, indices, color_dict, transform_kwargs)
                for indices in list_indices
            ]
            for val, list_indices in straights.items()
        ]
    )


def make_swap_paths(swaps, mode, color_dict, transform_kwargs, curve_kwargs):
    a, b = (0, 1) if mode == "over" else (1, 0)
    return unnest_svg_list(
        [
            [
                make_swap_path(
                    val, indices, color_dict, transform_kwargs, **curve_kwargs
                )
                for indices in list_indices[1:-1]
                if indices[a][0] < indices[b][0]
            ]
            for val, list_indices in swaps.items()
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

    # set up colors
    color_dict = get_color_dict(history[-1])

    # get path histories
    swaps, straights = get_swaps_and_straights(history)

    # actually make the svgs
    swap_kwargs = {
        "swaps": swaps,
        "color_dict": color_dict,
        "transform_kwargs": transform_kwargs,
        "curve_kwargs": curve_kwargs,
    }
    under_swap_paths = make_swap_paths(mode="under", **swap_kwargs)
    over_swap_paths = make_swap_paths(mode="over", **swap_kwargs)
    straight_paths = make_straight_paths(straights, color_dict, transform_kwargs)

    # compute svg dimensions
    num_vals = len(history[0])
    total_width = (num_vals) * spacing + num_vals * line_width
    total_height = (len(history) + 1) * line_height + 2 * y_offset

    with open(f"{filename}.svg", "w+") as text_file:
        text_file.write(
            f'<svg role="img" height="{int(total_height)}" width="{int(total_width)}"'
            f' xmlns="http://www.w3.org/2000/svg">'
            + straight_paths
            + under_swap_paths
            + over_swap_paths
            + "</svg>\n"
        )
