# Curly Comparer

A lightweight Python package for advanced string comparison and distance calculation.

## Overview

`curly_comparer` provides flexible string comparison algorithms, primarily focusing on Levenshtein distance calculations with customizable cost functions.

## Features

- **Basic Levenshtein Distance**: Quick string comparison
- **Weighted Levenshtein Distance**: Customizable cost functions for:
  - Character insertions
  - Character deletions
  - Character substitutions

## Installation

Install `curly_comparer` using pip:

```bash
pip install curly_comparer
```

### Requirements

- Python 3.10+
- NumPy 2.1+

## Usage

### Basic Levenshtein Distance

```python
from curly_comparer.algorithms.levenshtein import distace

# Calculate distance between two strings
distance = distace("hello", "hallo")
print(distance)  # Outputs: 1
```

### Weighted Levenshtein Distance

```python
from curly_comparer.algorithms.levenshtein import weighted_distance

# Custom cost functions
def custom_insertion_cost(char):
    return 1.5  # Different cost for inserting characters

def custom_substitution_cost(char1, char2):
    return 2.0  # Custom substitution cost

distance = weighted_distance(
    "hello", 
    "hallo", 
    insertion_fn=custom_insertion_cost,
    deletion_fn=lambda x: 1.0,
    subs_fn=custom_substitution_cost
)
```

## Advanced Customization

The `weighted_distance` function allows complete flexibility in defining costs for string transformations:

- `insertion_fn`: Cost of inserting a character
- `deletion_fn`: Cost of deleting a character
- `subs_fn`: Cost of substituting one character for another

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Licensed under the Apache License 2.0

## Author

Pedro Lopez (pdihax@gmail.com)
