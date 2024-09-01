import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Sorting algorithms
def bubble_sort(arr, ascending=True):
    steps = []
    n = len(arr)
    arr = arr.copy()
    for i in range(n):
        for j in range(0, n-i-1):
            if (ascending and arr[j] > arr[j+1]) or (not ascending and arr[j] < arr[j+1]):
                arr[j], arr[j+1] = arr[j+1], arr[j]
            steps.append(arr.copy())
    return arr, steps

def insertion_sort(arr, ascending=True):
    steps = []
    arr = arr.copy()
    for i in range(1, len(arr)):
        key = arr[i]
        j = i-1
        while j >= 0 and ((ascending and key < arr[j]) or (not ascending and key > arr[j])):
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        steps.append(arr.copy())
    return arr, steps

def selection_sort(arr, ascending=True):
    steps = []
    arr = arr.copy()
    for i in range(len(arr)):
        min_idx = i
        for j in range(i+1, len(arr)):
            if (ascending and arr[j] < arr[min_idx]) or (not ascending and arr[j] > arr[min_idx]):
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        steps.append(arr.copy())
    return arr, steps

def merge_sort(arr, ascending=True):
    steps = []

    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if (ascending and left[i] <= right[j]) or (not ascending and left[i] >= right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def sort(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = sort(arr[:mid])
        right = sort(arr[mid:])
        merged = merge(left, right)
        steps.append(merged.copy())
        return merged

    sorted_arr = sort(arr)
    return sorted_arr, steps

def quick_sort(arr, ascending=True):
    steps = []

    def sort(arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if (ascending and x < pivot) or (not ascending and x > pivot)]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if (ascending and x > pivot) or (not ascending and x < pivot)]
        result = sort(left) + middle + sort(right)
        steps.append(result.copy())
        return result

    sorted_arr = sort(arr)
    return sorted_arr, steps

def plot_steps(steps, algorithm_name):
    fig, ax = plt.subplots(figsize=(10, 6))
    for i, step in enumerate(steps):
        ax.plot(step, marker='o', label=f'Step {i+1}')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.legend()
    ax.set_title(f'{algorithm_name} Sorting Steps')
    ax.set_xlabel('Index')
    ax.set_ylabel('Value')
    st.pyplot(fig)

def get_algorithm_description(algorithm_name):
    descriptions = {
        "Bubble Sort": (
            "Bubble Sort repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order. "
            "The pass through the list is repeated until the list is sorted. This algorithm gets its name because smaller elements 'bubble' to the top of the list."
        ),
        "Insertion Sort": (
            "Insertion Sort builds the final sorted array one item at a time. It picks the next item and inserts it into the correct position within the sorted portion of the array. "
            "This process is repeated until the entire array is sorted."
        ),
        "Selection Sort": (
            "Selection Sort repeatedly selects the smallest (or largest, depending on the order) element from the unsorted portion of the list and moves it to the end of the sorted portion. "
            "This process is repeated for each position in the array until the array is sorted."
        ),
        "Merge Sort": (
            "Merge Sort divides the list into two halves, sorts each half, and then merges the two sorted halves back together. "
            "The divide-and-conquer approach helps in efficiently sorting the array by breaking it down into smaller, more manageable parts."
        ),
        "Quick Sort": (
            "Quick Sort selects a 'pivot' element from the array and partitions the other elements into two sub-arrays according to whether they are less than or greater than the pivot. "
            "The sub-arrays are then sorted recursively. The pivot element is placed in its correct position, and this process is repeated for the sub-arrays."
        )
    }
    return descriptions.get(algorithm_name, "Description not available.")

# Streamlit app
st.title('Sorting Algorithms Visualization By AV')

array_input = st.text_input('Enter an array (comma-separated):', '5, 2, 9, 1, 5, 6')
order = st.radio('Select order:', ('Ascending', 'Descending'))

if array_input:
    try:
        array = list(map(int, array_input.split(',')))
        ascending = order == 'Ascending'
    except ValueError:
        st.error('Invalid input. Please enter a valid array of integers.')
        st.stop()

    algorithm = st.selectbox('Choose a sorting algorithm:', ['Bubble Sort', 'Insertion Sort', 'Selection Sort', 'Merge Sort', 'Quick Sort'])

    if st.button('Sort'):
        if algorithm == 'Bubble Sort':
            sorted_array, steps = bubble_sort(array, ascending)
        elif algorithm == 'Insertion Sort':
            sorted_array, steps = insertion_sort(array, ascending)
        elif algorithm == 'Selection Sort':
            sorted_array, steps = selection_sort(array, ascending)
        elif algorithm == 'Merge Sort':
            sorted_array, steps = merge_sort(array, ascending)
        elif algorithm == 'Quick Sort':
            sorted_array, steps = quick_sort(array, ascending)

        st.write('Sorted Array:', sorted_array)
        st.write('Algorithm Description:', get_algorithm_description(algorithm))
        plot_steps(steps, algorithm)
