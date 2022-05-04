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

from datetime import date, timedelta

# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %% [markdown]
# ## Did Someone Say *Documentation*?
#
# Merely uttering the word *documentation* can instill dread in your coworkers.
# We all have so many negative emotions associated with *bad* documentation.
#
# No matter what your role, whether you're a manager,
# or you're fresh-out-of-college, chances are you need to write some documentation.
#
# So, how to we write *good* documentation instead of *bad* documentation?
# First, let's look at what makes *bad* documentation.

# %% [markdown]
# ## Common Characteristic of **Bad** Documentation
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
#

# %% [markdown]
# ## Characteristics of **Good** Documentation
#
# Now that we have an understanding of what *bad* documentation is,
# let's see how we can make *good* documentation.

# %% [markdown]
# ### Stays Up-to-date
#
# In order to keep documentation stay *up-to-date* the documentation must be *executable*.
# That means **no screenshots**, **no copy-pasting**, unless these processes are automated,
# or screenshots taken one day will be valid from now unto forever.
#
# If data needs to be used to generate a plot, then that's exactly what happens:
# data is fetched and a plot is generated.
#
# For example, imagine I want to get sales data
# for the last *n* number of days.

# %%
def get_sales_data(*, last_n_days: int):
    """Get the sales data for `last_n_days`.

    Here I'll create fake data, but in the real world it
    is probably in a database of some kind.
    """
    today = date.today()
    days = [today - timedelta(days=i) for i in range(last_n_days)]
    days = list(reversed(days))
    sales = [(i / 2) * np.random.uniform(low=10, high=20) for i in range(len(days))]

    df = pd.DataFrame({"date": days, "sales": sales})
    df.set_index("date")
    return df


df = get_sales_data(last_n_days=100)


def plot_sales(*, df: pd.DataFrame) -> None:
    """Plot sales data."""
    df.plot(x="date", y="sales", rot=90, xlabel="Date", ylabel="Sales [$]")
    plt.show()


plot_sales(df=df)

# %% [markdown]
# There's another important thing to mention here:
# if our documentation has any type of *requirements* or *pre-conditions*,
# then we should express those in our code.
#
# For example, if our documentation needs to talk to a database
# to get information, then our documentation should fail **LOUDLY**
# if a connection to the database cannot be established.

# %%
def test_db_connection():
    """Test that database can be connected to."""
    print("Testing database connection.")
    assert True


# %% [markdown]
# You might be thinking, "That kind of stuff doesn't belong in the documentation".
# Well, [just hide it!](https://jupyterbook.org/en/stable/interactive/hiding.html)
# Below is a code-cell calling our database-testing function,
# but the cell itself is hidden. You only see the output.

# %% tags=["remove-input"]
test_db_connection()

# %% [markdown]
# As this blog has grown I've learnt to put
# more of these types of *checks* throughout
# the code. These checks help ensure things are
# working correctly.

# %% [markdown]
# ### Is Easily Updated
#
# Once an issue is found, can I easily find its cause and fix it?
#
# For example, imagine that my *sales* were off by a factor of 2!
# In the database the sales are stored in "cents", and I thought it was "dollars".

# %%
# Convert sales to dollars
df["sales"] *= 0.01
plot_sales(df=df)

# %% [markdown]
# There's more to *easily updating*
# than just fixing code... it must be easy
# to distribute/deploy the fixed changes.
# For that, having a continuous integration system
# which automagically deploys the documentation is key.

# ### Easy to Reproduce
#
# Ideally, the documentation should be able to be generated from the command-line,
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
# This blog is built using [Jupyter Book](https://jupyterbook.org),
# which provides the wonderful functionality of linking each documentation
# page directly to a Git Repository. On the top right of the page
# you will see links to the Git Repository, as well as links for creating
# an *Issue*,
#
#

# %% [markdown]
# ## Structure of This Blog
#
# This blog


# ## Bad Documentation - A (Sadly True) Story
#
# Someone inserted an image of a plot into a document.
# The plot's data has been updated, but the documentation has not.
# The documentation is officially *out-of-date*.
#
# You try to fix this problem... how hard can it be?
# First, where is the updated data for the plot?
# Where is the original document?
# Maybe someone more *experienced* needs to fix this... who would that be?
#
# Finally, the plot is updated. Now, just need to update the document.
# But wait, I need to update a few more documents along with some power point presentations?
# Oh yeah, and one of our customers wants a report with the plot,
# but it needs to have a blue background...
#

# %% [markdown]
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

# %%
