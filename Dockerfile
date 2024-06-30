FROM python:3.12-slim

WORKDIR /code

COPY ./pyproject.toml ./

RUN python3 -m venv telegram_bot_env

RUN . telegram_bot_env/bin/activate

RUN python3 -m pip install .

COPY ./bot ./bot

CMD python3 -m bot.main

EXPOSE 8080