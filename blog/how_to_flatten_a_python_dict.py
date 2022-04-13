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
# # How to Flatten a Python `dict`

# %% [markdown]
# We've all had that moment.
# We are trying to analyze a nested `dict`.
# We start by peeling away the layers one at a time,
# hoping to find the values.
# Sometimes this approach works...
# and sometimes you need to **flatten it!**.
#
# ## What you'll learn
#
# * How to flatten a JSON-compatible `dict` in Python
# * How to customize the flattening function to work with other objects
#
# ## What do I mean by *flattening*?
#
# There are many ways to *flatten* a `dict`, but what I
# want is this:
#
# * I want to start with an JSON object
#
#   * a nested `dict` whose keys are all strings
#   * or a `list`
#
# * I want all of the *values*
# * I also want all of the *paths* to those values
# * I want the *paths* to be valid Python code
#
# <div class="alert alert-info">
#     NOTE: This implementation only works for JSON-friendly
#     data: i.e. all keys in the dict are strings.
#     If you have anything else to flatten please keep reading
#     to learn how to customize the function for your needs.
# </div>
#
# ### Example
#
# Imagine a classroom with students. If I wanted to store the *roster*
# in a `dict` it could look like this:

# %%
roster = {
    "students": [
        {
            "age": 25,
            "name": "John",
        },
        {
            "age": 30,
            "name": "Jane",
        },
    ],
    "class": {
        "title": "Philosophy 101",
        "id": 12345,
    },
}

# %% [markdown]
# Here are the *paths* and *values* I want, stored in a `pandas.DataFrame`
# because `pandas` rocks!

# %%
import pandas as pd

# %%
roster_flattened_expected = pd.DataFrame(
    {
        "path": [
            'roster["students"][0]["age"]',
            'roster["students"][0]["name"]',
            'roster["students"][1]["age"]',
            'roster["students"][1]["name"]',
            'roster["class"]["title"]',
            'roster["class"]["id"]',
        ],
        "value": [
            25,
            "John",
            30,
            "Jane",
            "Philosophy 101",
            12345,
        ],
    }
)
roster_flattened_expected

# %% [markdown]
# ## Let's Flatten Something!
#
# Let's create our function that does the actual flattening.
# I'll define it here, and explain parts of it later.

# %%
from typing import Any, Dict, List, Tuple, Union

JsonObject = Union[Dict, List]

Path = str
Paths = List[Path]

Value = Any
Values = List[Value]


def flatten_json(*, obj: JsonObject, name: str) -> Tuple[Paths, Values]:
    def do_flattening(
        *,
        obj: JsonObject,
        path: Path,
        paths: Paths,
        values: Values,
    ):
        obj_type = type(obj)

        if dict == obj_type:
            for key, value in obj.items():
                new_path = f'{path}["{key}"]'
                new_obj = value
                do_flattening(
                    obj=new_obj,
                    path=new_path,
                    paths=paths,
                    values=values,
                )

        elif list == obj_type:
            for i, item in enumerate(obj):
                new_path = f"{path}[{i}]"
                new_obj = item
                do_flattening(
                    obj=new_obj,
                    path=new_path,
                    paths=paths,
                    values=values,
                )

        else:
            paths.append(path)
            values.append(obj)

    paths = []
    values = []

    do_flattening(
        obj=obj,
        path=name,
        paths=paths,
        values=values,
    )

    return paths, values


def flatten_json_to_df(**kwargs) -> pd.DataFrame:

    paths, values = flatten_json(**kwargs)

    return pd.DataFrame({"path": paths, "value": values})


# %% [markdown]
# ### About our Function
#
# We name it `flatten_json` to be more explicit in that it **only** is expected
# to flatten JSON-compliant dictionaries whose keys are strings.
#
# You'll see that all the logic is contained in a nested function `do_flattening`.
# Values can be one of:
#
# * another JSON object (`dict`)
# * a list
# * a value
#
# We check the type of the *value*. If it is a `dict` or a `list`
# then we must dive deeper into the object. If it is anything else, then we
# have reached a *terminal value*. As we traverse the object we keep updating
# *path* until when we reach a *terminal value*, at which point we append our *path* and *value*
# to the list of *paths* and *values*, respectively.
#
# ### Testing our Function
#
# Let's see if our function can correctly flatten our *roster*.

# %%
roster_flattened = flatten_json_to_df(obj=roster, name="roster")
roster_flattened

# %%
assert roster_flattened.equals(roster_flattened_expected)

# %% [markdown]
# Yay! Looks like it works.
#
# ### Using our Function with Real Data
#
# Let's get some real JSON data from the internet
# and see if it works...

# %%
import requests

honolulu_bus_routes = requests.get(
    url="https://data.honolulu.gov/api/views/s5c7-gtgi/rows.json?accessType=DOWNLOAD"
).json()
honolulu_bus_routes_df = flatten_json_to_df(
    obj=honolulu_bus_routes, name="honolulu_bus_routes"
)
honolulu_bus_routes_df

# %% [markdown]
# Great, it works! What do we do with this now?
# I don't know... that's your problem to figure out.
#
# ## Customizing the Flattening Function
#
# You may be thinking, "Great, but I need a slightly different function".
# The good news is that you can use the flattening function as a template
# and customize it for your custom needs. The logic of the function
# should remain relatively unchanged regardless of the type of object.
#
# ### Flattening Paths
#
# For example, imagine if we just wanted to get all of the files
# residing in a specific folder:

from pathlib import Path
# %%
from typing import List


def flatten_path(*, path: Path) -> List[Path]:
    def do_flattening(
        *,
        path: Path,
        paths: List[Path],
    ):
        if path.is_dir():
            for new_path in path.iterdir():
                do_flattening(
                    path=new_path,
                    paths=paths,
                )
        else:
            paths.append(path)

    paths = []

    do_flattening(
        path=path,
        paths=paths,
    )

    return paths


flatten_path(path=Path("./"))

# %% [markdown]
# You'll see that we can express our logic as:
#
# * if our path is a directory
#
#   * get all the entries in the directory and flatten those
#
# * if our path is a file (i.e. a *terminal value*)
#
#   * append our file to the list of paths
#
# The nice thing about `Path` objects is that we don't need
# any complicated objects for updating the *path* as we traverse
# the directories since this information is inherently part of a `Path` object.
# Hooray for making things easy!
#
# ## Conclusion
#
# I hope you've learnt a great deal about flattening nesting
# `dict`s in Python, and I also hope you can take that knowledge
# with you in your quest to flatten other objects.
#
# Thanks for reading!
