# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.5
#   kernelspec:
#     display_name: pythonic_misadventures
#     language: python
#     name: pythonic_misadventures
# ---

# %% [markdown]
# # Problem 7


# %%
from project_euler import get_problem_description

get_problem_description(7)


# %%
def prime_numbers(n):
    assert n >= 1

    numbers = []

    def store(number):
        numbers.append(number)
        return numbers[-1]

    yield store(2)

    cur_number = 3
    while len(numbers) < n:
        if all(cur_number % n != 0 for n in numbers):
            yield store(cur_number)
        cur_number += 1


assert [2, 3, 5, 7, 11, 13] == list(prime_numbers(6))


def last(it):
    for i in it:
        pass
    return i


last(prime_numbers(10_001))
