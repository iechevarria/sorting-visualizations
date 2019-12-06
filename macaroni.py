import math


class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius


def get_inner_tangent_points(xp, yp, x, y, r):
    # equations from http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm

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


def get_inner_tangents(c1, c2):
    # equations from http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm

    a = c1.x
    b = c1.y
    c = c2.x
    d = c2.y
    r0 = c1.radius
    r1 = c2.radius

    xp = (a * r0 + c * r1) / (r0 + r1)
    yp = (b * r0 + d * r1) / (r0 + r1)

    c1t1, c1t2 = get_inner_tangent_points(xp, yp, a, b, r0)
    c2t1, c2t2 = get_inner_tangent_points(xp, yp, c, d, r1)

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


def line_to_svg(pt1, pt2, stroke_width=10, stroke_color="red", stroke_linecap="round"):
    x1, y1 = pt1
    x2, y2 = pt2

    return (
        f'<line x1="{round(x1, 4)}" y1="{round(y1, 4)}"'
        f' x2="{round(x2, 4)}" y2="{round(y2, 4)}"'
        f' stroke="{stroke_color}"'
        f' stroke-width="{stroke_width}"'
        f' stroke-linecap="{stroke_linecap}"/>'
    )


def arc_to_svg(
    pt1, pt2, r, arc_flag, stroke_width=10, stroke_color="red", stroke_linecap="round"
):
    x1, y1 = pt1
    x2, y2 = pt2

    return (
        f'<path d="M {round(x1, 4)} {round(y1, 4)} A {round(r, 4)}'
        f' {round(r, 4)} 0 0 {arc_flag} {round(x2, 4)} {round(y2, 4)}"'
        f' fill="transparent"'
        f' stroke="{stroke_color}"'
        f' stroke-linecap="{stroke_linecap}"'
        f' stroke-width="{stroke_width}"/>'
    )


def choose_tangent_line(tl1, tl2):
    # this is pretty hacky, it should really be done relative to line that
    # passes through the center of both circles. I just have the luxury of
    # never running into edge cases.
    return tl1 if tl1[0] < tl2[0] else tl2


def get_double_macaroni_connection_svg(
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

    radius_midpoint = radius + (stroke_width / 2)
    a = Circle(ax + radius_midpoint, ay, radius_midpoint)
    b = Circle(bx - radius_midpoint, by, radius_midpoint)

    arc_flag = int(a.y > b.y)

    tangent_lines = get_inner_tangents(a, b)
    p1, p2 = choose_tangent_line(tangent_lines[0], tangent_lines[1])

    svg = ""

    if display_circles:
        svg += circle_to_svg(a) + circle_to_svg(b)

    # background
    svg += line_to_svg(p1, p2, stroke_width + outline_width, "white", "round")
    svg += arc_to_svg(
        (ax, ay), p1, a.radius, arc_flag, stroke_width + outline_width, "white", "flat"
    )
    svg += arc_to_svg(
        (bx, by), p2, b.radius, arc_flag, stroke_width + outline_width, "white", "flat"
    )

    # foreground
    svg += line_to_svg(p1, p2, stroke_width, stroke_color, stroke_linecap)
    svg += arc_to_svg(
        (ax, ay), p1, a.radius, arc_flag, stroke_width, stroke_color, stroke_linecap
    )
    svg += arc_to_svg(
        (bx, by), p2, b.radius, arc_flag, stroke_width, stroke_color, stroke_linecap
    )

    return svg


if __name__ == "__main__":
    inner_svg = ""
    inner_svg += get_double_macaroni_connection_svg(
        x1=60,
        y1=60,
        x2=200,
        y2=200,
        radius=50,
        stroke_width=30,
        stroke_color="red",
        stroke_linecap="flat",
    )

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
