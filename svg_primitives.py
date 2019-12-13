def circle(circle):
    return (
        f'<circle cx="{circle.x}" cy="{circle.y}" r="{circle.radius}"'
        'fill="transparent" stroke="black"/>'
    )


def line(x1, y1, x2, y2, stroke_width=10, stroke_color="red", stroke_linecap="round"):
    return (
        f'<line x1="{round(x1, 4)}" y1="{round(y1, 4)}"'
        f' x2="{round(x2, 4)}" y2="{round(y2, 4)}"'
        f' stroke="{stroke_color}"'
        f' stroke-width="{stroke_width}"'
        f' stroke-linecap="{stroke_linecap}"/>'
    )


def arc(
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
