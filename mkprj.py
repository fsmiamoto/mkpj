#!/usr/bin/env python3

from os import getenv, mkdir
from shutil import rmtree
from os.path import join, exists
import argparse

from dotenv import load_dotenv
from github import Github
import git

# Access the HOME environment var.
HOME_DIR = getenv('HOME')

# Load dotenv file
dotenv_path = join(HOME_DIR, '.env')
load_dotenv(dotenv_path)

# GitHub personal access key
GITHUB_KEY = getenv('GITHUB_KEY')

# Projects directory
PROJECT_DIR = getenv("PROJECT_DIR")


def get_args():
    parser = argparse.ArgumentParser(
        description="Create a new project with git / GitHub.")

    parser.add_argument("name",
                        metavar='NAME',
                        type=str,
                        help='Name of the project')
    parser.add_argument("--github",
                        action="store_true",
                        help="Create a GitHub repo for the project")
    parser.add_argument("--description",
                        dest='description',
                        type=str,
                        help='Description of the new repo')
    parser.add_argument("--private",
                        action="store_true",
                        help='Makes the repo private (public by default)')
    return parser.parse_args()


def create_new_github_repo(name: str, description: str, private: bool) -> str:
    if GITHUB_KEY is None:
        raise ValueError('Missing GitHub key!')

    g = Github(GITHUB_KEY)
    user = g.get_user()

    user_repos_names = [repo.name for repo in user.get_repos()]

    if name in user_repos_names:
        raise ValueError('GitHub repo with this name already exists!')

    if description is None:
        new_repo = user.create_repo(name, private=private)
    else:
        new_repo = user.create_repo(name,
                                    description=description,
                                    private=private)
    return new_repo.ssh_url


if __name__ == '__main__':
    args = get_args()

    project_dir = join(PROJECT_DIR, args.name)

    if not exists(project_dir):
        try:
            # Create directory for the new project
            mkdir(project_dir)

            # Initialize git
            r = git.Repo.init(project_dir)

            # Create GitHub repo
            if args.github:
                remote_url = create_new_github_repo(args.name,
                                                    args.description,
                                                    args.private)
                r.create_remote('origin', remote_url)
        except Exception as e:
            print('mkprj: Error - {}'.format(e))

            # Remove directory for atomicity
            rmtree(project_dir)
    else:
        print('mkprj: Project with this name already exists!')
