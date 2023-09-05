#!/bin/bash
docker build --build-arg "OPENAI_API_KEY=$OPENAI_API_KEY" \
  -t mod-container . && \
docker run -it mod-container