#!/usr/bin/env python3
from os import getenv, mkdir, getcwd, chdir
from shutil import rmtree
from os.path import join, exists, dirname, realpath
from subprocess import call, DEVNULL
import argparse
import requests
import json


def get_args():
    parser = argparse.ArgumentParser(
        description='Create a new project with git / GitHub.')

    parser.add_argument('name',
                        metavar='NAME',
                        type=str,
                        help='Name of the project')
    parser.add_argument('--github',
                        action='store_true',
                        help='Create a GitHub repo for the project')
    parser.add_argument('--description',
                        dest='description',
                        type=str,
                        help='Description of the new repo')
    parser.add_argument('--private',
                        action='store_true',
                        help='Makes the repo private (public by default)')
    return parser.parse_args()


def create_new_github_repo(name: str, description: str, private: bool, token: str) -> str:
    '''
        Creates a new repo on GitHub
    '''
    if token is None:
        raise ValueError('Missing GitHub token!')

    if name is None:
        raise ValueError('Missing repo name!')

    payload = {'name': name}

    if description:
        payload['description'] = description

    if private:
        payload['private'] = private

    headers = {'Authorization': 'token {}'.format(token)}

    response = requests.post(
        'https://api.github.com/user/repos', data=json.dumps(payload), headers=headers)

    response = response.json()

    return response.get('ssh_url')


if __name__ == '__main__':
    args = get_args()

    # Path for the new directory
    project_dir = join(getcwd(), args.name)

    if not exists(project_dir):
        try:
            # Create directory for the new project
            mkdir(project_dir)

            # Move to directory
            chdir(project_dir)

            # Initialize repo
            return_value = call('git init', shell=True, stdout=DEVNULL)

            if return_value != 0:
                raise Exception

            print('->   Initialized Git repo')

            # Make a README
            return_value = call('touch README.md && echo "# {}" >> README.md'.format(
                args.name), shell=True, stdout=DEVNULL)

            if return_value != 0:
                raise Exception

            print('->   Created README.md')

            # Initial commit
            return_value = call(
                'git add . && git commit -m "Initial commit"', shell=True, stdout=DEVNULL)

            print('->   Commited README')

            if return_value != 0:
                raise Exception

            if args.github:

                # Path for key file
                path = dirname(realpath(__file__))
                path = join(path, 'key.txt')

                # Reads key
                with open(path, 'r') as f:
                    github_key = f.readline()

                # Create GitHub repo
                remote_url = create_new_github_repo(args.name,
                                                    args.description,
                                                    args.private,
                                                    github_key)

                # Add remote origin
                return_value = call(
                    'git remote add origin {}'.format(remote_url), shell=True, stdout=DEVNULL)

                if return_value != 0:
                    raise Exception

                print('->   Created GitHub repo')

                return_value = call(
                    'git push -u origin master', shell=True, stdout=DEVNULL)

                if return_value != 0:
                    raise Exception

                print('->   Pushed to GitHub')
        except Exception as e:
            print('mkpj: Error - {}'.format(e))

            # Remove directory for atomicity
            rmtree(project_dir)
    else:
        print('mkpj: Project with this name already exists!')
