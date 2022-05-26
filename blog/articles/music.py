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
# # What if Music Used a Different System?
#
# This thought has been in my mind for quite some time:
#
# > What if the notes of musical scales followed a *different* pattern?
# > For example, what if musical scales were based on the *decimal* system?
#
# ```{note}
# For more info on how musical scales work read [this](https://pages.mtu.edu/~suits/scales.html).
# There are also a ton of articles explaining how music works...
# ```
#
#
# ## Glossary
#
# Here is an attempte to define some terms I'll use throughout
# this article.
#
# ### Pitch
#
# When I refer to a *pitch*, I am referring to how, in classical music
# there are 12 total pitches:
#
# * `A`
# * `A-sharp/B-flat`
# * `B`
# * `C`
# * `C-sharp/D-flat`
# * `D`
# * `D-sharp/E-flat`
# * `E`
# * `F`
# * `F-sharp/G-flat`
# * `G`
# * `G-sharp/A-flat`
#
# As the pitch ascend (`A` to `G`), the frequency increases.
# The pattern of pitches `A` to `G` keeps repeating: `A`-`B`-...-`F`-`G`-`A`-`B`-... .
#
# ```{note}
# I'll be using numbers to refer to pitches instead of letters throughout this article.
# ```
#
# ### Octave
#
# Each suqsequent time a pitch is encoutered
# it's frequency is double what it previously was.
# This is what an *octave* represents.
#
# For example, a special `A` (denoted `A4`) has a frequency of `440 Hz`,
# so the next `A` (`A5`) has a frequency of `880 Hz`,
# and the previous `A` (`A3`) has a frequency of `220 Hz`.
#
# This pattern of *doubling* means that frequencies increase *exponentially* as notes increase.
#
# ### Note
#
# The combination of *octave* and *pitch* are used to define an individual *note*.
# Above you saw `A4` (*pitch* `A`, *octave* `4`).
#
# ### Step
#
# How distance in *pitches* between two notes.
# For example, `A4` and `B4` are 2 steps apart.
#
# ### Reference Note and Frequency
#
# In order for any of this to work we must assign a specific frequency
# to a specific note. For example, `A4` is assigned a frequency of `440 Hz`.
#
# I'm sure there's a reason behing this, but I'll be assigning *reference frequencies*
# to *reference notes* more arbitrarily in this article.


# %% [markdown]
# ## Reusable Classes and Functions
#
# So, I think we're ready to get started with some code now.
# Remember, the idea is to try out some different *musical systems*,
# so we want to create some reusable functionality.
#
# I'll try to explain things as I go, and I'll use the standard
# classical music system as a demo before we get into anything more crazy.


# %%
from typing import Iterator, List

import numpy as np
from IPython.display import Audio, display


class Note:
    """Simple data structure for representing a note."""

    def __init__(self, octave: int, pitch: int):
        self.octave = octave
        self.pitch = pitch

    def __repr__(self) -> str:
        return f"Note(octave={self.octave}, pitch={self.pitch})"


class MusicalSystem:
    """Represents how a note should be interpreted."""

    def __init__(
        self, *, num_pitches: int, ref_frequency: float, ref_note: Note
    ) -> None:
        """Initialize musical system."""
        self.num_pitches = num_pitches
        self.ref_frequency = ref_frequency
        self.ref_note = ref_note

    def frequency(self, note: Note) -> float:
        """Compute the frequency of a note."""
        return self.ref_frequency * pow(
            2, (self.steps(self.ref_note, note) / self.num_pitches)
        )

    def steps(self, note_start: Note, note_end: Note) -> int:
        """Compute the number of steps between two notes."""
        return (self.num_pitches * (note_end.octave - note_start.octave)) + (
            note_end.pitch - note_start.pitch
        )

    def octave_iter(self, octave: int) -> Iterator[Note]:
        """Iterate over all notes in a given octave."""
        for pitch in range(self.num_pitches):
            yield Note(octave, pitch)


classical = MusicalSystem(num_pitches=12, ref_frequency=440.0, ref_note=Note(4, 0))


