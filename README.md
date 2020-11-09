# Nico Bakomihalis Personal Website

This is the code for my personal website.
This code gets built into *html* and is hosted at
https://nicobako.github.io

## Building the code

Create a new Python virtual environment,
and then use `Sphinx` to build the code.

```bash
<path-to-python3> -m venv .venv
source .venv/bin/activate # different on Windows
pip install -r requirements.txt

cd doc
make html # different on Windows

cd build/html
touch .nojekyll
git init
git add .
git commit -m "built html pages for gh-pages branch"
git remote add origin https://github.com/nicobako/nicobako.github.io.git
git push --force origin master:gh-pages
```