def insertion_sort_history(arr):
    history = [arr.copy()]

    i = 1
    while i < len(arr):
        j = i
        while j > 0 and arr[j - 1] > arr[j]:
            arr[j], arr[j - 1] = arr[j - 1], arr[j]
            history.append(arr.copy())
            j -= 1
        i += 1

    return history


def bubble_sort_history(arr):
    history = [arr.copy()]

    flag = True
    while flag:
        flag = False
        for i in range(len(arr) - 1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                history.append(arr.copy())
                flag = True

    return history


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


def quicksort_lomuto_history(arr):
    history = [arr.copy()]
    quicksort_lomuto(arr, history, 0, len(arr) - 1)
    return history


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


def quicksort_hoare_history(arr):
    history = [arr.copy()]
    quicksort_hoare(arr, history, 0, len(arr) - 1)
    return history
