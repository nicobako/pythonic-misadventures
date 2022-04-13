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
# # Problem 3

# %%
from math import remainder
from typing import Iterable

from project_euler import get_problem_description

get_problem_description(3)

# %% [markdown]
# First, we need to write some logic for determining whether
# a number is a *prime number* or not.

# %%
def is_prime_number(number: int) -> bool:
    if number == 1:
        return False
    if number == 2:
        return True
    # first, check if number is even
    if number % 2 == 0:
        return False
    low_num = 2
    high_num = number
    while low_num < high_num:
        high_num = number // low_num
        remainder = number % low_num
        if remainder == 0 and low_num != high_num:
            return False
        low_num += 1
    return True


# %% [markdown]
# Let's see this function in action

# %%
list(filter(is_prime_number, range(50)))

# %% [markdown]
# Looks good to me...

# %% [markdown]
# Now, we need a function for getting the factors of a number

# %%
def get_factors(number: int) -> Iterable[int]:
    factors = set([1, number])
    low_num = 2
    high_num = number
    while low_num <= high_num:
        remainder = number % low_num
        if remainder == 0:
            factors.add(low_num)
            high_num = number // low_num
            factors.add(high_num)
        low_num += 1
    return sorted(factors)


# %% [markdown]
# Let's see this function in action.

# %%
assert [1, 2, 4] == list(get_factors(4))

# %%
assert [1, 2, 4, 5, 10, 20, 25, 50, 100] == list(get_factors(100))

# %% [markdown]
# Looks good, I think.

# %% [markdown]
# Let's see if we can recreate the list mentioned above,
# the prime factors of `13195`.

# %%
assert [5, 7, 13, 29] == list(filter(is_prime_number, get_factors(13195)))

# %% [markdown]
# Looks good!

# %% [markdown]
# Okay, now the real test...

# %%
max(filter(is_prime_number, get_factors(600851475143)))

# %% [markdown]
# Yay! Solution is correct!
