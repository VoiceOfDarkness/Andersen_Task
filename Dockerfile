FROM python:3.13.2

ENV APP_ENV=development \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=2.1.2 \
  PYTHONPATH=/pysetup

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /pysetup

COPY poetry.lock pyproject.toml /pysetup/
COPY . /pysetup

RUN poetry install $(test $APP_ENV && echo "--only=main") --no-interaction --no-ansi --no-root

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
