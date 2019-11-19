import math

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius



def create_macaroni(x, y, r1, r2):
    r = (r1 + r2) / 2
    return Circle(x, y, r)



def get_inner_tangent_points(xp, yp, x, y, r):
    # equations from http://www.ambrsoft.com/TrigoCalc/Circles2/Circles2Tangent_.htm

    xp_a = xp - x
    yp_b = yp - x
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
    return f'<circle cx="{c.x}" cy="{c.y}" r="{c.radius}" fill="transparent" stroke="black"/>'



def line_to_svg(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    return f'''
        <line x1="{round(x1, 4)}" y1="{round(y1, 4)}" 
        x2="{round(x2, 4)}" y2="{round(y2, 4)}"
        stroke-width="1" stroke="black"/>\n>
    '''



def arc_to_svg(pt1, pt2, r, case='lr'):
    x1, y1 = pt1
    x2, y2 = pt2
    arc_flag = 0 if case == 'lr' else 1

    return f'''
        <path d="
            M {round(x1, 4)} {round(y1, 4)}
            A {r} {r} 0 0 {arc_flag} {round(x2, 4)} {round(y2, 4)}" 
        fill="transparent" stroke="red" stroke-linecap="round"
        stroke-width="10"/>
    '''
    inner_svg += f'''
    '''



def choose_tangent_line(tl1, tl2, case='lr'):
    # this is pretty hacky, it should really be done relative to line that 
    # passes through the center of both circles. I just have the luxury of 
    # never running into edge cases.
    if case=='lr':
        return tl1 if tl1[0] < tl2[0] else tl2
    else:
        return tl1 if tl1[0] > tl2[0] else tl2



def get_arc_termini(c1, c2, case='lr'):
    if case=='lr':
        return (
            (c1.x - c1.radius, c1.y),
            (c2.x + c2.radius, c2.y)
        )
    else:
        return (
            (c1.x + c1.radius, c1.y),
            (c2.x - c2.radius, c2.y)
        )



if __name__=="__main__":
    a = create_macaroni(60, 60, 20, 30)
    b = create_macaroni(200, 200, 20, 30)
    # b = create_macaroni(200, 60, 20, 30)
    # a = create_macaroni(60, 200, 20, 30)

    case = 'lr'

    tangent_lines = get_inner_tangents(a, b)
    inner_svg = ''
    
    print(tangent_lines)

    p1, p2 = choose_tangent_line(tangent_lines[0], tangent_lines[1], case)
    inner_svg += line_to_svg(p1, p2)

    inner_svg += circle_to_svg(a)
    inner_svg += circle_to_svg(b)

    at1, at2 = get_arc_termini(a, b, case)

    inner_svg += arc_to_svg(at1, p1, a.radius, case)
    inner_svg += arc_to_svg(at2, p2, b.radius, case)

    with open("tangent_test.html", "w+") as text_file:
        text_file.write(f"""
            <!DOCTYPE html>
            <html>
            <body>
            <svg width="400" height="400">
            {inner_svg}
            </svg>
            </body>
            </html>
        """)
