# Use the official Python 3.12 image as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install -r requirements.txt
RUN ipython kernel install --user --name=pythonic_misadventures
# RUN jupyter-book build book # --warningiserror
# RUN rm -rf docs
# RUN mv book/_build/html/ docs
# RUN touch docs/.nojekyll
# RUN touch  docs/CNAME
# RUN echo "pythonic-misadventures.nicobako.me" > docs/CNAME

# Specify the command to run the application
# CMD ["python", "-m", "jupyter", "notebook", "--port=5000" ]