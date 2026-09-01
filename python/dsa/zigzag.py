def solution(numbers):
    """
    Determines the zigzag pattern in a list of numbers.
    A zigzag pattern is defined as a sequence where the middle element is either 
    greater than both its neighbors or less than both its neighbors.
    Args:
        numbers (list of int): A list of integers to be analyzed.
    Returns:
        list of int: A list of 1s and 0s where 1 indicates a zigzag pattern at that 
        position and 0 indicates no zigzag pattern.
    Example:
        >>> solution([1, 3, 2, 4, 5])
        [1, 1, 0]
    """
    # Initialize the result list
    arr = []
    
    # Loop through the list starting from the second element to the second last element
    for i in range(1, len(numbers) - 1):
        # Check if the current element forms a zigzag pattern
        if (numbers[i - 1] < numbers[i] > numbers[i + 1]) or \
           (numbers[i - 1] > numbers[i] < numbers[i + 1]):
            arr.append(1)  # Append 1 if it is a zigzag pattern
        else:
            arr.append(0)  # Append 0 if it is not a zigzag pattern
    
    return arr
