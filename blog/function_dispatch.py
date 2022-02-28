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
# # Custom Function Dispatching
#
#
# ```{note}
# In progress.
# ```
#
# I used to do a lot of C++, and when I switched to Python I never wanted to look back.
# Every now and then, I encounter a situation where I miss some of C++'s features...
# I particularly miss how easy it was to overload functions.
# Functions can be overloaded based on the types of the arguments, even the number of arguments!
# Wouldn't it be cool if we could do the same thing in Python?
#
# With a little creativity, we can get Python to do the same thing!
# In this article we'll create a custom and generic function dispatching infrastructure.
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
from inspect import signature, Signature, BoundArguments
from typing import Callable, Hashable, Type, Any, TypeAlias
from functools import wraps, partial

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
def my_custom_func(x:int, y:float, z:str, *args, **kwargs):
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
# So, I will just go ahead and write the code here for our *custom function dispatching solution*,
# and then demo it after.

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
            func_impl = registry.get(key, func)
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
def f(x: Any, y:Any):
    print("default implementation", x, y)


@f.register
def _(x: int, y:int):
    print("int implementation", x, y)

@f.register
def _(x:float, y:int):
    print("float-int implementation")

@f.register
def _(x: str, y:str):
    print("str-str implementation", x)


# %%
f(1,1)

# %%
f(5.0, 0)

# %%
f("hello", "goodbye")

# %% [markdown]
# ## Dispatch Based on Values

# %%
from datetime import date, timedelta

def prediction_static_dispatcher(
    signature: Signature
):
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
def predict_future(start:date, finish: date,):
    """Base function for predicting the future"""
    print(f"You will do great things with Python! from {start} to {finish}!")
    
@predict_future.register(
    key="start-past"
)
def _(start:date, finish: date):
    print("Predicting the past is easy! You will soon read a blog about Python function dispatching.")
    
@predict_future.register(
    key="far-in-future"
)
def _(start:date, finish:date):
    print("Predicting far into the future is also easy, robots will take over the world!")
    


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
