# json_category_counter

A Python package to count categories and tests from a JSON file.

## Installation

You can install this package using pip:


## Usage

```python
from json_category_counter import count_category_and_total

json_file = 'path_to_your_json_file.json'
key_one = 'Mathematicstest'

total, category_dict = count_category_and_total(json_file, key_one)

print("Total count:", total)
print("Category counts:", category_dict)
