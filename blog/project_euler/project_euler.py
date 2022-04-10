import requests
from typing import Any


def check(problem_number: int, answer: Any) -> bool:
    return requests.post(
        f"https://projecteuler.net/problem={problem_number}",
        {
            f"guess_{problem_number}": answer,
        },
    )


print(check(1, 5))

print(check(1, 233168))
