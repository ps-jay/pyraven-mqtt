FROM python:3.9-slim AS base

ARG PIP_NO_CACHE_DIR=1
RUN pip install -U pip pipenv

ADD Pipfile* /tmp/
WORKDIR /tmp
RUN pipenv install --system --ignore-pipfile

WORKDIR /app

##----------------------------------------------------------------------

FROM base AS testing

WORKDIR /tmp
RUN pipenv install --system --dev --ignore-pipfile

ADD *.py /app/

RUN chmod a+rw /app
WORKDIR /app

##----------------------------------------------------------------------

FROM testing AS pylint

ADD .pylintrc /tmp

ARG PYTHONPATH=.
RUN pylint --rcfile "/tmp/.pylintrc" *.py

##----------------------------------------------------------------------

FROM base AS runtime

# Ensure all testing has been run when using BuildKit
COPY --from=pylint /app/*.py /app/
WORKDIR /app

ENTRYPOINT ["python", "pyrmqtt.py"]
