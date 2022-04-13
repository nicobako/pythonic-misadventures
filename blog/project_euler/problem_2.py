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
# # Problem 2

# %%
from project_euler import get_problem_description

get_problem_description(2)

# %% [markdown]
# Let's begin by creating a *generator* which will
# create our fibonacci numbers

# %%
def fibonacci():
    first_term = 1
    yield first_term
    second_term = 2
    yield second_term
    while True:
        next_term = first_term + second_term
        yield next_term
        first_term = second_term
        second_term = next_term


# %% [markdown]
# Let's try it out.

# %%
f = fibonacci()
[next(f) for _ in range(10)]

# %% [markdown]
# Looks like our numbers match!
# Now let's see if we can solve the problem.

# %%
total = 0
f = fibonacci()
while num := next(f):
    if num < 4e6 and num % 2 == 0:
        total += num
    if num > 4e6:
        break

print(total)

# %% [markdown]
# And our result looks correct!
