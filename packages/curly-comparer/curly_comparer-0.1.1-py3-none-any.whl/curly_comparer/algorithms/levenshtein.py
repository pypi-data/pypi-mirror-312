from typing import Callable, TypeAlias
import numpy as np

CostFunction: TypeAlias = Callable[[str], float]
SubstitutionFunction: TypeAlias = Callable[[str, str], float]


def distace(str1: str, str2: str) -> int:
    """
    Computes the basic distance between two strings, assuming equal costs
     for insertion, deletion, and substitution.

    Parameters:
    - str1 (str): The first string.
    - str2 (str): The second string.

    Returns:
    - int: The computed distance between the two strings.
    """
    return int(weighted_distance(
        str1,
        str2,
        lambda x: 1,
        lambda x: 1,
        lambda x, y: 1
    ))


def weighted_distance(
        str1: str,
        str2: str,
        insertion_fn: CostFunction,
        deletion_fn: CostFunction,
        subs_fn: SubstitutionFunction
) -> float:
    """
    Computes the weighted distance between two strings using customizable 
    cost functions for insertion, deletion, and substitution.

    Parameters:
    - str1 (str): The first string.
    - str2 (str): The second string.
    - insertion_fn (CostFunction): A function to calculate the cost of 
      inserting a character.
    - deletion_fn (CostFunction): A function to calculate the cost of 
      deleting a character.
    - subs_fn (SubstitutionFunction): A function to calculate the cost of 
      substituting one character for another.

    Returns:
    - float: The weighted distance between the two strings.

    Notes:
    - The algorithm uses dynamic programming to compute the minimum cost
      of transforming one string into another.
    - Costs are derived from the provided functions, allowing flexible 
      customization of operation costs.
    """
    len1 = len(str1) + 1
    len2 = len(str2) + 1
    matrix = np.zeros((len1, len2), dtype=float)

    for i, c in enumerate(str1):
        matrix[i+1, 0] = matrix[i, 0] + deletion_fn(c)
    for j, c in enumerate(str2):
        matrix[0, j+1] = matrix[0, j] + insertion_fn(c)
    for j in range(1, len2):
        for i in range(1, len1):
            cost = (0 if str1[i-1] == str2[j-1]
                    else subs_fn(str1[i-1], str2[j-1])
                    )
            matrix[i, j] = min(
                matrix[i-1,   j] + deletion_fn(str2[j-1]),
                matrix[i,   j-1] + insertion_fn(str1[i-1]),
                matrix[i-1, j-1] + cost
            )
    return float(matrix[len1 - 1, len2 - 1])
