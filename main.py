from macaroni import get_double_macaroni_connection_svg

import random

from matplotlib import cm

cmap = cm.get_cmap("plasma_r")



def print_svg(history, filename):
    num_vals = len(history[0])
    colors = {
        val: tuple(int(v * 255) for v in cmap(idx / (num_vals - 1)))[:3]
        for idx, val in enumerate(history[-1])
    }

    # pad history at the beginning and end to make my life easier
    padded_history = history.copy()
    padded_history.insert(0, padded_history[0])
    padded_history.append(padded_history[-1])

    # set up some params
    spacing = 3
    line_width = 10
    line_height = 50
    curve_radius = line_height / 5
    total_width = (num_vals + 2) * spacing + num_vals * line_width
    total_height = len(padded_history) * line_height

    svg = ""

    for idx, tup in enumerate(zip(padded_history, padded_history[1:])):
        pre, post = tup

        swap_paths = ""
        straight_paths = ""

        for preidx, val in enumerate(pre):
            r, g, b = colors[val]
            postidx = post.index(val)

            x1 = preidx * spacing + (preidx + 1) * line_width
            y1 = (idx + 0.25) * line_height
            x2 = postidx * spacing + (postidx + 1) * line_width
            y2 = (idx + 1.25) * line_height

            stroke_color = f"rgba({r},{g},{b},1.0)"

            if preidx == postidx:
                straight_paths = (
                    f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"'
                    f'stroke="{stroke_color}" stroke-linecap="round"'
                    'stroke-width="10" />'
                ) + straight_paths

            else:
                swap_paths = (
                    get_double_macaroni_connection_svg(
                        x1, y1, x2, y2, curve_radius, stroke_color=stroke_color
                    )
                    + swap_paths
                )

        svg += straight_paths + swap_paths

    with open(f"{filename}.html", "w+") as text_file:
        text_file.write(
            f"""
                <!DOCTYPE html>
                <html>
                <body>
                <svg width="{total_width}" height="{total_height}">
                {svg}
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


def partition(arr, history, low, high):
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


def quicksort(arr, history, low, high):
    if low < high:
        split_index = partition(arr, history, low, high)
        quicksort(arr, history, low, split_index)
        quicksort(arr, history, split_index + 1, high)


def quicksort_svg(arr):
    history = [arr.copy()]
    quicksort(list_to_sort, history, 0, len(arr) - 1)
    print_svg(history, "quicksort")


if __name__ == "__main__":
    list_length = 40
    list_to_sort = list(range(list_length))
    random.Random(10).shuffle(list_to_sort)

    insertion_sort([list_to_sort[:20]])
    bubble_sort([list_to_sort[:20]])
    quicksort_svg(list_to_sort)
