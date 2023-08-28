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
# # Custom Function Dispatching
#
#
# ```{note}
# In progress.
# ```
#
# I used to do a lot of C++ programming,
# I really love its strong typing system, and
# how easy it is to overload functions.
#
# There are some existing solutions in Python for overloading functions,
# but I always felt they were missing something.
# Just like any determined *Pythonista*, I set out on an adventure to implement a solution myself!
#
# It took me a while to figure it out, but I think this is a decent solution!
# In this article we'll create a custom and generic function dispatching infrastructure.
# If you like it, feel free to copy-paste this solution into your codebase and customize it as needed.
#

# %% [markdown]
# ## Existing Function Dispatching Solutions
#
# I won't go into too much detail here, but if you're interested in function dispatching,
# you should probably familiarize yourself with these existing solutions before
# trying to create a custom solution.
#
# ### [`functools.dispatch`](https://docs.python.org/3/library/functools.html#functools.singledispatch)
#
# This is built into the standard library, and should be your *first choice*.
# It provides functionality for dispatching functions based on the type of the first argument.
# It even supports [*type hinting*](https://docs.python.org/3/library/typing.html),
# which I hope you are all doing by now.
#
# ### [`multipledispatch`](https://pypi.org/project/multipledispatch/)
#
# If you need to dispatch functions based on types of multiple arguments,
# then this is a really good solution.
#

# %% [markdown]
# ## How Dispatching Works
#
# In order for function dispatching to work we need to be able to look at the values *at runtime* and match them to an appropriate *statically defined function*. I'm using the terms *runtime* and *static* intentionally here, since they play a critical role in how this works.


# %%
from datetime import date, timedelta
from functools import partial, wraps
from inspect import BoundArguments, Signature, signature
from typing import Any, Callable, Hashable, Type, TypeAlias

# %% [markdown]
# ### Static vs Runtime
#
# I won't go into too much detail, but *static* refers to properties of the *code itself* and *runtime* refert to properties of the *values themselves*. Here's a simple expample.

# %%
x: int = 5


# %% [markdown]
# Above, `x` has a *runtime value* of `5`, and a *static type-hint* of `int`.
#
# When we define a function, we can inspect *static properties* of the function via its *function signature*.

# %%
def my_custom_func(x: int, y: float, z: str, *args, **kwargs):
    pass


signature(my_custom_func)

# %% [markdown]
# When we call a function with certain arguments, we can inspect those values at runtime by looking at which values are *bound* to which which function parameter.

# %%
signature(my_custom_func).bind(5, 3.0, "hello", 0, 1, 2, a="a", b="b")

# %% [markdown]
# By combining these two methods (of inspecting *static* and *runtime* properties) we can devise a simple method for creating a custom *dispatching solution*.

# %% [markdown]
# ## Custom Dispatching Solution
#
# We will inspect *static function signatures* to generate a *key*.
# We will *register* functions one-by-one, keeping track of each function's key.
# When functions are called at runtime, we will inspect *runtime bound arguments* to generate a *key*,
# and look for a function whose key matches.
# If no match is found, then the default implementation is used.

# I will just go ahead and write the code here for our *custom function dispatching solution*.
#

# %%
Key: TypeAlias = Hashable
StaticDispatcher = Callable[[Signature], Key]
RuntimeDispatcher = Callable[[BoundArguments], Key]


def custom_dispatch(
    static_dispatcher: StaticDispatcher,
    runtime_dispatcher: RuntimeDispatcher,
):
    def decorator(func):
        default_impl = func
        default_signature = signature(func)
        registry = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_args = default_signature.bind(*args, **kwargs)
            key = runtime_dispatcher(bound_args)
            func_impl = registry.get(key, default_impl)
            return func_impl(*args, **kwargs)

        def register_decorator(func=None, *, key=None):
            if func is None:
                return partial(register_decorator, key=key)

            func_sig = signature(func)
            key = key or static_dispatcher(func_sig)
            registry[key] = func
            return func

        wrapper.register = register_decorator
        return wrapper

    return decorator


# %% [markdown]
# ## Dispatching Based on Types

# %%
def get_static_key(signature: Signature) -> Type:
    """Get the annotation of x (from function signature)."""
    params = signature.parameters
    return params["x"].annotation, params["y"].annotation


def get_runtime_key(bound_arguments: BoundArguments) -> Type:
    args = bound_arguments.arguments
    return type(args["x"]), type(args["y"])


dispatch = custom_dispatch(
    static_dispatcher=get_static_key,
    runtime_dispatcher=get_runtime_key,
)


@dispatch
def f(x: Any, y: Any):
    print("default implementation", x, y)


@f.register
def _(x: int, y: int):
    print("int implementation", x, y)


@f.register
def _(x: float, y: int):
    print("float-int implementation")


@f.register
def _(x: str, y: str):
    print("str-str implementation", x)


# %%
f(1, 1)

# %%
f(5.0, 0)

# %%
f("hello", "goodbye")

# %% [markdown]
# ## Dispatch Based on Values

# %%


def prediction_static_dispatcher(signature: Signature):
    raise ValueError("No static dispatching possible.")


def prediction_runtime_dispatcher(
    bound_arguments: BoundArguments,
):
    start = bound_arguments.arguments["start"]
    finish = bound_arguments.arguments["finish"]

    today = date.today()
    if start < today:
        return "start-past"
    if timedelta(days=30) < finish - today:
        return "far-in-future"


prediction_dispatcher = custom_dispatch(
    static_dispatcher=prediction_static_dispatcher,
    runtime_dispatcher=prediction_runtime_dispatcher,
)


@prediction_dispatcher
def predict_future(
    start: date,
    finish: date,
):
    """Base function for predicting the future"""
    print(f"You will do great things with Python! from {start} to {finish}!")


@predict_future.register(key="start-past")
def _(start: date, finish: date):
    print(
        "Predicting the past is easy! You will soon read an article about Python function dispatching."
    )


@predict_future.register(key="far-in-future")
def _(start: date, finish: date):
    print(
        "Predicting far into the future is also easy... robots will take over the world!"
    )


# %%
today = date.today()
yesterday = today - timedelta(days=1)

predict_future(start=yesterday, finish=today)

# %%
next_year = today + timedelta(days=365)
predict_future(start=today, finish=next_year)

# %%
one_week_from_today = today + timedelta(days=7)
predict_future(start=today, finish=one_week_from_today)


# %% [markdown]
# ## Conclusion
#
# I hope you learnt a lot reading this article.
# Most importantly, I hope you see that, with Python,
# you can do just about anything!
#
# The only caveat is that it's up to you
# to make sure that your final solution *improved your code*
# instead of *making it worse*... It's still not clear to me whether
# custom-function-dispatching leads to better or worse code.
# I'll let you be the judge of that.
#