note_a4 = Note(4, 0)
note_b4 = Note(4, 2)
assert 2 == classical.steps(note_a4, note_b4)
assert 440.0 == classical.frequency(note_a4)
assert 880.0 == classical.frequency(Note(5, 0))

# %% [markdown]
# Now we have the basic building blocks for representing
# both a musical note, as well as musical systems.
# Let's create some functionality for generating some
# useful visualizations and audio - this is about music, after all.

# %%
FRAME_RATE = 44100


def compute_waveform(frequency: float, duration: float) -> np.ndarray:
    time = np.linspace(0, duration, int(FRAME_RATE * duration))
    waveform = np.sin(2.0 * np.pi * time * frequency)
    return waveform


def play(waveform: np.ndarray) -> Audio:
    return Audio(
        data=waveform,
        rate=FRAME_RATE,
    )


play(
    compute_waveform(classical.frequency(note_a4), 1.0),
)


# %%
def gen_chord_waveform(
    musical_system: MusicalSystem, notes: List[Note], duration: float
) -> np.ndarray:
    return np.sum(
        [
            compute_waveform(
                musical_system.frequency(note),
                duration,
            )
            for note in notes
        ],
        axis=0,
    )


minor_third = gen_chord_waveform(
    classical,
    [Note(3, 6), Note(3, 9)],
    2.0,
)

play(minor_third)

# %%
major_third = gen_chord_waveform(classical, [Note(3, 6), Note(3, 10)], 2.0)
play(major_third)


# %%
def play_all_notes_in_octave(
    musical_system: MusicalSystem,
    octave: int,
):
    waveforms = [
        compute_waveform(
            musical_system.frequency(
                note,
            ),
            0.5,
        )
        for note in musical_system.octave_iter(octave)
    ]
    waveforms = np.hstack(waveforms)
    return play(waveforms)


play_all_notes_in_octave(
    classical,
    3,
)

# %%
def play_all_intervals_in_octave(
    musical_system: MusicalSystem,
    octave: int,
):
    notes = list(musical_system.octave_iter(octave))
    first_note = notes.pop(0)

    waveforms = []
    for note in notes:
        wvf_first_note = compute_waveform(
            musical_system.frequency(first_note),
            0.25,
        )
        wvf_note = compute_waveform(
            musical_system.frequency(note),
            0.25,
        )
        wvf_chord = gen_chord_waveform(
            musical_system,
            [first_note, note],
            0.5,
        )
        waveforms.append(wvf_first_note)
        waveforms.append(wvf_note)
        waveforms.append(wvf_chord)
    waveforms = np.hstack(waveforms)
    return play(waveforms)


play_all_intervals_in_octave(
    classical,
    3,
)


# %%
def create_report(
    musical_system: MusicalSystem,
    octave: int,
):
    play_notes = play_all_notes_in_octave(musical_system, octave)
    play_intervals = play_all_intervals_in_octave(musical_system, octave)

    return display(play_notes, play_intervals)


create_report(classical, 3)

# %% [markdown]
# ## Custom Musical Systems
#
# Okay, now it's time to create some custom musical systems!
#
# ### Decimal System
#
# Imagine a system based purely on the *decimal* system.
# In my mind, it would look like this:

# %%
decimal_system = MusicalSystem(
    num_pitches=10,
    ref_frequency=10.0,
    ref_note=Note(0, 0),
)

create_report(
    decimal_system,
    4,
)

# %% [markdown]
# ### Baker's Dozen
#
# In real music there are 12 pitches... what if there were 13?

# %%
bakers_dozen_system = MusicalSystem(
    num_pitches=13, ref_frequency=440, ref_note=Note(4, 0)
)

create_report(
    bakers_dozen_system,
    3,
)

# %% [markdown]
# ### System of 6 Notes
#
# What if a system had 6 notes?

# %%
six_system = MusicalSystem(num_pitches=6, ref_frequency=440, ref_note=Note(4, 0))

create_report(six_system, 3)

# %% [markdown]
# ### System of 20 Notes
#
# What if we had 20 notes?

# %%
twenty_system = MusicalSystem(num_pitches=20, ref_frequency=20, ref_note=Note(0, 0))

create_report(twenty_system, 3)
