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
# ## Custom Dispatching Solution
#
# So, I will just go ahead and write the code here for our *custom function dispatching solution*,
# and then demo it after.

# %%
from inspect import signature, Signature, BoundArguments
from typing import Callable, Hashable, Type, Any
from functools import wraps

StaticDispatcher = Callable[[Signature], Hashable]
RuntimeDispatcher = Callable[[BoundArguments], Hashable]


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

        def register_decorator(func):
            func_sig = signature(func)
            key = static_dispatcher(func_sig)
            registry[key] = func

            @wraps(func)
            def register_wrapper(*args, **kwargs):
                func(*args, **kwargs)

            return register_wrapper

        wrapper.register = register_decorator
        return wrapper

    return decorator


# %%
def get_x_annotation(signature: Signature) -> Type:
    return signature.parameters["x"].annotation


def get_x_type(bound_arguments: BoundArguments) -> Type:
    return type(bound_arguments.arguments["x"])


dispatch_x = custom_dispatch(
    static_dispatcher=get_x_annotation,
    runtime_dispatcher=get_x_type,
)


@dispatch_x
def f(x: Any):
    print("default implementation", x)


@f.register
def f_int(x: int):
    print("int implementation", x)


@f.register
def f_str(x: str):
    print("str implementation", x)


# %%
f(1)

# %%
f("x")

# %%
f(2.0)
