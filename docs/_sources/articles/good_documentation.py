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
# # On Good Documentation
#
# No matter what your role, whether you're a manager,
# or you're fresh-out-of-college, chances are you need to write some documentation.
#
# We need to write documentation for all sorts of reasons.
# Sometimes we need to document our progress on a task, or outline the steps of a process,
# or create a users manual for a a tool.
#
# Sometimes our documentation is in the form of a word document,
# presentation slides, a formal report, or a simple `README.txt`.
#
# Sadly, even though we are all writing documentation,
# very few people *enjoy* writing documentation.
# and very few people succeed in writing *good documentation*.
#
# It took me a while to realize just how important writing *good documentatin* is,
# and that, when we set up our *documentation infrastructure* properly,
# we can *actually have fun writing good documentation*!
#
# ## Blogging is a Form of Documentation
#
# I first began writing this blog with the intention of learning
# important skills for creating *professional-level* documentation.
#
# I treated this blog as a testing ground for exploring
# a documentation infrastructure that can ensure
# that documentation is always of professional quality.
# All of my design decisions bore this in mind.
#
# Of course, I made plenty of mistakes along the way,
# and wrote plenty of *bad documentation*
# before I developed a better system, and subsequently, better documentation.

# %% [markdown]
# ## Lessons Learned
#
# Writing *good documentation* entails much more than just *writing*.
# How do you ensure that your documentation is *correct*, *up-to-date*,
# of *high-quality*, and, most importantly, *looks good*?
#
# I've learnt that having a solid continuous integration pipeline,
# complete with quality-assurance, testing, building, and deployment,
# is essential to having high-quality documentation.
#
# In essence, the same principles that apply to haivg *good softawre>
# apply to having *good documentation*.

# %% [markdown]
# ### Staying Up-to-date
#
# Technology moves so quickly that documentation goes out-of-date faster than we can write it.
# So, how do we ensure that it is always *up-to-date*?
#
# In order to keep documentation stay *up-to-date* it must be *executable*.
# This means that any images/plots in the documentation are freshly generated.
#
# A common use case would be needing to add a plot to some documentation.
# Imagine I want to get sales data for the last *n* number of days.
# Instead of *copy-pasting* an image of a plot created elsewhere, I just make the plot right here:

# %%
from datetime import date, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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
# This is made possible by such wonderful tools as [Jupyter notebooks](https://jupyter.org/),
# which allow us to mix *code* and *text* into one *executable document*.
#
# Initially, I used Jupyter notebooks for this blog, and still
# consider it a solid choice. I currently use [the percent py format](https://jupytext.readthedocs.io/en/latest/formats.html#the-percent-format)
# for reasons I'll elaborate on later.

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
# ### Distributing Documentation
#
# There's also more to *easily updating* than just fixing code.
# You must distribute the fixed changes to your audience.
# How do you ensure your readers get the latest documentation?
#
# For that, having a continuous integration system
# which automagically deploys the documentation is essential.
# This blog uses
# [GitHub Actions](https://docs.github.com/en/actions)
# to automate the testing, building, and deployment of this blog,
# and [GitHub Pages](https://pages.github.com/) for hosting the blog.
#
# ### Easy to Reproduce
#
# Reproducibility is one of the foundational concepts of the *scientific method*.
# It is an essential part of *peer reviewed research*.
# If your results can't be reproduced, then there is a **real problem**.
#
# The documentation should be able to be generated from the command-line,
# and having continuous integration is really helpful here.
#
# In this blog people can see the text, the plots, but also the code!
# This has the added benefit that people can understand how their plots were created.
# If they ever need to improve anything, they can more easily do that.
#
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
# ### Writing an Article - Process Overview
#
# ```{mermaid}
# flowchart TB
#     write(Write/Edit Article)
#     build(Build Blog)
#
#     write --> build
#
#     happy{Hapy with Article?}
#
#     build --> happy
#
#     commit(git commit)
#
#     happy -->|Yes| commit
#     happy -->|No| write
#
#     pre-commit(pre-commit)
#     pre-commit-successful{pre-commit Successful?}
#     push(git push)
#
#     commit --> pre-commit
#     pre-commit --> pre-commit-successful
#     pre-commit-successful -->|Yes| push
#     pre-commit-successful -->|No| write
#
#     run-ci(Run Continuous Integration)
#     push --> run-ci
#     ci-successful{CI Successful?}
#
#     run-ci --> ci-successful
#
#     deploy(Deploy)
#     ci-successful -->|Yes| deploy
#     ci-successful -->|No| write
# ```


# %% [markdown]
# ## Conclusion
#
# Writing good documentation is a lot like writing good software:
#
# * Do your best to write *correct* documentation
# * In the event that any portion of the documentation is *incorrect*
#   * Fix the issue quickly
#   * Distribute correct documentation quickly to all readers
#
# Having a robust infrastructure for testing, building, and deploying
# your documentation is key to having *good documentation*.
#
# Making your documentation easy to fix is key to ensuring that
# your documentation *stays good* over time.
#
# Your solution to *good documentation* will look different than mine,
# but the *principles of good documentation* will be the same.
# Actually, yours might be better...
#
# Anyway, happy documenting!
