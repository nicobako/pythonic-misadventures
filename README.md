# Nico Bakomihalis Personal Website

This is the code for my personal website.
This code gets built into *html* and is hosted at
https://pythonic-misadventures.nicobako.me

`book` directory contains the source-code for the book, while `docs` contains the github-pages-publishable book.

## Building the Book

```bash
# set up
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip wheel
pip install -r requirements.txt
pre-commit install
ipython kernel install --user --name=pythonic_misadventures

# build
jupyter-book build book/ --warningiserror

# deploy
rm -rf docs
mv book/_build/html/ docs
touch docs/.nojekyll
touch  docs/CNAME
echo "pythonic-misadventures.nicobako.me" > docs/CNAME
git add .
git commit -m "updated blog"
git push
```

# Docker

```
docker build -t pythonic-misadventures .
docker run  \
  --mount type=bind,src=/c/nb/projects/pythonic-misadventures/book/_build,dst=/app/book/_build \
  -it pythonic-misadventures \
  bash
```