# Use the official Python 3.12 image as the base image
FROM python:3.12-slim AS base
WORKDIR /app
COPY . /app

# Build the documentation
FROM base AS build
COPY --from=base /app /app
RUN pip install -r requirements.txt
RUN ipython kernel install --user --name=pythonic_misadventures
RUN jupyter-book build book
RUN touch ./book/_build/html/.nojekyll
RUN touch  ./book/_build/html/CNAME
RUN echo "pythonic-misadventures.nicobako.me" > ./book/_build/html/CNAME

FROM nginx:alpine AS nginx
COPY --from=build /app/book/_build/html /usr/share/nginx/html/
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