FROM mcr.microsoft.com/vscode/devcontainers/python:3.12-bullseye

# Add env variables
ENV PATH="${PATH}:/root/.poetry/bin"
ENV SHELL /bin/bash
ENV LISTEN_PORT=6000
EXPOSE 6000

# Update the base image, upgrade pip, & install poetry. 
RUN sudo apt-get update && pip3 install --upgrade pip \
    && pip3 install poetry \
    && poetry config virtualenvs.create false
