# mkprj

A simple tool to automate the creation of a new git / GitHub project

### Dependencies
- PyGithub
- GitPython
- python-dotenv 

### Usage

First, you'll need these environment variables set in order to use the tool
```bash
$ export PROJECT_DIR=$HOME/MyProjectsDir
$ export GITHUB_KEY=********************** # If you want GitHub integration
```
Alternatively, you can have a `.env` file at your `$HOME` with the environment
variables above.

You can then start to create projects:
```bash
# Creates a new directory named MyNewProject at yout projects directory with git initialized
$ python mkprj.py MyNewProject

# The same as above but with a new GitHub repo
$ python mkprj.py MyNewProjectWithGitHub --github --description "So cool!" --private
```
The created GitHub repo will have the same name as the directory (i.e. `MyNewProjectWithGitHub`) and it'll be auto added to git remote locations.

Repos are public by default, but you can change that with
the `--private` option as showed above.
