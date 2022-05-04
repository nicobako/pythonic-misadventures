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
# # On Good Documentation
#
# No matter what your role, whether you're a manager,
# or you're fresh-out-of-college, chances are you need to write some documentation.
#
# We need to write documentation for all sorts of reasons.
# Sometimes we need to document our progress on a task, or the steps of a process,
# or how-to use a tool.
#
# Sometimes our documentation is in the form of a word document,
# presentation slides, a formal report, or a simple `README.txt`.
#
# Most of the time, however, we don't enjoy writing documentation...
# we see it as a means to an end.
# The thought of *writing documentation* sounded like a bore.
#
# It took me a while to realize just how important writing documentation is,
# and that, when we set up our *documentation infrastructure* properly,
# we can *actually have fun writing good documentation*!
#
# ## Blogging is a Form of Documentation
#
# I first began writing this blog with the intention of learning
# important skills for creating *professional-level* documentation.
#
# But, before I ever wrote any *decent* documentation,
# I wrote **a lot** of **bad** documentation.
# I learned a lot along the way.

# ## Common Characteristic of **Bad** Documentation
#
# My first attempts at writing documentation usually ended disastrously.
# Here are some of the most common recurring issues I experienced.
#
# ### Easily Out-of-date
#
# It's all too easy for documentation to become *out-of-date*.
# With how often we - or our customers - upgrade software,
# documentation can become obsolete faster than you can write it.
#
# ### Difficult to Update
#
# Have you ever been given a *pdf* document that had a typo in it.
# You wanted to fix the typo, but *how do you fix a typo in a PDF*?
#
# ### Difficult or Impossible to Suggest Improvements
#
# If you find a typo, and can't fix it yourself,
# is there someone else you can ask to fix it?
# How do you get in touch with them and tell them about the issue?
#
# ### Difficult or Impossible to Reproduce
#
# Reproducibility is one of the foundational concepts of the *scientific method*.
# It is an essential part of *peer reviewed research*.
# If your results can't be reproduced, then there is a **real problem**.


# %%
from datetime import date, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %% [markdown]
# ## Lessons Learnt
#
# Writing *good documentation* is about a lot more than just *writing*.
# How do you ensure that your documentation is *correct*, *up-to-date*,
# of *high-quality*, and, most importantly, *looks good*?
#
# I've learnt that having a solid continuous integration pipeline,
# complete with quality-assurance, testing, building, and deployment,
# is essential to having high-quality documentation.

# %% [markdown]
# ### Staying Up-to-date
#
# Technology moves so quickly that documentation goes out-of-date faster than we can write it.
# So, how do we ensure that it is always *up-to-date*?
#
# In order to keep documentation stay *up-to-date* it must be *executable*.
# This means that any images/plots in the documentation are freshly generated.
#
# This is made possible by such wonderful tools as [Jupyter notebooks](https://jupyter.org/),
# which allow us to mix *code* and *text* into one *executable document*.
#
# Initially, I used Jupyter notebooks for this blog, and still
# consider it a solid choice. I currently use [the percent py format](https://jupytext.readthedocs.io/en/latest/formats.html#the-percent-format)
# for reasons I'll elaborate on later.

# A common use case would be wanting to add a plot to my documentation.
# Imagine I want to get sales data
# for the last *n* number of days.
# Instead of *copy-pasting* an image of a plot
# created elsewhere, I just make the plot right here:

# %%
def get_sales_data(*, last_n_days: int):
    """Get the sales data for `last_n_days`.

    Here I'll create fake data, but in the real world it
    is probably in a database of some kind.
    """
    today = date.today()
    days = sorted([today - timedelta(days=i) for i in range(last_n_days)])
    sales = [np.random.uniform(low=1000, high=2000) for i in range(len(days))]

    df = pd.DataFrame({"date": days, "sales": sales})
    df.set_index("date")
    return df


def plot_sales(*, df: pd.DataFrame) -> None:
    """Plot sales data."""
    df.plot(x="date", y="sales", rot=45, xlabel="Date", ylabel="Sales [$]")
    plt.show()


