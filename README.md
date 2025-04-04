# Nico Bakomihalis Personal Website

This is the code for my personal website.
This code gets built into *html* and is hosted at
https://pythonic-misadventures.nicobako.me

`book` directory contains the source-code for the book, while `docs` contains the github-pages-publishable book.

## Building the Book

```bask
docker compose up --watch --build
docker container cp pythonic-misadventures-web-preview:/usr/share/nginx/html ./docs/
```

### Manual instructions

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

# Docker Notes

I'm new to docker, so these are just my personal notes on commands that have worked.

```
docker build -t pythonic-misadventures .
docker run  \
  --mount type=bind,src=/c/nb/projects/pythonic-misadventures/book/_build,dst=/app/book/_build \
  -it pythonic-misadventures \
  bash
$ docker run  --mount type=bind,src=/c/nb/projects/pythonic-misadventures/book/_build,dst=/app/book/_build -it pythonic-misadventures jupyter-book build book
```

```
docker build -t pythonic-misadventures .
docker run -d -p 8080:80 --name pythonic-misadventures pythonic-misadventures
```

```
docker compose up -d
rm -rf ./docs/
docker container cp pythonic-misadventures:/usr/share/nginx/html ./docs/
```