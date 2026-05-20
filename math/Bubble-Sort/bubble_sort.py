def bubble_sort(arr):
    """
    Sorts a list in-place using the Bubble Sort algorithm.
    Returns the sorted list.
    """
    n = len(arr)
    for i in range(n):
        swapped = False
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j+1]:
                arr[j],arr[j+1]=arr[j+1],arr[j]
                swapped = True
        # If no two elements were swapped by inner loop , then break
        if not swapped:
            break
    return arr

def test_bubble_sort():
    """Background test cases to ensure logic accuracy before user input."""
    assert bubble_sort([64, 34, 25, 12, 22, 11, 90]) == [11, 12, 22, 25, 34, 64, 90]
    assert bubble_sort([5, 1, 4, 2, 8]) == [1, 2, 4, 5, 8]

if __name__ == "__main__":
    #Background testing execution
    test_bubble_sort()

    # --- USER INTERACTION SECTION ---
    print("=== Bubble Sort Interactive Tool ===")
    try:
        user_input = input("Enter numbers to sort seperated by spaces (e.g., 64 34 25) :")
        if not user_input.strip():
            print("Error: Input cannot be empty!")
        else:
            # Convert String Input  into  List of Integers
            arr=[int(x) for x in user_input.split()]
            print(f"Original list : {arr}")

            # Sort operation performed
            sorted_arr = bubble_sort(arr)
            print(f"Sorted list: {sorted_arr}")
    except ValueError:
        print("Error: Please enter valid integers only.")