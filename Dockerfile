FROM python:3.12-slim AS python
WORKDIR /python
COPY --chown=app:app ./requirements.txt /python/requirements.txt
RUN pip install -r requirements.txt

# Build the documentation
# Use the official Python 3.12 image as the base image
FROM python AS build
WORKDIR /app
COPY --chown=app:app . /app
RUN ipython kernel install --user --name=pythonic_misadventures 
RUN jupyter-book build book
RUN touch /app/book/_build/html/.nojekyll
RUN touch /app/book/_build/html/CNAME
RUN echo "pythonic-misadventures.nicobako.me" > /app/book/_build//html/CNAME

# RUN touch ./_build/html/.nojekyll
# RUN touch  ./_build/html/CNAME
# RUN echo "pythonic-misadventures.nicobako.me" > ./_build/html/CNAME

FROM nginx:alpine AS web-preview
COPY --from=build --chown=app:app /app/book/_build/html /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

# RUN jupyter-book build book # --warningiserror
# RUN rm -rf docs
# RUN mv book/_build/html/ docs
# RUN touch docs/.nojekyll
# RUN touch  docs/CNAME
# RUN echo "pythonic-misadventures.nicobako.me" > docs/CNAME

# Specify the command to run the application
# CMD ["python", "-m", "jupyter", "notebook", "--port=5000" ]