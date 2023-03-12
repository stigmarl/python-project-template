import os
from typing import Optional


def get_git_user() -> Optional[str]:
    name = os.popen("git config --get user.name").read().strip()
    email = os.popen("git config --get user.email").read().strip()

    if name and email:
        return f"{name} <{email}>"
    return None


def prompt(name: str, default: Optional[str] = None) -> str:
    prompt_default = f" [default: {default}]" if default else ""

    while True:
        answer = input(f"Enter {name}{prompt_default}: ")

        if not answer:
            if default:
                return default
        else:
            return answer


def choice(name: str, choices: list[str], default: Optional[str] = None) -> str:
    while True:
        answer = prompt(f"{name} ({'/'.join(choices)})", default)
        if answer in choices:
            return answer
        if answer in choices:
            return answer
