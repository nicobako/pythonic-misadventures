# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.5
#   kernelspec:
#     display_name: nicobako.github.io
#     language: python
#     name: nicobako.github.io
# ---

# %% [markdown]
# # Problem 4

# %%
from itertools import product
from typing import Tuple

from project_euler import get_problem_description

get_problem_description(4)

# %% [markdown]
# Okay, first let's create a function for checking if
# a number is a palindrome.

# %%
def is_palindrome(number: int) -> bool:
    num_as_string = str(number)
    return num_as_string == num_as_string[::-1]


assert is_palindrome(101)
assert is_palindrome(9009)
assert not is_palindrome(123)

# %% [markdown]
# Okay, so good so far.

# %% [markdown]
# Now let's try and solve the problem.

# %%


def product_if_palindrome(numbers: Tuple[int, int]) -> int:
    prod = numbers[0] * numbers[1]
    if is_palindrome(prod):
        return prod
    else:
        return 0


three_digit_numbers = range(100, 1000)
max(
    product_if_palindrome(prod)
    for prod in product(three_digit_numbers, three_digit_numbers)
)

# %% [markdown]
# And the answer is correct!
