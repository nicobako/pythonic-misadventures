# Nico Bakomihalis Personal Website

This is the code for my personal website.
This code gets built into *html* and is hosted at
https://nicobako.github.io

## Building the code

```bash
# set up
python -m venv .venv
source .venv/Scripts/activate
python -m install --upgrade pip wheel
pip install -r requirements.txt
ipython kernel install --user --name=nicobako_blog

# build
jupyter-book build blog

# deploy
rm -rf docs
mv blog/_build/html/ docs
touch docs/.nojekyll
git add.
git commit -m "updated blog"
git push
```
