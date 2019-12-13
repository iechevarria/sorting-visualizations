import math

import svg_primitives


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius


def get_inner_tangents(xp, yp, x, y, r):
    """Gets both inner tangent points for one circle
    
    equations from http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm
    """
    xp_a = xp - x
    yp_b = yp - y
    xp_a_2 = xp_a ** 2
    yp_b_2 = yp_b ** 2
    r_2 = r ** 2

    denom = xp_a_2 + yp_b_2

    xt_pt1 = r_2 * xp_a
    xt_pt2 = r * yp_b * math.sqrt(xp_a_2 + yp_b_2 - r_2)

    xt1 = x + (xt_pt1 + xt_pt2) / denom
    xt2 = x + (xt_pt1 - xt_pt2) / denom

    yt_pt1 = r_2 * yp_b
    yt_pt2 = r * xp_a * math.sqrt(xp_a_2 + yp_b_2 - r_2)

    yt1 = y + (yt_pt1 - yt_pt2) / denom
    yt2 = y + (yt_pt1 + yt_pt2) / denom

    return (xt1, yt1), (xt2, yt2)


def get_tangent_lines(c1, c2):
    """Gets both inner tangent points for each circle"""
    # equations from http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm

    a = c1.x
    b = c1.y
    c = c2.x
    d = c2.y
    r0 = c1.radius
    r1 = c2.radius

    xp = (a * r0 + c * r1) / (r0 + r1)
    yp = (b * r0 + d * r1) / (r0 + r1)

    c1t1, c1t2 = get_inner_tangents(xp, yp, a, b, r0)
    c2t1, c2t2 = get_inner_tangents(xp, yp, c, d, r1)

    return (c1t1, c2t1), (c1t2, c2t2)


def choose_tangent_line(tl1, tl2):
    # this is pretty hacky but I have luxury of never running into edge cases
    return tl1 if tl1[0] < tl2[0] else tl2


def double_macaroni(
    x1,
    y1,
    x2,
    y2,
    radius,
    stroke_width=10,
    stroke_color="red",
    stroke_linecap="round",
    outline_width=1.5,
    display_circles=False,
):
    # make sure we're drawing from left to right (this is a shortcut)
    if x1 < x2:
        ax, ay, bx, by = x1, y1, x2, y2
    else:
        ax, ay, bx, by = x2, y2, x1, y1

    # set up circles for inner tangent calculations
    radius_midpoint = radius + (stroke_width / 2)
    a = Circle(ax + radius_midpoint, ay, radius_midpoint)
    b = Circle(bx - radius_midpoint, by, radius_midpoint)

    # get the points that define the tangent line we care about
    p1, p2 = choose_tangent_line(*get_tangent_lines(a, b))

    # set up kwargs for svg drawing
    arc1_kwargs = {
        "pt1": (ax, ay),
        "pt2": p1,
        "radius": a.radius,
    }
    arc2_kwargs = {
        "pt1": (bx, by),
        "pt2": p2,
        "radius": b.radius,
    }
    bg_kwargs = {
        "stroke_width": stroke_width + outline_width,
        "stroke_color": "white",
        "stroke_linecap": "flat",
    }
    fg_kwargs = {
        "stroke_width": stroke_width,
        "stroke_color": stroke_color,
        "stroke_linecap": stroke_linecap,
    }
    arc_flag = int(a.y > b.y)

    return (
        svg_primitives.line(*p1, *p2, **{**bg_kwargs, "stroke_linecap": "round"})
        + svg_primitives.arc(**arc1_kwargs, **bg_kwargs, arc_flag=arc_flag)
        + svg_primitives.arc(**arc2_kwargs, **bg_kwargs, arc_flag=arc_flag)
        + svg_primitives.line(*p1, *p2, **fg_kwargs)
        + svg_primitives.arc(**arc1_kwargs, **fg_kwargs, arc_flag=arc_flag)
        + svg_primitives.arc(**arc2_kwargs, **fg_kwargs, arc_flag=arc_flag)
    )
