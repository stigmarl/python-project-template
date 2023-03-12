import os

import requests

from .utils import choice, prompt

main_template = """
def main() -> None:
    print("Hello world!")


if __name__ == "__main__":
    main()
"""

vscode_settings_template = """
{
    "python.formatting.provider": "black",
    "python.linting.mypyEnabled": true,
    "ruff.organizeImports": true,
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        },
        "editor.formatOnSave": true
    }
}
"""

gitignore_vscode_template = """
#
# VS Code project settings
.vscode/
"""


def initialize_project() -> None:
    project_name = prompt("project_name").replace(" ", "-").lower()
    package_name = project_name.replace("-", "_")

    os.system(f"poetry new {project_name}")

    with open(
        os.path.join(project_name, package_name, "__main__.py"), "w"
    ) as main_file:
        main_file.write(main_template)

    print("Fetching gitignore template from GitHub")
    gitignore_template = (
        requests.get(
            "https://raw.githubusercontent.com/github/gitignore/master/Python.gitignore"
        ).text
        + gitignore_vscode_template
    )
    with open(os.path.join(project_name, ".gitignore"), "w") as gitignore_file:
        gitignore_file.write(gitignore_template)

    if not os.path.isdir(os.path.join(project_name, ".git")):
        os.system(f"cd {project_name} && git init")

    print("Should a basic .vscode/settings.json file be included?")
    vscode_settings_template_include = choice("settings.json", ["yes", "no"], "yes")
    if vscode_settings_template_include == "yes":
        os.mkdir(os.path.join(project_name, ".vscode"))
        with open(
            os.path.join(project_name, ".vscode/settings.json"), "w"
        ) as settings_file:
            settings_file.write(vscode_settings_template)

    os.system(f"poetry add --group dev mypy ruff black --directory {project_name}")
    os.system(f"poetry add --group test pytest --directory {project_name}")
    os.system(f"poetry lock --directory {project_name}")
    os.system(f"poetry install --directory {project_name}")
