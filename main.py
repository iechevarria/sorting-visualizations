import random
from itertools import chain

from matplotlib import cm

from macaroni import get_double_macaroni_connection_svg


def unnest_svg_list(svg_list):
    return "\n".join(list(chain(*svg_list)))


def print_svg(history, filename):
    num_vals = len(history[0])

    # customize the colormap and create correspondence
    cmap = cm.get_cmap("magma_r")
    colors = {
        val: tuple(int(v * 255) for v in cmap(0.075 + 0.8 * idx / (num_vals - 1)))[:3]
        for idx, val in enumerate(history[-1])
    }

    # pad history at the beginning and end to make my life easier
    padded_history = history.copy()
    padded_history.insert(0, padded_history[0])
    padded_history.append(padded_history[-1])

    # set up some params
    spacing = 2
    line_width = 6
    line_height = 24
    y_offset = line_width / 2

    # compute svg dimensions
    total_width = (num_vals) * spacing + num_vals * line_width
    total_height = (len(padded_history) - 1) * line_height + 2 * y_offset

    # compute curves
    min_curve_radius_denominator = 5
    max_curve_radius = line_height - line_width - spacing
    min_curve_radius = (line_height - line_width) / min_curve_radius_denominator
    curve_radius_delta = max_curve_radius - min_curve_radius

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

    def get_drawing_coords(coords):
        p1, p2 = coords
        x1, y1 = p1
        x2, y2 = p2

        xa1 = x1 * spacing + (x1 + 0.5) * line_width
        ya1 = y1 * line_height + y_offset
        xa2 = x2 * spacing + (x2 + 0.5) * line_width
        ya2 = y2 * line_height + y_offset

        return xa1, ya1, xa2, ya2

    def get_color(val):
        r, g, b = colors[val]
        return f"rgba({r},{g},{b},1.0)"

    def make_straight_path(val, coords):
        x1, y1, x2, y2 = get_drawing_coords(coords)
        stroke_color = get_color(val)
        return (
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"'
            f'stroke="{stroke_color}" stroke-linecap="round"'
            f'stroke-width="{line_width}" />'
        )

    def make_curved_path(val, coords):
        x1, y1, x2, y2 = get_drawing_coords(coords)
        stroke_color = get_color(val)

        distance = abs(coords[0][0] - coords[1][0])
        curve_radius = min_curve_radius + curve_radius_delta / distance

        return get_double_macaroni_connection_svg(
            x1,
            y1,
            x2,
            y2,
            curve_radius,
            stroke_width=line_width,
            stroke_color=stroke_color,
        )

    # actually make the svgs
    straight_paths = unnest_svg_list(
        [
            [make_straight_path(val, coord) for coord in coords]
            for val, coords in straights.items()
        ]
    )
    curved_paths = unnest_svg_list(
        [
            [make_curved_path(val, coord) for coord in coords[1:-1]]
            for val, coords in swaps.items()
        ]
    )

    with open(f"{filename}.html", "w+") as text_file:
        text_file.write(
            f"""
                <!DOCTYPE html>
                <html>
                <body>
                <svg width="{total_width}" height="{total_height}">
                {straight_paths + curved_paths}
                </svg>
                </body>
                </html>
            """
        )


def swap(history, idx1, idx2):

    arr = history[-1].copy()
    tmp = arr[idx1]
    arr[idx1] = arr[idx2]
    arr[idx2] = tmp

    return history + [arr]


def insertion_sort(arr):
    i = 1

    while i < len(arr[0]):
        j = i
        while j > 0 and arr[-1][j - 1] > arr[-1][j]:
            arr = swap(arr, j, j - 1)
            j -= 1
        i += 1

    print_svg(arr, "insertion_sort")


def bubble_sort(arr):
    flag = True
    while flag:
        flag = False
        for i in range(len(arr[-1]) - 1):
            if arr[-1][i] > arr[-1][i + 1]:
                arr = swap(arr, i, i + 1)
                flag = True

    print_svg(arr, "bubble_sort")


def partition_lomuto(arr, history, low, high):
    pivot = arr[high]
    i = low
    for j in range(low, high):
        if arr[j] < pivot:
            if j != i:
                arr[i], arr[j] = arr[j], arr[i]
                history.append(arr.copy())
            i += 1

    if i != high:
        arr[i], arr[high] = arr[high], arr[i]
        history.append(arr.copy())
    return i


def quicksort_lomuto(arr, history, low, high):
    if low < high:
        p = partition_lomuto(arr, history, low, high)
        quicksort_lomuto(arr, history, low, p - 1)
        quicksort_lomuto(arr, history, p + 1, high)


def quicksort_lomuto_svg(arr):
    history = [arr.copy()]
    quicksort_lomuto(arr, history, 0, len(arr) - 1)
    print_svg(history, "quicksort_lomuto")


def partition_hoare(arr, history, low, high):
    pivot = arr[low]
    i = low - 1
    j = high + 1
    while True:
        i += 1
        while arr[i] < pivot:
            i += 1

        j -= 1
        while arr[j] > pivot:
            j -= 1

        if i >= j:
            return j

        arr[i], arr[j] = arr[j], arr[i]
        history.append(arr.copy())


def quicksort_hoare(arr, history, low, high):
    if low < high:
        split_index = partition_hoare(arr, history, low, high)
        quicksort_hoare(arr, history, low, split_index)
        quicksort_hoare(arr, history, split_index + 1, high)


def quicksort_hoare_svg(arr):
    history = [arr.copy()]
    quicksort_hoare(list_to_sort, history, 0, len(arr) - 1)
    print_svg(history, "quicksort_hoare")


if __name__ == "__main__":
    list_length = 80
    list_to_sort = list(range(list_length))
    random.Random(777).shuffle(list_to_sort)

    insertion_sort([list_to_sort[:20]])
    bubble_sort([list_to_sort[:20]])
    quicksort_lomuto_svg(list_to_sort.copy())
    quicksort_hoare_svg(list_to_sort)
