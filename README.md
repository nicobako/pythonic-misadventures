# Nico Bakomihalis Personal Website

This is the code for my personal website.
This code gets built into *html* and is hosted at
https://nicobako.github.io

## Building the code

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m install --upgrade pip wheel
pip install -r requirements.txt

# build blog
ipython kernel install --user --name=nicobako_blog
jupyter-book build blog

# deploy
rm -rf docs
mv blog/_build/html/ docs
touch docs/.nojekkyl
git add.
git commit -m "message"
git push
```
