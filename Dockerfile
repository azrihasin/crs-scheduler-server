# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./


# Install production dependencies.
RUN pip install Flask gunicorn
RUN pip install -r requirements.txt

#Install tesseract
RUN apt-get update -qqy && apt-get install -qqy \
  tesseract-ocr \
  libtesseract-dev

RUN apt-get update && apt-get install -y --no-install-recommends \
  imagemagick && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

RUN apt update -y && apt install -y ghostscript

ARG imagemagic_config=/etc/ImageMagick-6/policy.xml

RUN if [ -f $imagemagic_config ] ; then sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="read|write" pattern="PDF" \/>/g' $imagemagic_config ; else echo did not see file $imagemagic_config ; fi

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app