df = get_sales_data(last_n_days=100)

plot_sales(df=df)

# %% [markdown]
# ### Is Easily Updated
#
# No matter how hard you try, there will always be a *bug* or *issue*
# that will need to be fixed.
# The question is: how easily can I find and fix bugs in the documentation?
#
# For example, imagine that my *sales* from the previous example were off by a factor of 2!
# In the database the sales are stored in "cents", and I thought it was "dollars".
# Since the plot is generated right here, this is really easy to fix:
# %%
# Convert sales from cents to dollars
df["sales"] *= 0.01
plot_sales(df=df)

# %% [markdown]
# One reason I switched from using Jupyter notebooks to using percent-format
# Python scripts was precisely because Python scripts (which are plain text files)
# are much easier to modify and fix than Jupyter notebooks (which are JSON files).
#
# There's also more to *easily updating* than just fixing code.
# You must distribute the fixed changes to your audience.
# How do you ensure your readers get the latest documentation?
#
# For that, having a continuous integration system
# which automagically deploys the documentation is essential.
# This blog uses
# [GitHub Actions](https://docs.github.com/en/actions)
# [GitHub Pages](https://pages.github.com/) for hosting
# to automate the testing, building, and deployment of this blog.
#
# ### Easy to Reproduce
#
# Reproducibility is one of the foundational concepts of the *scientific method*.
# It is an essential part of *peer reviewed research*.
# If your results can't be reproduced, then there is a **real problem**.
#
# The documentation should be able to be generated from the command-line,
# and setting up an environment to generate the documentation should be fully automated.
# As mentioned earlier, having continuous integration is really helpful here.
#
# In this blog people can see the text, the plots, but also the code!
# This has the added benefit that people can understand how their plots were created.
# If they ever need to improve anything, they can more easily do that.

# ### Can Easily Suggest Improvements
#
# All documentation will have some issues and/or inaccuracies.
# It should be as easy as possible for avid users to be able to suggest improvements.
#
# This blog used to be built using [Sphinx](https://www.sphinx-doc.org/en/master/),
# which is a solid tool,
# but I now use [Jupyter Book](https://jupyterbook.org).
# Besides having a really nice layout,
# Jupyter Book provides other wonderful functionality.
#
# On the top right of the page you will see links to the Git Repository,
# as well as links for creating an *issue* and suggesting a change.

# %% [markdown]
# ## Structure of This Blog
#
# Anyway, it's time to wrap up this post,
# and what better way to do that than with a diagram
# made *automagically* with code?
#
# This diagram is built using
# [mermaid extension for Sphinx](https://github.com/mgaitan/sphinxcontrib-mermaid),
# which itself uses
# [mermaid.js](https://mermaid-js.github.io/mermaid/#/).
#
# ```{note}
# This diagram is subject to getting *out-of-date*.
# ```
#
# ```{mermaid}
# sequenceDiagram
#   participant Alice
#   participant Bob
#   Alice->John: Hello John, how are you?
#   loop Healthcheck
#       John->John: Fight against hypochondria
#   end
#   Note right of John: Rational thoughts <br/>prevail...
#   John-->Alice: Great!
#   John->Bob: How about you?
#   Bob-->John: Jolly good!
# ```

# As a software engineer, I am jast as interested in the
# infrastructure of my blog's continuous integration
# than I am about the content I was writing.
#
# # How This Blog Works
#
# I've been meaning to write up an article
# about how this blog works, and why I've designed it in such a way.
#
# The key takeaway is that the infrastructure of this blog was designed
# to mimmick the infrasructure required to create professional documentation.
# By *professional documentation*, I mean something that is of good enough quality to hand to your boss and say:
# "Here's that documentation you asked for".
#
# Great care has been taken to ensure the system is robust, flexible, and scaleable.
# Of course I make mistakes, but at least I can fix them as needed,
# and the fixes automagically apply to the entire blog!
# The lessons I learnt creating this blog can be directly
# applied to creating professional documentation.
