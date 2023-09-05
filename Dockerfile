# This docker workflow is used to test that the instructions from the README
# work as expected. It is not used for the actual deployment of the application.
# It is intended to be used via ./docker.sh.
FROM ubuntu:latest

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Install some system dependencies
RUN apt-get update -y && apt-get install -y git && apt-get install python3-pip -y

COPY . /testing-area

# Set the working directory
WORKDIR /testing-area

RUN  pip install -r requirements.txt

RUN ln -s /testing-area/mod.py /usr/local/bin/mod

# Ensure the example file that we're going to create doesn't already exist
RUN [ ! -f "examples/convert_code/example.py" ] || (echo "Error: File already exists." && return 1)

RUN mod --config examples/convert_code/config.yaml

# Make sure the example file was created
RUN [ -f "examples/convert_code/example.py" ] || (echo "Error: File does not exist." && return 1)

# Keep the container running and allow for interactive terminal access
CMD [ "bash" ]