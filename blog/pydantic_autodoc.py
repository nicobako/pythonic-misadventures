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
# # Autodocumenting Pydantic Models
#
# First, a shout-out to [pydantic](https://pydantic-docs.helpmanual.io/).
# *pydantic* is a wonderful tool that I find myself using quite often!
# Honestly, I probably use it too much... but who cares! I love *pydantic*!
#
#
# ## What do I mean by *autodocumenting*
#
# What I mean by *autodocumenting pydantic models* is:
# automatically setting the `__doc__` string of *pydantic models*.
#
# The idea originated from [this GitHub issue](https://github.com/samuelcolvin/pydantic/issues/638).
# Esentially, the idea is that, since the *pydantic* model already
# knows a lot of information about itself (such as the field types, descriptions, etc.),
# then why can't a model's `__doc__` string be created automatically by `pydantic`?
# Sounds like a reasonable thing, right?
#
# However, there are many reasons why it wouldn't be wise to
# integrate this functionality into *pydantic*.
# First of all, generating a *docstring* could be really expensive,
# and could decrease performance. Secondly, there is little consensus
# on how `__doc__` strings should be formatted.
# For example, some of the formatting styles are numpy-style, google-style, rst-style, etc.
#
#
# ## Some existing solutions
#
# This tutorial wouldn't be complete without first acknoweldging that there
# are existing tools that can generate documentation for *pydantic* models.
#
# Most notable of all is [autodoc_pydantic](https://github.com/mansenfranzen/autodoc_pydantic).
# This tool won't modify a *pydantic* model's `__doc__` string,
# but it wil arguably do more... it wiL generate really beautiful [Sphinx](https://www.sphinx-doc.org/en/master/contents.html)
# documentation for your *pydantic* classes!
#
# ```{warning}
# So, if you are already using *Sphinx* for documentation,
# then please consider using *autodoc_pydantic* instead of following the advice
# in this tutorial.
# ```

# %% [markdown]
# ## How *autodocumentation* will work
#
# Since we want this behaviour of *auto-generating* `__doc__` strings
# to effect all of our models, we will follow the advice given by *pydantic* on
# [how to change behaviour of models globally](https://pydantic-docs.helpmanual.io/usage/model_config/#change-behaviour-globally).
# We define our own *BaseModel* that provides us with the `__doc__` string functionality,
# and all our *models* will be *subclasses* of this *BaseModel*.
#
# We will also follow the advice from
# [this GitHub issue comment](https://github.com/samuelcolvin/pydantic/issues/638#issuecomment-535701292)
# (which was also mentioned above) for *how* to implement this `__doc__` string functionality.
# The idea is, since all of our models will be *subclasses* of a custom *BaseModel*,
# then we can take advantage of `__init_subclass__` to perform the set the `__doc__` string
# of all subclasses.
#

# %% [markdown]
# ### Pydantic autodoc template
#
# This is the *template* of what our solution will look like.
# There are many ways to solve this problem, but this *template* will
# serve as our starting point.

# %%
import pydantic as pd
from typing import Type


def generate_docs(cls: Type[pd.BaseModel]) -> str:
    doc = "Auto-generated docs!\n"
    doc += f"Model name : {cls.__name__}\n"
    doc += f"Fields: {', '.join(cls.__fields__)}\n"
    return doc


class BaseModel(pd.BaseModel):
    def __init_subclass__(cls: Type[pd.BaseModel]) -> None:
        cls.__doc__ = generate_docs(cls)


class Person(BaseModel):
    name: str
    age: int


print(Person.__doc__)

# %% [markdown]
# You'll see that there is a *free function* which takes a
# *BaseModel Class*, and generates the *doc-string* for that class.
# We define a custom *BaseModel* for our project.
# In the `__init_subclass__` function the `__doc__` string gets set.
# All of our *models* inherit from this *BaseModel*
# and will thereby have their *docstrings* set automatically!

# %% [markdown]
# ### One More Example
#
# Let's go a little crazy and do some more interesting stuff!

# %%
import pydantic as pd
from typing import Type


class AutoDocBase(pd.BaseModel):
    class Doc:
        short_description: str
        long_description: str


def generate_docs(cls: Type[AutoDocBase]) -> str:
    doc = ""
    doc += f"# {cls.__name__}\n\n"
    doc += f"{cls.Doc.short_description}\n\n"
    doc += f"{cls.Doc.long_description}\n\n"
    doc += "## Fields\n\n"
    for name, field in cls.__fields__.items():
        field_info: pd.fields.FieldInfo = field.field_info
        doc += f"### {name}\n\n"
        doc += f"{field_info.description}\n\n"
        for constraint in field_info.get_constraints():
            doc += (
                f"* constraint : `{constraint} = {getattr(field_info, constraint)}`\n\n"
            )

    return doc


class BaseModel(AutoDocBase):
    def __init_subclass__(cls: Type[AutoDocBase]) -> None:
        cls.__doc__ = generate_docs(cls)


class Person(BaseModel):
    class Doc:
        short_description = "Short description of a Person."
        long_description = "Long description of a person."

    name: str = pd.Field(
        ..., description="Name of a person.", regex=r"[A-Z][a-zA-Z\s]+"
    )
    age: int = pd.Field(..., description="Age of a person.", gt=0, lt=150)


print(Person.__doc__)

# %%
from rich.markdown import Markdown

Markdown(Person.__doc__)

# %% [markdown]
# ## Conclusion
#
# So, I hope you've seen that it's pretty easy to customize the look and feel
# of the `__doc__` string for your *pydantic* models.
#
# But, **please**, use [autodoc_pydantic](https://github.com/mansenfranzen/autodoc_pydantic) instead.
# since it integrates really nicely into *Sphinx* documentation.
# Besides, do people really look at the `__doc__` string anymore?
# They are much more likely to browse the *Sphinx* documentation.
