from typing import List # this is used to add type hints for List type

def remove_from_list(my_list: List[int], index: int) -> List[int]:
    """
    Removes an element from the list at the specified index.
    If the index is out of bounds, it does nothing.
    Args:
        my_list (List[int]): The list from which to remove the element.
        index (int): The index of the element to remove.
    Returns:
        List[int]: The modified list after removal.
    """
    # Check if the index is within the bounds of the list
    if index < 0 or index >= len(my_list):
        return my_list  # Return the list unchanged if index is out of bounds
    
    # Remove the element at the specified index
    del my_list[index]
    return my_list


def pop_n_from_list(my_list: List[int], n: int) -> List[int]:
    """
    Pops the last n elements from the list.
    If n is greater than the length of the list, it pops all elements.
    Args:
        my_list (List[int]): The list from which to pop elements.
        n (int): The number of elements to pop from the end of the list.
    Returns:
        List[int]: The modified list after popping elements.
    """
    # Check if n is greater than the length of the list
    if n >= len(my_list):
        return []  # Return an empty list if n is greater than or equal to length
    
    # Pop the last n elements from the list
    return my_list[:-n]  # Return the list excluding the last n elements



# don't modify below this line
print(remove_from_list([1, 2, 3, 4, 5], 2))
print(remove_from_list([1, 2, 3, 4, 5], 0))
print(remove_from_list([1, 2, 3, 4, 5], 4))

print(pop_n_from_list([1, 2, 3, 4, 5], 2))
print(pop_n_from_list([1, 2, 3, 4, 5], 0))
print(pop_n_from_list([1, 2, 3, 4, 5], 5))
