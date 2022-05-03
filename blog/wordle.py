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
# # Best Wordle Words
#
# [Wordle](https://www.powerlanguage.co.uk/wordle/) is extremely popular these days,
# and for good reason: it is so simple and elegant; a real joy.
#
# *Wordle* reminds us that the best of games are simple in nature, with few rules,
# and a great deal of freedom for players to develop their own strategies.
# But, don't let *Wordle*'s apparent simplicity fool you... it is all too easy
# to guess words ineffectively, and to lose!
#
# In this arrticle I will try to come up with some good words for initial guesses to *Wordle*.
#
# ## 5-Letter Words
#
# Let's assume that the only rule to *Wordle*'s choice of words is that it is a 5-letter word.
# So, let's just get all 5-letter words.

# %%
import string

import matplotlib.pyplot as plt
import pandas as pd
import requests


def plot_table(df: pd.DataFrame):
    return df.style.background_gradient("YlGn")


words_request = requests.get(
    "https://gist.githubusercontent.com/nicobako/759adb8f0e7fa514f408afb946e80042/raw/d9783627c731268fb2935a731a618aa8e95cf465/words"
)
all_words = words_request.content.decode("utf-8").lower().split()

five_letter_words = pd.DataFrame(
    (
        word
        for word in all_words
        if len(word) == 5 and all(letter in string.ascii_lowercase for letter in word)
    ),
    columns=["word"],
)

# %% [markdown]
# How many 5-letter words do we have?

# %%
len(five_letter_words)


# %% [markdown]
# Wow! That's a lot!

# %% [markdown]
# ## Criteria for a Good Guess
#
# There are many theories on what makes a good guess,
# so please don't judge... but here is my naive simple criteria for a good guess:
#
# * Contains as many common letters as possible
# * Contains as many different letters as possible
# * Contains as many letters in common places as possible
#
# For now, let's keep it this simple. We can always make things more complicated later...

# %% [markdown]
# ## Collecting the Data
#
# This is not so tricky...
# We look at each word, look at which letters we find at each position in each word,
# and keep track of everything.
# Later we can use this data to calculate everything we need.

# %%
def get_letters_data():
    data = []
    for word in five_letter_words["word"]:
        for position, letter in enumerate(word):
            data.append({"letter": letter, "position": position + 1})
    return pd.DataFrame(data)


letters = get_letters_data()

# %% [markdown]
# This data is a table whose rows contain two values: a letter; its position in a word.
# It might not seem like much, but it's all we need. Here's a quick glance at what
# this table looks like:

# %%
letters.head()

# %% [markdown]
# ## Most Common Letters
#
# Given our data, we can now count the occurences of each letter.
# This reflects how commonly each letter is found in any word.
# To calculate this we take a look at our letters data,
# group them by letter, and tally up the count.

# %%
letters_count = letters.groupby("letter").count()
letters_count.columns = ["count"]
letters_count = letters_count.sort_values(by="count", ascending=False)
letters_count.plot.barh(y="count")
plt.show()

# %% [markdown]
# I don't know about you, but these results surprised me!
# The top 10 letters are:

# %%
plot_table(letters_count.head(10))

# %% [markdown]
# And the lowest 10 are:

# %%
plot_table(letters_count.tail(10))

# %% [markdown]
# Let's create a new column in our letters-count table
# with the percent occurence of each letter:

# %%
letters_count["percent"] = 100 * letters_count["count"] / letters_count["count"].sum()

# %% [markdown]
# As usual, the sum of the percent column should equal 100%.

# %%
letters_count["percent"].sum()

# %%
letters_count["percent"].plot.pie(y="letter")
plt.show()


# %% [markdown]
# ## Words With Most Common Letters
#
# Using the occurence of each letter, we can look
# at all of our words, and give them a score
# based on how common the letters of the word are.
#
# We also don't want to give words extra points for having
# the same letter multiple times... Remember, the whole
# point of this is to come up with a good first guess for Wordle,
# so it would be more helpful if our first guess contained unique letters.

# %%
def score_based_on_letters_count(word: str) -> float:
    score = 0.0
    unique_letters = list(set(word))
    for letter in unique_letters:
        score += letters_count.loc[letter].percent
    return round(score, 2)


# %% [markdown]
# In this way, the score of a letter like `apple` is:

