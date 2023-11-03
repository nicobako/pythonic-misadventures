# Nico Bakomihalis Personal Website

This is the code for my personal website.
This code gets built into *html* and is hosted at
https://nicobako.github.io

`book` directory contains the source-code for the book, while `docs` contains the github-pages-publishable book.

## Building the Book

```bash
# set up
python -m venv .venv
source .venv/Scripts/activate
python -m install --upgrade pip wheel
pip install -r requirements.txt
pre-commit install
ipython kernel install --user --name=pythonic_misadventures

# build
jupyter-book build book --warningiserror

# deploy
rm -rf docs
mv book/_build/html/ docs
touch docs/.nojekyll
git add.
git commit -m "updated"
git push
```
