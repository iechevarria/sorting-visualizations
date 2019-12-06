import random

import svg


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

    svg.generate(arr, "insertion_sort")


def bubble_sort(arr):
    flag = True
    while flag:
        flag = False
        for i in range(len(arr[-1]) - 1):
            if arr[-1][i] > arr[-1][i + 1]:
                arr = swap(arr, i, i + 1)
                flag = True

    svg.generate(arr, "bubble_sort")


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
    svg.generate(history, "quicksort_lomuto")


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
    svg.generate(history, "quicksort_hoare")


if __name__ == "__main__":
    list_length = 30
    list_to_sort = list(range(list_length))
    random.Random(777).shuffle(list_to_sort)

    insertion_sort([list_to_sort[:20]])
    bubble_sort([list_to_sort[:20]])
    quicksort_lomuto_svg(list_to_sort.copy())
    quicksort_hoare_svg(list_to_sort)
