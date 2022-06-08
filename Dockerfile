FROM sagemath/sagemath:9.1

# Ignore APT warnings about not having a TTY
ENV DEBIAN_FRONTEND noninteractive


# Inspired from https://mybinder.readthedocs.io/en/latest/dockerfile.html#preparing-your-dockerfile
# Make sure the contents of our repo are in ${HOME}
COPY . ${HOME}
