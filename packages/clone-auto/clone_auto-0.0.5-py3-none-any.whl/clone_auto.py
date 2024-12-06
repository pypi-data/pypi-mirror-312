import os
import subprocess

import requests

from _version import __version__
from term_args import term_args

def get_repo(api: str, user: str, json_keyword: str, *args, **kwargs) -> list:
    """Public repositories from a user on a given platform API
    """
    try:
        response = requests.get(api.replace("USER", user), *args, **kwargs)
        response.raise_for_status()
    
    except requests.exceptions.RequestException as error:
        print(error)
        return []

    user_json = response.json()

    repos = [repo[json_keyword] for repo in user_json]
    return repos

def clone_repo(git_url: str) -> bool:
    """git clone git_url
    """
    command = ["git", "clone", git_url]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)

    for c in iter(lambda: process.stdout.read(1), b""):
        print(c.decode('ascii'), end="")

PLATFORMS = {
        'gitlab': [
            "https://gitlab.com/api/v4/users/USER/projects",
            "http_url_to_repo"
            ],
        'codeberg': [
            "https://codeberg.org/api/v1/users/USER/repos",
            "clone_url"
            ],
        'github': [
            "https://api.github.com/users/USER/repos",
            "clone_url"
            ]
        }

def main():
    terminal = term_args()
    [user] = terminal.user
    path = os.path.abspath(terminal.path)
    for platform in terminal.platforms:
        save_path = os.path.join(path, platform)
        os.makedirs(save_path, exist_ok = True)
        os.chdir(save_path)
        api, json_keyword = PLATFORMS[platform]
        for repo_url in get_repo(
                api,
                user,
                json_keyword,
                timeout=terminal.timeout):
            clone_repo(repo_url)

if __name__ == '__main__':
    main()
