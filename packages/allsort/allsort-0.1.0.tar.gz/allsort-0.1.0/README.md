# allsort

`allsort` is a Python utility for sorting various iterable types such as dictionaries, lists, tuples, and sets. It's lightweight, easy to use, and works with custom sorting criteria.

## Installation

Install with pip:

```bash
pip install allsort
```

## Usage

````
from allsort.allsort import sortit

# Sorting a list
nums = [3, 1, 4, 1, 5]
print(sortit(nums))  # [1, 1, 3, 4, 5]

# Sorting a dictionary by values
data = {'a': 3, 'b': 1, 'c': 2}
print(sortit(data, key=1))  # {'b': 1, 'c': 2, 'a': 3}

# Sorting a set
nums_set = {3, 1, 4, 1, 5}
print(sortit(nums_set))  # [1, 3, 4, 5]
````

## Features

1. Sorts lists, tuples, sets, and dictionaries.

2. Supports ascending and descending orders.

3. Allows custom sorting keys for flexibility.

Contributions
---
Contributions are welcome! Fork the repository and submit a pull request.

