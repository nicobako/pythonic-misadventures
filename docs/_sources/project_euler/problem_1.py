# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.5
#   kernelspec:
#     display_name: nicobako_blog
#     language: python
#     name: nicobako_blog
# ---

# %% [markdown]
# # Problem 1


# %%
from typing import Iterable

from project_euler import get_problem_description

get_problem_description(1)

# %% [markdown]
# This problem is perhaps the simplest on project euler.
# First, let's devise a method for determining if a number is a multiple of another number.

# %%
def is_multiple_of(
    multiple: int,
    number: int,
) -> bool:
    return number % multiple == 0


# %% [markdown]
# Let's see this function in action.

# %%
assert is_multiple_of(5, 5)

# %%
assert not is_multiple_of(2, 5)

# %% [markdown]
# Now, we should check our function with the simple question answer provided above.

# %%


def is_multiple_of_3_or_5(number: int) -> bool:
    return is_multiple_of(3, number) or is_multiple_of(5, number)


def get_numbers_multiple_of_3_or_5(numbers: Iterable[int]) -> Iterable[int]:
    return filter(is_multiple_of_3_or_5, (n for n in numbers))


sum(get_numbers_multiple_of_3_or_5(range(10)))

# %% [markdown]
# Our code looks good so far!

# %%
sum(get_numbers_multiple_of_3_or_5(range(1000)))

# %% [markdown]
# And our answer is correct!