# %%
score_based_on_letters_count("apple")

# %% [markdown]
# We can take this metric and calculate a score for all of our 5-letter words.

# %%
five_letter_words["score_letters_count"] = [
    score_based_on_letters_count(word) for word in five_letter_words["word"]
]

# %% [markdown]
# Let's take a look at some of the top words:

# %%
plot_table(
    five_letter_words.sort_values("score_letters_count", ascending=False)
    .head(10)
    .set_index("word")
)

# %% [markdown]
# ## Most Common Positions of Letters
#
# Another important thing to look at is the relative position of the
# letters in our first guess. We want a word whose letters
# are not only common, but whose positions of letters are in common places.
#
# This is a little trickier to do, but stil not that tough.
# We group our data by letter and position, and count how many occurences
# of each letter-position combination.

# %%
letters_position = pd.DataFrame(
    {"count": letters.groupby(["letter", "position"]).size()}
)

# %% [markdown]
# Here's what it looks like for the letter `a`

# %%
letters_position.loc["a"]

# %% [markdown]
# You  can see that `a` is most commonly in the second position.
#
# Let's create a *percent* column for this table as well.

# %%
letters_position["percent"] = (
    100 * letters_position["count"] / letters_position["count"].sum()
)
letters_position["percent"] = [round(num, 2) for num in letters_position["percent"]]

# %% [markdown]
# Let's make sure the sum of the percent is 100%.

# %%
letters_position["percent"].sum()

# %% [markdown]
# And here's a fancy chart displaying how the letters and positions
# look for each letter:

# %%
letters_position_pivoted = letters_position.reset_index().pivot(
    index="letter", columns="position", values="percent"
)
letters_position_pivoted.sort_values("letter")
letters_position_pivoted.style.background_gradient("YlGn")


# %% [markdown]
# This chart is really quite useful, from a glance you can see that
# some letters are much more likely to be in certain positions of the word,
# so when making guesses, it's important to keep this in mind.

# %% [markdown]
# ## Words with Most Common Letter Positions
#
# We can use the above data to score each of our 5-letter words
# based on the positions of the letters.
# We just look at all of the letters of our word and their corresponding
# positions, and tally up the percent chance of encountering each
# letter in its position.
#
# Here will count all letters, even duplicates... not sure why, it just feels right.

# %%
def score_based_on_letters_position(word: str) -> float:
    score = 0.0
    for i, letter in enumerate(word):
        position = i + 1
        score += letters_position.loc[letter, position]["percent"]
    return score


# %% [markdown]
# So, the score of `apple` in this case would be:

# %%
score_based_on_letters_position("apple")

# %% [markdown]
# You can see right away that the score for the word `apple` is very different than before.
#
# Let's calculate the score for each of our 5-letter words based on the positions
# of its letters.

# %%
five_letter_words["score_letters_position"] = [
    score_based_on_letters_position(word) for word in five_letter_words["word"]
]

# %% [markdown]
# Let's take a look at the top 10 in this case.

# %%
plot_table(
    five_letter_words[["word", "score_letters_position"]]
    .sort_values("score_letters_position", ascending=False)
    .head(10)
    .set_index("word")
)

# %% [markdown]
# You may be surprised, as I was, to find that these two ways of scoring words
# generated very different lists!

# %% [markdown]
# ## What is the Best Guess?
#
# So, what is the best first guess.
# We'll naively assume that is a combination of these two scoring methods.
# We'll just add up the scores for letter-count and letter-position,
# and look at the top words.

# %%
five_letter_words["final_score"] = (
    five_letter_words["score_letters_count"]
    + five_letter_words["score_letters_position"]
)

# %%
plot_table(
    five_letter_words.sort_values("final_score", ascending=False)
    .set_index("word")
    .head(20)
)

# %% [markdown]
# ## Conclusion
#
# Don't let this fancy code and math fool you,
# this is a naive approach. We are simply looking at
# which letters are most common, and which positions of letters
# are most common, and picking words that maximize this combination.
# There are a ton of other details that this code simply isn't considering,
# and a lot of ways this code can be improved.
#
# In the end, this article may help you come up with a decent first guess,
# but the rest is up to you! Anyway, good luck on your next *Wordle*  game,
# and don't forget to try out one of the top words!
