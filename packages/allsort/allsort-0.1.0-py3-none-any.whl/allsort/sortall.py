def sortit(iterable, reverse_flag=False, key=None):
    """
    Sorts various iterable types such as dictionaries, lists, tuples, and sets.

    Parameters:
        iterable: The collection to sort (list, tuple, set, dict).
        reverse_flag (bool): Sort in descending order if True. Default is False.
        key (callable): A function specifying the sorting key. Default is None.

    Returns:
        The sorted collection. The type depends on the input.
    """
    if isinstance(iterable, dict):
        return dict(sorted(iterable.items(), key=lambda x: x[key], reverse=reverse_flag))
    elif isinstance(iterable, (list, tuple, set)):
        sorted_iterable = sorted(iterable, key=key, reverse=reverse_flag)
        if isinstance(iterable, tuple):
            return tuple(sorted_iterable)
        elif isinstance(iterable, set):
            return sorted_iterable  # Return as list, since sets are unordered
        return sorted_iterable
    else:
        raise TypeError(f"Unsupported type: {type(iterable).__name__}")
