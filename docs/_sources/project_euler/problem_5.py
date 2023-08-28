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
# # Problem 5


# %%
from functools import reduce
from typing import Iterable

from project_euler import get_problem_description

get_problem_description(5)

# %% [markdown]
# So, I'm not sure how to solve this... but here goes nothing.

# %% [markdown]
# ## Hypothesis 1 - Find the prime numbers
#
# My first attempt will be to analyze the role that *prime numbers*
# have in this question. I am guessing that, if you find all the prime
# numbers between 1 and 10, and multiple them together, then you might get `2520`.
# Here goes nothing.

# %%
def is_prime(number: int) -> bool:
    """Simple (and inefficient) check to see if number is prime."""
    if number == 1:
        return False

    for i in range(2, number):
        if number % i == 0:
            return False
    else:
        return True


assert not is_prime(1)
assert is_prime(2)
assert is_prime(3)
assert not is_prime(4)

list(filter(is_prime, range(1, 11)))

# %% [markdown]
# Okay, I think we can assume our `is_prime` function works.
# Now let's see if our hypothesis is correct?

# %%


def multiply(num1, num2):
    return num1 * num2


reduce(multiply, filter(is_prime, range(1, 11)))

# %% [markdown]
# Okay, obviously there is something else going on...

# %% [markdown]
# Let's do a brute force solution to get a better idea of what's going on.

# %%
def brute_force_solution(number_range):
    n = 1
    while True:
        if not all(n % i == 0 for i in number_range):
            n += 1
        else:
            break
    return n


brute_force_solution(range(1, 11))

# %% [markdown]
# That was easy, but as we know,
# brute force solutions don't scale well...
# We're going to need a different approach!

# %% [markdown]
# # Hypothesis 2 - Start big, then simplify!
#
# Here's the gist of our strategy:
# 1. Start by multiplying all of our divisors together
#   * In the example, that would be numbers 1 - 10
# 2. Take this *very large* product, and try to simplify it
#   1. For every divisor, divide the large-product by the divisor
#   2. If the smaller-product is still divisible by all the divisors, then this simplified-product replaces the large-product
#   3. If none of the smaller-products are divisible by all divisors, then the large-product cannot be simplified
#   4. Repeat until product cannot be simplified

# %%


def is_divisible(num: int, divisor: int) -> bool:
    return num % divisor == 0


def are_all_divisible(num: int, divisors: Iterable[int]) -> bool:
    return all(is_divisible(num, d) for d in divisors)


def simplify(num: int, divisors: Iterable[int]) -> int:
    assert are_all_divisible(num, divisors)
    divisors_not_one = [d for d in divisors if d != 1]
    for d in divisors_not_one:
        new_num = num / d
        if are_all_divisible(new_num, divisors):
            print(f"{num} / {d} = {int(new_num)}")
            return simplify(int(new_num), divisors)
    else:
        return num


def solve(divisors):
    print("Divisors: ", divisors)
    # start by multiplying all divisors together
    # to get a large product
    large_product = reduce(multiply, divisors)
    print("Large product: ", large_product)

    return simplify(large_product, divisors)


# %% [markdown]
# Okay, let's try it...

# %%
solve(range(1, 11))

# %% [markdown]
# *WOW*, it worked! Now, let's try it with numbers 1 - 20.

# %%
solve(range(1, 21))
