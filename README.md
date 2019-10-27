# mkpj

A small tool to automate the creation of a new git / GitHub project

### Dependencies

It only depends on `requests` library

You can `pip install --user requests` if you're missing it

### Getting started

```bash
# Clone the repo
git clone https://github.com/fsmiamoto/mkpj.git

# Go to the new directory
cd mkpj

# Add your GitHub key to the a file (optional)
echo "PLACE YOUR KEY HERE" > key.txt
```

You can then start to create projects:

```bash
# Creates a new directory named MyNewProject directory with git initialized and a README file
$ python mkpj.py MyNewProject

# The same as above but with a new GitHub repo
$ python mkpj.py MyNewProjectWithGitHub --github --description "So cool!" --private
```

The created GitHub repo will have the same name as the directory (i.e. `MyNewProjectWithGitHub`) and it'll be auto added to git remote locations.

Repos are public by default, but you can change that with
the `--private` option as showed above.
