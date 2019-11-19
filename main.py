from random import shuffle

from matplotlib import cm

cmap = cm.get_cmap('winter')


list_to_sort = list(range(30))
shuffle(list_to_sort)


# data
class knowledge_arr():
    def __init__(self, arr):
        self.arr = arr
        self.looking_idxs = set()
        self.length = len(arr)
        self.arr_history = [arr.copy()]


    def get(self, idx):
        self.looking_idxs.add(idx)
        return self.arr[idx]


    def gt(self, idx1, idx2):
        return self.get(idx1) > self.get(idx2)


    def reset(self):
        self.looking_idxs = set()

    
    def swap(self, idx1, idx2):
        self.looking_idxs.add(idx1)
        self.looking_idxs.add(idx2)
        tmp = self.arr[idx1]
        self.arr[idx1] = self.arr[idx2]
        self.arr[idx2] = tmp
        self.arr_history.append(self.arr.copy())


# display stuff
def underline_all_chars(str_):
    ret = ''
    for char in str_:
        ret += '\u0332' + char 

    return ret


def print_annoted_arr(k_arr):
    print(
        ' ' + ' '.join([
            underline_all_chars(str(t)) if idx in k_arr.looking_idxs else str(t)
            for idx, t in enumerate(k_arr.arr)
        ])
    )


def print_svg(k_arr):
    num_vals = len(k_arr.arr)
    colors = {
        val: tuple(int(v * 255) for v in cmap(idx / (num_vals - 1)))[:3]
        for idx, val in enumerate(k_arr.arr)
    }

    # pad history at the beginning and end to make my life easier
    padded_history = k_arr.arr_history.copy()
    padded_history.insert(0, padded_history[0])
    padded_history.append(padded_history[-1])

    spacing = 2
    line_width = 10
    line_height = 40
    total_width = (num_vals + 1) * spacing + num_vals * line_width
    total_height = (len(padded_history) - 1) * line_height

    svg = f"""
        <!DOCTYPE html>
        <html>
        <body>
        <svg width="{total_width}" height="{total_height}">
    """

    for idx, tup in enumerate(zip(padded_history, padded_history[1:])):
        pre, post = tup

        paths = ''

        for preidx, val in enumerate(pre):
            r, g, b = colors[val]
            postidx = post.index(val)
            x1 = preidx * spacing + (preidx) * line_width 
            y1 = idx * line_height
            x2 = preidx * spacing + (preidx + 1) * line_width
            y2 = idx * line_height
            x3 = postidx * spacing + (postidx + 1) * line_width
            y3 = (idx + 1) * line_height
            x4 = postidx * spacing + (postidx) * line_width
            y4 = (idx + 1) * line_height

            paths = (
                f'<path d="M {x1},{y1} L {x2},{y2} L {x3},{y3} L {x4},{y4}' 
                f'L {x1},{y1} z" fill="rgba({r},{g},{b},1.0)"/>\n'
            ) + paths

        svg += paths

    svg += """
        </svg>
        </body>
        </html>
    """
    with open("output.html", "w+") as text_file:
        text_file.write(svg)



# sorting
def sort_thing(thing):
    i = 1

    while i < thing.length:
        thing.reset()
        j = i
        while j > 0 and thing.gt(j - 1, j):
            print_annoted_arr(thing)
            thing.reset()

            thing.swap(j, j-1)
            j -= 1

            print_annoted_arr(thing)
            thing.reset()

        i += 1    
        print_annoted_arr(thing)


    print_svg(thing)



if __name__=='__main__':
    sort_thing(knowledge_arr(list_to_sort))