# Nico Bakomihalis Personal Website

This is the code for my personal website.
This code gets built into *html* and is hosted at
https://nicobako.github.io

## Building the code

Create a new Python virtual environment,
and then use `Sphinx` to build the code.

```bash
<path-to-python3> -m venv .venv
source .venv/bin/activate # or different on Windows
pip install -r requirements.txt

sphinx-build source/ build/

cd build
git init
git add .
git commit -m "Built html pages"
git remote add origin https://nicobako.github.io.git
git push --force origin master:gh-pages
```