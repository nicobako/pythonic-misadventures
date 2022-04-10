import requests
from typing import Any


def check(problem_number: int, answer: Any) -> bool:
    return requests.post(
        f"https://projecteuler.net/problem={problem_number}",
        {
            f"guess_{problem_number}": answer,
        },
    )

def get_problem_description(problem:int):
    from IPython.display import HTML
    return HTML(
        requests.get(
            f"https://projecteuler.net/minimal={problem}"
        ).content.decode("utf-8")
    )

