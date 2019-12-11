import math


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


def circle_to_svg(c):
    return f"""
        <circle
            cx="{c.x}"
            cy="{c.y}"
            r="{c.radius}"
            fill="transparent"
            stroke="black"
        />
    """


def make_line_svg(
    x1, y1, x2, y2, stroke_width=10, stroke_color="red", stroke_linecap="round"
):
    return (
        f'<line x1="{round(x1, 4)}" y1="{round(y1, 4)}"'
        f' x2="{round(x2, 4)}" y2="{round(y2, 4)}"'
        f' stroke="{stroke_color}"'
        f' stroke-width="{stroke_width}"'
        f' stroke-linecap="{stroke_linecap}"/>'
    )


def make_arc_svg(
    pt1,
    pt2,
    radius,
    arc_flag,
    stroke_width=10,
    stroke_color="red",
    stroke_linecap="round",
):
    x1, y1 = pt1
    x2, y2 = pt2

    return (
        f'<path d="M {round(x1, 4)} {round(y1, 4)} A {round(radius, 4)}'
        f' {round(radius, 4)} 0 0 {arc_flag} {round(x2, 4)} {round(y2, 4)}"'
        f' fill="transparent"'
        f' stroke="{stroke_color}"'
        f' stroke-linecap="{stroke_linecap}"'
        f' stroke-width="{stroke_width}"/>'
    )


def choose_tangent_line(tl1, tl2):
    # this is pretty hacky but I have luxury of never running into edge cases
    return tl1 if tl1[0] < tl2[0] else tl2


def make_double_macaroni_connection_svg(
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
        make_line_svg(*p1, *p2, **{**bg_kwargs, "stroke_linecap": "round"})
        + make_arc_svg(**arc1_kwargs, **bg_kwargs, arc_flag=arc_flag)
        + make_arc_svg(**arc2_kwargs, **bg_kwargs, arc_flag=arc_flag)
        + make_line_svg(*p1, *p2, **fg_kwargs)
        + make_arc_svg(**arc1_kwargs, **fg_kwargs, arc_flag=arc_flag)
        + make_arc_svg(**arc2_kwargs, **fg_kwargs, arc_flag=arc_flag)
    )


if __name__ == "__main__":
    inner_svg = ""
    inner_svg += make_double_macaroni_connection_svg(
        x1=60,
        y1=60,
        x2=200,
        y2=200,
        radius=50,
        stroke_width=30,
        stroke_color="red",
        stroke_linecap="flat",
    )

    svg = ""
    if display_circles:
        svg = circle_to_svg(a) + circle_to_svg(b)


    with open("tangent_test.html", "w+") as text_file:
        text_file.write(
            f"""
                <!DOCTYPE html>
                <html>
                <body>
                <svg width="400" height="400">
                {inner_svg}
                </svg>
                </body>
                </html>
            """
        )
