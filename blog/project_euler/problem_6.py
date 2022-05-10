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
# # Problem 6


# %%
from project_euler import get_problem_description

get_problem_description(6)

# %%
def sum_of_squares(numbers):
    return sum((num**2 for num in numbers))


def square_of_sum(numbers):
    return sum(numbers) ** 2


numbers = range(11)
assert sum_of_squares(numbers) == 385

assert square_of_sum(numbers) == 3025

# %%
numbers = range(101)
square_of_sum(numbers) - sum_of_squares(numbers)
