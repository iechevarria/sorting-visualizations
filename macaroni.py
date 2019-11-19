import math

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius



class Macaroni:
    def __init__(self, x, y, r1, r2):
        self.inner = Circle(x, y, r1)
        self.outer = Circle(x, y, r2)



def get_inner_tangent_points(xp, yp, x, y, r):
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



def get_macaroni_tangents(macaroni_1, macaroni_2):
    tl1, tl2 = get_inner_tangents(macaroni_1.inner, macaroni_2.outer)
    tl3, tl4 = get_inner_tangents(macaroni_1.outer, macaroni_2.inner)

    return tl1, tl2, tl3, tl4



def circle_to_svg(c):
    return f'<circle cx="{c.x}" cy="{c.y}" r="{c.radius}" fill="transparent" stroke="black"/>'



if __name__=="__main__":
    a = Macaroni(60, 60, 20, 30)
    b = Macaroni(200, 200, 20, 30)

    tangent_lines = get_macaroni_tangents(a, b)
    
    inner_svg = ''

    for tl in tangent_lines:
        p1, p2 = tl
        x1, y1 = p1
        x2, y2 = p2
        inner_svg += f'''
            <line x1="{round(x1, 2)}" y1="{round(y1, 2)}" 
            x2="{round(x2, 2)}" y2="{round(y2, 2)}"
            stroke-width="1" stroke="black"/>\n
        '''
    
    inner_svg += circle_to_svg(a.inner)
    inner_svg += circle_to_svg(a.outer)
    inner_svg += circle_to_svg(b.inner)
    inner_svg += circle_to_svg(b.outer)

    inner_svg += f'''            
        <line x1="178" y1="211.6" 
        x2="82" y2="48.2"
        stroke-width="10" stroke="pink" stroke-linecap="round"/>\n
    '''
    inner_svg += f'''<path d="
        M 200 225
        A 25 25 0 0 1 178 211.6
        " fill="transparent" stroke="red" stroke-linecap="round"
        stroke-width="10"/>
    '''

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
