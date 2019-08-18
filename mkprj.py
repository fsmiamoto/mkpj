#!/usr/bin/env python3

from os import getenv, mkdir
from os.path import join, dirname, exists
import argparse

from dotenv import load_dotenv
from github import Github
import git

# Load dotenv file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# GitHub personal access key
GITHUB_KEY = getenv('GITHUB_KEY')

# Access $HOME environment var.
HOME_DIR = getenv('HOME')

# Projects directory
PROJECTS_DIR = join(HOME_DIR, "Dev")


def get_args():
    parser = argparse.ArgumentParser(description="Create a new GitHub repo.")

    parser.add_argument("name",
                        metavar='NAME',
                        type=str,
                        help='Name of the repo')
    parser.add_argument("--github",
                        action="store_true",
                        help="Create a GitHub repo for the project")
    parser.add_argument("--description",
                        dest='description',
                        type=str,
                        help='Description of the repo')
    parser.add_argument("--private",
                        action="store_true",
                        help='Makes the repo private (public by default)')
    return parser.parse_args()


def create_new_github_repo(name: str, description: str, private: bool) -> str:
    g = Github(GITHUB_KEY)
    user = g.get_user()

    new_repo = user.create_repo(name, description=description, private=private)

    return new_repo.ssh_url


if __name__ == '__main__':
    args = get_args()

    project_dir = join(PROJECTS_DIR, args.name)

    if not exists(project_dir):
        # Create directory for the new project
        mkdir(project_dir)

        # Initialize git
        r = git.Repo.init(project_dir)

        # Create GitHub repo
        if args.github:
            remote_url = create_new_github_repo(args.name, args.description,
                                                args.private)
            r.create_remote('origin', remote_url)
    else:
        print('mkprj: Project with this name already exists!')

